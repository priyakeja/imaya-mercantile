(function () {
    const items = document.querySelectorAll('[data-reveal]');
    if (!items.length) return;

    items.forEach(el => {
        if (el.dataset.delay) el.style.setProperty('--d', el.dataset.delay + 'ms');
    });

    if (!('IntersectionObserver' in window)) {
        items.forEach(el => el.classList.add('is-visible'));
        return;
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });

    items.forEach(el => observer.observe(el));
})();