/**
 * Interacciones dinámicas para el Panel de Banco de Preguntas.
 * Cumple con políticas de CSP (sin inline JS, eventos delegados en document).
 */

// ── Acordeón fluido ──────────────────────────────────────────────────────────

function initSmoothAccordion(root) {
    const base = root || document;
    base.querySelectorAll('.acc details, .gen-level, .eval-config-panel').forEach(el => {
        if (el._smooth) return;
        el._smooth = true;

        const summary = el.querySelector(':scope > summary');
        if (!summary) return;

        // Impedir que el clic en un checkbox haga toggle del acordeón
        summary.querySelectorAll('.q-check, .q-select-all').forEach(cb => {
            cb.addEventListener('click', e => e.stopPropagation());
        });

        summary.addEventListener('click', e => {
            e.preventDefault();
            if (el._animating) return;

            const body = el.querySelector(':scope > div');
            if (!body) return;

            el._animating = true;
            const ease = '0.28s cubic-bezier(0.4,0,0.2,1)';
            let timer;

            const onHeightEnd = (cb) => {
                const handler = (ev) => {
                    if (ev.propertyName !== 'height') return;
                    body.removeEventListener('transitionend', handler);
                    cb();
                };
                body.addEventListener('transitionend', handler);
            };

            const done = (removing) => {
                clearTimeout(timer);
                if (removing) el.removeAttribute('open');
                body.style.cssText = '';
                el._animating = false;
            };

            if (el.open) {
                // CLOSE: atenuar contenido y colapsar altura
                const h = body.scrollHeight;
                body.style.overflow = 'hidden';
                body.style.height = h + 'px';
                body.style.opacity = '1';
                body.offsetHeight; // forzar reflow
                body.style.transition = 'height ' + ease + ', opacity 0.1s ease';
                body.style.height = '0px';
                body.style.opacity = '0';
                onHeightEnd(() => done(true));
                timer = setTimeout(() => done(true), 400);
            } else {
                // OPEN: fijar height=0 antes de hacer visible → sin flash
                body.style.overflow = 'hidden';
                body.style.height = '0px';
                el.setAttribute('open', '');
                const h = body.scrollHeight;
                body.style.transition = 'height ' + ease;
                body.style.height = h + 'px';
                onHeightEnd(() => done(false));
                timer = setTimeout(() => done(false), 400);
            }
        });
    });
}

// ── Bulk actions ─────────────────────────────────────────────────────────────

function updateBulkBar(qlist) {
    if (!qlist || !qlist.id) return;
    const suffix = qlist.id.replace('qlist-', '');
    const bar = document.getElementById('bulk-bar-' + suffix);
    if (!bar) return;

    const checked = qlist.querySelectorAll('.q-check:checked');
    if (checked.length > 0) {
        bar.hidden = false;
        const countEl = bar.querySelector('.bulk-bar__count');
        if (countEl) {
            const n = checked.length;
            countEl.textContent = n + ' seleccionada' + (n === 1 ? '' : 's');
        }
    } else {
        bar.hidden = true;
        const modeBody = bar.closest('.acc-mode__body');
        if (modeBody) {
            const sa = modeBody.querySelector('.q-select-all');
            if (sa) sa.checked = false;
        }
    }
}

function resetBulkBar(qlistId) {
    const suffix = qlistId.replace('qlist-', '');
    const bar = document.getElementById('bulk-bar-' + suffix);
    if (!bar) return;
    bar.hidden = true;
    const modeBody = bar.closest('.acc-mode__body');
    if (modeBody) {
        const sa = modeBody.querySelector('.q-select-all');
        if (sa) sa.checked = false;
    }
}

// ── Generación con IA (orquestador por niveles/modos) ─────────────────────────

const GENX_MODE_LABEL = { preparacion: 'Práctica', evaluacion: 'Evaluación' };
const GENX_BATCH = 5; // tope por petición para no chocar el timeout de gunicorn

