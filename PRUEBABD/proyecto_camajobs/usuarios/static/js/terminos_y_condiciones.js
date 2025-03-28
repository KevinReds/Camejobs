document.addEventListener("DOMContentLoaded", function() {
    // ==============================================
    // FUNCIONALIDAD DE ACORDEÓN (Términos y condiciones)
    // ==============================================
    const accordionCards = document.querySelectorAll('.terms-card');
    
    // Inicializar todas las tarjetas como cerradas
    accordionCards.forEach(card => {
        card.classList.remove('active');
        
        const header = card.querySelector('.terms-card-header');
        header.addEventListener('click', function() {
            // Cerrar todas las tarjetas primero
            accordionCards.forEach(otherCard => {
                if (otherCard !== card) {
                    otherCard.classList.remove('active');
                }
            });
            
            // Alternar estado de la tarjeta clickeada
            card.classList.toggle('active');
            
            // Forzar repintado para asegurar la animación
            void card.offsetWidth;
        });
    });
});