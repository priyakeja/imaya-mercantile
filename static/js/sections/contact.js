(function () {
    'use strict';

        /* email link: mobile la mail app, desktop la Gmail compose */
    const mailLink = document.querySelector('[data-mailto]');
    if (mailLink && /Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) {
        mailLink.href = mailLink.dataset.mailto;
        mailLink.removeAttribute('target');
    }

    const form = document.getElementById('enquiryForm');
    if (!form) return;

    /* ---------- country list (server la irundhu) ---------- */
    const dataEl = document.getElementById('countryData');
    const cdata = dataEl ? JSON.parse(dataEl.textContent) : { countries: [], aliases: {} };
    const countryMap = new Map();
    cdata.countries.forEach(c => countryMap.set(c.toLowerCase(), c));
    Object.keys(cdata.aliases).forEach(k => countryMap.set(k.toLowerCase(), cdata.aliases[k]));
    const findCountry = v => countryMap.get(v.replace(/\s+/g, ' ').trim().toLowerCase());

    /* ---------- validators (order = form order) ---------- */
    const validators = {
        name(v) {
            if (!v) return 'Please enter your name.';
            if (v.length < 3) return 'Name must be at least 3 characters.';
            if (!/^\p{L}[\p{L}\p{M} .'’-]*$/u.test(v)) return "Name can contain only letters, spaces and . ' -";
            return '';
        },
        country(v) {
            if (!v) return 'Please enter your country.';
            if (!findCountry(v)) return 'Please enter a valid country name (for example: India).';
            return '';
        },
        email(v) {
            if (!v) return 'Please enter your email address.';
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return 'Please enter a valid email address (for example: name@example.com).';
            return '';
        },
        quantity(v) {
            if (!v) return '';
            if (!/^\d+$/.test(v)) return 'Required quantity must be a number (digits only).';
            if (Number(v) === 0) return 'Required quantity must be greater than 0.';
            return '';
        },
        phone(v) {
            if (!v) return '';
            if (!/^\d{10}$/.test(v)) return 'Phone number must be exactly 10 digits.';
            return '';
        },
        message(v) {
            if (!v) return 'Please enter your message.';
            return '';
        },
    };

    const fields = {};
    Object.keys(validators).forEach(n => { fields[n] = form.querySelector('[name="' + n + '"]'); });

    function setError(name, msg) {
        const el = fields[name];
        if (!el) return;
        const wrap = el.closest('.field');
        wrap.classList.toggle('has-error', !!msg);
        wrap.querySelector('.field-error').textContent = msg || '';
        el.setAttribute('aria-invalid', msg ? 'true' : 'false');
    }

    function check(name) {
        const msg = validators[name](fields[name].value.trim());
        setError(name, msg);
        return !msg;
    }

    Object.keys(fields).forEach(n => {
        const el = fields[n];
        el.addEventListener('blur', () => {
            if (n === 'country') {
                const proper = findCountry(el.value);
                if (proper) el.value = proper;
            }
            check(n);
        });
        el.addEventListener('input', () => {
            if (n === 'quantity' || n === 'phone') el.value = el.value.replace(/\D/g, '');
            if (el.closest('.field').classList.contains('has-error')) check(n);
        });
    });

    /* ---------- status message ---------- */
    const statusEl = document.getElementById('formStatus');
    function showStatus(text, type) {
        statusEl.textContent = text;
        statusEl.className = 'form-status show ' + type;
    }
    function hideStatus() { statusEl.className = 'form-status'; statusEl.textContent = ''; }

    /* ---------- products multi select ---------- */
    const sel = document.getElementById('productSelect');
    if (sel) {
        const btn = sel.querySelector('.select-btn');
        const panel = sel.querySelector('.select-panel');
        const val = sel.querySelector('.select-value');
        const placeholder = val.dataset.placeholder;

        const setOpen = open => {
            panel.hidden = !open;
            btn.setAttribute('aria-expanded', open ? 'true' : 'false');
            sel.classList.toggle('open', open);
        };
        const refresh = () => {
            const chosen = Array.from(panel.querySelectorAll('input:checked')).map(i => i.value);
            val.textContent = chosen.length ? chosen.join(', ') : placeholder;
            btn.classList.toggle('has-value', chosen.length > 0);
        };

        btn.addEventListener('click', () => setOpen(panel.hidden));
        panel.addEventListener('change', refresh);
        document.addEventListener('click', e => { if (!sel.contains(e.target)) setOpen(false); });
        document.addEventListener('keydown', e => { if (e.key === 'Escape') setOpen(false); });
        form.addEventListener('reset', () => setTimeout(refresh, 0));
    }

    /* ---------- submit ---------- */
    const submitBtn = form.querySelector('.enq-submit');
    const submitLabel = submitBtn.querySelector('.enq-label');
    const labelText = submitLabel.textContent;

    form.addEventListener('submit', async e => {
        e.preventDefault();
        hideStatus();

        let firstBad = null;
        Object.keys(validators).forEach(n => {
            if (!check(n) && !firstBad) firstBad = fields[n];
        });
        if (firstBad) {
            showStatus('Please correct the highlighted fields before submitting.', 'error');
            firstBad.focus();
            return;
        }

        const proper = findCountry(fields.country.value);
        if (proper) fields.country.value = proper;

        submitBtn.disabled = true;
        submitLabel.textContent = 'Sending…';

        try {
            const res = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
            });
            let data = {};
            try { data = await res.json(); } catch (_) { /* ignore */ }

            if (res.ok && data.ok) {
                form.reset();
                Object.keys(fields).forEach(n => setError(n, ''));
                showStatus(data.message, 'success');
            } else {
                if (data.errors) Object.keys(data.errors).forEach(n => setError(n, data.errors[n]));
                showStatus(data.message || 'Something went wrong. Please try again.', 'error');
            }
        } catch (err) {
            showStatus('Network error. Please check your connection and try again.', 'error');
        } finally {
            submitBtn.disabled = false;
            submitLabel.textContent = labelText;
        }
    });
})();