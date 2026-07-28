import os
import csv
import io
from functools import wraps
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, g, Response, send_from_directory, current_app, jsonify
from flask_mail import Message
from ..extensions import db, mail
from ..models import AdminUser, ContactMessage, EnrollmentRequest, ConsultationRequest, TrainingCourse
from .forms import AdminLoginForm, StatusUpdateForm, SendReplyForm, CreateAdminUserForm, ChangePasswordForm, CourseForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, 'static', 'images'),
        'dashboard-icon.png',
        mimetype='image/png'
    )

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_user_id' not in session:
            flash('Please log in to access the Admin Dashboard.', 'warning')
            return redirect(url_for('admin.login', next=request.url))
        if g.admin_user and g.admin_user.must_change_password and request.endpoint != 'admin.change_password':
            flash('Security Requirement: You must change your default password before proceeding.', 'warning')
            return redirect(url_for('admin.change_password'))
        return f(*args, **kwargs)
    return decorated_function

def super_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.admin_user or not g.admin_user.is_super_admin:
            flash('Access restricted: Only Super Administrators can manage dashboard users.', 'danger')
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def not_readonly_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.admin_user and g.admin_user.is_readonly:
            flash('Action prohibited: Read-Only Administrators are not permitted to modify data or send replies.', 'warning')
            return redirect(request.referrer or url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.before_request
def load_logged_in_admin():
    admin_id = session.get('admin_user_id')
    if admin_id is None:
        g.admin_user = None
    else:
        g.admin_user = db.session.get(AdminUser, admin_id)
        g.unread_messages_count = ContactMessage.query.filter_by(is_read=False).count()
        g.pending_enrollments_count = EnrollmentRequest.query.filter_by(status='Pending').count()


LOGIN_ATTEMPTS = {}
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_TIME_SECONDS = 900  # 15 minutes

def is_rate_limited(ip_address):
    now = datetime.utcnow().timestamp()
    if ip_address in LOGIN_ATTEMPTS:
        attempts, lock_until = LOGIN_ATTEMPTS[ip_address]
        if now < lock_until:
            return True, int(lock_until - now)
        elif now >= lock_until and attempts >= MAX_LOGIN_ATTEMPTS:
            LOGIN_ATTEMPTS[ip_address] = (0, 0)
    return False, 0

def record_failed_attempt(ip_address):
    now = datetime.utcnow().timestamp()
    attempts, lock_until = LOGIN_ATTEMPTS.get(ip_address, (0, 0))
    attempts += 1
    if attempts >= MAX_LOGIN_ATTEMPTS:
        lock_until = now + LOCKOUT_TIME_SECONDS
    LOGIN_ATTEMPTS[ip_address] = (attempts, lock_until)

def clear_failed_attempts(ip_address):
    LOGIN_ATTEMPTS.pop(ip_address, None)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if g.admin_user:
        return redirect(url_for('admin.dashboard'))
    
    client_ip = request.remote_addr or '127.0.0.1'
    limited, wait_seconds = is_rate_limited(client_ip)
    if limited:
        flash(f'Security Lockout: Too many failed login attempts. Please try again in {wait_seconds // 60 + 1} minutes.', 'danger')
        form = AdminLoginForm()
        return render_template('admin/login.html', title='Admin Login | 360IT', form=form), 429
    
    form = AdminLoginForm()
    if form.validate_on_submit():
        login_input = form.username.data.strip()
        password = form.password.data.strip()
        
        user = AdminUser.query.filter(
            (AdminUser.username == login_input) | (AdminUser.email == login_input)
        ).first()
        
        if user and user.check_password(password):
            clear_failed_attempts(client_ip)
            session.clear()
            session['admin_user_id'] = user.id
            flash(f'Welcome back, {user.full_name}!', 'success')
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/admin'):
                next_page = url_for('admin.dashboard')
            return redirect(next_page)
        else:
            record_failed_attempt(client_ip)
            flash('Invalid username/email or password.', 'danger')
            
    return render_template('admin/login.html', title='Admin Login | 360IT', form=form)

@admin_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/change-password', methods=['GET', 'POST'])
@admin_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not g.admin_user.check_password(form.current_password.data):
            flash('Current password entered is incorrect.', 'danger')
        else:
            g.admin_user.set_password(form.new_password.data)
            g.admin_user.must_change_password = False
            db.session.commit()
            flash('Your password has been updated successfully.', 'success')
            return redirect(url_for('admin.dashboard'))
            
    return render_template('admin/change_password.html', title='Change Password | 360IT Admin', form=form)

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    # Metrics
    total_messages = ContactMessage.query.count()
    new_messages = ContactMessage.query.filter_by(is_read=False).count()
    
    total_enrollments = EnrollmentRequest.query.count()
    pending_enrollments = EnrollmentRequest.query.filter_by(status='Pending').count()
    
    total_consultations = ConsultationRequest.query.count()
    pending_consultations = ConsultationRequest.query.filter_by(status='Pending').count()
    
    # Recent items
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    recent_enrollments = EnrollmentRequest.query.order_by(EnrollmentRequest.created_at.desc()).limit(5).all()
    
    # Course application stats
    courses = TrainingCourse.query.all()
    course_stats = []
    for c in courses:
        count = EnrollmentRequest.query.filter_by(course_title=c.title).count()
        if count > 0:
            course_stats.append({'title': c.title, 'count': count})
            
    return render_template('admin/dashboard.html',
                           title='Dashboard Overview | 360IT Admin',
                           total_messages=total_messages,
                           new_messages=new_messages,
                           total_enrollments=total_enrollments,
                           pending_enrollments=pending_enrollments,
                           total_consultations=total_consultations,
                           pending_consultations=pending_consultations,
                           recent_messages=recent_messages,
                           recent_enrollments=recent_enrollments,
                           course_stats=course_stats)

# ==================== CONTACT MESSAGES ====================

@admin_bp.route('/contact-messages')
@admin_required
def contact_messages():
    status_filter = request.args.get('status', 'all')
    search_query = request.args.get('q', '').strip()
    
    query = ContactMessage.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
        
    if search_query:
        like_str = f"%{search_query}%"
        query = query.filter(
            (ContactMessage.name.ilike(like_str)) |
            (ContactMessage.email.ilike(like_str)) |
            (ContactMessage.subject.ilike(like_str)) |
            (ContactMessage.message.ilike(like_str))
        )
        
    messages = query.order_by(ContactMessage.created_at.desc()).all()
    
    # Counts for status filter tabs
    counts = {
        'all': ContactMessage.query.count(),
        'New': ContactMessage.query.filter_by(status='New').count(),
        'In Review': ContactMessage.query.filter_by(status='In Review').count(),
        'Replied': ContactMessage.query.filter_by(status='Replied').count(),
        'Archived': ContactMessage.query.filter_by(status='Archived').count()
    }
    
    return render_template('admin/contact_messages.html',
                           title='Contact Messages | 360IT Admin',
                           messages=messages,
                           status_filter=status_filter,
                           search_query=search_query,
                           counts=counts)

@admin_bp.route('/contact-messages/<int:id>')
@admin_required
def contact_message_detail(id):
    msg = ContactMessage.query.get_or_404(id)
    if not msg.is_read:
        msg.is_read = True
        db.session.commit()
        
    reply_form = SendReplyForm(recipient_email=msg.email, subject=f"Re: {msg.subject}")
    return render_template('admin/contact_message_detail.html',
                           title=f'Message #{msg.id} - {msg.name} | 360IT Admin',
                           message=msg,
                           reply_form=reply_form)

@admin_bp.route('/contact-messages/<int:id>/update', methods=['POST'])
@admin_required
@not_readonly_required
def update_contact_message(id):
    msg = ContactMessage.query.get_or_404(id)
    new_status = request.form.get('status')
    notes = request.form.get('admin_notes')
    
    if new_status:
        msg.status = new_status
    if notes is not None:
        msg.admin_notes = notes
    msg.updated_at = datetime.utcnow()
    
    db.session.commit()
    flash(f'Contact Message #{msg.id} updated successfully.', 'success')
    return redirect(request.referrer or url_for('admin.contact_message_detail', id=msg.id))

@admin_bp.route('/contact-messages/<int:id>/delete', methods=['POST'])
@admin_required
@not_readonly_required
def delete_contact_message(id):
    msg = ContactMessage.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    flash(f'Contact Message #{id} has been deleted.', 'success')
    return redirect(url_for('admin.contact_messages'))

@admin_bp.route('/contact-messages/<int:id>/reply', methods=['POST'])
@admin_required
@not_readonly_required
def reply_contact_message(id):
    msg = ContactMessage.query.get_or_404(id)
    reply_form = SendReplyForm()
    
    if reply_form.validate_on_submit():
        body = reply_form.body.data
        subject = reply_form.subject.data
        try:
            email_msg = Message(
                subject=subject,
                recipients=[msg.email],
                body=body
            )
            mail.send(email_msg)
            msg.status = 'Replied'
            if msg.admin_notes:
                msg.admin_notes += f"\n[{datetime.utcnow().strftime('%Y-%m-%d %H:%M')}] Replied via Admin Dashboard."
            else:
                msg.admin_notes = f"[{datetime.utcnow().strftime('%Y-%m-%d %H:%M')}] Replied via Admin Dashboard."
            db.session.commit()
            flash(f'Email reply sent successfully to {msg.email}.', 'success')
        except Exception as e:
            flash(f'Message saved as Replied, but email dispatch failed: {e}', 'warning')
            msg.status = 'Replied'
            db.session.commit()
            
    return redirect(url_for('admin.contact_message_detail', id=msg.id))

@admin_bp.route('/contact-messages/bulk', methods=['POST'])
@admin_required
@not_readonly_required
def bulk_contact_messages():
    action = request.form.get('action')
    message_ids = request.form.getlist('selected_ids')
    
    if not message_ids:
        flash('No messages selected for bulk action.', 'warning')
        return redirect(url_for('admin.contact_messages'))
        
    ids = [int(i) for i in message_ids if i.isdigit()]
    messages = ContactMessage.query.filter(ContactMessage.id.in_(ids)).all()
    
    if action == 'mark_read':
        for m in messages:
            m.is_read = True
        flash(f'Marked {len(messages)} message(s) as read.', 'success')
    elif action == 'mark_archived':
        for m in messages:
            m.status = 'Archived'
        flash(f'Archived {len(messages)} message(s).', 'success')
    elif action == 'delete':
        for m in messages:
            db.session.delete(m)
        flash(f'Deleted {len(messages)} message(s).', 'success')
        
    db.session.commit()
    return redirect(url_for('admin.contact_messages'))


# ==================== COURSE ENROLLMENT APPLICATIONS ====================

@admin_bp.route('/course-enrollments')
@admin_required
def course_enrollments():
    status_filter = request.args.get('status', 'all')
    course_filter = request.args.get('course', 'all')
    search_query = request.args.get('q', '').strip()
    
    query = EnrollmentRequest.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
        
    if course_filter != 'all':
        query = query.filter_by(course_title=course_filter)
        
    if search_query:
        like_str = f"%{search_query}%"
        query = query.filter(
            (EnrollmentRequest.name.ilike(like_str)) |
            (EnrollmentRequest.email.ilike(like_str)) |
            (EnrollmentRequest.phone.ilike(like_str)) |
            (EnrollmentRequest.course_title.ilike(like_str)) |
            (EnrollmentRequest.message.ilike(like_str))
        )
        
    enrollments = query.order_by(EnrollmentRequest.created_at.desc()).all()
    
    # Available courses for filter dropdown
    all_courses = [c.title for c in TrainingCourse.query.all()]
    
    # Counts for status filter tabs
    counts = {
        'all': EnrollmentRequest.query.count(),
        'Pending': EnrollmentRequest.query.filter_by(status='Pending').count(),
        'Reviewed': EnrollmentRequest.query.filter_by(status='Reviewed').count(),
        'Accepted': EnrollmentRequest.query.filter_by(status='Accepted').count(),
        'Enrolled': EnrollmentRequest.query.filter_by(status='Enrolled').count(),
        'Rejected': EnrollmentRequest.query.filter_by(status='Rejected').count()
    }
    
    return render_template('admin/course_enrollments.html',
                           title='Course Enrollment Applications | 360IT Admin',
                           enrollments=enrollments,
                           status_filter=status_filter,
                           course_filter=course_filter,
                           search_query=search_query,
                           all_courses=all_courses,
                           counts=counts)

@admin_bp.route('/course-enrollments/<int:id>')
@admin_required
def course_enrollment_detail(id):
    enrollment = EnrollmentRequest.query.get_or_404(id)
    if not enrollment.is_read:
        enrollment.is_read = True
        db.session.commit()
        
    reply_form = SendReplyForm(
        recipient_email=enrollment.email,
        subject=f"Update regarding your enrollment application for {enrollment.course_title}"
    )
    return render_template('admin/course_enrollment_detail.html',
                           title=f'Enrollment #{enrollment.id} - {enrollment.name} | 360IT Admin',
                           enrollment=enrollment,
                           reply_form=reply_form)

@admin_bp.route('/course-enrollments/<int:id>/update', methods=['POST'])
@admin_required
@not_readonly_required
def update_course_enrollment(id):
    enrollment = EnrollmentRequest.query.get_or_404(id)
    new_status = request.form.get('status')
    notes = request.form.get('admin_notes')
    
    if new_status:
        enrollment.status = new_status
    if notes is not None:
        enrollment.admin_notes = notes
    enrollment.updated_at = datetime.utcnow()
    
    db.session.commit()
    flash(f'Enrollment Application #{enrollment.id} updated to status "{enrollment.status}".', 'success')
    return redirect(request.referrer or url_for('admin.course_enrollment_detail', id=enrollment.id))

@admin_bp.route('/course-enrollments/<int:id>/delete', methods=['POST'])
@admin_required
@not_readonly_required
def delete_course_enrollment(id):
    enrollment = EnrollmentRequest.query.get_or_404(id)
    db.session.delete(enrollment)
    db.session.commit()
    flash(f'Course Enrollment Application #{id} deleted.', 'success')
    return redirect(url_for('admin.course_enrollments'))

@admin_bp.route('/course-enrollments/bulk', methods=['POST'])
@admin_required
@not_readonly_required
def bulk_course_enrollments():
    action = request.form.get('action')
    enrollment_ids = request.form.getlist('selected_ids')
    
    if not enrollment_ids:
        flash('No applications selected for bulk action.', 'warning')
        return redirect(url_for('admin.course_enrollments'))
        
    ids = [int(i) for i in enrollment_ids if i.isdigit()]
    enrollments = EnrollmentRequest.query.filter(EnrollmentRequest.id.in_(ids)).all()
    
    if action == 'mark_reviewed':
        for e in enrollments:
            e.status = 'Reviewed'
        flash(f'Updated {len(enrollments)} application(s) to Reviewed.', 'success')
    elif action == 'mark_accepted':
        for e in enrollments:
            e.status = 'Accepted'
        flash(f'Updated {len(enrollments)} application(s) to Accepted.', 'success')
    elif action == 'mark_enrolled':
        for e in enrollments:
            e.status = 'Enrolled'
        flash(f'Updated {len(enrollments)} application(s) to Enrolled.', 'success')
    elif action == 'delete':
        for e in enrollments:
            db.session.delete(e)
        flash(f'Deleted {len(enrollments)} application(s).', 'success')
        
    db.session.commit()
    return redirect(url_for('admin.course_enrollments'))


# ==================== CONSULTATION REQUESTS ====================

@admin_bp.route('/consultations')
@admin_required
def consultations():
    status_filter = request.args.get('status', 'all')
    search_query = request.args.get('q', '').strip()
    
    query = ConsultationRequest.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
        
    if search_query:
        like_str = f"%{search_query}%"
        query = query.filter(
            (ConsultationRequest.name.ilike(like_str)) |
            (ConsultationRequest.email.ilike(like_str)) |
            (ConsultationRequest.organization.ilike(like_str)) |
            (ConsultationRequest.service_interest.ilike(like_str))
        )
        
    consultations = query.order_by(ConsultationRequest.created_at.desc()).all()
    
    counts = {
        'all': ConsultationRequest.query.count(),
        'Pending': ConsultationRequest.query.filter_by(status='Pending').count(),
        'Contacted': ConsultationRequest.query.filter_by(status='Contacted').count(),
        'Scheduled': ConsultationRequest.query.filter_by(status='Scheduled').count(),
        'Completed': ConsultationRequest.query.filter_by(status='Completed').count(),
        'Archived': ConsultationRequest.query.filter_by(status='Archived').count()
    }
    
    return render_template('admin/consultations.html',
                           title='Consultation Requests | 360IT Admin',
                           consultations=consultations,
                           status_filter=status_filter,
                           search_query=search_query,
                           counts=counts)

@admin_bp.route('/consultations/<int:id>')
@admin_required
def consultation_detail(id):
    req = ConsultationRequest.query.get_or_404(id)
    if not req.is_read:
        req.is_read = True
        db.session.commit()
        
    reply_form = SendReplyForm(
        recipient_email=req.email,
        subject=f"360IT Consultation Request: {req.service_interest}"
    )
    return render_template('admin/consultation_detail.html',
                           title=f'Consultation #{req.id} - {req.name} | 360IT Admin',
                           consultation=req,
                           reply_form=reply_form)

@admin_bp.route('/consultations/<int:id>/update', methods=['POST'])
@admin_required
@not_readonly_required
def update_consultation(id):
    req = ConsultationRequest.query.get_or_404(id)
    new_status = request.form.get('status')
    notes = request.form.get('admin_notes')
    
    if new_status:
        req.status = new_status
    if notes is not None:
        req.admin_notes = notes
    req.updated_at = datetime.utcnow()
    
    db.session.commit()
    flash(f'Consultation Request #{req.id} updated.', 'success')
    return redirect(request.referrer or url_for('admin.consultation_detail', id=req.id))

@admin_bp.route('/consultations/<int:id>/delete', methods=['POST'])
@admin_required
@not_readonly_required
def delete_consultation(id):
    req = ConsultationRequest.query.get_or_404(id)
    db.session.delete(req)
    db.session.commit()
    flash(f'Consultation Request #{id} deleted.', 'success')
    return redirect(url_for('admin.consultations'))


# ==================== DATA EXPORTS (CSV) ====================

@admin_bp.route('/export/contact-messages')
@admin_required
def export_contact_messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Subject', 'Message', 'Status', 'Is Read', 'Admin Notes', 'Date Submitted'])
    
    for m in messages:
        writer.writerow([
            m.id,
            m.name,
            m.email,
            m.phone or '',
            m.subject,
            m.message,
            m.status,
            'Yes' if m.is_read else 'No',
            m.admin_notes or '',
            m.created_at.strftime('%Y-%m-%d %H:%M:%S') if m.created_at else ''
        ])
        
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-disposition": "attachment; filename=360it_contact_messages.csv"}
    )

