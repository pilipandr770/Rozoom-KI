from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_required, current_user
import stripe
import os
from datetime import datetime
from app import db
from app.models import PricePackage
from app.models.stripe_payment import StripePayment

# Create payment blueprint
payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

# Set up Stripe with keys from environment
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
publishable_key = os.environ.get('STRIPE_PUBLISHABLE_KEY')
webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')

@payment_bp.route('/form')
def payment_form():
    """Display the payment form for hourly rates"""
    # Get active pricing packages
    packages = PricePackage.query.filter_by(is_active=True).order_by(PricePackage.hours).all()
    
    return render_template(
        'payment_form.html',
        packages=packages,
        stripe_key=publishable_key
    )

@payment_bp.route('/create-checkout', methods=['POST'])
def create_checkout():
    """Create a Stripe checkout session for the selected hours"""
    try:
        # Get form data
        hours = float(request.form.get('hours', 10))
        hourly_rate = float(request.form.get('hourly_rate', 85.0))
        total_amount = float(request.form.get('amount', hours * hourly_rate))
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        
        # Optional fields
        package_id = request.form.get('package_id')
        if package_id:
            try:
                package_id = int(package_id)
            except (ValueError, TypeError):
                package_id = None

        # Create a payment record
        payment = StripePayment(
            amount=total_amount,
            hours_purchased=hours,
            hourly_rate=hourly_rate,
            status='pending',
            customer_email=email,
            customer_name=name,
            price_package_id=package_id,
            user_id=current_user.id if current_user.is_authenticated else None
        )
        db.session.add(payment)
        db.session.flush()  # Get the ID without committing
        
        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': f'{hours} Development Hours',
                        'description': f'Purchase of {hours} hours of development time at €{hourly_rate}/hour',
                        'metadata': {
                            'hours': hours,
                            'hourly_rate': hourly_rate,
                            'payment_id': payment.id
                        }
                    },
                    'unit_amount': int(total_amount * 100),  # Convert to cents
                },
                'quantity': 1,
            }],
            mode='payment',
            customer_email=email,
            success_url=request.host_url + url_for('payment.success', _external=False) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.host_url + url_for('payment.cancel', _external=False),
            metadata={
                'payment_id': payment.id,
                'hours': hours,
                'hourly_rate': hourly_rate
            }
        )
        
        # Update payment record with Stripe session ID
        payment.checkout_session_id = checkout_session.id
        db.session.commit()
        
        # Redirect to Stripe checkout
        return redirect(checkout_session.url)
    
    except Exception as e:
        current_app.logger.error(f"Stripe checkout error: {str(e)}")
        db.session.rollback()
        flash("An error occurred while processing your payment. Please try again.", "error")
        return redirect(url_for('payment.payment_form'))

@payment_bp.route('/success')
def success():
    """Handle successful payment"""
    session_id = request.args.get('session_id')
    
    if not session_id:
        return redirect(url_for('pages.pricing'))
    
    try:
        # Retrieve the session
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        
        # Find corresponding payment record
        payment = StripePayment.query.filter_by(checkout_session_id=session_id).first()
        
        if payment:
            # Update payment status
            payment.status = 'succeeded'
            payment.payment_intent_id = checkout_session.payment_intent
            payment.completed_at = datetime.utcnow()
            db.session.commit()
        
        return render_template(
            'payment_success.html',
            payment=payment,
            session=checkout_session
        )
    
    except Exception as e:
        current_app.logger.error(f"Error processing successful payment: {str(e)}")
        flash("We've received your payment, but there was an issue updating your account. Our team will contact you shortly.", "warning")
        return render_template('payment_success.html')

@payment_bp.route('/cancel')
def cancel():
    """Handle cancelled payment"""
    return render_template('payment_cancel.html')

@payment_bp.route('/webhook', methods=['POST'])
def webhook():
    """Handle Stripe webhooks"""
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        current_app.logger.error(f"Invalid Stripe webhook payload: {str(e)}")
        return jsonify(success=False), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        current_app.logger.error(f"Invalid Stripe webhook signature: {str(e)}")
        return jsonify(success=False), 400
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Find the payment record
        payment_id = session.get('metadata', {}).get('payment_id')
        if payment_id:
            payment = StripePayment.query.get(payment_id)
            if payment:
                payment.status = 'succeeded'
                payment.payment_intent_id = session.get('payment_intent')
                payment.completed_at = datetime.utcnow()
                db.session.commit()
                
                # Additional processing if needed (e.g., notify admins)
                try:
                    # Import notify functions from notification service
                    from app.services.notification import send_admin_notification
                    
                    # Send notification to admin about new payment
                    send_admin_notification(
                        subject="New Payment Received",
                        message=f"New payment of €{payment.amount:.2f} for {payment.hours_purchased} hours received from {payment.customer_email}"
                    )
                except Exception as e:
                    current_app.logger.error(f"Failed to send payment notification: {str(e)}")
    
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        
        # Find affected payment records
        payment = StripePayment.query.filter_by(payment_intent_id=payment_intent.id).first()
        if payment:
            payment.status = 'failed'
            db.session.commit()
    
    return jsonify(success=True)