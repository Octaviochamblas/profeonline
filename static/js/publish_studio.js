document.addEventListener("DOMContentLoaded", function () {
    const areaSelect = document.getElementById("area_id");
    const subjectSelect = document.getElementById("subject_id");
    const topicSelect = document.getElementById("topic_id");
    const moduleSelect = document.getElementById("module_id");
    const titleInput = document.getElementById("title");
    const generateCopyBtn = document.getElementById("btn-generate-copy");
    const descriptionTextarea = document.getElementById("description");
    const contentTextarea = document.getElementById("content_md");
    const playlistInput = document.getElementById("playlist_id");
    const skipPlaylistCheckbox = document.getElementById("skip_playlist");
    const downloadForm = document.getElementById("publish-studio-form");
    const downloadBtn = document.getElementById("btn-download-job");
    const duplicatesBox = document.getElementById("duplicates-box");
    const warningsBox = document.getElementById("warnings-box");

    // CSRF Token helper
    function getCsrfToken() {
        const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfInput ? csrfInput.value : "";
    }

    // Extraction of playlist_id from URL
    if (playlistInput) {
        playlistInput.addEventListener("blur", function () {
            let value = playlistInput.value.trim();
            if (value) {
                // If it looks like a URL (contains slashes or protocol)
                if (value.includes("://") || value.startsWith("www.") || value.includes("/")) {
                    try {
                        let urlString = value;
                        if (!value.includes("://")) {
                            urlString = "https://" + value;
                        }
                        const url = new URL(urlString);
                        const listId = url.searchParams.get("list");
                        if (listId) {
                            playlistInput.value = listId;
                        } else {
                            playlistInput.value = "";
                        }
                    } catch (e) {
                        playlistInput.value = "";
                        console.error("URL de playlist invalida:", e);
                    }
                }
            }
            validateForm();
        });
    }

    if (skipPlaylistCheckbox && playlistInput) {
        skipPlaylistCheckbox.addEventListener("change", function () {
            playlistInput.disabled = skipPlaylistCheckbox.checked;
            if (skipPlaylistCheckbox.checked) {
                playlistInput.value = "";
            }
            validateForm();
        });
    }

    // Dependent Selects: Area -> Subject
    if (areaSelect) {
        areaSelect.addEventListener("change", function () {
            const areaId = areaSelect.value;
            subjectSelect.innerHTML = '<option value="">-- Selecciona Asignatura --</option>';
            topicSelect.innerHTML = '<option value="">-- Selecciona Tema --</option>';
            moduleSelect.innerHTML = '<option value="">-- Selecciona Modulo (Opcional) --</option>';

            if (!areaId) {
                validateForm();
                return;
            }

            fetch(`/publicar/opciones/asignaturas/?area_id=${areaId}`)
                .then(res => res.json())
                .then(data => {
                    data.subjects.forEach(sub => {
                        const opt = document.createElement("option");
                        opt.value = sub.id;
                        opt.textContent = sub.name;
                        subjectSelect.appendChild(opt);
                    });
                    validateForm();
                })
                .catch(err => console.error("Error cargando asignaturas:", err));
        });
    }

    // Dependent Selects: Subject -> Topic & Module
    if (subjectSelect) {
        subjectSelect.addEventListener("change", function () {
            const subjectId = subjectSelect.value;
            topicSelect.innerHTML = '<option value="">-- Selecciona Tema --</option>';
            moduleSelect.innerHTML = '<option value="">-- Selecciona Modulo (Opcional) --</option>';

            if (!subjectId) {
                validateForm();
                return;
            }

            // Load topics
            fetch(`/temas/opciones/?subject_id=${subjectId}`)
                .then(res => res.json())
                .then(data => {
                    data.topics.forEach(top => {
                        const opt = document.createElement("option");
                        opt.value = top.id;
                        opt.textContent = top.name;
                        topicSelect.appendChild(opt);
                    });
                    validateForm();
                })
                .catch(err => console.error("Error cargando temas:", err));

            // Load modules
            fetch(`/publicar/opciones/modulos/?subject_id=${subjectId}`)
                .then(res => res.json())
                .then(data => {
                    data.modules.forEach(mod => {
                        const opt = document.createElement("option");
                        opt.value = mod.id;
                        opt.textContent = mod.title;
                        moduleSelect.appendChild(opt);
                    });
                    validateForm();
                })
                .catch(err => console.error("Error cargando modulos:", err));
        });
    }

    if (topicSelect) {
        topicSelect.addEventListener("change", function () {
            validateForm();
            checkDuplicates();
        });
    }

    if (titleInput) {
        titleInput.addEventListener("input", function () {
            validateForm();
            checkDuplicates();
        });
    }

    // Generate Copy
    if (generateCopyBtn) {
        generateCopyBtn.addEventListener("click", function () {
            const title = titleInput.value.trim();
            const subjectId = subjectSelect.value;
            const topicId = topicSelect.value;

            if (!title || !subjectId || !topicId) {
                alert("Debes completar el Titulo, Asignatura y Tema para generar la copia.");
                return;
            }

            generateCopyBtn.disabled = true;
            generateCopyBtn.textContent = "Generando...";

            fetch(`/publicar/copy/preview/?title=${encodeURIComponent(title)}&subject_id=${subjectId}&topic_id=${topicId}`)
                .then(res => {
                    if (!res.ok) throw new Error("Error en la peticion de copia");
                    return res.json();
                })
                .then(data => {
                    if (descriptionTextarea) descriptionTextarea.value = data.description;
                    if (contentTextarea) contentTextarea.value = data.content_md;
                    validateForm();
                })
                .catch(err => {
                    console.error(err);
                    alert("Ocurrio un error al generar la copia.");
                })
                .finally(() => {
                    generateCopyBtn.disabled = false;
                    generateCopyBtn.textContent = "Generar Copia y Apuntes";
                });
        });
    }

    // Check duplicates
    function checkDuplicates() {
        const title = titleInput ? titleInput.value.trim() : "";
        const topicId = topicSelect ? topicSelect.value : "";

        if (!title || !topicId) {
            if (duplicatesBox) duplicatesBox.innerHTML = "";
            return;
        }

        fetch(`/publicar/duplicados/?title=${encodeURIComponent(title)}&topic_id=${topicId}`)
            .then(res => res.json())
            .then(data => {
                if (duplicatesBox) {
                    duplicatesBox.innerHTML = "";
                    if (data.length > 0) {
                        const alertDiv = document.createElement("div");
                        alertDiv.className = "alert alert--warning";

                        const p = document.createElement("p");
                        const strong = document.createElement("strong");
                        strong.textContent = "¡Posibles Duplicados Detectados!";
                        p.appendChild(strong);
                        alertDiv.appendChild(p);

                        const ul = document.createElement("ul");
                        data.forEach(item => {
                            const li = document.createElement("li");
                            const a = document.createElement("a");
                            a.href = item.url;
                            a.target = "_blank";
                            a.textContent = `${item.title} (ver recurso)`;
                            li.appendChild(a);
                            ul.appendChild(li);
                        });
                        alertDiv.appendChild(ul);
                        duplicatesBox.appendChild(alertDiv);
                    }
                }
            })
            .catch(err => console.error("Error buscando duplicados:", err));
    }

    // Dynamic Form Validation
    function validateForm() {
        const warnings = [];

        const fileName = document.getElementById("file_name").value.trim();
        if (!fileName) warnings.push("Falta especificar el nombre del archivo de video.");

        const areaId = areaSelect ? areaSelect.value : "";
        if (!areaId) warnings.push("Falta seleccionar el Area.");

        const subjectId = subjectSelect ? subjectSelect.value : "";
        if (!subjectId) warnings.push("Falta seleccionar la Asignatura.");

        const topicId = topicSelect ? topicSelect.value : "";
        if (!topicId) warnings.push("Falta seleccionar el Tema.");

        const levelChecked = Array.from(document.querySelectorAll('input[name="level_ids"]:checked, input[name="level_ids[]"]:checked')).length > 0;
        if (!levelChecked) warnings.push("Debes seleccionar al menos un Nivel.");

        const privacy = document.getElementById("privacy").value;
        if (!privacy) warnings.push("Falta seleccionar la Privacidad.");

        const skipPlaylist = skipPlaylistCheckbox ? skipPlaylistCheckbox.checked : false;
        const playlistId = playlistInput ? playlistInput.value.trim() : "";
        if (!skipPlaylist && !playlistId) {
            warnings.push("Debes especificar una Playlist o marcar la opcion de omitirla.");
        }

        const title = titleInput ? titleInput.value.trim() : "";
        if (!title) warnings.push("Falta el Titulo del recurso.");

        const mainText = document.getElementById("main_text").value.trim();
        if (!mainText) warnings.push("Falta el Texto principal para la miniatura.");

        const description = descriptionTextarea ? descriptionTextarea.value.trim() : "";
        const content = contentTextarea ? contentTextarea.value.trim() : "";
        if (!description || !content) {
            warnings.push("La descripcion y los apuntes de copia deben ser generados.");
        }

        if (warningsBox) {
            if (warnings.length > 0) {
                let html = '<div class="alert alert--info"><p><strong>Orden de Trabajo Incompleta:</strong></p><ul>';
                warnings.forEach(w => {
                    html += `<li>${w}</li>`;
                });
                html += '</ul></div>';
                warningsBox.innerHTML = html;
                if (downloadBtn) downloadBtn.disabled = true;
            } else {
                warningsBox.innerHTML = '<div class="alert alert--success"><p><strong>✓ ¡Orden de trabajo lista para descargar!</strong></p></div>';
                if (downloadBtn) downloadBtn.disabled = false;
            }
        }
    }

    // Modal Handling for inline creations
    const modalToggles = document.querySelectorAll("[data-open-modal]");
    modalToggles.forEach(btn => {
        btn.addEventListener("click", function () {
            const targetId = btn.getAttribute("data-open-modal");
            const modal = document.getElementById(targetId);
            if (modal) {
                // Set context IDs in modal forms dynamically
                if (targetId === "modal-subject") {
                    const modalAreaInput = modal.querySelector('[name="area_id"]');
                    if (modalAreaInput && areaSelect) modalAreaInput.value = areaSelect.value;
                } else if (targetId === "modal-topic") {
                    const modalSubjectSelect = modal.querySelector('[name="subject"]');
                    if (modalSubjectSelect && subjectSelect) modalSubjectSelect.value = subjectSelect.value;
                } else if (targetId === "modal-module") {
                    const modalSubjectInput = modal.querySelector('[name="subject_id"]');
                    if (modalSubjectInput && subjectSelect) modalSubjectInput.value = subjectSelect.value;
                    const modalTopicInput = modal.querySelector('[name="topic_id"]');
                    if (modalTopicInput && topicSelect) modalTopicInput.value = topicSelect.value;

                    // Set levels selected in main form in module creation
                    const selectedLevels = Array.from(document.querySelectorAll('input[name="level_ids"]:checked, input[name="level_ids[]"]:checked')).map(cb => cb.value);
                    const levelsContainer = modal.querySelector(".modal-levels-container");
                    if (levelsContainer) {
                        levelsContainer.innerHTML = "";
                        selectedLevels.forEach(lid => {
                            const hidden = document.createElement("input");
                            hidden.type = "hidden";
                            hidden.name = "level_ids";
                            hidden.value = lid;
                            levelsContainer.appendChild(hidden);
                        });
                    }
                }

                modal.removeAttribute("hidden");
                modal.classList.add("modal-open");
                const firstInput = modal.querySelector("input:not([type=hidden]), textarea, select");
                if (firstInput) firstInput.focus();
            }
        });
    });

    const modalCloses = document.querySelectorAll("[data-close-modal]");
    modalCloses.forEach(btn => {
        btn.addEventListener("click", function () {
            const modal = btn.closest(".modal-overlay");
            if (modal) {
                modal.setAttribute("hidden", "");
                modal.classList.remove("modal-open");
            }
        });
    });

    // Handle AJAX form submission inside modals
    const modalForms = document.querySelectorAll(".modal-form");
    modalForms.forEach(form => {
        form.addEventListener("submit", function (e) {
            e.preventDefault();
            const actionUrl = form.getAttribute("action");
            const entityType = form.getAttribute("data-entity-type");
            const formData = new FormData(form);

            // Add contextual fields if not present
            if (entityType === "subject" && !formData.has("area_id") && areaSelect) {
                formData.append("area_id", areaSelect.value);
            }
            if (entityType === "module") {
                if (!formData.has("subject_id") && subjectSelect) formData.append("subject_id", subjectSelect.value);
                if (!formData.has("topic_id") && topicSelect) formData.append("topic_id", topicSelect.value);

                // Append selected levels from context
                const selectedLevels = Array.from(document.querySelectorAll('input[name="level_ids"]:checked, input[name="level_ids[]"]:checked')).map(cb => cb.value);
                selectedLevels.forEach(lid => {
                    formData.append("level_ids", lid);
                });
            }

            const errorContainer = form.querySelector(".modal-errors");
            if (errorContainer) errorContainer.innerHTML = "";

            const submitBtn = form.querySelector('[type="submit"]');
            const originalBtnText = submitBtn ? submitBtn.textContent : "Guardar";
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = "Guardando...";
            }

            fetch(actionUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCsrfToken()
                },
                body: formData
            })
            .then(res => {
                return res.json().then(data => {
                    if (!res.ok) {
                        return Promise.reject(data);
                    }
                    return data;
                });
            })
            .then(data => {
                // Success: Add created element to the select and select it
                let selectElement;
                if (entityType === "area") selectElement = areaSelect;
                else if (entityType === "subject") selectElement = subjectSelect;
                else if (entityType === "topic") selectElement = topicSelect;
                else if (entityType === "module") selectElement = moduleSelect;
                else if (entityType === "level") {
                    // Level is checkboxes. Let's dynamically add checkbox
                    const container = document.getElementById("levels-checkboxes-container");
                    if (container) {
                        const wrapper = document.createElement("label");
                        wrapper.className = "checkbox-label";

                        const checkbox = document.createElement("input");
                        checkbox.type = "checkbox";
                        checkbox.name = "level_ids";
                        checkbox.value = data.id;
                        checkbox.checked = true;

                        wrapper.appendChild(checkbox);
                        wrapper.appendChild(document.createTextNode(" " + data.name));
                        container.appendChild(wrapper);

                        // wire up event listener for the new checkbox
                        checkbox.addEventListener("change", validateForm);
                    }
                }

                if (selectElement) {
                    const opt = document.createElement("option");
                    opt.value = data.id;
                    opt.textContent = data.name;
                    opt.selected = true;
                    selectElement.appendChild(opt);

                    // Trigger change listeners to reload dependent inputs
                    selectElement.dispatchEvent(new Event("change"));
                }

                // Clean form and close modal
                form.reset();
                const modal = form.closest(".modal-overlay");
                if (modal) {
                    modal.setAttribute("hidden", "");
                    modal.classList.remove("modal-open");
                }
                validateForm();
            })
            .catch(err => {
                console.error("Error en creacion inline:", err);
                if (errorContainer && err.errors) {
                    let errHtml = '<div class="alert alert--danger"><ul>';
                    for (const field in err.errors) {
                        err.errors[field].forEach(msg => {
                            errHtml += `<li><strong>${field}:</strong> ${msg}</li>`;
                        });
                    }
                    errHtml += '</ul></div>';
                    errorContainer.innerHTML = errHtml;
                } else {
                    if (errorContainer) {
                        errorContainer.innerHTML = '<div class="alert alert--danger"><p>Ocurrio un error inesperado al guardar.</p></div>';
                    }
                }
            })
            .finally(() => {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalBtnText;
                }
            });
        });
    });

    // Connect inputs for real-time validation
    const inputsToValidate = [
        "file_name", "privacy", "main_text"
    ];
    inputsToValidate.forEach(id => {
        const input = document.getElementById(id);
        if (input) {
            input.addEventListener("input", validateForm);
            input.addEventListener("change", validateForm);
        }
    });

    // Level checkboxes events
    const levelCheckboxes = document.querySelectorAll('input[name="level_ids"], input[name="level_ids[]"]');
    levelCheckboxes.forEach(cb => {
        cb.addEventListener("change", validateForm);
    });

    // Run initial validation
    validateForm();
});
