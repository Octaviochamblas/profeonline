document.addEventListener("DOMContentLoaded", function () {
    const areaSelect = document.getElementById("area_id");
    const subjectSelect = document.getElementById("subject_id");
    const topicSelect = document.getElementById("topic_id");
    const moduleSelect = document.getElementById("module_id");
    const fileInput = document.getElementById("file_input");
    const fileNamesInput = document.getElementById("file_names");
    const fileListPreview = document.getElementById("file-list-preview");
    const playlistInput = document.getElementById("playlist_id");
    const playlistTitleInput = document.getElementById("playlist_title");
    const createPlaylistCheckbox = document.getElementById("create_playlist");
    const newPlaylistFields = document.getElementById("new-playlist-fields");
    const newPlaylistTitleInput = document.getElementById("new_playlist_title");
    const downloadBtn = document.getElementById("btn-download-job");
    const warningsBox = document.getElementById("warnings-box");

    // CSRF Token helper
    function getCsrfToken() {
        const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfInput ? csrfInput.value : "";
    }

    // Render files list safely using DOM API
    function renderFileList(names) {
        fileListPreview.innerHTML = "";
        if (names.length === 0) {
            const span = document.createElement("span");
            span.className = "text-muted";
            span.textContent = "Ningun archivo seleccionado.";
            fileListPreview.appendChild(span);
            return;
        }

        const ul = document.createElement("ul");
        ul.className = "file-preview-list";
        names.forEach(name => {
            const li = document.createElement("li");
            li.textContent = name;
            ul.appendChild(li);
        });
        fileListPreview.appendChild(ul);
    }

    // Parse initial files from hidden input
    let selectedFiles = [];
    try {
        if (fileNamesInput && fileNamesInput.value) {
            selectedFiles = JSON.parse(fileNamesInput.value);
            if (!Array.isArray(selectedFiles)) {
                selectedFiles = [];
            }
        }
    } catch (e) {
        selectedFiles = [];
    }
    renderFileList(selectedFiles);

    // File input change listener
    if (fileInput) {
        fileInput.addEventListener("change", function () {
            selectedFiles = [];
            for (let i = 0; i < fileInput.files.length; i++) {
                selectedFiles.push(fileInput.files[i].name);
            }
            if (fileNamesInput) {
                fileNamesInput.value = JSON.stringify(selectedFiles);
            }
            renderFileList(selectedFiles);
            validateForm();
        });
    }

    // Extraction of playlist_id from URL
    if (playlistInput) {
        playlistInput.addEventListener("blur", function () {
            let value = playlistInput.value.trim();
            if (value) {
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

    function syncPlaylistMode() {
        const shouldCreatePlaylist = createPlaylistCheckbox ? createPlaylistCheckbox.checked : false;

        if (newPlaylistFields) {
            newPlaylistFields.hidden = !shouldCreatePlaylist;
        }

        if (playlistInput) {
            playlistInput.disabled = shouldCreatePlaylist;
        }

        if (playlistTitleInput) {
            playlistTitleInput.disabled = shouldCreatePlaylist;
        }
    }

    // Cascade dropdowns
    if (areaSelect) {
        areaSelect.addEventListener("change", function () {
            const areaId = areaSelect.value;
            // Clear dependents
            subjectSelect.innerHTML = '<option value="">-- Selecciona Asignatura --</option>';
            topicSelect.innerHTML = '<option value="">-- Selecciona Tema --</option>';
            moduleSelect.innerHTML = '<option value="">-- Selecciona Modulo (Opcional) --</option>';

            if (areaId) {
                fetch(`/publicar/opciones/asignaturas/?area_id=${areaId}`)
                    .then(res => res.json())
                    .then(data => {
                        data.subjects.forEach(sub => {
                            const opt = document.createElement("option");
                            opt.value = sub.id;
                            opt.textContent = sub.name;
                            subjectSelect.appendChild(opt);
                        });
                    })
                    .catch(err => console.error("Error cargando asignaturas:", err));
            }
            validateForm();
        });
    }

    if (subjectSelect) {
        subjectSelect.addEventListener("change", function () {
            const subjectId = subjectSelect.value;
            topicSelect.innerHTML = '<option value="">-- Selecciona Tema --</option>';
            moduleSelect.innerHTML = '<option value="">-- Selecciona Modulo (Opcional) --</option>';

            if (subjectId) {
                // Fetch topics
                fetch(`/temas/opciones/?subject_id=${subjectId}`)
                    .then(res => res.json())
                    .then(data => {
                        data.topics.forEach(top => {
                            const opt = document.createElement("option");
                            opt.value = top.id;
                            opt.textContent = top.name;
                            topicSelect.appendChild(opt);
                        });
                    })
                    .catch(err => console.error("Error cargando temas:", err));

                // Fetch modules
                fetch(`/publicar/opciones/modulos/?subject_id=${subjectId}`)
                    .then(res => res.json())
                    .then(data => {
                        data.modules.forEach(mod => {
                            const opt = document.createElement("option");
                            opt.value = mod.id;
                            opt.textContent = mod.title;
                            moduleSelect.appendChild(opt);
                        });
                    })
                    .catch(err => console.error("Error cargando modulos:", err));
            }
            validateForm();
        });
    }

    if (topicSelect) {
        topicSelect.addEventListener("change", validateForm);
    }
    if (moduleSelect) {
        moduleSelect.addEventListener("change", validateForm);
    }
    if (playlistInput) {
        playlistInput.addEventListener("input", validateForm);
    }
    if (createPlaylistCheckbox) {
        createPlaylistCheckbox.addEventListener("change", function () {
            syncPlaylistMode();
            validateForm();
        });
    }
    if (newPlaylistTitleInput) {
        newPlaylistTitleInput.addEventListener("input", validateForm);
    }

    // Form Validation (visual warnings + download block)
    function validateForm() {
        const warnings = [];

        if (selectedFiles.length === 0) {
            warnings.push("Debes seleccionar al menos un archivo de video.");
        }

        const areaId = areaSelect ? areaSelect.value : "";
        if (!areaId) warnings.push("Falta seleccionar el Area.");

        const subjectId = subjectSelect ? subjectSelect.value : "";
        if (!subjectId) warnings.push("Falta seleccionar la Asignatura.");

        const topicId = topicSelect ? topicSelect.value : "";
        if (!topicId) warnings.push("Falta seleccionar el Tema.");

        if (createPlaylistCheckbox && createPlaylistCheckbox.checked) {
            const newPlaylistTitle = newPlaylistTitleInput ? newPlaylistTitleInput.value.trim() : "";
            if (!newPlaylistTitle) warnings.push("Debes indicar el titulo de la nueva playlist.");
        }

        // Render warnings
        if (warningsBox) {
            warningsBox.innerHTML = "";
            if (warnings.length > 0) {
                const alertDiv = document.createElement("div");
                alertDiv.className = "alert alert--warning";

                const p = document.createElement("p");
                const strong = document.createElement("strong");
                strong.textContent = "Datos Faltantes / Errores:";
                p.appendChild(strong);
                alertDiv.appendChild(p);

                const ul = document.createElement("ul");
                warnings.forEach(w => {
                    const li = document.createElement("li");
                    li.textContent = w;
                    ul.appendChild(li);
                });
                alertDiv.appendChild(ul);
                warningsBox.appendChild(alertDiv);

                downloadBtn.disabled = true;
            } else {
                const alertDiv = document.createElement("div");
                alertDiv.className = "alert alert--success";
                const p = document.createElement("p");
                p.textContent = "¡Todo listo para descargar!";
                alertDiv.appendChild(p);
                warningsBox.appendChild(alertDiv);

                downloadBtn.disabled = false;
            }
        }
    }

    // Inline creations (Modals)
    const modalButtons = document.querySelectorAll("[data-open-modal]");
    modalButtons.forEach(btn => {
        btn.addEventListener("click", function () {
            const modalId = btn.getAttribute("data-open-modal");
            const modal = document.getElementById(modalId);
            if (modal) {
                // Populate parent context keys in modal forms
                if (modalId === "modal-subject") {
                    modal.querySelector('[name="area_id"]').value = areaSelect.value;
                } else if (modalId === "modal-topic") {
                    modal.querySelector('[name="subject"]').value = subjectSelect.value;
                } else if (modalId === "modal-module") {
                    modal.querySelector('[name="subject_id"]').value = subjectSelect.value;
                    modal.querySelector('[name="topic_id"]').value = topicSelect.value;
                }
                modal.removeAttribute("hidden");
            }
        });
    });

    const closeButtons = document.querySelectorAll("[data-close-modal], .modal-overlay");
    closeButtons.forEach(btn => {
        btn.addEventListener("click", function (e) {
            // Close only if click is on backdrop or close button
            if (btn.hasAttribute("data-close-modal") || e.target === btn) {
                const modal = btn.closest(".modal-overlay");
                if (modal) {
                    modal.setAttribute("hidden", "");
                    // Clear errors and input fields
                    const errorDiv = modal.querySelector(".modal-errors");
                    if (errorDiv) errorDiv.innerHTML = "";
                    modal.querySelector("form").reset();
                }
            }
        });
    });

    // Handle AJAX form submissions inside modals
    const modalForms = document.querySelectorAll(".modal-form");
    modalForms.forEach(form => {
        form.addEventListener("submit", function (e) {
            e.preventDefault();
            const entityType = form.getAttribute("data-entity-type");
            const url = form.getAttribute("action");
            const errorDiv = form.querySelector(".modal-errors");
            if (errorDiv) errorDiv.innerHTML = "";

            const formData = new FormData(form);

            fetch(url, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": getCsrfToken()
                }
            })
            .then(res => {
                if (!res.ok) {
                    return res.json().then(errData => { throw errData; });
                }
                return res.json();
            })
            .then(data => {
                // Success: close modal
                const modal = form.closest(".modal-overlay");
                modal.setAttribute("hidden", "");
                form.reset();

                // Add and auto-select the newly created item in the parent select
                let targetSelect;
                if (entityType === "area") targetSelect = areaSelect;
                else if (entityType === "subject") targetSelect = subjectSelect;
                else if (entityType === "topic") targetSelect = topicSelect;
                else if (entityType === "module") targetSelect = moduleSelect;

                if (targetSelect) {
                    const opt = document.createElement("option");
                    opt.value = data.id;
                    opt.textContent = data.name;
                    opt.selected = true;
                    targetSelect.appendChild(opt);

                    // Trigger change to update cascading children if necessary
                    targetSelect.dispatchEvent(new Event("change"));
                }
            })
            .catch(errData => {
                console.error("Error en creacion inline:", errData);
                if (errorDiv && errData.errors) {
                    errorDiv.innerHTML = "";
                    const alertDiv = document.createElement("div");
                    alertDiv.className = "alert alert--danger";
                    const ul = document.createElement("ul");
                    Object.keys(errData.errors).forEach(field => {
                        errData.errors[field].forEach(msg => {
                            const li = document.createElement("li");
                            li.textContent = field + ": " + msg;
                            ul.appendChild(li);
                        });
                    });
                    alertDiv.appendChild(ul);
                    errorDiv.appendChild(alertDiv);
                }
            });
        });
    });

    // Initial validation call
    syncPlaylistMode();
    validateForm();
});
