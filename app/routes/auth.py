from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Project, ProjectTask, ProjectUpdate
from app.auth import AdminUser  # Добавляем импорт AdminUser
from app import db
from datetime import datetime
import json

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        login_id = request.form.get('login')  # Could be email or username
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        # Сначала пробуем найти AdminUser
        admin = AdminUser.query.filter_by(email=login_id).first()
        if not admin:
            admin = AdminUser.query.filter_by(username=login_id).first()
        
        if admin and admin.check_password(password):
            login_user(admin, remember=remember)
            flash('Вход выполнен успешно!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))
        
        # Если AdminUser не найден, пробуем обычного User
        user = User.query.filter_by(email=login_id).first()
        if not user:
            user = User.query.filter_by(username=login_id).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            flash('Неверные учетные данные', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle new user registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        username = request.form.get('username') or email.split('@')[0]  # Use part before @ from email as default username
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        company = request.form.get('company', '')
        phone = request.form.get('phone', '')
        
        # Form validation
        if not all([email, name, password, password_confirm]):
            flash('All required fields must be filled', 'danger')
        elif password != password_confirm:
            flash('Passwords do not match', 'danger')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
        elif username and User.query.filter_by(username=username).first():
            flash('Username already taken', 'danger')
        else:
            # Create new user
            user = User(
                email=email,
                username=username,
                name=name,
                company=company,
                phone=phone,
                created_at=datetime.utcnow()
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! You can now login.', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('pages.index'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handle password reset request"""
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            # In a real implementation, send password reset email
            # For now, just show a message
            flash('Password reset instructions have been sent to your email.', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash('Email address not found', 'danger')
    
    return render_template('auth/forgot_password.html')
