document.addEventListener("DOMContentLoaded", () => {
    const panel = document.getElementById("zeus-panel");
    const button = document.getElementById("zeus-button");

    button.addEventListener("click", () => {
        panel.classList.toggle("open");
    });
});
