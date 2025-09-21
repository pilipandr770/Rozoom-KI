from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import current_user
from app.models import PricePackage, StripePayment
from app import db
import stripe
import os
from datetime import datetime

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

@payment_bp.before_request
def setup_stripe():
    """Configure Stripe API key before each request"""
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

@payment_bp.route('/form', methods=['GET'])
def payment_form():
    """Display payment form for purchasing development hours"""
    # Get all active pricing packages
    package_objs = PricePackage.query.filter_by(is_active=True).order_by(PricePackage.hours.asc()).all()
    
    if not package_objs:
        flash('No pricing packages are currently available. Please contact us for custom pricing.', 'warning')
        return redirect(url_for('pages.contact'))
    
    # Convert PricePackage objects to dictionaries for JSON serialization
    packages = []
    for pkg in package_objs:
        packages.append({
            'id': pkg.id,
            'name': pkg.name,
            'hours': pkg.hours,
            'price_per_hour': pkg.price_per_hour,
            'description': pkg.description if hasattr(pkg, 'description') else None
        })
    
    return render_template('payment/payment_form.html', packages=packages)

@payment_bp.route('/create-checkout', methods=['POST'])
def create_checkout():
    """Create a Stripe checkout session"""
    try:
        # Get form data
        hours = int(request.form.get('hours', 10))
        
        if hours < 5:
            hours = 5  # Minimum hours
        
        # Get all active pricing packages
        package_objs = PricePackage.query.filter_by(is_active=True).order_by(PricePackage.hours.asc()).all()
        
        if not package_objs:
            flash('No pricing packages are currently available. Please contact us for custom pricing.', 'warning')
            return redirect(url_for('pages.contact'))
        
        # Find applicable package (default to first/smallest package)
        applicable_package = package_objs[0]
        
        # Find the largest package that applies to the selected hours
        for package in package_objs:
            if hours >= package.hours:
                applicable_package = package
            else:
                break
        
        # Calculate price
        hourly_rate = applicable_package.price_per_hour
        amount = hours * hourly_rate
        
        # Create a payment record
        payment = StripePayment(
            hours_purchased=hours,
            hourly_rate=hourly_rate,
            amount=amount,
            status='pending',
            price_package_id=applicable_package.id
        )
        
        # If user is logged in, link the payment to them
        if current_user.is_authenticated:
            payment.user_id = current_user.id
        
        db.session.add(payment)
        db.session.commit()
        
        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': f'Development Hours ({hours} hours)',
                            'description': f'Purchase of {hours} development hours at €{hourly_rate:.2f}/hour'
                        },
                        'unit_amount': int(hourly_rate * 100),  # Stripe needs amounts in cents
                    },
                    'quantity': hours,
                },
            ],
            metadata={
                'payment_id': payment.id,
                'hours': hours,
                'hourly_rate': hourly_rate,
                'package_id': applicable_package.id,
                'package_name': applicable_package.name
            },
            mode='payment',
            success_url=url_for('payment.success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('payment.cancel', _external=True),
        )
        
        # Update payment with checkout session ID
        payment.checkout_session_id = checkout_session.id
        
        # If customer email was provided in the checkout
        if getattr(checkout_session, 'customer_email', None):
            payment.customer_email = checkout_session.customer_email
        
        db.session.commit()
        
        # Redirect to Stripe checkout
        return redirect(checkout_session.url, code=303)
    
    except Exception as e:
        current_app.logger.error(f"Error creating checkout session: {str(e)}")
        flash('An error occurred while processing your payment. Please try again later.', 'error')
        return redirect(url_for('payment.payment_form'))

