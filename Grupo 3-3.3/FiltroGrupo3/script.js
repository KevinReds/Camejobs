function applyFilters() {
    const modalidad = document.getElementById('filterModalidad').value;
    const experiencia = document.getElementById('filterExperience').value;
    const localizacion = document.getElementById('filterCompany').value;
    const searchQuery = document.getElementById('filterInput').value.toLowerCase();

    const userList = document.getElementById('userList');
    const users = userList.getElementsByTagName('li');

    for (let user of users) {
        const userModalidad = user.getAttribute('data-modalidad');
        const userExperiencia = user.getAttribute('data-experiencia');
        const userLocalizacion = user.getAttribute('data-localizacion');
        const userName = user.querySelector('.nombre').textContent.toLowerCase();

        const modalidadMatch = !modalidad || userModalidad === modalidad;
        const experienciaMatch = !experiencia || userExperiencia === experiencia;
        const localizacionMatch = !localizacion || userLocalizacion === localizacion;
        const searchMatch = userName.includes(searchQuery);

        if (modalidadMatch && experienciaMatch && localizacionMatch && searchMatch) {
            user.style.display = 'block';
        } else {
            user.style.display = 'none';
        }
    }
}

function updateSalary(value) {
    document.getElementById('salario1').textContent = value;
}

function setFilter(type, value) {
    switch (type) {
        case 'modalidad':
            document.getElementById('filterModalidad').value = value;
            break;
        case 'company':
            document.getElementById('filterCompany').value = value;
            break;
        case 'experience':
            document.getElementById('filterExperience').value = value;
            break;
        default:
            break;
    }
    applyFilters();
}
