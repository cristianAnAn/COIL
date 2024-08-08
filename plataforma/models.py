from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import os


class Rol(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class UsuarioManager(BaseUserManager):
    def create_user(self, nombre_usuario, password=None , rol=None):
        if not nombre_usuario:
            raise ValueError('Los usuarios deben tener un nombre de usuario')
        
        user = self.model(
            nombre_usuario=nombre_usuario,
            rol=rol
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre_usuario, password=None):
        user = self.create_user(nombre_usuario, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre_usuario = models.CharField(max_length=100, unique=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    correo_institucional = models.EmailField(unique=True)
    objects = UsuarioManager()
    is_firstLogin = models.BooleanField(default=True)
    is_firstRegister = models.BooleanField(default=True)
    USERNAME_FIELD = 'nombre_usuario'

    def __str__(self):
        return self.nombre_usuario

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin




class Catalogo(models.Model):
    nombre_universidad = models.CharField(max_length=200)
    pais = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_universidad

class Alumno(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'No Binario'),
    ]
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    matricula_dni = models.CharField(max_length=50)
    universidad_origen = models.ForeignKey(Catalogo, on_delete=models.CASCADE)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    id_usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

class Profesor(models.Model):
    GENERO_CHOICES = [
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('no_binario', 'No Binario')
    ]
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    idmex_dni = models.CharField(max_length=20)
    universidad_origen = models.ForeignKey(Catalogo, on_delete=models.CASCADE)
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES)
    id_usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    trayectoria_academica = models.TextField(null=True, blank=True)
    trayectoria_profesional = models.TextField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    gustos_personales = models.TextField(null=True, blank=True)
    imagen = models.ImageField(upload_to='imagenes_profesores', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

    def save(self, *args, **kwargs):
        # Check if there is an existing image before saving a new one
        self.nombre = self.nombre.title()
        self.apellidos = self.apellidos.title()
        try:
            this = Profesor.objects.get(id=self.id)
            if this.imagen != self.imagen:
                if this.imagen:  # Check if an image exists
                    if os.path.isfile(this.imagen.path):
                        os.remove(this.imagen.path)
        except Profesor.DoesNotExist:
            pass  # This is a new object, no need to check for an old image

        super(Profesor, self).save(*args, **kwargs)
    
#*Cosas agregadas por Daniel
class Proyectos(models.Model):
    nombre = models.CharField(max_length=100)
    materia = models.CharField(max_length=50, null=True)
    codigo = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    ciclo_escolar = models.TextField()
    achivo_proyecto = models.BooleanField(default=False)
    color = models.CharField(max_length=10)
    enlace_zoom = models.TextField(null=True)
    id_profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)

class Anuncios(models.Model):
    comentario = models.TextField(null=True)
    fecha = models.DateTimeField()
    fecha_edit = models.DateTimeField()
    id_profesor = models.ForeignKey(Profesor, null=True, on_delete=models.CASCADE)
    id_alumno = models.ForeignKey(Alumno, null=True, on_delete=models.CASCADE)
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)

class Anuncios_archivos(models.Model):
    path = models.FileField(upload_to='archivos_foro', null=True, blank=True)
    fecha = models.DateField()
    id_anuncio= models.ForeignKey(Anuncios,on_delete=models.CASCADE)

class Anuncios_enlaces(models.Model):
    titulo = models.TextField()
    path = models.TextField()
    fecha = models.DateField()
    id_anuncio= models.ForeignKey(Anuncios,on_delete=models.CASCADE)

class Anuncios_comentarios(models.Model):
    comentario = models.TextField()
    fecha = models.DateTimeField()
    fecha_edit = models.DateTimeField()
    id_profesor = models.ForeignKey(Profesor, null=True, on_delete=models.CASCADE)
    id_alumno = models.ForeignKey(Alumno, null=True, on_delete=models.CASCADE)
    id_anuncio= models.ForeignKey(Anuncios,on_delete=models.CASCADE)
class Fases(models.Model):
    titulo = models.CharField(max_length=50)
    puntuacion = models.CharField(max_length=5)
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)

class Profesores_proyecto(models.Model):
    fecha_ingreso = models.DateField()
    id_profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)

