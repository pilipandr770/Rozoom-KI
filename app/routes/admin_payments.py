# Admin routes for payments
@admin.route('/payments')
@login_required
def payments():
    """List all payments."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.index'))
    
    # Get query parameters
    status = request.args.get('status', None)
    sort = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'desc')
    
    # Base query
    query = StripePayment.query
    
    # Apply filters
    if status:
        query = query.filter(StripePayment.status == status)
    
    # Apply sorting
    if hasattr(StripePayment, sort):
        sort_attr = getattr(StripePayment, sort)
        if order == 'desc':
            query = query.order_by(sort_attr.desc())
        else:
            query = query.order_by(sort_attr.asc())
    else:
        query = query.order_by(StripePayment.created_at.desc())
    
    # Paginate results
    page = request.args.get('page', 1, type=int)
    per_page = 20
    payments = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Summary stats
    total_payments = StripePayment.query.count()
    total_amount = db.session.query(db.func.sum(StripePayment.amount)).filter(StripePayment.status == 'succeeded').scalar() or 0
    total_hours = db.session.query(db.func.sum(StripePayment.hours_purchased)).filter(StripePayment.status == 'succeeded').scalar() or 0
    
    return render_template(
        'admin/payments.html',
        payments=payments,
        status=status,
        sort=sort,
        order=order,
        total_payments=total_payments,
        total_amount=total_amount,
        total_hours=total_hours
    )

@admin.route('/payments/<int:payment_id>')
@login_required
def payment_detail(payment_id):
    """View payment details."""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.index'))
    
    payment = StripePayment.query.get_or_404(payment_id)
    
    return render_template('admin/payment_detail.html', payment=payment)