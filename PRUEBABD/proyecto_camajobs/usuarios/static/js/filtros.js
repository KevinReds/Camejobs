function applyFilters() {
    const searchText = document.getElementById('searchBar').value.toLowerCase();
    const ubicacion = document.getElementById('filterUbicacion').value.toLowerCase();

    const perfiles = document.querySelectorAll('.persona'); // Lista de personas

    perfiles.forEach(perfil => {
        // Obtener ubicación del contenido del elemento con clase persona-ubicacion
        const ubicacionElement = perfil.querySelector('.persona-ubicacion');
        const perfilUbicacion = ubicacionElement ? ubicacionElement.textContent.toLowerCase().replace("📍 ", "") : "";

        // Obtener nombre y profesión del perfil
        const nombreElement = perfil.querySelector('.persona-nombre');
        const profesionElement = perfil.querySelector('.persona-profesion');
        
        const perfilNombre = nombreElement ? nombreElement.textContent.toLowerCase() : "";
        const perfilProfesion = profesionElement ? profesionElement.textContent.toLowerCase() : "";

        // Verificación de coincidencias
        const ubicacionMatch = !ubicacion || perfilUbicacion.includes(ubicacion);
        const searchMatch =
            perfilNombre.includes(searchText) ||
            perfilProfesion.includes(searchText) ||
            perfilUbicacion.includes(searchText) ||
            searchText === "";

        // Mostrar u ocultar el perfil según los filtros
        if (ubicacionMatch && searchMatch) {
            perfil.style.visibility = "visible";  
            perfil.style.opacity = "1";  
            perfil.style.position = "relative"; 
        } else {
            perfil.style.visibility = "hidden";  
            perfil.style.opacity = "0";  
            perfil.style.position = "absolute";  

        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const toggleFiltrosBtn = document.getElementById('toggleFiltros');
    const filtrosContainer = document.getElementById('filtrosContainer');

    if (toggleFiltrosBtn && filtrosContainer) {
        toggleFiltrosBtn.addEventListener('click', function () {
            filtrosContainer.classList.toggle('show'); // Muestra/oculta filtros
        });
    }

    // Aplicar filtros automáticamente en tiempo real
    document.getElementById('searchBar').addEventListener('input', applyFilters);
    document.getElementById('filterUbicacion').addEventListener('change', applyFilters);
});