class Alumnos_proyecto(models.Model):
    fecha_ingreso = models.DateField()
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)

#!Falta tareas, materiales y presentación profesor
#*Cosas de Mateo
class Materiales(models.Model):
    descripcion = models.TextField()
    fecha = models.DateField()
    id_fase = models.BigIntegerField()
    titulo = models.CharField(max_length=100)
    id_profesor = models.IntegerField()
    
    def _str_(self):
        return self.titulo
    
class Materiales_Comentarios(models.Model):
    comentario = models.TextField()
    fecha = models.DateTimeField()
    fecha_edit = models.DateTimeField()
    id_profesor = models.ForeignKey(Profesor, null=True, on_delete=models.CASCADE)
    id_alumno = models.ForeignKey(Alumno, null=True, on_delete=models.CASCADE)
    id_material= models.ForeignKey(Materiales,on_delete=models.CASCADE)

class Materiales_enlaces(models.Model):
    titulo = models.TextField()
    path = models.TextField()
    fecha = models.DateField()
    id_anuncio= models.ForeignKey(Materiales,on_delete=models.CASCADE)

    #PODER ADJUNTAR ARCHIVOS EN MATERIALES
class SubirArchivos_Materiales(models.Model):
    path = models.FileField(upload_to='archivos_materiales', null=True, blank=True)
    fecha = models.DateField()
    id_material= models.ForeignKey(Materiales,on_delete=models.CASCADE)

class Materiales_Comentarios_priv(models.Model):
    comentario = models.TextField()
    fecha = models.DateTimeField()
    fecha_edit = models.DateTimeField()
    id_profesor = models.ForeignKey(Profesor, null=True, on_delete=models.CASCADE)
    id_alumno = models.ForeignKey(Alumno, null=True, on_delete=models.CASCADE)
    id_material= models.ForeignKey(Materiales,on_delete=models.CASCADE)





# APARTADO DE ACTIVIDADES (ABAJO)
class Actividades(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()
    id_fase = models.BigIntegerField()
    id_profesor = models.IntegerField()
    
    def _str_(self):
        return self.titulo
    
#LINKS DE LAS ACTIVIDADES
class Actividades_enlaces(models.Model):
    titulo = models.TextField()
    path = models.TextField()
    fecha = models.DateField()
    id_anuncio= models.ForeignKey(Actividades,on_delete=models.CASCADE)

    #PODER ADJUNTAR ARCHIVOS EN ACTIVIDADES
class SubirArchivos_Actividades(models.Model):
    path = models.FileField(upload_to='archivos_actividades', null=True, blank=True)
    fecha = models.DateField()
    id_actividad= models.ForeignKey(Actividades,on_delete=models.CASCADE)
    
#HACER COMENTARIOS 
class Actividades_Comentarios(models.Model):
    comentario = models.TextField()
    fecha = models.DateTimeField()
    fecha_edit = models.DateTimeField()
    id_profesor = models.ForeignKey(Profesor, null=True, on_delete=models.CASCADE)
    id_alumno = models.ForeignKey(Alumno, null=True, on_delete=models.CASCADE)
    id_actividad= models.ForeignKey(Actividades,on_delete=models.CASCADE)


#HACER COMENTARIOS PRIVADOS
class Actividades_Comentarios_priv(models.Model):
    comentario = models.TextField()
    fecha = models.DateTimeField()
    fecha_edit = models.DateTimeField()
    id_profesor = models.ForeignKey(Profesor, null=True, on_delete=models.CASCADE)
    id_alumno = models.ForeignKey(Alumno, null=True, on_delete=models.CASCADE)
    id_actividad= models.ForeignKey(Actividades,on_delete=models.CASCADE)

#TODO: Entregas
class Entregas_Actividades(models.Model):
    path = models.FileField(upload_to='entregas', null=True, blank=True)
    fecha = models.DateField()
    id_actividad= models.ForeignKey(Actividades,on_delete=models.CASCADE)
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)

class Asignar_actividad(models.Model):
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    id_actividad = models.ForeignKey(Actividades, on_delete=models.CASCADE)
    calificacion = models.BooleanField(null=True)
    entregada = models.BooleanField(default=False)