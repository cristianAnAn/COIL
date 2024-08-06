document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('enlaceForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Evita la recarga de la página

        const titulo = document.getElementById('tituloEnlace').value;
        const url = document.getElementById('urlEnlace').value;

        if (!titulo || !url) {
            alert('Por favor, ingrese un título y una URL.');
            return;
        }

        // Crear un nuevo elemento de lista
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';

        li.innerHTML = `
            <span>
                <strong>${titulo}</strong>: <a href="${url}" target="_blank">${url}</a>
                <input type="hidden" name="linkname" value="${titulo}">
                <input type="hidden" name="link" value="${url}">
            </span>
            <span>
                <button class="btn btn-sm btn-warning edit-btn">Editar</button>
                <button class="btn btn-sm btn-danger delete-btn">Eliminar</button>
            </span>
        `;

        // Añadir el nuevo elemento a la lista
        document.getElementById('enlacesList').appendChild(li);

        // Limpiar el formulario
        document.getElementById('enlaceForm').reset();

        // Cerrar el modal de enlaces
        const enlacesModal = bootstrap.Modal.getInstance(document.getElementById('Enlaces'));
        enlacesModal.hide();

        // Reabrir el primer modal después de un breve retraso
        setTimeout(function() {
            const materialModal = new bootstrap.Modal(document.getElementById('crearMaterial2'));
            materialModal.show();
        }, 500);

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
                li.querySelector('input[name="linkname"]').value = `${newTitulo}`;
                li.querySelector('input[name="link"]').value = `${newUrl}`;
            }
        });

        li.querySelector('.delete-btn').addEventListener('click', function() {
            li.remove();
        });
    });
});
