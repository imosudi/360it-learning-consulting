/* ==========================================================================
   360IT Learning & Consulting - Interactive Frontend Scripts
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Toastify Notification Helper
    function notifyToast(text, type = 'info', duration = 3500) {
        if (typeof Toastify === 'function') {
            let bgGradient = 'linear-gradient(135deg, #0d6efd 0%, #0284c7 100%)';
            if (type === 'success') {
                bgGradient = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
            } else if (type === 'warning') {
                bgGradient = 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)';
            } else if (type === 'error') {
                bgGradient = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
            }

            Toastify({
                text: text,
                duration: duration,
                close: true,
                gravity: 'top',
                position: 'right',
                stopOnFocus: true,
                style: {
                    background: bgGradient,
                    borderRadius: '12px',
                    boxShadow: '0 10px 25px rgba(0, 0, 0, 0.15)',
                    fontFamily: "'Plus Jakarta Sans', sans-serif",
                    fontSize: '0.9rem',
                    fontWeight: '600',
                    color: '#ffffff',
                    padding: '12px 20px'
                }
            }).showToast();
        }
    }

    // 2. Sticky Navbar & Scroll Effects
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 40) {
            navbar?.classList.add('scrolled');
        } else {
            navbar?.classList.remove('scrolled');
        }
    });

    // 3. Mobile Drawer Navigation Toggle
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navLinks = document.querySelector('.nav-links');
    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const icon = mobileToggle.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-bars');
                icon.classList.toggle('fa-times');
            }
        });
    }

    // 4. Projects Category Filter Buttons with AOS & Toastify Refresh
    const filterBtns = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filterValue = btn.getAttribute('data-filter');
            const catLabel = btn.innerText || filterValue;
            
            notifyToast(`Filtered projects by: ${catLabel}`, 'info', 2500);

            projectCards.forEach(card => {
                const category = card.getAttribute('data-category');
                if (filterValue === 'all' || category === filterValue) {
                    card.style.display = 'flex';
                    card.style.opacity = '1';
                    card.classList.add('aos-animate');
                } else {
                    card.style.display = 'none';
                    card.style.opacity = '0';
                }
            });

            if (typeof AOS !== 'undefined') {
                AOS.refresh();
            }
        });
    });

    // 5. Card Mouse Over Effects & Toastify Hinting
    const allInteractiveCards = document.querySelectorAll('.course-card, .service-card, .project-card');
    allInteractiveCards.forEach(card => {
        // Smooth hover tilt & shadow elevation on mouseover
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-6px)';
            card.style.transition = 'all 0.3s cubic-bezier(0.16, 1, 0.3, 1)';
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });

    // Toastify Feedback when clicking "Enroll Now"
    document.querySelectorAll('[data-open-modal="enrollment"]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const courseTitle = btn.getAttribute('data-course') || 'Program';
            notifyToast(`Selected: ${courseTitle}. Reserve your spot below!`, 'success', 4000);
        });
    });

    // Toastify Feedback when clicking "Schedule Consultation"
    document.querySelectorAll('[data-open-modal="consultation"]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            notifyToast('Opening enterprise consultation request modal...', 'info', 3000);
        });
    });

    // 6. Modal Triggers (Consultation & Enrollment Modals)
    const consultationModal = document.getElementById('consultationModal');
    const enrollmentModal = document.getElementById('enrollmentModal');
    
    document.querySelectorAll('[data-open-modal="consultation"]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            if (consultationModal) consultationModal.classList.add('active');
        });
    });

    document.querySelectorAll('[data-open-modal="enrollment"]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const courseTitle = btn.getAttribute('data-course');
            if (enrollmentModal) {
                if (courseTitle) {
                    const selectElem = enrollmentModal.querySelector('select[name="course_title"]');
                    if (selectElem) selectElem.value = courseTitle;
                }
                enrollmentModal.classList.add('active');
            }
        });
    });

    // Modal Close buttons
    document.querySelectorAll('.modal-close, .modal-overlay').forEach(element => {
        element.addEventListener('click', (e) => {
            if (e.target === element || element.classList.contains('modal-close')) {
                consultationModal?.classList.remove('active');
                enrollmentModal?.classList.remove('active');
            }
        });
    });

    // Prevent closing when clicking inside modal box
    document.querySelectorAll('.modal-container').forEach(box => {
        box.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    });

    // 7. Form Submissions with Toastify Feedback
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const action = form.getAttribute('action') || '';
            if (action.includes('newsletter')) {
                notifyToast('Thank you for subscribing to 360IT Tech Updates!', 'success', 4000);
            }
        });
    });
});
