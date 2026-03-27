from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Student, Company, PlacementDrive, Application, Admin

bp = Blueprint('admin', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    if not isinstance(current_user, Admin):
        return redirect(url_for('main.home'))
    students_count = Student.query.count()
    companies_count = Company.query.count()
    drives_count = PlacementDrive.query.count()
    applications_count = Application.query.count()
    return render_template(
        'admin/dashboard.html',
        students=students_count,
        companies=companies_count,
        drives=drives_count,
        applications=applications_count
    )

@bp.route('/companies')
@login_required
def companies():
    if not isinstance(current_user, Admin):
        return redirect(url_for('main.home'))
    query = request.args.get('query', '')
    if query:
        companies = Company.query.filter(Company.name.ilike(f'%{query}%')).all()
    else:
        companies = Company.query.all()
    return render_template('admin/companies.html', companies=companies)

@bp.route('/approve_company/<int:company_id>')
@login_required
def approve_company(company_id):
    if not isinstance(current_user, Admin):
        return redirect(url_for('main.home'))
    company = Company.query.get_or_404(company_id)
    company.approved = True
    db.session.commit()
    flash(f'Company {company.name} approved.', 'success')
    return redirect(url_for('admin.companies'))

@bp.route('/delete_company/<int:company_id>')
@login_required
def delete_company(company_id):
    if not isinstance(current_user, Admin):
        return redirect(url_for('main.home'))
    company = Company.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()
    flash('Company deleted.', 'warning')
    return redirect(url_for("admin.companies"))

@bp.route('/drives')
@login_required
def drives():
    if not isinstance(current_user, Admin):
        return redirect(url_for('main.home'))
    drives = PlacementDrive.query.all()
    return render_template("admin/drives.html", drives=drives)

@bp.route('/approve_drive/<int:drive_id>')
@login_required
def approve_drive(drive_id):
    if not isinstance(current_user, Admin):
        return redirect(url_for('main.home'))
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = "Approved"
    db.session.commit()
    flash('Drive approved.', 'success')
    return redirect(url_for('admin.drives'))

@bp.route('/students')
@login_required
def students():
    if not isinstance(current_user, Admin):
        return redirect(url_for('main.home'))
    query = request.args.get('query', '')
    if query:
        students = Student.query.filter(Student.name.ilike(f'%{query}%')).all()
    else:
        students = Student.query.all()
    return render_template("admin/students.html", students=students)

@bp.route('/blacklist_student/<int:student_id>')
@login_required
def blacklist_student(student_id):
    if not isinstance(current_user, Admin):
        return redirect(url_for('main.home'))
    student = Student.query.get_or_404(student_id)
    student.is_blacklisted = not student.is_blacklisted
    db.session.commit()
    status = "blacklisted" if student.is_blacklisted else "un-blacklisted"
    flash(f"Student {student.name} has been {status}.", "info")
    return redirect(url_for('admin.students'))

@bp.route('/blacklist_company/<int:company_id>')
@login_required
def blacklist_company(company_id):
    if not isinstance(current_user, Admin):
        return redirect(url_for('main.home'))
    company = Company.query.get_or_404(company_id)
    company.is_blacklisted = not company.is_blacklisted
    db.session.commit()
    status = "blacklisted" if company.is_blacklisted else "un-blacklisted"
    flash(f"Company {company.name} has been {status}.", "info")
    return redirect(url_for('admin.companies'))
