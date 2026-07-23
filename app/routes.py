from flask import render_template, redirect, url_for, flash, request
from . import app
from .extensions import db
from .models import Service, TrainingCourse, Project, Testimonial, ContactMessage, ConsultationRequest, EnrollmentRequest
from .forms import ContactForm, ConsultationForm, EnrollmentForm

@app.context_processor
def inject_global_forms():
    return {
        'consultation_form': ConsultationForm(),
        'enrollment_form': EnrollmentForm()
    }

@app.route('/')
def index():
    services = Service.query.all()
    courses = TrainingCourse.query.filter_by(featured=True).all()
    projects = Project.query.filter_by(featured=True).all()
    testimonials = Testimonial.query.all()
    contact_form = ContactForm()
    
    return render_template('index.html',
                           title='360IT Learning & Consulting | Enterprise IT Solutions & Technical Training',
                           services=services,
                           courses=courses,
                           projects=projects,
                           testimonials=testimonials,
                           contact_form=contact_form)

@app.route('/about')
def about():
    return render_template('about.html', title='About Us | 360IT Learning & Consulting')

@app.route('/services')
def services():
    all_services = Service.query.all()
    return render_template('services.html', title='IT Consulting Services | 360IT', services=all_services)

@app.route('/services/<slug>')
def service_detail(slug):
    service = Service.query.filter_by(slug=slug).first_or_404()
    related_services = Service.query.filter(Service.id != service.id).limit(3).all()
    return render_template('service_detail.html', title=f'{service.title} | 360IT Consulting', service=service, related_services=related_services)

@app.route('/training')
def training():
    all_courses = TrainingCourse.query.all()
    return render_template('training.html', title='Professional IT Training Programs | 360IT', courses=all_courses)

@app.route('/training/<slug>')
def course_detail(slug):
    course = TrainingCourse.query.filter_by(slug=slug).first_or_404()
    syllabus_items = course.syllabus_list.split('|') if course.syllabus_list else []
    return render_template('course_detail.html', title=f'{course.title} Bootcamp | 360IT Training', course=course, syllabus_items=syllabus_items)

@app.route('/projects')
def projects():
    all_projects = Project.query.all()
    return render_template('projects.html', title='Projects & Contracts Portfolio | 360IT', projects=all_projects)

@app.route('/projects/<slug>')
def project_detail(slug):
    project = Project.query.filter_by(slug=slug).first_or_404()
    tech_list = [t.strip() for t in project.tech_stack.split(',')]
    return render_template('project_detail.html', title=f'{project.title} | 360IT Projects', project=project, tech_list=tech_list)

@app.route('/technologies')
def technologies():
    return render_template('technologies.html', title='Technology Stack & Competencies | 360IT')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            subject=form.subject.data or dict(form.subject_choice.choices).get(form.subject_choice.data, 'General'),
            message=form.message.data
        )
        db.session.add(msg)
        db.session.commit()
        flash('Thank you for reaching out! Your message has been received and our team will get back to you shortly.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', title='Contact Us | 360IT Learning & Consulting', form=form)

@app.route('/request-consultation', methods=['POST'])
def request_consultation():
    form = ConsultationForm()
    if form.validate_on_submit():
        req = ConsultationRequest(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            organization=form.organization.data,
            service_interest=form.service_interest.data,
            message=form.message.data
        )
        db.session.add(req)
        db.session.commit()
        flash('Your consultation request has been submitted successfully! A senior consultant will contact you within 24 hours.', 'success')
    else:
        flash('There was an error in your submission. Please check the required fields.', 'danger')
    return redirect(request.referrer or url_for('index'))

@app.route('/enroll-course', methods=['POST'])
def enroll_course():
    form = EnrollmentForm()
    if form.validate_on_submit():
        req = EnrollmentRequest(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            course_title=form.course_title.data,
            delivery_mode=form.delivery_mode.data,
            message=form.message.data
        )
        db.session.add(req)
        db.session.commit()
        flash(f'Congratulations! Your enrollment request for "{form.course_title.data}" has been recorded. Our admissions advisor will contact you with batch schedules.', 'success')
    else:
        flash('Failed to submit enrollment request. Please fill out all required fields.', 'danger')
    return redirect(request.referrer or url_for('index'))

@app.route('/newsletter-subscribe', methods=['POST'])
def newsletter_subscribe():
    email = request.form.get('email')
    if email:
        flash('Thank you for subscribing to 360IT Tech Insights newsletter!', 'success')
    return redirect(request.referrer or url_for('index'))
