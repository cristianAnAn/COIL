//*sweet alert para eliminar
function eliminar(event, element) {
    event.preventDefault(); // Evita que el enlace navegue a otra página
    const link = element.getAttribute('data-url');
    Swal.fire({
        title: '¿Estás seguro?',
        text: 'Esta acción no se puede deshacer',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Aceptar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire('¡Hecho!', 'La acción ha sido confirmada.', 'success').then(() => {
                window.location.href = link; // Redirige a la página deseada
            });
        } else if (result.dismiss === Swal.DismissReason.cancel) {
            Swal.fire('Cancelado', 'La acción ha sido cancelada.', 'error');
        }
    });
}

//*procesa los enlaces
document.getElementById('enlaceForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita la recarga de la página
    const titulo = document.getElementById('tituloEnlace').value;
    const url = document.getElementById('urlEnlace').value;

    // Crear un nuevo elemento de lista
    const li = document.createElement('li');
    li.className = 'list-group-item d-flex justify-content-between align-items-center';
    li.innerHTML = `
        <span>
            <strong>${titulo}</strong>: <a href="${url}" target="_blank">${url}</a>
            <input type="text" style="display: none;" value="${url}" name="link"/>
            <input type="text" style="display: none;" value="${titulo}" name="linkname"/>
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

    // Cerrar el modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('Enlaces'));
    modal.hide();

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
        }
    });

    li.querySelector('.delete-btn').addEventListener('click', function() {
        li.remove();
    });
});

//*desactivar los botones para evitar multiples envios
function disableButtons() {
    const buttons = document.getElementsByClassName("submitBtn");
    for (let button of buttons) {
        button.disabled = true;
    }
}


//*Mostrar archivos
const addedFiles = [];

document.getElementById('files').addEventListener('change', function(event) {
    const files = event.target.files;
    const preview = document.getElementById('preview');

    Array.from(files).forEach((file) => {
        if (!addedFiles.includes(file)) {
            addedFiles.push(file);

            const reader = new FileReader();
            reader.onload = function(e) {
                const div = document.createElement('div');
                div.classList.add('preview-item');
                div.innerHTML = `
                    <embed src="${e.target.result}" alt="${file.name}" style="width:10%; height:50px;">
                    <span>${file.name}</span>
                    <button class="btn btn-danger ms-2 me-2" onclick="removeFile(event, ${addedFiles.length - 1})">Eliminar</button>
                `;
                preview.appendChild(div);
            };
            reader.onerror = function() {
                console.error("Error al leer el archivo", file.name);
            };
            reader.readAsDataURL(file);
        }
    });

    updateInputFiles();
});

function removeFile(event, index) {
    event.preventDefault(); // Evita el comportamiento por defecto del botón

    addedFiles.splice(index, 1); // Elimina el archivo de la lista de archivos agregados

    // Actualiza la vista previa
    const preview = document.getElementById('preview');
    preview.innerHTML = '';
    addedFiles.forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = function(e) {
            const div = document.createElement('div');
            div.classList.add('preview-item');
            div.innerHTML = `
                <embed src="${e.target.result}" alt="${file.name}" style="width:10%; height:50px;">
                <span>${file.name}</span>
                <button class="btn btn-danger ms-2 me-2" onclick="removeFile(event, ${index})">Eliminar</button>
            `;
            preview.appendChild(div);
        };
        reader.readAsDataURL(file);
    });

    updateInputFiles();
}

function updateInputFiles() {
    const input = document.getElementById('files');
    const dataTransfer = new DataTransfer();

    addedFiles.forEach(file => {
        dataTransfer.items.add(file);
    });

    input.files = dataTransfer.files;
}

