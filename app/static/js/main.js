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

    // ==========================================================================
    // 8. Cookie Engine & Management Suite
    // ==========================================================================
    const CookieManager = {
        set: function(name, value, days) {
            let expires = "";
            if (days) {
                const date = new Date();
                date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
                expires = "; expires=" + date.toUTCString();
            }
            document.cookie = name + "=" + encodeURIComponent(value) + expires + "; path=/; SameSite=Lax";
        },
        get: function(name) {
            const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
            return match ? decodeURIComponent(match[2]) : null;
        },
        delete: function(name) {
            document.cookie = name + '=; Max-Age=-99999999; path=/; SameSite=Lax';
        }
    };

    // Expose CookieManager globally
    window.CookieManager = CookieManager;

    // A. Cookie Consent Banner Logic
    const cookieBanner = document.getElementById('cookieBanner');
    const btnAcceptAll = document.getElementById('btnCookieAcceptAll');
    const btnEssential = document.getElementById('btnCookieEssential');

    if (cookieBanner) {
        const consent = CookieManager.get('cookie_consent');
        if (!consent) {
            setTimeout(() => {
                cookieBanner.style.display = 'block';
            }, 800);
        }

        if (btnAcceptAll) {
            btnAcceptAll.addEventListener('click', () => {
                CookieManager.set('cookie_consent', 'accepted', 365);
                cookieBanner.style.display = 'none';
                notifyToast('Cookie preferences saved: All cookies accepted.', 'success', 3000);
            });
        }

        if (btnEssential) {
            btnEssential.addEventListener('click', () => {
                CookieManager.set('cookie_consent', 'essential', 365);
                cookieBanner.style.display = 'none';
                notifyToast('Cookie preferences saved: Essential cookies only.', 'info', 3000);
            });
        }
    }

    // B. Theme Cookie Integration
    window.set360ITTheme = function(theme) {
        if (theme === 'dark') {
            document.documentElement.classList.add('theme-dark');
            localStorage.setItem('360it_theme', 'dark');
            CookieManager.set('360it_theme', 'dark', 365);
        } else {
            document.documentElement.classList.remove('theme-dark');
            localStorage.setItem('360it_theme', 'light');
            CookieManager.set('360it_theme', 'light', 365);
        }
    };

    // C. Marketing Campaign Lead Source Cookie Tracking
    const urlParams = new URLSearchParams(window.location.search);
    const utmSource = urlParams.get('utm_source') || urlParams.get('ref');
    const utmCampaign = urlParams.get('utm_campaign');
    if (utmSource) {
        const sourceVal = `source:${utmSource}` + (utmCampaign ? `|campaign:${utmCampaign}` : '');
        CookieManager.set('lead_source', sourceVal, 30);
    }

    // D. Recently Viewed Bootcamps Cookie
    const pageHeading = document.querySelector('h1')?.innerText || '';
    if (pageHeading.includes('Bootcamp') || window.location.pathname.includes('/courses/')) {
        const courseTitle = pageHeading.replace(' Bootcamp', '').trim();
        if (courseTitle) {
            let recent = [];
            try {
                recent = JSON.parse(CookieManager.get('recent_courses') || '[]');
            } catch (e) {
                recent = [];
            }
            recent = recent.filter(c => c !== courseTitle);
            recent.unshift(courseTitle);
            if (recent.length > 3) recent = recent.slice(0, 3);
            CookieManager.set('recent_courses', JSON.stringify(recent), 30);
        }
    }

    // Auto-suggest recently viewed course in enrollment modal if no course selected
    document.querySelectorAll('[data-open-modal="enrollment"]').forEach(btn => {
        btn.addEventListener('click', () => {
            const selectElem = document.querySelector('#enrollmentModal select[name="course_title"]');
            if (selectElem && (!selectElem.value || selectElem.value === '')) {
                try {
                    const recent = JSON.parse(CookieManager.get('recent_courses') || '[]');
                    if (recent.length > 0 && Array.from(selectElem.options).some(o => o.value === recent[0])) {
                        selectElem.value = recent[0];
                        notifyToast(`Auto-selected your recently viewed bootcamp: ${recent[0]}`, 'info', 3000);
                    }
                } catch (e) {}
            }
        });
    });

    // E. Unsaved Form Draft Recovery Cookie Persistence
    const formsToSave = document.querySelectorAll('#main-contact-form, #contact-page-form, #consultationModal form');
    formsToSave.forEach(form => {
        const formId = form.id || 'form_draft';
        // Restore saved draft input if present
        const savedDraft = CookieManager.get(`draft_${formId}`);
        if (savedDraft) {
            try {
                const fields = JSON.parse(savedDraft);
                Object.keys(fields).forEach(name => {
                    const input = form.querySelector(`[name="${name}"]`);
                    if (input && !input.value) {
                        input.value = fields[name];
                    }
                });
            } catch (e) {}
        }

        // Save draft on input change
        form.addEventListener('input', () => {
            const formData = {};
            const inputs = form.querySelectorAll('input:not([type="hidden"]), textarea');
            inputs.forEach(input => {
                if (input.name && input.value) {
                    formData[input.name] = input.value;
                }
            });
            CookieManager.set(`draft_${formId}`, JSON.stringify(formData), 7);
        });

        // Clear draft cookie upon form submission
        form.addEventListener('submit', () => {
            CookieManager.delete(`draft_${formId}`);
        });
    });
});

