import os
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory, current_app, Response
from .extensions import db
from .models import Service, TrainingCourse, Project, Testimonial, ContactMessage, ConsultationRequest, EnrollmentRequest, NewsletterSubscriber
from .forms import ContactForm, ConsultationForm, EnrollmentForm

bp = Blueprint('main', __name__)

STOP_WORDS = {'and', 'or', 'the', 'for', 'with', 'in', 'on', 'at', 'to', 'a', 'an', 'is', 'of', 'by', 'it', 'its', 'our', 'your', 'about'}

def calculate_relevance(item, query, words, title_attr='title', desc_attr='short_desc', long_desc_attr='long_desc', cat_attr='category'):
    score = 0
    query_lower = query.lower()
    
    title_val = getattr(item, title_attr, '') or ''
    desc_val = getattr(item, desc_attr, '') or ''
    long_desc_val = getattr(item, long_desc_attr, '') or ''
    cat_val = getattr(item, cat_attr, '') or ''
    
    # Phrase matches
    if query_lower in title_val.lower():
        score += 30
    if query_lower in cat_val.lower():
        score += 20
    if query_lower in desc_val.lower():
        score += 15
        
    # Keyword matches
    for word in words:
        w_lower = word.lower()
        if w_lower in title_val.lower():
            score += 10
        if w_lower in cat_val.lower():
            score += 7
        if w_lower in desc_val.lower():
            score += 5
        if w_lower in long_desc_val.lower():
            score += 2
            
    return score

@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, 'static', 'images', 'favicon'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@bp.app_context_processor
def inject_global_forms():
    return {
        'consultation_form': ConsultationForm(),
        'enrollment_form': EnrollmentForm()
    }

@bp.route('/')
def index():
    services = Service.query.all()
    courses = TrainingCourse.query.filter_by(featured=True).all()
    projects = Project.query.filter_by(featured=True).all()
    testimonials = Testimonial.query.limit(3).all()
    contact_form = ContactForm()
    
    return render_template('index.html',
                           title='360IT Learning & Consulting | Enterprise IT Solutions & Technical Training',
                           services=services,
                           courses=courses,
                           projects=projects,
                           testimonials=testimonials,
                           contact_form=contact_form)

@bp.route('/about')
def about():
    return render_template('about.html', title='About Us | 360IT Learning & Consulting')

@bp.route('/services')
def services():
    all_services = Service.query.all()
    return render_template('services.html', title='IT Consulting Services | 360IT', services=all_services)

@bp.route('/services/<slug>')
def service_detail(slug):
    service = Service.query.filter_by(slug=slug).first_or_404()
    related_services = Service.query.filter(Service.id != service.id).limit(3).all()
    return render_template('service_detail.html', title=f'{service.title} | 360IT Consulting', service=service, related_services=related_services)

@bp.route('/training')
def training():
    all_courses = TrainingCourse.query.all()
    return render_template('training.html', title='Professional IT Training Programs | 360IT', courses=all_courses)

@bp.route('/training/<slug>')
def course_detail(slug):
    course = TrainingCourse.query.filter_by(slug=slug).first_or_404()
    syllabus_items = course.syllabus_list.split('|') if course.syllabus_list else []
    return render_template('course_detail.html', title=f'{course.title} Bootcamp | 360IT Training', course=course, syllabus_items=syllabus_items)

@bp.route('/projects')
def projects():
    all_projects = Project.query.all()
    return render_template('projects.html', title='Projects & Contracts Portfolio | 360IT', projects=all_projects)

@bp.route('/projects/<slug>')
def project_detail(slug):
    project = Project.query.filter_by(slug=slug).first_or_404()
    tech_list = [t.strip() for t in project.tech_stack.split(',')]
    return render_template('project_detail.html', title=f'{project.title} | 360IT Projects', project=project, tech_list=tech_list)

@bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    results = {
        'services': [],
        'courses': [],
        'projects': [],
        'testimonials': [],
        'pages': []
    }
    if query:
        raw_words = [w.strip() for w in query.split() if len(w.strip()) > 1]
        words = [w for w in raw_words if w.lower() not in STOP_WORDS]
        if not words:
            words = raw_words or [query]

        # 1. Services
        service_filters = []
        for word in words:
            pattern = f"%{word}%"
            service_filters.append(
                (Service.title.ilike(pattern)) |
                (Service.short_desc.ilike(pattern)) |
                (Service.long_desc.ilike(pattern)) |
                (Service.features_list.ilike(pattern)) |
                (Service.category.ilike(pattern)) |
                (Service.platforms.ilike(pattern))
            )
        matched_services = Service.query.filter(db.or_(*service_filters)).all() if service_filters else []
        results['services'] = sorted(
            matched_services,
            key=lambda s: calculate_relevance(s, query, words, 'title', 'short_desc', 'long_desc', 'category'),
            reverse=True
        )

        # 2. Training Courses
        course_filters = []
        for word in words:
            pattern = f"%{word}%"
            course_filters.append(
                (TrainingCourse.title.ilike(pattern)) |
                (TrainingCourse.short_desc.ilike(pattern)) |
                (TrainingCourse.long_desc.ilike(pattern)) |
                (TrainingCourse.syllabus_list.ilike(pattern)) |
                (TrainingCourse.delivery_mode.ilike(pattern)) |
                (TrainingCourse.skill_level.ilike(pattern))
            )
        matched_courses = TrainingCourse.query.filter(db.or_(*course_filters)).all() if course_filters else []
        results['courses'] = sorted(
            matched_courses,
            key=lambda c: calculate_relevance(c, query, words, 'title', 'short_desc', 'long_desc', 'syllabus_list'),
            reverse=True
        )

        # 3. Projects
        project_filters = []
        for word in words:
            pattern = f"%{word}%"
            project_filters.append(
                (Project.title.ilike(pattern)) |
                (Project.industry.ilike(pattern)) |
                (Project.tech_stack.ilike(pattern)) |
                (Project.short_desc.ilike(pattern)) |
                (Project.long_desc.ilike(pattern)) |
                (Project.category.ilike(pattern))
            )
        matched_projects = Project.query.filter(db.or_(*project_filters)).all() if project_filters else []
        results['projects'] = sorted(
            matched_projects,
            key=lambda p: calculate_relevance(p, query, words, 'title', 'short_desc', 'long_desc', 'tech_stack'),
            reverse=True
        )

        # 4. Testimonials
        testimonial_filters = []
        for word in words:
            pattern = f"%{word}%"
            testimonial_filters.append(
                (Testimonial.name.ilike(pattern)) |
                (Testimonial.position.ilike(pattern)) |
                (Testimonial.organization.ilike(pattern)) |
                (Testimonial.quote.ilike(pattern)) |
                (Testimonial.service_type.ilike(pattern))
            )
        matched_testimonials = Testimonial.query.filter(db.or_(*testimonial_filters)).all() if testimonial_filters else []
        results['testimonials'] = sorted(
            matched_testimonials,
            key=lambda t: calculate_relevance(t, query, words, 'name', 'quote', 'organization', 'service_type'),
            reverse=True
        )

        # 5. Information Pages
        static_pages = [
            {'title': 'About Us', 'url': url_for('main.about'), 'desc': 'Learn about 360IT Learning & Consulting, our mission, core values, and enterprise solutions.'},
            {'title': 'Contact Us', 'url': url_for('main.contact'), 'desc': 'Get in touch with 360IT consultants, request inquiries, or visit our office location.'},
            {'title': 'Frequently Asked Questions (FAQs)', 'url': url_for('main.faqs'), 'desc': 'Common questions about our consulting services, bootcamp training, delivery options, and certifications.'},
            {'title': 'Privacy Policy', 'url': url_for('main.privacy'), 'desc': 'Information governance, data privacy, security practices, and compliance.'},
            {'title': 'Terms & Conditions', 'url': url_for('main.terms'), 'desc': 'Terms of service, consulting agreements, and website use guidelines.'}
        ]
        
        scored_pages = []
        for page in static_pages:
            score = 0
            combined_text = f"{page['title']} {page['desc']}".lower()
            if query.lower() in combined_text:
                score += 20
            for w in words:
                if w.lower() in combined_text:
                    score += 5
            if score > 0:
                scored_pages.append((score, page))
        
        results['pages'] = [p for s, p in sorted(scored_pages, key=lambda x: x[0], reverse=True)]

    total_count = (len(results['services']) + len(results['courses']) + 
                   len(results['projects']) + len(results['testimonials']) + 
                   len(results['pages']))
                   
    return render_template('search_results.html',
                           title=f'Search Results for "{query}" | 360IT' if query else 'Search | 360IT',
                           query=query,
                           results=results,
                           total_count=total_count)

