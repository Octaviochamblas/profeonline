// JS seguro para la gestión de guías ProfeOnline (Fase 2)
(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        initGuideEvents();
    });

    function initGuideEvents() {
        // Escucha eventos HTMX para reaccionar al swap de los contenedores
        document.body.addEventListener('htmx:afterSwap', function(event) {
            if (event.detail.target.id === 'originality-report-container' ||
                event.detail.target.id === 'guide-details-container') {
                updatePublishButtonState();
            }
        });
    }

    function updatePublishButtonState() {
        const originalityPassedElem = document.getElementById('originality-passed-flag');
        const publishBtn = document.getElementById('btn-publish-guide');

        if (publishBtn) {
            if (originalityPassedElem && originalityPassedElem.value === 'true') {
                publishBtn.removeAttribute('disabled');
                publishBtn.style.opacity = '1';
                publishBtn.style.cursor = 'pointer';
            } else {
                publishBtn.setAttribute('disabled', 'true');
                publishBtn.style.opacity = '0.5';
                publishBtn.style.cursor = 'not-allowed';
            }
        }
    }
})();
