from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.models import Student, Company, Admin
from app.extensions import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        student = Student.query.filter_by(email=email, password=password).first()
        if student:
            if student.is_blacklisted:
                flash('Your account is blacklisted.', 'danger')
                return redirect(url_for('auth.login'))
            login_user(student)
            return redirect(url_for('student.dashboard'))
        
        company = Company.query.filter_by(email=email, password=password).first()
        if company:
            if company.is_blacklisted:
                flash('Your account is blacklisted.', 'danger')
                return redirect(url_for('auth.login'))
            if not company.approved:
                flash('Company not approved by admin yet.', 'warning')
                return redirect(url_for('auth.login'))
            login_user(company)
            return redirect(url_for('company.dashboard'))
        
        admin = Admin.query.filter_by(email=email, password=password).first()
        if admin:
            login_user(admin)
            return redirect(url_for('admin.dashboard'))
            
        flash('Invalid email or password', 'danger')
        
    return render_template('auth/login.html')

@bp.route('/register/student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if Student.query.filter_by(email=email).first():
            flash('Student already exists', 'warning')
            return redirect(url_for('auth.register_student'))
            
        student = Student(name=name, email=email, password=password)
        db.session.add(student)
        db.session.commit()
        flash('Registration Successful. Please login', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register_student.html')

@bp.route('/register/company', methods=['GET', 'POST'])
def register_company():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        website = request.form.get('website')
        
        if Company.query.filter_by(email=email).first():
            flash('Company already registered', 'warning')
            return redirect(url_for('auth.register_company'))
    
        company = Company(name=name, email=email, password=password, website=website)
        db.session.add(company)
        db.session.commit()
        flash('Company registered. Wait for admin approval.', 'info')
        return redirect(url_for("auth.login"))
    return render_template('auth/register_company.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
