from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from ...extensions import login_manager, UserSession, db
from ...models import User
import bcrypt

auth_bp = Blueprint('auth', __name__, template_folder='templates')


@login_manager.user_loader
def load_user(user_id):
    user = db.session.get(User, int(user_id))
    if user:
        return UserSession(user.id, user.email, user.name, user.is_admin)
    return None


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        name = request.form.get('name', '').strip()
        password_raw = request.form.get('password', '').encode('utf-8')
        if not email or not password_raw:
            flash('Email and password required', 'error')
            return redirect(url_for('auth.register'))
        existing = User.query.filter_by(email=email).first()
        if existing:
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register'))
        hashed = bcrypt.hashpw(password_raw, bcrypt.gensalt()).decode('utf-8')
        user = User(email=email, password=hashed, name=name, is_admin=False)
        db.session.add(user)
        db.session.commit()
        login_user(UserSession(user.id, user.email, user.name, user.is_admin))
        flash('Registration successful', 'success')
        return redirect(url_for('recipes.list_recipes'))
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password_raw = request.form.get('password', '').encode('utf-8')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password_raw, user.password.encode('utf-8')):
            login_user(UserSession(user.id, user.email, user.name, user.is_admin))
            flash('Logged in successfully', 'success')
            return redirect(url_for('recipes.list_recipes'))
        flash('Invalid credentials', 'error')
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))
