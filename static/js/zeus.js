console.log("Zeus inicializado.");

document.getElementById("zeus-button").addEventListener("click", () => {
    const panel = document.getElementById("zeus-panel");
    panel.classList.toggle("open");
});
