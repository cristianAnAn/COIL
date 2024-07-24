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
