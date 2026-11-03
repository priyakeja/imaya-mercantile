document.addEventListener('DOMContentLoaded', () => {
    const hero = document.querySelector('.hero');
    if (!hero) return;

    const slides = Array.from(hero.querySelectorAll('.hero-slide'));
    const dots = Array.from(hero.querySelectorAll('.dot'));
    const prevBtn = hero.querySelector('.arrow-prev');
    const nextBtn = hero.querySelector('.arrow-next');

    const delay = (parseFloat(hero.dataset.delay) || 6) * 1000;
    const autoplay = hero.dataset.autoplay === 'true';

    let current = 0;
    let timer = null;

    function goTo(index) {
        index = (index + slides.length) % slides.length;
        if (index === current) return;

        const old = slides[current];
        old.classList.remove('active');
        old.classList.add('leaving');
        setTimeout(() => old.classList.remove('leaving'), 1000);

        slides[index].classList.add('active');

        if (dots[current]) dots[current].classList.remove('active');
        if (dots[index]) dots[index].classList.add('active');

        current = index;
    }

    function start() {
        if (!autoplay || slides.length < 2) return;
        stop();
        timer = setInterval(() => goTo(current + 1), delay);
    }

    function stop() {
        if (timer) clearInterval(timer);
    }

    if (slides.length < 2) return;

    if (nextBtn) nextBtn.addEventListener('click', () => { goTo(current + 1); start(); });
    if (prevBtn) prevBtn.addEventListener('click', () => { goTo(current - 1); start(); });
    dots.forEach(dot => {
        dot.addEventListener('click', () => { goTo(parseInt(dot.dataset.index, 10)); start(); });
    });

    start();
});