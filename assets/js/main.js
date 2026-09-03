/**
 * FONDATION ÉCOLE KÉ BIEN — ÉCOLE KÉ FUTA (EKBF)
 * Main JavaScript Engine
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Sticky Header Effect
    const header = document.querySelector('.header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 30) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }

    // 2. Mobile Menu Toggle with Body Scroll Lock
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (mobileToggle && navMenu) {
        mobileToggle.addEventListener('click', () => {
            const isOpen = navMenu.classList.toggle('open');
            document.body.classList.toggle('menu-open', isOpen);
            const icon = mobileToggle.querySelector('i');
            if (icon) {
                if (isOpen) {
                    icon.classList.remove('fa-bars');
                    icon.classList.add('fa-xmark');
                } else {
                    icon.classList.remove('fa-xmark');
                    icon.classList.add('fa-bars');
                }
            }
        });

        // Close menu on link click
        navMenu.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('open');
                document.body.classList.remove('menu-open');
                const icon = mobileToggle.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-xmark');
                    icon.classList.add('fa-bars');
                }
            });
        });
    }

    // 3. Scroll Reveal Animation via IntersectionObserver
    const revealElements = document.querySelectorAll('.reveal');
    if ('IntersectionObserver' in window && revealElements.length > 0) {
        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            root: null,
            threshold: 0.12,
            rootMargin: '0px 0px -40px 0px'
        });

        revealElements.forEach(el => revealObserver.observe(el));
    } else {
        // Fallback for older browsers
        revealElements.forEach(el => el.classList.add('active'));
    }

    // 4. Countdown Timer to JSB 2027 (Target: March 15, 2027)
    const targetDate = new Date('2027-03-15T08:30:00').getTime();
    
    function updateCountdown() {
        const now = new Date().getTime();
        const difference = targetDate - now;

        if (difference > 0) {
            const days = Math.floor(difference / (1000 * 60 * 60 * 24));
            const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((difference % (1000 * 60)) / 1000);

            const daysEl = document.getElementById('cd-days');
            const hoursEl = document.getElementById('cd-hours');
            const minutesEl = document.getElementById('cd-minutes');
            const secondsEl = document.getElementById('cd-seconds');

            if (daysEl) daysEl.innerText = days < 10 ? '0' + days : days;
            if (hoursEl) hoursEl.innerText = hours < 10 ? '0' + hours : hours;
            if (minutesEl) minutesEl.innerText = minutes < 10 ? '0' + minutes : minutes;
            if (secondsEl) secondsEl.innerText = seconds < 10 ? '0' + seconds : seconds;
        }
    }

    if (document.getElementById('cd-days')) {
        updateCountdown();
        setInterval(updateCountdown, 1000);
    }

    // 5. Interactive FAQ Accordion
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        if (question) {
            question.addEventListener('click', () => {
                const isActive = item.classList.contains('active');
                // Close all others
                faqItems.forEach(other => other.classList.remove('active'));
                if (!isActive) {
                    item.classList.add('active');
                }
            });
        }
    });

    // 6. Active Navbar Link on Scroll
    const sections = document.querySelectorAll('section[id]');
    function highlightNav() {
        const scrollY = window.pageYOffset;
        sections.forEach(current => {
            const sectionHeight = current.offsetHeight;
            const sectionTop = current.offsetTop - 120;
            const sectionId = current.getAttribute('id');
            const navItem = document.querySelector(`.nav-menu a[href*=${sectionId}]`);
            if (navItem) {
                if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                    navItem.classList.add('active');
                } else {
                    navItem.classList.remove('active');
                }
            }
        });
    }
    window.addEventListener('scroll', highlightNav);

    // 7. Interactive Official Badge Simulator
    const simTabs = document.querySelectorAll('.sim-tab-btn');
    const simCard = document.getElementById('sim-badge-card');
    const simHeader = document.getElementById('sim-badge-header');
    const simSecPill = document.getElementById('sim-sec-pill');
    const simRoleTitle = document.getElementById('sim-role-title');
    const simRoleDesc = document.getElementById('sim-role-desc');
    const simRolePill = document.getElementById('sim-role-pill');
    const simCodeTxt = document.getElementById('sim-code-txt');
    const simCtaBtn = document.getElementById('sim-cta-btn');
    const simNameInput = document.getElementById('sim-name-input');
    const simAttendeeName = document.getElementById('sim-attendee-name');
    const simAttendeeAffil = document.getElementById('sim-attendee-affil');

    const roleConfigs = {
        auditeur: {
            borderClass: 'card-border-auditeur',
            headerClass: 'auditeur',
            secText: 'Accréditation Officielle',
            roleTitle: 'Participant / Auditeur',
            roleDesc: 'Accès Conférences, Ateliers & Posters',
            rolePillBorder: '#38bdf8',
            rolePillBg: '#eff6ff',
            roleTitleColor: '#163b5c',
            roleDescColor: '#0284c7',
            codePrefix: 'JSB27-AUD-1484',
            defaultAffil: 'Université Marien Ngouabi • Brazzaville',
            btnText: "S'inscrire comme Auditeur (Badge Offert)",
            btnIcon: 'fa-ticket'
        },
        candidat: {
            borderClass: 'card-border-candidat',
            headerClass: 'candidat',
            secText: 'Prix Innovation 2027',
            roleTitle: 'Candidat au Grand Prix',
            roleDesc: 'Compétition & Pitch devant le Jury',
            rolePillBorder: '#f97316',
            rolePillBg: '#fff7ed',
            roleTitleColor: '#c2410c',
            roleDescColor: '#ea580c',
            codePrefix: 'JSB27-CAN-7602',
            defaultAffil: 'Enseignant-Chercheur / Innovateur • IRA',
            btnText: 'Déposer ma Candidature au Grand Prix',
            btnIcon: 'fa-trophy'
        },
        partenaire: {
            borderClass: 'card-border-partenaire',
            headerClass: 'partenaire',
            secText: 'Accès VIP Officiel',
            roleTitle: 'Partenaire & Sponsoring',
            roleDesc: 'Accès VIP & Espace Partenaires',
            rolePillBorder: '#10b981',
            rolePillBg: '#f0fdf4',
            roleTitleColor: '#065f46',
            roleDescColor: '#059669',
            codePrefix: 'JSB27-SPO-1969',
            defaultAffil: 'Institution / Entreprise Partenaire',
            btnText: 'Devenir Partenaire Officiel JSB 2027',
            btnIcon: 'fa-handshake'
        }
    };

    if (simTabs.length > 0 && simCard) {
        simTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const role = tab.getAttribute('data-role');
                if (!roleConfigs[role]) return;

                simTabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');

                const cfg = roleConfigs[role];
                
                // Update card border
                simCard.className = 'sim-badge-card ' + cfg.borderClass;
                
                // Update header
                simHeader.className = 'sim-badge-header ' + cfg.headerClass;
                simSecPill.innerText = cfg.secText;
                
                // Update role pill
                simRoleTitle.innerText = cfg.roleTitle;
                simRoleDesc.innerText = cfg.roleDesc;
                simRoleTitle.style.color = cfg.roleTitleColor;
                simRoleDesc.style.color = cfg.roleDescColor;
                simRolePill.style.backgroundColor = cfg.rolePillBg;
                simRolePill.style.borderColor = cfg.rolePillBorder;

                // Update code and affiliation
                simCodeTxt.innerText = cfg.codePrefix;
                if (simAttendeeAffil) simAttendeeAffil.innerText = cfg.defaultAffil;

                // Update CTA button
                if (simCtaBtn) {
                    simCtaBtn.innerHTML = `<i class="fa-solid ${cfg.btnIcon}"></i> ${cfg.btnText}`;
                }
            });
        });
    }

    if (simNameInput && simAttendeeName) {
        simNameInput.addEventListener('input', (e) => {
            const val = e.target.value.trim();
            simAttendeeName.innerText = val ? val : 'Dr. Yannick Okouakoua';
        });
    }
});
