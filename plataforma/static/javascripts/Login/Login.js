document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const usernameField = document.getElementById('id_nombre_usuario');
    const passwordField = document.getElementById('id_password');
    const usernameFeedback = document.getElementById('usernameFeedback');
    const passwordFeedback = document.getElementById('passwordFeedback');

    
    // Check if username exists and validate credentials
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        const username = usernameField.value;
        const password = passwordField.value;

        fetch(`/Validatecredentials/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            if (!data.user_exists) {
                usernameField.classList.add('is-invalid');
                usernameFeedback.style.display = 'block';
            } else {
                usernameField.classList.remove('is-invalid');
                usernameFeedback.style.display = 'none';
            }

            if (!data.credentials_valid) {
                passwordField.classList.add('is-invalid');
                passwordFeedback.style.display = 'block';
            } else {
                passwordField.classList.remove('is-invalid');
                passwordFeedback.style.display = 'none';
            }

            if (data.user_exists && data.credentials_valid) {
                loginForm.submit(); // Submit the form if validation passes
            }
        });
    });
});