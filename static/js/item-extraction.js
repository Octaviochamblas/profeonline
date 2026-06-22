// Panel de extracción de ítems de aprendizaje (Fase 1).
// Lógica de selección/fusión sin handlers inline (CSP con nonce, sin onclick).
(function () {
    "use strict";

    function visibleMergeButton() {
        var btn = document.getElementById("btn-merge-selected");
        if (!btn) return;
        var checked = document.querySelectorAll(".item-select-checkbox:checked");
        btn.style.display = checked.length >= 2 ? "inline-block" : "none";
    }

    function submitMergeForm() {
        var checkboxes = document.querySelectorAll(".item-select-checkbox:checked");
        if (checkboxes.length < 2) return;

        if (!window.confirm(
            "¿Estás seguro de fusionar los ítems seleccionados? " +
            "Se creará uno nuevo y los actuales se archivarán."
        )) {
            return;
        }

        var topicSelect = document.querySelector("[name=topic_id]");
        var mergeBtn = document.getElementById("btn-merge-selected");
        var url = mergeBtn ? mergeBtn.getAttribute("data-merge-url") : "";
        if (!url || typeof window.htmx === "undefined") return;

        window.htmx.ajax("POST", url, {
            target: "#items-list-container",
            values: {
                item_ids: Array.prototype.map.call(checkboxes, function (cb) { return cb.value; }),
                topic_id: topicSelect ? topicSelect.value : ""
            }
        });
    }

    // Habilitar/deshabilitar el botón de fusión al marcar checkboxes (delegación).
    document.addEventListener("change", function (e) {
        if (e.target && e.target.classList && e.target.classList.contains("item-select-checkbox")) {
            visibleMergeButton();
        }
    });

    // Click del botón de fusión (el botón vive en la página, no en el parcial swappeado).
    document.addEventListener("click", function (e) {
        var btn = e.target.closest ? e.target.closest("#btn-merge-selected") : null;
        if (btn) {
            e.preventDefault();
            submitMergeForm();
        }
    });

    // Resetear visibilidad al recargar el listado vía HTMX.
    document.addEventListener("htmx:afterSwap", function (e) {
        if (e.detail && e.detail.target && e.detail.target.id === "items-list-container") {
            var mergeBtn = document.getElementById("btn-merge-selected");
            if (mergeBtn) mergeBtn.style.display = "none";
        }
    });
})();
