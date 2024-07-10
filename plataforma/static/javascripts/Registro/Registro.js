document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('registroForm');
    const passwordInput = document.getElementById('id_password');
    const confirmPasswordInput = document.getElementById('id_confirmar_password');
    const usernameInput = document.getElementById('id_nombre_usuario');
    const passwordMismatch = document.getElementById('passwordFeedback');
    const usernameFeedback = document.getElementById('usernameFeedback');
    const passwordCriteria = document.getElementById('passwordCriteria');
    const togglePassword = document.getElementById('togglePassword');
    const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');

    function validatePasswordStrength(password) {
        const minLength = 8;
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumbers = /[0-9]/.test(password);
        const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
        const consecutiveChars = /(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)/.test(password); // Patrón para caracteres consecutivos
        
        return password.length >= minLength && 
               hasUpperCase && 
               hasLowerCase && 
               hasNumbers && 
               hasSpecialChar &&
               !consecutiveChars;
    }

    function validatePasswords() {
        const passwordValue = passwordInput.value.trim();
        const confirmPasswordValue = confirmPasswordInput.value.trim();

        if (passwordValue === '' || confirmPasswordValue === '') {
            // Si alguno de los campos está vacío
            confirmPasswordInput.classList.remove('is-valid');
            confirmPasswordInput.classList.add('is-invalid');
            passwordMismatch.classList.remove('d-none');
        } else if (passwordValue !== confirmPasswordValue) {
            confirmPasswordInput.classList.remove('is-valid');
            confirmPasswordInput.classList.add('is-invalid');
            passwordMismatch.classList.remove('d-none');
        } else {
            confirmPasswordInput.classList.remove('is-invalid');
            confirmPasswordInput.classList.add('is-valid');
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

    togglePassword.addEventListener('click', function () {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        togglePassword.querySelector('i').classList.toggle('bi-eye');
        togglePassword.querySelector('i').classList.toggle('bi-eye-slash');
    });

    toggleConfirmPassword.addEventListener('click', function () {
        const type = confirmPasswordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        confirmPasswordInput.setAttribute('type', type);
        toggleConfirmPassword.querySelector('i').classList.toggle('bi-eye');
        toggleConfirmPassword.querySelector('i').classList.toggle('bi-eye-slash');
    });

    passwordInput.addEventListener('input', function () {
        validatePasswords();
        if (!validatePasswordStrength(passwordInput.value)) {
            passwordInput.classList.add('is-invalid');
            passwordInput.classList.remove('is-valid');
            passwordCriteria.classList.remove('d-none');
        } else {
            passwordInput.classList.remove('is-invalid');
            passwordInput.classList.add('is-valid');
            passwordCriteria.classList.add('d-none');
        }
    });

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
        const passwordValue = passwordInput.value.trim();
        const confirmPasswordValue = confirmPasswordInput.value.trim();

        if (passwordValue === '' || confirmPasswordValue === '') {
            // Si alguno de los campos está vacío
            confirmPasswordInput.classList.remove('is-valid');
            confirmPasswordInput.classList.add('is-invalid');
            passwordMismatch.classList.remove('d-none');
            return; // Detener el proceso si las contraseñas están vacías
        } else if (passwordValue !== confirmPasswordValue) {
            confirmPasswordInput.classList.remove('is-valid');
            confirmPasswordInput.classList.add('is-invalid');
            passwordMismatch.classList.remove('d-none');
            return; // Detener el proceso si las contraseñas no coinciden
        } else {
            confirmPasswordInput.classList.remove('is-invalid');
            confirmPasswordInput.classList.add('is-valid');
            passwordMismatch.classList.add('d-none');
        }

        // Validar nombre de usuario usando fetch
        const username = usernameInput.value;
        if (username) {
            checkUsernameAvailability(username);
        }

        // Si todo está validado correctamente, enviar el formulario
        if (passwordValue !== '' && confirmPasswordValue !== '' && passwordValue === confirmPasswordValue) {
            form.submit();
        }
    });
});
