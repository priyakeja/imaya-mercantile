document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.about-tab');
    const panels = document.querySelectorAll('.about-panel');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));

            tab.classList.add('active');
            const panel = document.getElementById(tab.dataset.tab);
            if (panel) panel.classList.add('active');
        });
    });
});