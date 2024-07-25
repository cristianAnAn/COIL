    $(document).ready(function(){
        $('#profesorForm').on('submit', function(event){
            event.preventDefault(); // Previene el envío del formulario estándar
            
            var formData = new FormData(this);
            
            $.ajax({
                url: '',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response){
                    if(response.success){
                        Swal.fire({
                            title: 'Éxito',
                            text: 'Datos ingresados correctamente',
                            icon: 'success',
                            timer: 5000,
                            timerProgressBar: true,
                            showConfirmButton: false,
                            willClose: () => {
                                window.location.href = "{% url 'ListaProyectos' %}";
                            }
                        });

                        // Redirigir después de 5 segundos
                        setTimeout(() => {
                            window.location.href = "{% url 'ListaProyectos' %}";
                        }, 5000);
                    } else {
                        var errors = response.errors;
                        var errorMessages = '';
                        for (var field in errors) {
                            if (errors.hasOwnProperty(field)) {
                                errors[field].forEach(function(error){
                                    errorMessages += '<p>' + error + '</p>';
                                });
                            }
                        }
                        Swal.fire({
                            title: 'Error',
                            html: errorMessages,
                            icon: 'error',
                        });
                    }
                },
                error: function(xhr, status, error){
                    Swal.fire({
                        title: 'Error',
                        text: 'Hubo un problema con el servidor. Inténtalo de nuevo más tarde.',
                        icon: 'error',
                    });
                }
            });
        });

        $('input[type="file"]').on('change', function(){
            var reader = new FileReader();
            reader.onload = function(e){
                $('#imagenPreview').attr('src', e.target.result);
                $('#imagenCard').show();
            }
            reader.readAsDataURL(this.files[0]);
        });
    });

