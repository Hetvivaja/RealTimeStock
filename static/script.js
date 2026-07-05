const navToggle = document.querySelector(".nav-toggle");
const navPanel = document.querySelector(".nav-panel");

if (navToggle && navPanel) {
    navToggle.addEventListener("click", () => {
        const isOpen = navToggle.getAttribute("aria-expanded") === "true";
        navToggle.setAttribute("aria-expanded", String(!isOpen));
        navPanel.classList.toggle("open", !isOpen);
    });
}

document.querySelectorAll("[data-search-form]").forEach((form) => {
    form.addEventListener("submit", (event) => {
        const input = form.querySelector("input[name='query']");
        if (!input) {
            return;
        }

        input.value = input.value.trim().toUpperCase();
        if (!input.value) {
            event.preventDefault();
            input.focus();
        }
    });
});
