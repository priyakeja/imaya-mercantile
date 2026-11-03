document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('.site-header');
    const toggle = document.getElementById('navToggle');
    const nav = document.getElementById('mainNav');
    const links = Array.from(document.querySelectorAll('.main-nav ul a'));

    /* mobile menu */
    if (toggle && nav) {
        toggle.addEventListener('click', () => {
            toggle.classList.toggle('open');
            nav.classList.toggle('open');
        });
        links.forEach(a => a.addEventListener('click', () => {
            toggle.classList.remove('open');
            nav.classList.remove('open');
        }));
    }

    /* menu link -> section map */
    const map = links.map(a => {
        const href = a.getAttribute('href') || '';
        if (href.startsWith('#') && href.length > 1) {
            const sec = document.querySelector(href);
            if (sec) return { a, sec };
        }
        return null;
    }).filter(Boolean);

    const homeLink = links.find(a => ['/', '#home'].includes(a.getAttribute('href')));

    function update() {
        if (header) header.classList.toggle('scrolled', window.scrollY > 40);

        const y = window.scrollY + 140;
        let current = null;
        map.forEach(m => {
            const top = m.sec.getBoundingClientRect().top + window.scrollY;
            if (top <= y) current = m;
        });

        links.forEach(a => a.classList.remove('active'));
        if (current) current.a.classList.add('active');
        else if (homeLink) homeLink.classList.add('active');
    }

    window.addEventListener('scroll', update, { passive: true });
    update();
});