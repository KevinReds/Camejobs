document.addEventListener("DOMContentLoaded", function () {
    // Selecciona todas las tarjetas de personas
    document.querySelectorAll(".persona").forEach(function (card) {
        card.addEventListener("click", function (event) {
            // Evita que el clic en un enlace u otro elemento interfiera
            if (event.target.closest(".perfil_link")) return;

            // Encuentra el enlace dentro de la tarjeta
            const link = this.querySelector(".perfil_link");
            if (link && link.href) {
                window.location.href = link.href;
            }
        });
    });
});