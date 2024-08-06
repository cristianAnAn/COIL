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
