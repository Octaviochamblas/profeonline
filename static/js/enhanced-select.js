(() => {
    const enhancedClass = "enhanced-select-native";
    const readyAttr = "data-enhanced-select-ready";

    function closeAll(exceptWrapper = null) {
        document.querySelectorAll(".custom-select.open").forEach((button) => {
            const wrapper = button.closest(".custom-select-wrapper");
            if (wrapper && wrapper !== exceptWrapper) {
                button.classList.remove("open");
                button.setAttribute("aria-expanded", "false");
            }
        });
    }

    function syncButton(select, button, optionsList) {
        const selectedOption = select.options[select.selectedIndex];
        button.querySelector(".custom-select-trigger").textContent = selectedOption ? selectedOption.textContent : "";

        optionsList.querySelectorAll(".custom-option").forEach((optionButton) => {
            const isSelected = optionButton.dataset.value === select.value;
            optionButton.classList.toggle("selected", isSelected);
            optionButton.setAttribute("aria-selected", isSelected ? "true" : "false");
        });
    }

    function buildEnhancedSelect(select) {
        if (
            select.hasAttribute(readyAttr) ||
            select.multiple ||
            select.dataset.enhanceSelect === "false"
        ) {
            return;
        }

        select.setAttribute(readyAttr, "true");
        select.classList.add(enhancedClass);
        select.setAttribute("aria-hidden", "true");
        select.tabIndex = -1;

        const wrapper = document.createElement("div");
        wrapper.className = "custom-select-wrapper";

        const button = document.createElement("button");
        button.type = "button";
        button.className = "custom-select";
        button.setAttribute("role", "combobox");
        button.setAttribute("aria-haspopup", "listbox");
        button.setAttribute("aria-expanded", "false");

        const trigger = document.createElement("span");
        trigger.className = "custom-select-trigger";

        const arrow = document.createElement("span");
        arrow.className = "custom-select-arrow";
        arrow.setAttribute("aria-hidden", "true");

        const optionsList = document.createElement("div");
        optionsList.className = "custom-options";
        optionsList.setAttribute("role", "listbox");

        Array.from(select.options).forEach((option) => {
            const optionButton = document.createElement("button");
            optionButton.type = "button";
            optionButton.className = "custom-option";
            optionButton.textContent = option.textContent;
            optionButton.dataset.value = option.value;
            optionButton.setAttribute("role", "option");
            optionButton.setAttribute("aria-selected", option.selected ? "true" : "false");

            optionButton.addEventListener("click", () => {
                select.value = option.value;
                select.dispatchEvent(new Event("change", { bubbles: true }));
                syncButton(select, button, optionsList);
                button.classList.remove("open");
                button.setAttribute("aria-expanded", "false");
            });

            optionsList.appendChild(optionButton);
        });

        button.appendChild(trigger);
        button.appendChild(arrow);

        wrapper.appendChild(button);
        wrapper.appendChild(optionsList);

        select.parentNode.insertBefore(wrapper, select);
        wrapper.appendChild(select);

        if (select.id) {
            const labelText = Array.from(document.querySelectorAll(`label[for="${select.id}"]`))
                .map((label) => label.textContent.trim())
                .filter(Boolean)
                .join(" ");

            if (labelText) {
                button.setAttribute("aria-label", labelText);
            }

            document.querySelectorAll(`label[for="${select.id}"]`).forEach((label) => {
                label.style.cursor = "pointer";
                label.addEventListener("click", (event) => {
                    event.preventDefault();
                    event.stopPropagation();
                    button.click();
                    button.focus();
                });
            });
        }

        select.addEventListener("change", () => {
            syncButton(select, button, optionsList);
        });

        button.addEventListener("click", (event) => {
            event.preventDefault();
            const isOpen = button.classList.contains("open");
            closeAll(wrapper);
            button.classList.toggle("open", !isOpen);
            button.setAttribute("aria-expanded", (!isOpen).toString());
        });

        button.addEventListener("keydown", (event) => {
            if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                button.click();
            }

            if (event.key === "Escape") {
                button.classList.remove("open");
                button.setAttribute("aria-expanded", "false");
            }
        });

        syncButton(select, button, optionsList);
    }

    function init() {
        document
            .querySelectorAll(`select:not([multiple]):not([${readyAttr}])`)
            .forEach((select) => buildEnhancedSelect(select));
    }

    document.addEventListener("DOMContentLoaded", init);
    document.addEventListener("htmx:afterSwap", init);
    document.addEventListener("click", (event) => {
        if (!event.target.closest(".custom-select-wrapper")) {
            closeAll();
        }
    });
})();
