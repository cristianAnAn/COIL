document.addEventListener('DOMContentLoaded', (event) => {
    const today = new Date().toISOString().split('T')[0];
    const fechaInicio = document.querySelectorAll('.fecha-inicio1');
    const fechaFin = document.querySelectorAll('.fecha-fin1');

    fechaInicio.forEach((element) => {
        element.setAttribute('min', today);
    });

    fechaFin.forEach((element) => {
        element.setAttribute('min', today);
    });

    fechaInicio.forEach((element) => {
        element.addEventListener('change', (e) => {
            const startDate = e.target.value;
            fechaFin.forEach((finElement) => {
                finElement.setAttribute('min', startDate);
            });
        });
    });

    fechaFin.forEach((element) => {
        element.addEventListener('change', (e) => {
            if (e.target.value <= fechaInicio[0].value) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'La fecha de inicio no puede ser igual a la fecha de fin',
                });
                e.target.value = '';
            }
        });
    });
});

