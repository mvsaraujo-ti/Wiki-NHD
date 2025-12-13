// Lista de páginas que NÃO exigem login
const publicPages = ["/login.html"];

// Página atual
const currentPage = window.location.pathname;

// Se a página NÃO for pública → exigir login
if (!publicPages.includes(currentPage)) {
    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href = "/login.html";
    }
}
