# mi_app/validators.py
import re
from django.core.exceptions import ValidationError

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("La contraseña debe contener al menos una letra minúscula.")
        if not re.search(r'\d', password):
            raise ValidationError("La contraseña debe contener al menos un número.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("La contraseña debe contener al menos un carácter especial.")
        if re.search(r'(.)\1', password):
            raise ValidationError("La contraseña no puede contener caracteres consecutivos iguales.")
        if any(password[i:i+3] in 'abcdefghijklmnopqrstuvwxyz' or password[i:i+3] in '0123456789' for i in range(len(password)-2)):
            raise ValidationError("La contraseña no puede contener secuencias consecutivas de letras o números.")

    def get_help_text(self):
        return (
            "La contraseña debe tener al menos 8 caracteres, una letra mayúscula, "
            "una letra minúscula, un número y un carácter especial. "
            "Además, no puede contener caracteres consecutivos iguales ni secuencias consecutivas de letras o números."
        )
