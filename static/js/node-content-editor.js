(function () {
    "use strict";

    const dialog = document.querySelector("[data-content-editor-dialog]");
    if (!dialog) return;

    const form = dialog.querySelector("[data-content-editor-form]");
    const errors = dialog.querySelector("[data-content-editor-errors]");
    const status = dialog.querySelector("[data-content-editor-status]");
    const saveButton = dialog.querySelector("[data-content-editor-save]");
    const openButton = document.querySelector("[data-content-editor-open]");
    const itemTemplate = document.querySelector('[data-template="list-item"]');
    const exampleTemplate = document.querySelector('[data-template="example"]');

    function setErrors(messages) {
        const values = (Array.isArray(messages) ? messages : [messages]).filter(Boolean);
        errors.replaceChildren();
        if (values.length) {
            const list = document.createElement("ul");
            values.forEach(message => {
                const item = document.createElement("li");
                item.textContent = message;
                list.appendChild(item);
            });
            errors.appendChild(list);
        }
        errors.hidden = values.length === 0;
    }

    function flattenErrors(payload) {
        if (payload.error) return [payload.error];
        const messages = [];
        Object.values(payload.errors || {}).forEach(items => {
            items.forEach(item => messages.push(item.message || String(item)));
        });
        return messages.length ? messages : ["No fue posible guardar el contenido."];
    }

    function cloneListItem(label) {
        const fragment = itemTemplate.content.cloneNode(true);
        fragment.querySelector("label").firstChild.textContent = label;
        const accessibleLabel = label.toLowerCase();
        fragment.querySelector('[data-move="up"]').setAttribute("aria-label", `Subir ${accessibleLabel}`);
        fragment.querySelector('[data-move="down"]').setAttribute("aria-label", `Bajar ${accessibleLabel}`);
        fragment.querySelector("[data-remove]").setAttribute("aria-label", `Eliminar ${accessibleLabel}`);
        return fragment;
    }

    function addListItem(listName) {
        const list = dialog.querySelector(`[data-list="${listName}"]`);
        const fragment = cloneListItem(listName === "procedimiento" ? "Paso" : "Error");
        list.appendChild(fragment);
        list.lastElementChild.querySelector("textarea").focus();
    }

    function addSolution(button) {
        const list = button.closest("[data-item]").querySelector("[data-solution-list]");
        const fragment = cloneListItem("Solución");
        fragment.querySelector("[data-item]").classList.add("content-editor__solution");
        list.appendChild(fragment);
        list.lastElementChild.querySelector("textarea").focus();
    }

    function moveItem(button, direction) {
        const item = button.closest("[data-item]");
        const sibling = direction === "up" ? item.previousElementSibling : item.nextElementSibling;
        if (!sibling) return;
        if (direction === "up") item.parentElement.insertBefore(item, sibling);
        else item.parentElement.insertBefore(sibling, item);
        button.focus();
    }

    function collectStringList(selector) {
        return Array.from(dialog.querySelector(selector).children)
            .map(item => item.querySelector("[data-value]").value.trim())
            .filter(Boolean);
    }

    function collectExamples() {
        return Array.from(dialog.querySelector('[data-list="ejemplos"]').children).map(item => ({
            titulo: item.querySelector('[data-example-field="titulo"]').value.trim(),
            enunciado: item.querySelector('[data-example-field="enunciado"]').value.trim(),
            respuesta: item.querySelector('[data-example-field="respuesta"]').value,
            solucion_pasos: Array.from(item.querySelector("[data-solution-list]").children)
                .map(step => step.querySelector("[data-value]").value.trim())
                .filter(Boolean),
        }));
    }

    function buildPayload() {
        return {
            objetivo: form.elements.objetivo.value,
            introduccion: form.elements.introduccion.value,
            resumen: form.elements.resumen.value,
            explicacion: form.elements.explicacion.value,
            procedimiento: collectStringList('[data-list="procedimiento"]'),
            ejemplos: collectExamples(),
            errores_frecuentes: collectStringList('[data-list="errores_frecuentes"]'),
            fuente: form.elements.fuente.value,
            estado: form.elements.estado.value,
            updated_at: form.elements.updated_at.value,
        };
    }

    openButton.addEventListener("click", () => {
        setErrors([]);
        status.textContent = "";
        dialog.showModal();
        const firstField = dialog.querySelector("textarea, input:not([type=hidden]), select");
        if (firstField) firstField.focus();
    });

    dialog.querySelectorAll("[data-content-editor-close]").forEach(button => {
        button.addEventListener("click", () => dialog.close());
    });

    dialog.addEventListener("keydown", event => {
        if (event.key === "Escape") {
            event.preventDefault();
            dialog.close();
        }
    });

    dialog.addEventListener("click", event => {
        const addItem = event.target.closest("[data-add-item]");
        if (addItem) {
            const listName = addItem.dataset.addItem;
            if (listName === "ejemplos") {
                const list = dialog.querySelector('[data-list="ejemplos"]');
                list.appendChild(exampleTemplate.content.cloneNode(true));
                list.lastElementChild.querySelector("input").focus();
            } else {
                addListItem(listName);
            }
            return;
        }
        const addSolutionButton = event.target.closest("[data-add-solution]");
        if (addSolutionButton) {
            addSolution(addSolutionButton);
            return;
        }
        const removeButton = event.target.closest("[data-remove]");
        if (removeButton) {
            removeButton.closest("[data-item]").remove();
            return;
        }
        const moveButton = event.target.closest("[data-move]");
        if (moveButton) moveItem(moveButton, moveButton.dataset.move);
    });

    form.addEventListener("submit", async event => {
        event.preventDefault();
        setErrors([]);
        status.textContent = "Guardando…";
        saveButton.disabled = true;
        dialog.setAttribute("aria-busy", "true");
        try {
            const response = await fetch(form.dataset.endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": form.elements.csrfmiddlewaretoken.value,
                },
                body: JSON.stringify(buildPayload()),
            });
            const payload = await response.json();
            if (!response.ok) {
                setErrors(flattenErrors(payload));
                status.textContent = "Revisa los errores antes de guardar.";
                return;
            }
            status.textContent = "Guardado. Actualizando la ficha…";
            window.location.reload();
        } catch (error) {
            setErrors(["No se pudo conectar con el servidor. Intenta nuevamente."]);
            status.textContent = "Error de conexión.";
        } finally {
            saveButton.disabled = false;
            dialog.removeAttribute("aria-busy");
        }
    });
}());