@payment_bp.route('/success', methods=['GET'])
def success():
    """Handle successful payment"""
    session_id = request.args.get('session_id')
    
    if not session_id:
        return redirect(url_for('pages.index'))
    
    try:
        # Get payment data from database
        payment = StripePayment.query.filter_by(checkout_session_id=session_id).first()
        
        if not payment:
            flash('Payment information not found.', 'warning')
            return redirect(url_for('pages.index'))
        
        # If payment status is still pending, update it
        if payment.status == 'pending':
            # Get session data from Stripe
            checkout_session = stripe.checkout.Session.retrieve(session_id)
            
            if checkout_session.payment_status == 'paid':
                payment.status = 'succeeded'
                payment.payment_intent_id = checkout_session.payment_intent
                payment.completed_at = datetime.utcnow()
                
                # Update customer email if available
                if getattr(checkout_session, 'customer_email', None):
                    payment.customer_email = checkout_session.customer_email
                    
                # Update customer name if available
                if getattr(checkout_session, 'customer_details', None) and getattr(checkout_session.customer_details, 'name', None):
                    payment.customer_name = checkout_session.customer_details.name
                    
                db.session.commit()
                
                # Send notification to admin (optional)
                # send_payment_notification(payment)
                
                flash('Payment successful! Thank you for your purchase.', 'success')
            else:
                flash('Payment is being processed. We will update you when it completes.', 'info')
        
        return render_template('payment/success.html', payment=payment)
    
    except Exception as e:
        current_app.logger.error(f"Error processing successful payment: {str(e)}")
        flash('An error occurred while processing your payment information.', 'error')
        return redirect(url_for('pages.index'))

@payment_bp.route('/cancel', methods=['GET'])
def cancel():
    """Handle cancelled payment"""
    return render_template('payment/cancel.html')

@payment_bp.route('/webhook', methods=['POST'])
def webhook():
    """Handle Stripe webhook events"""
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
    
    try:
        if not webhook_secret:
            return jsonify({'error': 'Webhook secret not configured'}), 400
            
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
        
        # Handle the event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            
            # Get payment from database
            payment = StripePayment.query.filter_by(checkout_session_id=session.id).first()
            
            if payment:
                # Update payment status
                payment.status = 'succeeded'
                payment.payment_intent_id = session.payment_intent
                payment.completed_at = datetime.utcnow()
                
                # Update customer info if available
                if getattr(session, 'customer_email', None):
                    payment.customer_email = session.customer_email
                    
                if getattr(session, 'customer_details', None) and getattr(session.customer_details, 'name', None):
                    payment.customer_name = session.customer_details.name
                    
                db.session.commit()
                
                # Send notification to admin (optional)
                # send_payment_notification(payment)
                
                current_app.logger.info(f"Payment {payment.id} marked as succeeded via webhook")
            else:
                current_app.logger.warning(f"Payment not found for session {session.id}")
        
        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            
            # Get payment from database using payment intent ID
            payment = StripePayment.query.filter_by(payment_intent_id=payment_intent.id).first()
            
            if payment:
                # Update payment status
                payment.status = 'failed'
                db.session.commit()
                current_app.logger.info(f"Payment {payment.id} marked as failed via webhook")
            
        return jsonify({'status': 'success'})
    
    except ValueError as e:
        current_app.logger.error(f"Invalid payload: {str(e)}")
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        current_app.logger.error(f"Invalid signature: {str(e)}")
        return jsonify({'error': 'Invalid signature'}), 400
    except Exception as e:
        current_app.logger.error(f"Webhook error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Helper function to send notification to admin (optional implementation)
# def send_payment_notification(payment):
#     from app.utils.email_service import send_email
#     
#     subject = f"New payment received - {payment.id}"
#     body = f"""
#     A new payment has been received:
#     
#     Payment ID: {payment.id}
#     Amount: €{payment.amount:.2f}
#     Hours: {payment.hours_purchased}
#     Customer: {payment.customer_name or 'N/A'} ({payment.customer_email or 'N/A'})
#     Status: {payment.status}
#     Date: {payment.completed_at.strftime('%d-%m-%Y %H:%M') if payment.completed_at else payment.updated_at.strftime('%d-%m-%Y %H:%M')}
#     """
#     
#     # Get admin email from config
#     admin_email = current_app.config.get('ADMIN_EMAIL', 'admin@rozoom-ki.com')
#     
#     # Send email
#     send_email(subject, body, [admin_email])