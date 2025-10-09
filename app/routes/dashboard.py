from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file, abort
from flask_login import login_required, current_user
from app.models import User, Project, ProjectTask, ProjectUpdate, Message, MessageAttachment, Invoice, Payment
from app import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    """User dashboard home page"""
    # Get user's projects
    projects = Project.query.filter_by(client_id=current_user.id).order_by(Project.updated_at.desc()).all()
    
    return render_template('dashboard/index.html', projects=projects)

@dashboard_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management"""
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        company = request.form.get('company')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Update basic info
        current_user.name = name
        current_user.phone = phone
        current_user.company = company
        
        # Update password if provided
        if current_password and new_password and confirm_password:
            if not current_user.check_password(current_password):
                flash('Current password is incorrect', 'danger')
            elif new_password != confirm_password:
                flash('New passwords do not match', 'danger')
            else:
                current_user.set_password(new_password)
                flash('Password updated successfully', 'success')
        
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('dashboard.profile'))
        
    return render_template('dashboard/profile.html')

@dashboard_bp.route('/projects')
@login_required
def projects():
    """List all user projects"""
    projects = Project.query.filter_by(client_id=current_user.id).order_by(Project.updated_at.desc()).all()
    return render_template('dashboard/projects.html', projects=projects)

@dashboard_bp.route('/project/<int:project_id>')
@login_required
def project_detail(project_id):
    """Show project details"""
    project = Project.query.filter_by(id=project_id, client_id=current_user.id).first_or_404()
    
    # Get tasks and updates
    tasks = ProjectTask.query.filter_by(project_id=project.id).order_by(ProjectTask.due_date).all()
    updates = ProjectUpdate.query.filter_by(project_id=project.id).order_by(ProjectUpdate.created_at.desc()).all()
    
    return render_template('dashboard/project_detail.html', 
                           project=project, 
                           tasks=tasks,
                           updates=updates)

@dashboard_bp.route('/messages')
@login_required
def messages():
    """User messages/support tickets"""
    # In a real implementation, fetch these from a database
    # For now, we'll use sample data
    inbox_messages = [
        {
            'id': 1,
            'sender_name': 'Project Manager',
            'subject': 'Your project requirements',
            'content': 'Thank you for submitting your project requirements. We have reviewed them and would like to discuss some details with you.',
            'created_at': datetime.now(),
            'is_read': True,
            'project': {'title': 'Website Redesign'}
        },
        {
            'id': 2,
            'sender_name': 'Support Team',
            'subject': 'Welcome to Andrii Pylypchuk',
            'content': 'Welcome to Andrii Pylypchuk! We are excited to have you on board. Please let us know if you have any questions.',
            'created_at': datetime.now(),
            'is_read': False,
            'project': None
        }
    ]
    
    sent_messages = [
        {
            'id': 101,
            'recipient_name': 'Project Manager',
            'subject': 'RE: Your project requirements',
            'content': 'Thank you for your message. I am available to discuss the project details tomorrow.',
            'created_at': datetime.now(),
            'project': {'title': 'Website Redesign'}
        }
    ]
    
    # Get all admin users for the new message dropdown
    admins = User.query.filter_by(is_admin=True).all()
    
    # Get user's projects for project selection
    projects = Project.query.filter_by(client_id=current_user.id).all()
    
    return render_template('dashboard/messages.html', 
                          inbox_messages=inbox_messages,
                          sent_messages=sent_messages,
                          unread_count=1,
                          admins=admins,
                          projects=projects)

@dashboard_bp.route('/invoices')
@login_required
def invoices():
    """User invoices and payments"""
    # In a real implementation, fetch these from a database
    # For now, we'll use sample data
    invoices = [
        {
            'id': 1,
            'invoice_number': 'INV-2023-001',
            'project': {'id': 1, 'title': 'Website Redesign'},
            'issue_date': datetime.now(),
            'due_date': datetime.now(),
            'amount': 1500.00,
            'status': 'paid'
        },
        {
            'id': 2,
            'invoice_number': 'INV-2023-002',
            'project': {'id': 1, 'title': 'Website Redesign'},
            'issue_date': datetime.now(),
            'due_date': datetime.now(),
            'amount': 2000.00,
            'status': 'pending'
        },
        {
            'id': 3,
            'invoice_number': 'INV-2023-003',
            'project': {'id': 2, 'title': 'Mobile App Development'},
            'issue_date': datetime.now(),
            'due_date': datetime.now(),
            'amount': 3500.00,
            'status': 'overdue'
        }
    ]
    
    # Count by status
    paid_count = sum(1 for inv in invoices if inv['status'] == 'paid')
    pending_count = sum(1 for inv in invoices if inv['status'] == 'pending')
    overdue_count = sum(1 for inv in invoices if inv['status'] == 'overdue')
    
    return render_template('dashboard/invoices.html', 
                           invoices=invoices,
                           paid_count=paid_count,
                           pending_count=pending_count,
                           overdue_count=overdue_count)

@dashboard_bp.route('/send_message', methods=['POST'])
@login_required
def send_message():
    """Send a new message"""
    # In a real implementation, save the message to a database
    recipient_id = request.form.get('recipient_id')
    project_id = request.form.get('project_id')
    subject = request.form.get('subject')
    content = request.form.get('content')
    
    # Handle attachments
    attachments = request.files.getlist('attachments')
    if attachments:
        # Process and save attachments
        for attachment in attachments:
            if attachment.filename:
                # In a real implementation, save to a secure location and track in the database
                filename = secure_filename(attachment.filename)
                # Save the file...
    
    flash('Message sent successfully', 'success')
    return redirect(url_for('dashboard.messages'))

@dashboard_bp.route('/reply_message/<int:message_id>', methods=['POST'])
@login_required
def reply_message(message_id):
    """Reply to a message"""
    # In a real implementation, save the reply to a database
    content = request.form.get('content')
    
    # Handle attachments
    attachments = request.files.getlist('attachments')
    if attachments:
        # Process and save attachments
        for attachment in attachments:
            if attachment.filename:
                # In a real implementation, save to a secure location and track in the database
                filename = secure_filename(attachment.filename)
                # Save the file...
    
    flash('Reply sent successfully', 'success')
    return redirect(url_for('dashboard.messages'))

@dashboard_bp.route('/download_attachment/<int:attachment_id>')
@login_required
def download_attachment(attachment_id):
    """Download a message attachment"""
    # In a real implementation, retrieve the attachment from storage
    # For now, we'll just return a placeholder response
    return "Attachment download would be implemented here", 200

@dashboard_bp.route('/view_invoice/<int:invoice_id>')
@login_required
def view_invoice(invoice_id):
    """View invoice details"""
    # In a real implementation, fetch the invoice from database
    # For now, redirect to the invoices page
    flash('Invoice details view would be implemented here', 'info')
    return redirect(url_for('dashboard.invoices'))

@dashboard_bp.route('/download_invoice/<int:invoice_id>')
@login_required
def download_invoice(invoice_id):
    """Download invoice as PDF"""
    # In a real implementation, generate a PDF and send it
    # For now, we'll just return a placeholder response
    return "Invoice download would be implemented here", 200

@dashboard_bp.route('/pay_invoice/<int:invoice_id>')
@login_required
def pay_invoice(invoice_id):
    """Process payment for an invoice"""
    # In a real implementation, redirect to payment gateway
    # For now, redirect back with a message
    flash('Payment processing would be implemented here', 'info')
    return redirect(url_for('dashboard.invoices'))
