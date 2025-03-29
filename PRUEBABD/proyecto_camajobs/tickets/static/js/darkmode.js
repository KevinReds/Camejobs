// Espera a que el DOM cargue completamente
    document.addEventListener("DOMContentLoaded", function () {
        const toggle = document.getElementById("dark-mode-toggle"); // Obtén el toggle
        const body = document.body;
    
        // Verifica si hay una preferencia guardada
        if (localStorage.getItem("darkMode") === "enabled") {
            body.classList.add("dark-mode"); // Aplica el modo oscuro
            toggle.checked = true; // Marca el toggle si el modo oscuro está activo
        } else {
            body.classList.remove("dark-mode"); // Asegúrate de que el modo oscuro esté desactivado
            toggle.checked = false; // Desmarca el toggle si el modo oscuro está desactivado
        }
    
        // Evento para cambiar entre modos
        toggle.addEventListener("change", function () {
            if (this.checked) {
                body.classList.add("dark-mode");
                localStorage.setItem("darkMode", "enabled"); // Guarda la preferencia
            } else {
                body.classList.remove("dark-mode");
                localStorage.setItem("darkMode", "disabled"); // Guarda la preferencia
            }
        });
    });