(function() {
    // 1. Obtener el token CSRF desde la meta etiqueta
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';

    // 2. Función genérica para enviar eventos
    function sendEvent(name, metadata = {}) {
        const path = window.location.pathname;

        // No registrar visitas a los recursos si el usuario está autenticado,
        // ya que el ledger del backend (ResourceView) se encarga de esto.
        // Pero para el resto de eventos de cliente, se registran normalmente.

        if (navigator.sendBeacon) {
            const formData = new FormData();
            formData.append('csrfmiddlewaretoken', csrfToken);
            formData.append('name', name);
            formData.append('path', path);
            formData.append('metadata', JSON.stringify(metadata));

            navigator.sendBeacon('/eventos/', formData);
        } else {
            fetch('/eventos/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    name: name,
                    path: path,
                    metadata: metadata
                })
            }).catch(err => {
                console.error('Error al reportar analíticas:', err);
            });
        }
    }

    // Exportar al ámbito global por si se necesita disparar manualmente
    window.ProfeOnlineAnalytics = { sendEvent: sendEvent };

    // 3. Captura global de clics (delegación de eventos)
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a');
        if (!link) return;

        const href = link.getAttribute('href') || '';

        // Clics a WhatsApp
        if (href.includes('wa.me') || href.includes('api.whatsapp.com')) {
            sendEvent('whatsapp_click');
        }
        // Clics a Teléfono
        else if (href.startsWith('tel:')) {
            sendEvent('phone_click');
        }
        // Clics a Descargas de Recursos
        else if (link.hasAttribute('download') || href.includes('/media/')) {
            sendEvent('attachment_download');
        }
    });

    // 4. Integración con reproductor de YouTube
    window.addEventListener('message', function(event) {
        // Validación de origen estricta para evitar falsificaciones (S1)
        if (event.origin !== "https://www.youtube-nocookie.com") {
            return;
        }

        try {
            const data = JSON.parse(event.data);
            // YouTube Player API envía eventos onStateChange con info = 1 para PLAYING
            if (data.event === 'onStateChange' && data.info === 1) {
                const iframe = Array.from(document.querySelectorAll('iframe[src*="youtube-nocookie.com/embed/"]'))
                    .find(frame => frame.contentWindow === event.source);
                const videoId = iframe?.src?.split('/embed/')[1]?.split('?')[0] || '';
                sendEvent('video_play', videoId ? { video_id: videoId } : {});
            }
        } catch (e) {
            // Ignorar mensajes que no sean JSON
        }
    });
})();
