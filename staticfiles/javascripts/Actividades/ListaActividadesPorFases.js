function toggleOpciones() {
    var opciones = document.getElementById("opciones");
    if (opciones.classList.contains('opciones-ocultas')) {
        opciones.classList.remove('opciones-ocultas');
        opciones.classList.add('opciones-visibles');
    } else {
        opciones.classList.remove('opciones-visibles');
        opciones.classList.add('opciones-ocultas');
    }
}