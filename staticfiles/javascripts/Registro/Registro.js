document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('registroForm');
    const passwordInput = document.getElementById('id_password');
    const confirmPasswordInput = document.getElementById('id_confirmar_password');
    const usernameInput = document.getElementById('id_nombre_usuario');
    const passwordMismatch = document.getElementById('passwordFeedback');
    const usernameFeedback = document.getElementById('usernameFeedback');

    function validatePasswords() {
        if (passwordInput.value !== confirmPasswordInput.value) {
            confirmPasswordInput.classList.add('is-invalid');
            passwordMismatch.classList.remove('d-none');
        } else {
            confirmPasswordInput.classList.remove('is-invalid');
            passwordMismatch.classList.add('d-none');
        }
    }

    function checkUsernameAvailability(username) {
        fetch(`/Checkusername/?username=${username}`)
            .then(response => response.json())
            .then(data => {
                if (data.is_taken) {
                    usernameInput.classList.add('is-invalid');
                    usernameFeedback.classList.remove('d-none');
                } else {
                    usernameInput.classList.remove('is-invalid');
                    usernameFeedback.classList.add('d-none');
                }
            });
    }

    passwordInput.addEventListener('input', validatePasswords);
    confirmPasswordInput.addEventListener('input', validatePasswords);

    usernameInput.addEventListener('input', function () {
        const username = usernameInput.value;
        if (username) {
            checkUsernameAvailability(username);
        }
    });

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Evitar envío automático del formulario

        // Validar contraseñas
        if (passwordInput.value !== confirmPasswordInput.value) {
            confirmPasswordInput.classList.add('is-invalid');
            passwordMismatch.classList.remove('d-none');
            return; // Detener el proceso si las contraseñas no coinciden
        } else {
            confirmPasswordInput.classList.remove('is-invalid');
            passwordMismatch.classList.add('d-none');
        }

        // Validar nombre de usuario usando fetch
        const username = usernameInput.value;
        if (username) {
            fetch(`/check_username/?username=${username}`)
                .then(response => response.json())
                .then(data => {
                    if (data.is_taken) {
                        usernameInput.classList.add('is-invalid');
                        usernameFeedback.classList.remove('d-none');
                    } else {
                        usernameInput.classList.remove('is-invalid');
                        usernameFeedback.classList.add('d-none');
                        form.submit(); // Enviar formulario si el nombre de usuario está disponible
                    }
                });
        }
    });
});
