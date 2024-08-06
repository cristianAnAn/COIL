document.addEventListener('DOMContentLoaded', function() {
    // Agregar enlace a la lista
    document.getElementById('addEnlaceActividad').addEventListener('click', function() {
        const titulo = document.getElementById('tituloEnlaceActividad').value;
        const url = document.getElementById('urlEnlaceActividad').value;

        // Validar campos
        if (!titulo || !url) {
            alert('Por favor, ingrese tanto el título como la URL.');
            return;
        }

        // Crear un nuevo elemento de lista
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.innerHTML = `
            <span>
                <strong>${titulo}</strong>: <a href="${url}" target="_blank">${url}</a>
                <input type="hidden" value="${url}" name="link"/>
                <input type="hidden" value="${titulo}" name="linkname"/>
            </span>
            <span>
                <button class="btn btn-sm btn-warning edit-btn">Editar</button>
                <button class="btn btn-sm btn-danger delete-btn">Eliminar</button>
            </span>
        `;

        // Añadir el nuevo elemento a la lista
        document.getElementById('enlacesListActividad').appendChild(li);

        // Limpiar el formulario de enlaces
        document.getElementById('enlaceFormActividad').reset();

        // Cerrar el modal de enlaces
        const enlacesModal = bootstrap.Modal.getInstance(document.getElementById('EnlacesActividad'));
        enlacesModal.hide();

        // Abrir el modal principal
        const materialModal = new bootstrap.Modal(document.getElementById('crearTarea'));
        materialModal.show();

        // Añadir eventos para los botones de editar y eliminar
        li.querySelector('.edit-btn').addEventListener('click', function(event) {
            event.preventDefault();
            const newTitulo = prompt('Nuevo título:', titulo);
            const newUrl = prompt('Nuevo enlace:', url);
            if (newTitulo && newUrl) {
                li.querySelector('strong').textContent = newTitulo;
                const a = li.querySelector('a');
                a.textContent = newUrl;
                a.href = newUrl;
                li.querySelector('input[name="link"]').value = newUrl;
                li.querySelector('input[name="linkname"]').value = newTitulo;
            }
        });

        li.querySelector('.delete-btn').addEventListener('click', function() {
            li.remove();
        });
    });
});
