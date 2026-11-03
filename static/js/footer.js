(function () {
    'use strict';

    /* email links: mobile la mail app, desktop la Gmail compose */
    if (/Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) {
        document.querySelectorAll('[data-mailto]').forEach(function (link) {
            link.href = link.dataset.mailto;
            link.removeAttribute('target');
        });
    }
})();