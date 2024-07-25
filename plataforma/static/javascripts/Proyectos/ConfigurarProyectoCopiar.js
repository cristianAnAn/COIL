//*Funcion para verificar fechas

document.addEventListener('DOMContentLoaded', function () {
    const fechaInicioInputs = document.querySelectorAll('.fecha-inicio');
    const fechaFinInputs = document.querySelectorAll('.fecha-fin');

    fechaFinInputs.forEach(function (fechaFinInput) {
        fechaFinInput.addEventListener('change', function () {
            const fechaInicio = new Date(fechaInicioInputs[0].value);
            const fechaFin = new Date(fechaFinInput.value);

            if (fechaFin <= fechaInicio) {
                // Sumamos un día a la fecha de fin
                fechaFin.setDate(fechaInicio.getDate() + 1);

                // Actualizamos el valor del campo "Fecha de fin"
                fechaFinInput.valueAsDate = fechaFin;

                // Mostramos un mensaje de error
                Swal.fire({
                    icon: 'error',
                    title: 'Fecha inválida',
                    text: 'La fecha de fin no puede ser igual o menor a la fecha de inicio'
                }); 
            }
        });
    });
});

//*Funcion de copiado 
const copiarContenido = async (texto_id) => {
    texto = document.getElementById(texto_id).innerHTML;
    var mensaje = document.getElementById('mensaje');
    try {
        await navigator.clipboard.writeText(texto);
        mensaje.style.display = 'block';
        // Ocultar el mensaje después de 2 segundos
        setTimeout(function() {
            mensaje.style.display = 'none';
        }, 2000);
        console.log('Contenido copiado al portapapeles');
    } catch (err) {
        console.error('Error al copiar: ', err);
    }
}

const inputElement = document.getElementById("colorText");
const selectElement = document.getElementById("color");
selectElement.value = inputElement.value; // Asigna el valor de inputElement a selectElement


