from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import PlacementDrive, Company, Application

bp = Blueprint('company', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    if not isinstance(current_user, Company):
        return redirect(url_for('main.home'))
    drives = PlacementDrive.query.filter_by(company_id=current_user.id).all()
    return render_template('company/dashboard.html', drives=drives)
    
@bp.route('/create_drive', methods=['GET', 'POST'])
@login_required
def create_drive():
    if not isinstance(current_user, Company):
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        drive = PlacementDrive(
            job_title=request.form.get('job_title'),
            role_type=request.form.get('role_type'),
            description=request.form.get('description'),
            eligibility=request.form.get('eligibility'),
            ctc=request.form.get('ctc'),
            deadline=request.form.get('deadline'),
            company_id=current_user.id
        )
        db.session.add(drive)
        db.session.commit()
        flash('Drive created successfully and is pending admin approval.', 'success')
        return redirect(url_for('company.dashboard'))
    return render_template('company/create_drive.html')

@bp.route('/view_applications/<int:drive_id>')
@login_required
def view_applications(drive_id):
    if not isinstance(current_user, Company):
        return redirect(url_for('main.home'))
    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.company_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('company.dashboard'))
        
    applications = Application.query.filter_by(drive_id=drive_id).all()
    return render_template("company/view_applications.html", applications=applications, drive=drive)

@bp.route('/update_status/<int:application_id>/<status>')
@login_required
def update_status(application_id, status):
    if not isinstance(current_user, Company):
        return redirect(url_for('main.home'))
    application = Application.query.get_or_404(application_id)
    if application.drive.company_id != current_user.id:
        flash('Unauthorized block.', 'danger')
        return redirect(url_for('company.dashboard'))
        
    application.status = status
    db.session.commit()
    flash(f"Status updated to {status}.", "success")
    return redirect(url_for('company.view_applications', drive_id=application.drive_id))
