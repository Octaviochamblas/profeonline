/**
 * Interacciones dinámicas para el Generador de Preguntas IA.
 * Cumple con políticas de CSP (sin inline JS, eventos delegados en document).
 */

document.addEventListener('DOMContentLoaded', () => {
    // 0. Plegar/desplegar nodos del árbol (acordeón).
    document.addEventListener('click', (event) => {
        const toggle = event.target.closest('.tree-toggle');
        if (!toggle) return;
        const node = toggle.closest('.tree-area, .tree-subject, .tree-topic');
        if (!node) return;
        const children = node.querySelector(':scope > .tree-children');
        if (!children) return;

        const willOpen = children.hasAttribute('hidden');
        children.toggleAttribute('hidden', !willOpen);
        toggle.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
        const caret = toggle.querySelector('.tree-caret');
        if (caret) caret.textContent = willOpen ? '▾' : '▸';
    });

    // 1. Manejo del árbol de selección jerárquica
    document.addEventListener('change', (event) => {
        // Selector de Asignatura (marca todos sus temas y recursos)
        if (event.target.classList.contains('subject-selector')) {
            const subjectNode = event.target.closest('.subject-node');
            if (subjectNode) {
                const checked = event.target.checked;
                // Marcar todos los temas
                subjectNode.querySelectorAll('.topic-selector').forEach(cb => cb.checked = checked);
                // Marcar todos los recursos
                subjectNode.querySelectorAll('.resource-selector').forEach(cb => cb.checked = checked);
            }
        }

        // Selector de Tema (marca todos sus recursos)
        if (event.target.classList.contains('topic-selector')) {
            const topicNode = event.target.closest('.topic-node');
            if (topicNode) {
                const checked = event.target.checked;
                // Marcar todos los recursos
                topicNode.querySelectorAll('.resource-selector').forEach(cb => cb.checked = checked);

                // Actualizar asignatura padre
                updateSubjectParent(topicNode);
            }
        }

        // Selector de Recurso Individual
        if (event.target.classList.contains('resource-selector')) {
            const topicNode = event.target.closest('.topic-node');
            if (topicNode) {
                updateTopicParent(topicNode);
                updateSubjectParent(topicNode);
            }
        }
    });

    const updateTopicParent = (topicNode) => {
        const topicSelector = topicNode.querySelector('.topic-selector');
        const resources = topicNode.querySelectorAll('.resource-selector');
        const checkedResources = topicNode.querySelectorAll('.resource-selector:checked');

        if (topicSelector) {
            if (checkedResources.length === 0) {
                topicSelector.checked = false;
                topicSelector.indeterminate = false;
            } else if (checkedResources.length === resources.length) {
                topicSelector.checked = true;
                topicSelector.indeterminate = false;
            } else {
                topicSelector.checked = false;
                topicSelector.indeterminate = true;
            }
        }
    };

    const updateSubjectParent = (topicNode) => {
        const subjectNode = topicNode.closest('.subject-node');
        if (subjectNode) {
            const subjectSelector = subjectNode.querySelector('.subject-selector');
            const topics = subjectNode.querySelectorAll('.topic-selector');
            const checkedTopics = subjectNode.querySelectorAll('.topic-selector:checked');
            const indetTopics = Array.from(topics).some(t => t.indeterminate);

            if (subjectSelector) {
                if (checkedTopics.length === 0 && !indetTopics) {
                    subjectSelector.checked = false;
                    subjectSelector.indeterminate = false;
                } else if (checkedTopics.length === topics.length && !indetTopics) {
                    subjectSelector.checked = true;
                    subjectSelector.indeterminate = false;
                } else {
                    subjectSelector.checked = false;
                    subjectSelector.indeterminate = true;
                }
            }
        }
    };

    // 2. Inyectar los recursos seleccionados en la PETICIÓN de HTMX.
    //    Importante: se modifica event.detail.parameters (no el DOM), porque en
    //    htmx:configRequest htmx ya serializó el formulario; agregar inputs al DOM
    //    en este punto llega tarde y se ignoran.
    document.addEventListener('htmx:configRequest', (event) => {
        const elt = event.detail.elt;
        // Solo el formulario de generación en lote (no las tandas encadenadas).
        if (!elt || !elt.classList || !elt.classList.contains('studio-generation-form')) {
            return;
        }

        const selected = Array.from(document.querySelectorAll('.resource-selector:checked'));
        if (selected.length === 0) {
            event.preventDefault();
            alert('Por favor, selecciona al menos un recurso para generar.');
            return;
        }

        // Django lo leerá con request.POST.getlist('resources').
        event.detail.parameters['resources'] = selected.map((cb) => cb.value);

        // Confirmación para lotes grandes (cada recurso = 6 tandas de IA).
        if (selected.length > 5) {
            const ok = confirm(`Has seleccionado ${selected.length} recursos. Esto ejecutará ${selected.length * 6} tandas consecutivas de IA. ¿Deseas continuar?`);
            if (!ok) {
                event.preventDefault();
            }
        }
    });

    // 3. Scroll automático de los logs a medida que se inyectan
    document.addEventListener('htmx:afterSwap', (event) => {
        const logsContainer = document.getElementById('studio-logs-container');
        if (logsContainer) {
            logsContainer.scrollTop = logsContainer.scrollHeight;
        }
    });
});
