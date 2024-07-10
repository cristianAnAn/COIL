from django import forms
from .models import Usuario, Rol, Alumno, Catalogo, Profesor

# Formulario Registro General
class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Contraseña')
    confirmar_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirmar Contraseña')

    rol = forms.ModelChoiceField(queryset=Rol.objects.all(), empty_label="Seleccione", widget=forms.Select(attrs={'class': 'form-select'}))
    
    nombre_usuario = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'minlength': '8'}),
        label='Nombre de usuario'
    )

    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'password','correo_institucional' ,'confirmar_password', 'rol']
        widgets = {
            'correo_institucional': forms.EmailInput(attrs={'class': 'form-control'}),
            'nombre_usuario': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def clean_correo_institucional(self):
        correo = self.cleaned_data.get('correo_institucional')
        if correo:
            dominio_valido = any(correo.endswith(dom) for dom in ['@iua.edu.ar', '@uttt.edu.mx'])
            if not dominio_valido:
                raise forms.ValidationError("El correo debe ser institucional (@iua.edu.ar, @uttt.edu.mx)")
        return correo    


class VerificationCodeForm(forms.Form):
    code = forms.CharField(max_length=6)
            
# Formulario Registro Alumno (REGISTRO)
class RegistroAlumnoForm(forms.ModelForm):
    GENERO_CHOICES = [
        ('', 'Seleccione'),  # Opción por defecto
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'No Binario'),
    ]
    
    genero = forms.ChoiceField(choices=GENERO_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    
    universidad_origen = forms.ModelChoiceField(
        queryset=Catalogo.objects.all(),
        empty_label="Seleccione",
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Universidad de origen",  # Agrega un label para el campo
        to_field_name='nombre_universidad',  # Campo de modelo a utilizar para la opción mostrada
    )

    class Meta:
        model = Alumno
        fields = ['nombre', 'apellidos' , 'matricula_dni', 'universidad_origen', 'genero']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[A-Za-záéíóúÁÉÍÓÚñÑ ]+', 'title': 'Ingrese solo letras y espacios'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[A-Za-záéíóúÁÉÍÓÚñÑ ]+', 'title': 'Ingrese solo letras y espacios'}),
            'matricula_dni': forms.NumberInput(attrs={'class': 'form-control', 'min': '10000000', 'max': '99999999999',  'step': '1'}),
            'genero': forms.Select(attrs={'class': 'form-control'})
        }
    def clean_universidad_origen(self):
        universidad_origen = self.cleaned_data.get('universidad_origen')
        if universidad_origen == '':
            return None
        return universidad_origen


# Formulario Registro Profesor (REGISTRO)
class RegistroProfesorForm(forms.ModelForm):
    GENERO_CHOICES = [
        ('', 'Seleccione'),  # Opción por defecto
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('no_binario', 'No Binario'),
    ]

    genero = forms.ChoiceField(choices=GENERO_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    universidad_origen = forms.ModelChoiceField(
        queryset=Catalogo.objects.all(),
        empty_label="Seleccione",
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Universidad de origen",  # Agrega un label para el campo
        to_field_name='nombre_universidad',  # Campo de modelo a utilizar para la opción mostrada
    )
    
    class Meta:
        model = Profesor
        fields = ['nombre', 'apellidos', 'idmex_dni', 'universidad_origen', 'genero']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[A-Za-záéíóúÁÉÍÓÚñÑ ]+', 'title': 'Ingrese solo letras y espacios'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[A-Za-záéíóúÁÉÍÓÚñÑ ]+', 'title': 'Ingrese solo letras y espacios'}),
            'idmex_dni': forms.NumberInput(attrs={'class': 'form-control', 'min': '10000000', 'max': '99999999999', 'step': '1'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean_universidad_origen(self):
        universidad_origen = self.cleaned_data.get('universidad_origen')
        if universidad_origen == '':
            return None
        return universidad_origen



class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['trayectoria_academica', 'trayectoria_profesional', 'descripcion', 'gustos_personales']
        widgets = {
            'trayectoria_academica': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'trayectoria_profesional': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'gustos_personales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }





# Formulario Login
class LoginForm(forms.Form):
    nombre_usuario = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Contraseña')

class EmailForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')