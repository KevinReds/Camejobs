document.addEventListener('DOMContentLoaded', function() {
    // Verificar si estamos en una pantalla menor a 1024px
    if (window.innerWidth <= 1024) {
        transformTableToVertical();
    }
    
    // Escuchar cambios de tamaño para aplicar la transformación
    window.addEventListener('resize', function() {
        if (window.innerWidth <= 1024) {
            transformTableToVertical();
        } else {
            // Opcionalmente, restaurar la tabla original si se agranda la pantalla
            // restoreOriginalTable();
        }
    });
    
    function transformTableToVertical() {
        // Obtener la tabla y sus elementos
        const table = document.querySelector('.ticket-table');
        const thead = table.querySelector('thead');
        const tbody = table.querySelector('tbody');
        
        // Si ya está transformada, no hacer nada
        if (table.classList.contains('vertical-transformed')) {
            return;
        }
        
        // Guardar la estructura original
        table.setAttribute('data-original', table.innerHTML);
        
        // Obtener títulos de las columnas
        const headerTitles = Array.from(thead.querySelectorAll('th')).map(th => th.textContent.trim());
        
        // Crear nueva estructura
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const ticketData = [];
        
        rows.forEach(row => {
            const cells = Array.from(row.querySelectorAll('td'));
            const ticketInfo = cells.map(cell => cell.innerHTML);
            ticketData.push(ticketInfo);
        });
        
        // Limpiar tabla
        table.innerHTML = '';
        
        // Crear nueva tabla vertical
        const newTable = document.createElement('table');
        newTable.className = 'ticket-table vertical-transformed';
        
        // Crear filas para cada tipo de información (título, tipo, estado, etc.)
        headerTitles.forEach((title, index) => {
            const row = document.createElement('tr');
            
            // Añadir celda de título (primera columna fija)
            const titleCell = document.createElement('th');
            titleCell.textContent = title;
            titleCell.className = 'fixed-title';
            row.appendChild(titleCell);
            
            // Añadir datos de cada ticket
            ticketData.forEach(ticket => {
                const dataCell = document.createElement('td');
                dataCell.innerHTML = ticket[index] || '';
                row.appendChild(dataCell);
            });
            
            newTable.appendChild(row);
        });
        
        // Reemplazar tabla original
        table.parentNode.replaceChild(newTable, table);
        
        // Añadir estilos para la tabla vertical
        const style = document.createElement('style');
        style.textContent = `
            .ticket-table.vertical-transformed {
                width: auto;
                border-collapse: collapse;
            }
            
            .ticket-table.vertical-transformed th.fixed-title {
                position: sticky;
                left: 0;
                z-index: 2;
                background-color: var(--color-5, #102b3e);
                color: var(--text-primary, #fff);
                min-width: 150px;
                text-align: left;
                padding: 15px;
                border-bottom: 1px solid #E0E0E0;
            }
            
            .ticket-table.vertical-transformed td {
                min-width: 150px;
                padding: 15px;
                text-align: center;
                border-bottom: 1px solid #E0E0E0;
                white-space: nowrap;
            }
            
            .dark-mode .ticket-table.vertical-transformed th.fixed-title {
                background-color: var(--color-5, #102b3e);
                color: var(--text-primary, #fff);
            }
            
            .table-container {
                overflow-x: auto;
            }
        `;
        document.head.appendChild(style);
    }
    
    // Manejar la posición del botón de crear ticket
    const btnCrearTicket = document.querySelector('.btn-crear-ticket');
    btnCrearTicket.style.position = 'absolute';
    btnCrearTicket.style.bottom = '20px';
    btnCrearTicket.style.left = '50%';
    btnCrearTicket.style.transform = 'translateX(-50%)';
});