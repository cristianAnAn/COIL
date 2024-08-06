document.getElementById('enviarCorreos').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita la recarga de la página
    const titulo = document.getElementById('correo2').value;
    //TODO: aqui estan los correos permitidos
    var emailPattern = /^[a-zA-Z0-9._%+-]+@(uttt\.edu\.mx|iua\.edu\.ar|alumnos\.iua\.edu\.ar)$/;
    // Validar el correo electrónico
    if (!emailPattern.test(titulo)) {
        Swal.fire({
            icon: 'error',
            title: 'Correo inválido',
            text: 'Ingresa un correo con la extencion uttt.edu.mx, iua.edu.ar o alumnos.iua.edu.ar'
        }); 
        return;
    }else{
    // Crear un nuevo elemento de lista
    const li = document.createElement('li');
    li.className = 'list-group-item d-flex justify-content-between align-items-center';
    li.innerHTML = `
        <span>
            <p>${titulo}</p>
            <input type="text" style="display: none;" value="${titulo}" name="correos"/>
        </span>
        <span>
            <button class="btn btn-sm btn-warning edit-btn">Editar</button>
            <button class="btn btn-sm btn-danger delete-btn">Eliminar</button>
        </span>
    `;

    // Añadir el nuevo elemento a la lista
    document.getElementById('CorreosList').appendChild(li);

    // Limpiar el formulario
    document.getElementById('enviarCorreos').reset();

    // Añadir eventos para los botones de editar y eliminar
    li.querySelector('.edit-btn').addEventListener('click', function(event) {
        event.preventDefault();
        const newTitulo = prompt('Nuevo título:', titulo);
        if (newTitulo && emailPattern.test(newTitulo) ) {
            li.querySelector('p').textContent = newTitulo;
            li.querySelector('input').value = newTitulo;
        } else{
            Swal.fire({
                icon: 'error',
                title: 'Correo inválido',
                text: 'Ingresa un correo con la extencion uttt.edu.mx, iua.edu.ar o alumnos.iua.edu.ar'
            });
        }
    });
    
    li.querySelector('.delete-btn').addEventListener('click', function() {
        li.remove();
    });}
});
