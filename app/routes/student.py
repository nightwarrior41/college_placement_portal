from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, logout_user
from app.extensions import db
from app.models import PlacementDrive, Application, Student

bp = Blueprint('student', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    if not isinstance(current_user, Student):
        return redirect(url_for('main.home'))
    drives = PlacementDrive.query.filter_by(status="Approved").all()
    applications = Application.query.filter_by(student_id=current_user.id).all()
    return render_template('student/dashboard.html', drives=drives, applications=applications)

@bp.route('/apply/<int:drive_id>')
@login_required
def apply(drive_id):
    if not isinstance(current_user, Student):
        return redirect(url_for('main.home'))
    existing = Application.query.filter_by(student_id=current_user.id, drive_id=drive_id).first()
    if existing:
        flash("You have already applied for this drive.", "warning")
        return redirect(url_for('student.dashboard'))
    application = Application(student_id=current_user.id, drive_id=drive_id)
    db.session.add(application)
    db.session.commit()
    flash("Successfully applied!", "success")
    return redirect(url_for('student.dashboard'))

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if not isinstance(current_user, Student):
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.contact_number = request.form.get('contact_number')
        current_user.cgpa = request.form.get('cgpa')
        current_user.branch = request.form.get('branch')
        current_user.passing_year = request.form.get('passing_year')
        current_user.skills = request.form.get('skills')
        current_user.resume = request.form.get('resume')
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for('student.dashboard'))
    return render_template('student/edit_profile.html')
