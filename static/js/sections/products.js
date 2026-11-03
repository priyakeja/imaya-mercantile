document.addEventListener('DOMContentLoaded', () => {
    let active = null;
    let lastTrigger = null;

    function openModal(id, trigger) {
        const modal = document.getElementById(id);
        if (!modal) return;

        active = modal;
        lastTrigger = trigger;
        modal.classList.add('open');
        document.body.classList.add('modal-open');

        const body = modal.querySelector('.pmodal-body');
        if (body) body.scrollTop = 0;

        const closeBtn = modal.querySelector('.pmodal-close');
        if (closeBtn) closeBtn.focus({ preventScroll: true });
    }

    function closeModal() {
        if (!active) return;
        active.classList.remove('open');
        document.body.classList.remove('modal-open');
        if (lastTrigger) lastTrigger.focus({ preventScroll: true });
        active = null;
    }

    document.querySelectorAll('[data-modal-open]').forEach(btn => {
        btn.addEventListener('click', () => openModal(btn.dataset.modalOpen, btn));
    });

    document.querySelectorAll('[data-modal-close]').forEach(el => {
        el.addEventListener('click', closeModal);
    });

    document.addEventListener('keydown', e => {
        if (e.key === 'Escape') closeModal();
    });
});