function initGenx() {
    const root = document.querySelector('[data-genx]');
    if (!root) return;
    const url = root.dataset.genUrl;
    const runBtn = document.getElementById('genx-run');
    const log = document.getElementById('genx-log');

    // Habilitar/atenuar la config de cada nivel según su checkbox.
    root.querySelectorAll('.genx-level').forEach(lv => {
        const enable = lv.querySelector('.genx-level-enable');
        const cfg = lv.querySelector('.genx-level__cfg');
        const sync = () => lv.classList.toggle('is-on', enable.checked);
        enable.addEventListener('change', sync);
        sync();
    });

    function csrf() {
        const meta = document.querySelector('meta[name=csrf-token]');
        if (meta) return meta.getAttribute('content');
        const inp = document.querySelector('[name=csrfmiddlewaretoken]');
        return inp ? inp.value : '';
    }

    function appendLog(text) {
        const line = document.createElement('div');
        line.className = 'genx-log__line';
        line.textContent = text;
        log.appendChild(line);
        return line;
    }

    async function runJob(job, line) {
        const qlist = document.getElementById('qlist-' + job.level + '-' + job.mode);
        if (qlist) {
            const mode = qlist.closest('.acc-mode');
            const lvl = qlist.closest('.acc-level');
            if (lvl) lvl.setAttribute('open', '');
            if (mode) mode.setAttribute('open', '');
        }
        let done = 0;
        let remaining = job.count;
        const label = GENX_MODE_LABEL[job.mode] || job.mode;
        while (remaining > 0) {
            const batch = Math.min(GENX_BATCH, remaining);
            const body = new URLSearchParams();
            body.set('level', job.level);
            body.set('mode', job.mode);
            body.set('source', 'video');
            body.set('count', String(batch));
            if (job.desc) body.set('description', job.desc);
            line.textContent = 'Nivel ' + job.level + ' · ' + label + ': ' + done + '/' + job.count + '…';
            try {
                const resp = await fetch(url, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': csrf(), 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: body.toString(),
                });
                const html = await resp.text();
                if (qlist) {
                    const empty = qlist.querySelector('.acc-empty');
                    if (empty) empty.remove();
                    qlist.insertAdjacentHTML('beforeend', html);
                    if (window.htmx) window.htmx.process(qlist);
                    initSmoothAccordion(qlist);
                }
            } catch (err) {
                line.textContent = 'Nivel ' + job.level + ' · ' + label + ': error de red.';
                return;
            }
            done += batch;
            remaining -= batch;
        }
        line.textContent = 'Nivel ' + job.level + ' · ' + label + ': ' + job.count + ' generadas ✓';
    }

    runBtn.addEventListener('click', async () => {
        const jobs = [];
        root.querySelectorAll('.genx-level').forEach(lv => {
            if (!lv.querySelector('.genx-level-enable').checked) return;
            const level = lv.dataset.level;
            const desc = lv.querySelector('.genx-desc').value.trim();
            lv.querySelectorAll('.genx-mode-enable').forEach(cb => {
                if (!cb.checked) return;
                const mode = cb.dataset.mode;
                const input = lv.querySelector('.genx-mode-count[data-mode="' + mode + '"]');
                const count = Math.max(0, parseInt(input.value, 10) || 0);
                if (count > 0) jobs.push({ level, mode, count, desc });
            });
        });

        log.hidden = false;
        log.innerHTML = '';
        if (!jobs.length) {
            appendLog('Habilita al menos un nivel y un modo (práctica o evaluación) con cantidad mayor a 0.');
            return;
        }

        runBtn.disabled = true;
        for (const job of jobs) {
            const line = appendLog('Nivel ' + job.level + ' · ' + (GENX_MODE_LABEL[job.mode] || job.mode) + ': 0/' + job.count + '…');
            await runJob(job, line);
        }
        runBtn.disabled = false;
    });
}

// ── Init ─────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    initSmoothAccordion();
    initGenx();

    // 1. Toggle alternativas (Opciones)
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.btn-toggle-choices');
        if (!btn) return;
        const sel = btn.getAttribute('data-target');
        if (sel) {
            const row = document.querySelector(sel);
            if (row) row.classList.toggle('d-none');
        }
    });

    // 2. Cerrar alertas
    document.addEventListener('click', (e) => {
        const close = e.target.closest('.alert-close');
        if (!close) return;
        const alert = close.closest('.alert');
        if (alert) alert.remove();
    });

    // 3. Checkboxes individuales → actualizar bulk bar
    document.addEventListener('change', (e) => {
        if (e.target.classList.contains('q-check')) {
            const qlist = e.target.closest('.acc-qlist');
            if (!qlist) return;
            updateBulkBar(qlist);
            // Sincronizar select-all
            const modeBody = qlist.closest('.acc-mode__body');
            if (modeBody) {
                const all = qlist.querySelectorAll('.q-check');
                const ch  = qlist.querySelectorAll('.q-check:checked');
                const sa  = modeBody.querySelector('.q-select-all');
                if (sa) sa.checked = all.length > 0 && all.length === ch.length;
            }
        }

        // Select-all → marcar/desmarcar todo el modo
        if (e.target.classList.contains('q-select-all')) {
            const modeBody = e.target.closest('.acc-mode__body');
            if (!modeBody) return;
            const qlistId = e.target.dataset.qlist;
            const qlist   = qlistId ? document.getElementById(qlistId) : modeBody.querySelector('.acc-qlist');
            if (!qlist) return;
            qlist.querySelectorAll('.q-check').forEach(cb => { cb.checked = e.target.checked; });
            updateBulkBar(qlist);
        }
    });

    // 4. Botones de acción en lote (fetch CSP-safe)
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.bulk-action-btn');
        if (!btn) return;

        const action  = btn.dataset.action;
        const url     = btn.dataset.url;
        const qlistId = btn.dataset.qlist;
        const level   = btn.dataset.level;
        const mode    = btn.dataset.mode;
        const qlist   = document.getElementById(qlistId);
        if (!qlist || !url) return;

        const selected = Array.from(qlist.querySelectorAll('.q-check:checked')).map(cb => cb.value);
        if (selected.length === 0) return;

        if (action === 'eliminar') {
            const n = selected.length;
            if (!confirm('¿Eliminar ' + n + ' pregunta' + (n === 1 ? '' : 's') + '? Esta acción no se puede deshacer.')) return;
        }

        const csrf = document.querySelector('[name=csrfmiddlewaretoken]');
        const fd   = new FormData();
        if (csrf) fd.append('csrfmiddlewaretoken', csrf.value);
        fd.append('action', action);
        fd.append('level', level);
        fd.append('mode', mode);
        selected.forEach(id => fd.append('selected_questions', id));

        fetch(url, { method: 'POST', body: fd, headers: { 'HX-Request': 'true' } })
            .then(r => r.text())
            .then(html => {
                qlist.innerHTML = html;
                initSmoothAccordion(qlist);
                resetBulkBar(qlistId);
            })
            .catch(err => console.error('Bulk action error:', err));
    });

    // 5. Restaurar listeners tras actualizaciones HTMX
    document.addEventListener('htmx:afterSwap', (e) => {
        initSmoothAccordion(e.detail.target);
        if (e.detail.target.id && e.detail.target.id.startsWith('qlist-')) {
            resetBulkBar(e.detail.target.id);
        }
    });
});