@admin_bp.route('/export/course-enrollments')
@admin_required
def export_course_enrollments():
    enrollments = EnrollmentRequest.query.order_by(EnrollmentRequest.created_at.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Applicant Name', 'Email', 'Phone', 'Course Title', 'Delivery Mode', 'Applicant Notes', 'Status', 'Is Read', 'Admin Notes', 'Date Applied'])
    
    for e in enrollments:
        writer.writerow([
            e.id,
            e.name,
            e.email,
            e.phone or '',
            e.course_title,
            e.delivery_mode,
            e.message or '',
            e.status,
            'Yes' if e.is_read else 'No',
            e.admin_notes or '',
            e.created_at.strftime('%Y-%m-%d %H:%M:%S') if e.created_at else ''
        ])
        
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-disposition": "attachment; filename=360it_course_enrollments.csv"}
    )

# --- User Management Routes (Super Admin Only) ---

@admin_bp.route('/users')
@admin_required
@super_admin_required
def manage_users():
    users = AdminUser.query.order_by(AdminUser.id.asc()).all()
    return render_template('admin/users.html', title='User Management | 360IT Admin', users=users)

@admin_bp.route('/users/create', methods=['GET', 'POST'])
@admin_required
@super_admin_required
def create_user():
    form = CreateAdminUserForm()
    if form.validate_on_submit():
        existing_username = AdminUser.query.filter_by(username=form.username.data.strip()).first()
        existing_email = AdminUser.query.filter_by(email=form.email.data.strip().lower()).first()
        if existing_username:
            flash(f'Username "{form.username.data}" is already taken.', 'danger')
        elif existing_email:
            flash(f'Email "{form.email.data}" is already registered to another user.', 'danger')
        else:
            new_user = AdminUser(
                username=form.username.data.strip(),
                email=form.email.data.strip().lower(),
                full_name=form.full_name.data.strip(),
                role=form.role.data
            )
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Dashboard user "{new_user.username}" ({new_user.role}) was created successfully!', 'success')
            return redirect(url_for('admin.manage_users'))
            
    return render_template('admin/user_create.html', title='Create Dashboard User | 360IT Admin', form=form)

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
@super_admin_required
def delete_user(user_id):
    if user_id == g.admin_user.id:
        flash('Security Warning: You cannot delete your own active administrator account.', 'danger')
        return redirect(url_for('admin.manage_users'))
        
    target_user = db.session.get(AdminUser, user_id)
    if not target_user:
        flash('Specified administrator account was not found.', 'warning')
        return redirect(url_for('admin.manage_users'))
        
    user_name = target_user.username
    db.session.delete(target_user)
    db.session.commit()
    flash(f'Administrator user "{user_name}" has been permanently deleted.', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/kanban')
@admin_required
def kanban_pipeline():
    enrollments = EnrollmentRequest.query.order_by(EnrollmentRequest.created_at.desc()).all()
    consultations = ConsultationRequest.query.order_by(ConsultationRequest.created_at.desc()).all()
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    
    stages = {
        'New': [],
        'In Progress': [],
        'Completed': [],
        'Archived': []
    }
    
    for item in enrollments:
        stage = item.status if item.status in stages else 'New'
        stages[stage].append({
            'id': item.id,
            'type': 'enrollment',
            'title': item.course_title,
            'client': getattr(item, 'full_name', None) or getattr(item, 'name', 'N/A'),
            'email': item.email,
            'phone': item.phone or 'N/A',
            'date': item.created_at.strftime('%b %d, %Y') if item.created_at else 'N/A',
            'status': item.status
        })
        
    for item in consultations:
        stage = item.status if item.status in stages else 'New'
        stages[stage].append({
            'id': item.id,
            'type': 'consultation',
            'title': item.service_interest,
            'client': getattr(item, 'full_name', None) or getattr(item, 'name', 'N/A'),
            'org': item.organization or 'N/A',
            'email': item.email,
            'phone': item.phone or 'N/A',
            'date': item.created_at.strftime('%b %d, %Y') if item.created_at else 'N/A',
            'status': item.status
        })
        
    for item in messages:
        stage = 'New' if not item.is_read else ('Completed' if item.status == 'Replied' else 'In Progress')
        stages[stage].append({
            'id': item.id,
            'type': 'message',
            'title': getattr(item, 'subject', 'General Inquiry'),
            'client': getattr(item, 'full_name', None) or getattr(item, 'name', 'N/A'),
            'email': item.email,
            'phone': item.phone or 'N/A',
            'date': item.created_at.strftime('%b %d, %Y') if item.created_at else 'N/A',
            'status': 'Replied' if item.status == 'Replied' else ('Read' if item.is_read else 'Unread')
        })

    return render_template('admin/kanban.html', title='Lead Pipeline (Kanban) | 360IT Admin', stages=stages)

@admin_bp.route('/api/update-status', methods=['POST'])
@admin_required
@not_readonly_required
def api_update_status():
    data = request.get_json() or {}
    item_type = data.get('type')
    item_id = data.get('id')
    new_status = data.get('status')
    
    if not item_type or not item_id or not new_status:
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
    if item_type == 'enrollment':
        item = db.session.get(EnrollmentRequest, item_id)
        if item:
            item.status = new_status
            db.session.commit()
            return jsonify({'success': True, 'message': 'Enrollment status updated'})
    elif item_type == 'consultation':
        item = db.session.get(ConsultationRequest, item_id)
        if item:
            item.status = new_status
            db.session.commit()
            return jsonify({'success': True, 'message': 'Consultation status updated'})
    elif item_type == 'message':
        item = db.session.get(ContactMessage, item_id)
        if item:
            item.is_read = True
            if new_status in ['Completed', 'Replied']:
                item.status = 'Replied'
            db.session.commit()
            return jsonify({'success': True, 'message': 'Message status updated'})
            
    return jsonify({'success': False, 'message': 'Item not found'}), 404

import re

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return re.sub(r'^-+|-+$', '', text) or 'course'

@admin_bp.route('/courses')
@admin_required
def manage_courses():
    courses = TrainingCourse.query.order_by(TrainingCourse.id.desc()).all()
    return render_template('admin/courses.html', title='Manage Training Courses | 360IT Admin', courses=courses)

@admin_bp.route('/courses/create', methods=['GET', 'POST'])
@admin_required
@not_readonly_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        slug = slugify(form.title.data)
        existing = TrainingCourse.query.filter_by(slug=slug).first()
        if existing:
            slug = f"{slug}-{int(datetime.utcnow().timestamp())}"
            
        course = TrainingCourse(
            title=form.title.data.strip(),
            slug=slug,
            icon=form.icon.data.strip() or 'fa-graduation-cap',
            duration=form.duration.data.strip(),
            delivery_mode=form.delivery_mode.data.strip(),
            skill_level=form.skill_level.data,
            short_desc=form.short_desc.data.strip(),
            long_desc=form.long_desc.data.strip() if form.long_desc.data else None,
            syllabus_list=form.syllabus_list.data.strip() if form.syllabus_list.data else None,
            featured=form.featured.data
        )
        db.session.add(course)
        db.session.commit()
        flash(f'Training course "{course.title}" created successfully!', 'success')
        return redirect(url_for('admin.manage_courses'))
        
    return render_template('admin/course_form.html', title='Create Training Course | 360IT Admin', form=form, is_edit=False)

@admin_bp.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_required
@not_readonly_required
def edit_course(course_id):
    course = db.session.get(TrainingCourse, course_id)
    if not course:
        flash('Course not found.', 'danger')
        return redirect(url_for('admin.manage_courses'))
        
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        course.title = form.title.data.strip()
        course.icon = form.icon.data.strip()
        course.duration = form.duration.data.strip()
        course.delivery_mode = form.delivery_mode.data.strip()
        course.skill_level = form.skill_level.data
        course.short_desc = form.short_desc.data.strip()
        course.long_desc = form.long_desc.data.strip() if form.long_desc.data else None
        course.syllabus_list = form.syllabus_list.data.strip() if form.syllabus_list.data else None
        course.featured = form.featured.data
        
        db.session.commit()
        flash(f'Course "{course.title}" updated successfully!', 'success')
        return redirect(url_for('admin.manage_courses'))
        
    return render_template('admin/course_form.html', title=f'Edit Course: {course.title} | 360IT Admin', form=form, is_edit=True, course=course)

@admin_bp.route('/courses/<int:course_id>/delete', methods=['POST'])
@admin_required
@not_readonly_required
def delete_course(course_id):
    course = db.session.get(TrainingCourse, course_id)
    if not course:
        flash('Course not found.', 'danger')
        return redirect(url_for('admin.manage_courses'))
        
    title = course.title
    db.session.delete(course)
    db.session.commit()
    flash(f'Course "{title}" deleted successfully.', 'info')
    return redirect(url_for('admin.manage_courses'))


# Dummy Newsletter Subscribers Management
MOCK_NEWSLETTER_SUBSCRIBERS = [
    {'id': 1, 'email': 'john.doe@enterprise.com', 'status': 'Subscribed', 'source': 'Footer Form', 'created_at': '2026-07-28 14:30'},
    {'id': 2, 'email': 'sarah.connor@cyberdyne.org', 'status': 'Subscribed', 'source': 'Homepage Modal', 'created_at': '2026-07-27 09:15'},
    {'id': 3, 'email': 'alex.rivera@techsolutions.io', 'status': 'Unsubscribed', 'source': 'Blog Subscription', 'created_at': '2026-07-25 18:45'},
    {'id': 4, 'email': 'emily.watson@consulting.co', 'status': 'Subscribed', 'source': 'Footer Form', 'created_at': '2026-07-24 11:20'},
    {'id': 5, 'email': 'michael.brown@cloudnet.com', 'status': 'Subscribed', 'source': 'Training Page', 'created_at': '2026-07-22 16:10'},
]

@admin_bp.route('/newsletter-subscribers')
@admin_required
def newsletter_subscribers():
    status = request.args.get('status', 'all')
    q = request.args.get('q', '').strip().lower()

    subscribers = list(MOCK_NEWSLETTER_SUBSCRIBERS)

    if status and status != 'all':
        subscribers = [s for s in subscribers if s['status'].lower() == status.lower()]

    if q:
        subscribers = [s for s in subscribers if q in s['email'].lower()]

    total_count = len(MOCK_NEWSLETTER_SUBSCRIBERS)
    subscribed_count = sum(1 for s in MOCK_NEWSLETTER_SUBSCRIBERS if s['status'] == 'Subscribed')
    unsubscribed_count = sum(1 for s in MOCK_NEWSLETTER_SUBSCRIBERS if s['status'] == 'Unsubscribed')

    return render_template(
        'admin/newsletter_subscribers.html',
        title='Newsletter Subscribers | 360IT Admin',
        subscribers=subscribers,
        current_status=status,
        query=q,
        total_count=total_count,
        subscribed_count=subscribed_count,
        unsubscribed_count=unsubscribed_count
    )

@admin_bp.route('/export/newsletter-subscribers')
@admin_required
def export_newsletter_subscribers():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Email Address', 'Status', 'Acquisition Source', 'Subscribed Date'])

    for sub in MOCK_NEWSLETTER_SUBSCRIBERS:
        writer.writerow([sub['id'], sub['email'], sub['status'], sub['source'], sub['created_at']])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=newsletter_subscribers.csv'}
    )

@admin_bp.route('/newsletter-subscribers/<int:subscriber_id>/toggle', methods=['POST'])
@admin_required
@not_readonly_required
def toggle_newsletter_subscriber(subscriber_id):
    for sub in MOCK_NEWSLETTER_SUBSCRIBERS:
        if sub['id'] == subscriber_id:
            sub['status'] = 'Unsubscribed' if sub['status'] == 'Subscribed' else 'Subscribed'
            flash(f'Subscription status updated for {sub["email"]}', 'success')
            break
    return redirect(url_for('admin.newsletter_subscribers'))

