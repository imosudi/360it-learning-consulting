/* ==========================================================================
   360IT Learning & Consulting - Interactive Frontend Scripts
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Sticky Navbar & Scroll Effects
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 40) {
            navbar?.classList.add('scrolled');
        } else {
            navbar?.classList.remove('scrolled');
        }
    });

    // 2. Mobile Drawer Navigation Toggle
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

    // 3. Projects Category Filter Buttons
    const filterBtns = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filterValue = btn.getAttribute('data-filter');

            projectCards.forEach(card => {
                const category = card.getAttribute('data-category');
                if (filterValue === 'all' || category === filterValue) {
                    card.style.display = 'flex';
                    card.style.opacity = '1';
                } else {
                    card.style.display = 'none';
                    card.style.opacity = '0';
                }
            });
        });
    });

    // 4. Modal Triggers (Consultation & Enrollment Modals)
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
});
