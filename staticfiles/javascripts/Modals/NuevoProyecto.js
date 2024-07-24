    document.addEventListener('DOMContentLoaded', (event) => {
            const today = new Date().toISOString().split('T')[0];
            const fechaInicio = document.getElementsByName("fecha_inicio")[0];
            const fechaFin = document.getElementsByName("fecha_fin")[0];

            fechaInicio.setAttribute('min', today);
            fechaFin.setAttribute('min', today);

            fechaInicio.addEventListener('change', (e) => {
                const startDate = e.target.value;
                fechaFin.setAttribute('min', startDate);
            });

            fechaFin.addEventListener('change', (e) => {
                if (e.target.value <= fechaInicio.value) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'La fecha de inicio no puede ser igual a la fecha de fin',
                    });
                    e.target.value = "";
                }
            });
        });
