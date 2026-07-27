document.body.addEventListener('htmx:afterRequest', function (evt) {
    if (!evt.detail.pathInfo || !evt.detail.pathInfo.requestPath.includes('/opciones/nodos/')) return;
    var target = evt.detail.target;
    try {
        var data = JSON.parse(evt.detail.xhr.responseText);
        target.innerHTML = '';
        data.nodes.forEach(function (node) {
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn btn-sm';
            btn.textContent = node.label;
            btn.style.marginRight = '6px';
            btn.style.marginBottom = '6px';
            btn.addEventListener('click', function () {
                var form = target.closest('form');
                var hidden = form.querySelector('input[name="node_id"]');
                if (!hidden) {
                    hidden = document.createElement('input');
                    hidden.type = 'hidden';
                    hidden.name = 'node_id';
                    form.appendChild(hidden);
                }
                hidden.value = node.id;
                var submitBtn = form.querySelector('button[type="submit"]');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Vincular: ' + node.label;
            });
            target.appendChild(btn);
        });
    } catch (e) { /* respuesta no-JSON, ignorar */ }
});