@bp.route('/sitemap.xml')
def sitemap():
    services = Service.query.all()
    courses = TrainingCourse.query.all()
    projects = Project.query.all()
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    static_endpoints = ['main.index', 'main.about', 'main.services', 'main.training', 'main.projects', 'main.contact', 'main.faqs', 'main.privacy', 'main.terms']
    for ep in static_endpoints:
        xml.append(f'  <url><loc>{url_for(ep, _external=True)}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>')
        
    for s in services:
        xml.append(f'  <url><loc>{url_for("main.service_detail", slug=s.slug, _external=True)}</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>')
        
    for c in courses:
        xml.append(f'  <url><loc>{url_for("main.course_detail", slug=c.slug, _external=True)}</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>')
        
    for p in projects:
        xml.append(f'  <url><loc>{url_for("main.project_detail", slug=p.slug, _external=True)}</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>')
        
    xml.append('</urlset>')
    
    return Response('\n'.join(xml), mimetype='application/xml')

@bp.route('/robots.txt')
def robots():
    content = f"User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {url_for('main.sitemap', _external=True)}\n"
    return Response(content, mimetype='text/plain')

@bp.route('/faqs')
def faqs():
    return render_template('faqs.html', title='Frequently Asked Questions (FAQs) | 360IT Learning & Consulting')

@bp.route('/privacy')
def privacy():
    return render_template('privacy.html', title='Privacy Policy | 360IT Learning & Consulting')

@bp.route('/terms')
def terms():
    return render_template('terms.html', title='Terms & Conditions | 360IT Learning & Consulting')

@bp.route('/contact', methods=['GET', 'POST'])
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
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html', title='Contact Us | 360IT Learning & Consulting', form=form)

@bp.route('/request-consultation', methods=['POST'])
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
    return redirect(request.referrer or url_for('main.index'))

@bp.route('/enroll-course', methods=['POST'])
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
    return redirect(request.referrer or url_for('main.index'))

@bp.route('/newsletter-subscribe', methods=['POST'])
def newsletter_subscribe():
    email = request.form.get('email', '').strip().lower()
    source = request.form.get('source', 'Footer Form').strip()
    
    if not email or '@' not in email:
        flash('Please enter a valid email address to subscribe.', 'danger')
        return redirect(request.referrer or url_for('main.index'))
        
    try:
        subscriber = NewsletterSubscriber.query.filter_by(email=email).first()
        if subscriber:
            if subscriber.status == 'Unsubscribed':
                subscriber.status = 'Subscribed'
                subscriber.updated_at = datetime.utcnow()
                db.session.commit()
                flash('Welcome back! Your newsletter subscription has been reactivated.', 'success')
            else:
                flash('You are already subscribed to 360IT Tech Insights newsletter.', 'info')
        else:
            new_sub = NewsletterSubscriber(email=email, source=source, status='Subscribed')
            db.session.add(new_sub)
            db.session.commit()
            flash('Thank you for subscribing to 360IT Tech Insights newsletter!', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error subscribing email: {e}")
        flash('An error occurred while processing your subscription. Please try again.', 'danger')

    return redirect(request.referrer or url_for('main.index'))

