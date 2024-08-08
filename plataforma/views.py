from django.db import connection, transaction
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import Actividades, SubirArchivos_Actividades, SubirArchivos_Materiales, Usuario, Catalogo, Alumno, Profesor, Rol, Anuncios_archivos, Entregas_Actividades
import json
from django.contrib  import messages
from datetime import datetime
import random
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.db.models import Q
from django.views.generic.edit import FormView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse_lazy, reverse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
# Create your views here.
def index(request):
    return redirect('Login')

@csrf_protect
@login_required(login_url='Login')
def EditarUsuario(request):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    if tipo_usuario == "Alumno":
        alumno = Alumno.objects.get(id_usuario_id=usuario.id)
        nombres = alumno.nombre
        apellidos = alumno.apellidos
        matricula = alumno.matricula_dni
    elif tipo_usuario == "Profesor":
        profesor = Profesor.objects.get(id_usuario_id=usuario.id)
        nombres = profesor.nombre
        apellidos = profesor.apellidos
        matricula = profesor.idmex_dni
    
    return render(request, 'pages/Usuarios/editar_usuario.html', {
        'nombres': nombres,
        'apellidos': apellidos,
        'matricula': matricula,
        'tipo_usuario':tipo_usuario
    })

@login_required(login_url='Login')
def guardar_usuario(request):
    if request.method == 'POST':
        usuario = request.user
        tipo_usuario = usuario.rol.nombre
        
        nombres = request.POST['nombres']
        apellidos = request.POST['apellidos']
        matricula = request.POST['matricula']
        
        if tipo_usuario == "Alumno":
            alumno = Alumno.objects.get(id_usuario_id=usuario.id)
            alumno.nombre = nombres
            alumno.apellidos = apellidos
            alumno.matricula_dni = matricula
            alumno.save()
            
        elif tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            profesor.nombre = nombres
            profesor.apellidos = apellidos
            profesor.idmex_dni = matricula
            profesor.save()
        
        messages.success(request, 'Datos guardados correctamente.')
        return redirect('editar_usuario')  # Redirige al mismo formulario para mostrar el mensaje

    return redirect('editar_usuario')

def LlenarLayout(request): 
        usuario = request.user
        tipo_usuario = usuario.rol.nombre
        correo = request.user.correo_institucional
        try:
            if tipo_usuario == "Alumno":
                alumno = Alumno.objects.get(id_usuario_id=usuario.id)
                universidad = alumno.universidad_origen
                id_alumno = alumno.id
                nombres= alumno.nombre
                apellidos = alumno.apellidos
                matricula = alumno.matricula_dni
                usuarioLog= id_alumno
                with connection.cursor() as cursor:
                    cursor.callproc('BuscarNombreProyectos', [id_alumno])
                    listaProyectos = cursor.fetchall()
            elif tipo_usuario == "Profesor":
                profesor = Profesor.objects.get(id_usuario_id=usuario.id)
                id_profesor = profesor.id
                nombres= profesor.nombre
                apellidos = profesor.apellidos
                matricula = profesor.idmex_dni
                universidad = profesor.universidad_origen
                usuarioLog = id_profesor
                with connection.cursor() as cursor:
                    cursor.callproc('BuscarProyectoNombreImpartido', [id_profesor])
                    listaProyectos = cursor.fetchall()
            else:
                return redirect('logout')
        except (Alumno.DoesNotExist, Profesor.DoesNotExist):
            return redirect('logout')
        return [
            tipo_usuario,
            usuario,
            nombres,
            apellidos,
            correo,
            matricula,
            universidad,
            listaProyectos,
            usuarioLog]
@csrf_protect
@login_required(login_url='Login')
def ListaProyectos(request):
    usuario = request.user
    contexto = 'activo'
    if usuario.is_firstRegister == True and usuario.rol.nombre == 'Profesor':
        logout(request)
        return redirect('Login')
    else:
        layout = LlenarLayout(request)
        tipo_usuario = usuario.rol.nombre
        try:
            if tipo_usuario == "Alumno":
                alumno = Alumno.objects.get(id_usuario_id=usuario.id)
                id_alumno = alumno.id
                with connection.cursor() as cursor:
                    cursor.callproc('BuscarProyectos', [id_alumno])
                    proyectos = cursor.fetchall()
            elif tipo_usuario == "Profesor":
                profesor = Profesor.objects.get(id_usuario_id=usuario.id)
                id_profesor = profesor.id
                with connection.cursor() as cursor:
                    cursor.callproc('BuscarProyectoImpartido', [id_profesor])
                    proyectos = cursor.fetchall()
            else:
                return redirect('logout')
        except (Alumno.DoesNotExist, Profesor.DoesNotExist):
            return redirect('logout')
        return render(request, 'pages/Proyectos/ListaProyectos.html', {
            'proyectos': proyectos,
            'usuario' : usuario,
            'layout' : layout,
            'contexto': contexto})
@csrf_protect
@login_required(login_url='Login')
def ListaArchivoProyectos(request):
    layout = LlenarLayout(request)
    usuario = request.user
    contexto = 'archivo'
    tipo_usuario = usuario.rol.nombre
    try:
        if tipo_usuario == "Alumno":
            alumno = Alumno.objects.get(id_usuario_id=usuario.id)
            id_alumno = alumno.id
            with connection.cursor() as cursor:
                cursor.callproc('BuscarProyectosArchivado', [id_alumno])
                proyectos = cursor.fetchall()
        elif tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            id_profesor = profesor.id
            with connection.cursor() as cursor:
                cursor.callproc('BuscarProyectoImpartidoArchivado', [id_profesor])
                proyectos = cursor.fetchall()
        else:
            return redirect('Error', 'Datos no válidos')
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')
    return render(request, 'pages/Proyectos/ListaProyectos.html', {
        'rol': tipo_usuario,
        'proyectos': proyectos,
        'usuario' : usuario,
        'layout' : layout,
        'contexto': contexto})
def generar_codigo_unico():
    while True:
        codigo = random.randint(-999999999, 999999999)
        with connection.cursor() as cursor:
            cursor.callproc('CodigosClase', [])
            codigos_clase = cursor.fetchall()
            codigos_existentes = {codigo_clase[0] for codigo_clase in codigos_clase}
            if codigo not in codigos_existentes:
                return codigo
@csrf_protect
@login_required(login_url='Login')
def crearProyecto(request):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    try:
        if tipo_usuario == "Alumno":
            return redirect('Error', 'sin permisos')
        elif tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            id_profesor = profesor.id
        else:
            return redirect('Error', 'Datos no válidos')
        nombre = request.POST.get('nombre')
        materia = request.POST.get('materia')
        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        ciclo_escolar = request.POST.get('ciclo_escolar')
        color = request.POST.get('color')
        codigo = generar_codigo_unico() 
        with connection.cursor() as cursor:
            cursor.callproc('CrearProyectocoil', [
                id_profesor,
                str(nombre),
                str(materia),
                str(codigo),
                str(descripcion),
                datetime.strptime(fecha_inicio, '%Y-%m-%d').date(),
                datetime.strptime(fecha_fin, '%Y-%m-%d').date(),
                str(ciclo_escolar),
                str(color)
            ])
            resultado = cursor.fetchone()[0]
        if resultado == 'Proyecto creado exitosamente':
            return redirect('IntroduccionCoil', codigo)
        else:
            return redirect('Error', resultado)
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')
def ComprobarCodigoUsuario(request,codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    try:
        if tipo_usuario == "Alumno":
            alumno = Alumno.objects.get(id_usuario_id=usuario.id)
            id_alumno = alumno.id
            with connection.cursor() as cursor:
                cursor.callproc('CodigosClase', [])
                codigos_bd = cursor.fetchall()
                proyecto_existe = False
                for tupla_codigo in codigos_bd:
                    if codigo in tupla_codigo:
                        proyecto_existe = True
                if proyecto_existe:
                    cursor.callproc('ComprobarAlumnoProyecto', [id_alumno, codigo])
                    comprobar = cursor.fetchone()[0]
                    if comprobar != codigo:
                        return 'No inscrito'
                    else:
                        return 'Inscrito'
                if not proyecto_existe:
                    return 'El proyecto de este código no existe'
        elif tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            id_profesor = profesor.id
            with connection.cursor() as cursor:
                cursor.callproc('CodigosClase', [])
                codigos_bd = cursor.fetchall()
                proyecto_existe = False
                for tupla_codigo in codigos_bd:
                    if codigo in tupla_codigo:
                        proyecto_existe = True
                if proyecto_existe:
                    cursor.callproc('ComprobarProfesorProyecto', [id_profesor, codigo])
                    comprobar = cursor.fetchone()[0]
                    if comprobar != codigo:
                        return 'No inscrito'
                    else:
                        return 'Inscrito'
                if not proyecto_existe:
                    return 'El proyecto de este código no existe'
        else:
            return 'Datos no válidos'
    except Exception as e:
        return e
    return 'Algo fallo'
@csrf_protect
@login_required(login_url='Login')
def UnirteProyecto(request):
    codigo = request.POST['codigo']
    terminos = request.POST['terminos']
    comprobacion = ComprobarCodigoUsuario(request,codigo)
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    if comprobacion == 'No inscrito':
        try:
            if tipo_usuario == "Alumno":
                alumno = Alumno.objects.get(id_usuario_id=usuario.id)
                id_alumno = alumno.id
                with connection.cursor() as cursor:
                    with transaction.atomic():
                        cursor.callproc('buscarProyectoPorCodigo', [codigo])
                        proyecto = cursor.fetchone()[0]
                        cursor.callproc('AgregarAlumno', [id_alumno, proyecto])
                        respuesta = cursor.fetchone()[0]
                        if respuesta == 'Agregado exitosamente':
                            return redirect('IntroduccionCoil', codigo)
                        else:
                            return redirect('Error','Error al agregar al proyecto')
            elif tipo_usuario == "Profesor":
                profesor = Profesor.objects.get(id_usuario_id=usuario.id)
                id_profesor = profesor.id
                with connection.cursor() as cursor:
                    cursor.callproc('buscarProyectoPorCodigo', [codigo])
                    proyecto = cursor.fetchone()[0]
                    with transaction.atomic():
                        cursor.callproc('AgregarProfesor', [id_profesor, proyecto])
                        respuesta = cursor.fetchone()[0]
                        if respuesta == 'Agregado exitosamente':
                            return redirect('IntroduccionCoil', codigo)
                        else:
                            return redirect('Error','Error al agregar al proyecto')
            else:
                return redirect('Error', 'Datos no válidos')
        except Exception as e:
            return redirect('Error',e)
    elif comprobacion == 'Inscrito':
        return redirect('FasesCoil', codigo)
    else:
        return redirect('Error', comprobacion)
@csrf_protect
@login_required(login_url='Login')
def AgregarUsuarioProyecto(request,proyecto,codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    try:
        if tipo_usuario == "Alumno":
            alumno = Alumno.objects.get(id_usuario_id=usuario.id)
            id_alumno = alumno.id
            with connection.cursor() as cursor:
                with transaction.atomic():
                        cursor.callproc('AgregarAlumno', [ id_alumno, proyecto])
                        respuesta = cursor.fetchone()[0]
                        if respuesta == 'Agregado exitosamente':
                            return redirect('IntroduccionCoil',codigo)
                        else:
                            return redirect('Error','Error al agregar al proyecto')
        elif tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            id_profesor = profesor.id
            with connection.cursor() as cursor:
                with transaction.atomic():
                        cursor.callproc('AgregarProfesor', [id_profesor, proyecto])
                        respuesta = cursor.fetchone()[0]
                        if respuesta == 'Agregado exitosamente':
                            return redirect('IntroduccionCoil',codigo)
                        else:
                            return redirect('Error','Error al agregar al proyecto')
        else:
            return redirect('Error','Datos no validos')
    except Exception as e:
        return redirect('Error',e)
    return redirect('Error','Algo fallo')
@csrf_protect
@login_required(login_url='Login')
def UnirteProyectoPage(request, codigo):
    layout = LlenarLayout(request)
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comprobacion = ComprobarCodigoUsuario(request,codigo)
    if comprobacion == 'No inscrito':
        try:
            with connection.cursor() as cursor:
                cursor.callproc('buscarProyectoPorCodigo', [codigo])
                proyectoCodigo = cursor.fetchone()[0]
                cursor.callproc('BuscarNombreProyectosByCodigo', [codigo])
                ProyectoNombre = cursor.fetchone()[0]
                return render(request,'pages/Proyectos/EntrarProyecto.html', {
                    'usuario' : usuario,
                    'Proyecto':ProyectoNombre,
                    'proyectoCodigo':proyectoCodigo,
                    'codigo': codigo,
                    'layout' : layout})
        except Exception as e:
            return redirect('Error',e)
    elif comprobacion == 'Inscrito':
        return redirect('FasesCoil', codigo)
    else:
        return redirect('Error', comprobacion)
@csrf_protect
@login_required(login_url='Login')
def IntroduccionCoil(request, codigo):
    layout = LlenarLayout(request)
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comprobacion = ComprobarCodigoUsuario(request,codigo)
    if comprobacion == 'No inscrito':
        return redirect('EntrarProyecto', codigo)
    elif comprobacion == 'Inscrito':
        with connection.cursor() as cursor:
            cursor.callproc('BuscarProyectoByCodigo', [codigo])
            proyectoDetails = cursor.fetchall()
            return render(request,'pages/Proyectos/IntroduccionCoil.html',{
                'enlace_activo': 'coil',
                'proyectoDetails': proyectoDetails,
                'codigo': codigo,
                'usuario' : usuario,
                'layout' : layout})
    else:
        return redirect('Error', comprobacion)
@csrf_protect
@login_required(login_url='Login')
def indexFases(request, codigo):
    layout = LlenarLayout(request)
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comprobacion = ComprobarCodigoUsuario(request,codigo)
    if comprobacion == 'No inscrito':
        return redirect('EntrarProyecto', codigo)
    elif comprobacion == 'Inscrito':
        with connection.cursor() as cursor:
            cursor.callproc('BuscarProyectoByCodigo', [codigo])
            proyectoDetails = cursor.fetchall()
            cursor.callproc('buscarProyectoPorCodigo', [codigo])
            proyectoCodigo = cursor.fetchone()[0]
            cursor.callproc('ListasFasesByProyecto', [proyectoCodigo])
            fases = cursor.fetchall()
            cursor.callproc('BuscarProyectoAlumnos', [proyectoCodigo])
            alumnos = cursor.fetchall()
            return render(request,'pages/FasesCoil/indexFases.html',{
                'enlace_activo': 'tareas',
                'enlace_activo1': 'fases',
                'proyectoDetails': proyectoDetails,
                'codigo': codigo,
                'usuario' : usuario,
                'layout' : layout,
                'fases': fases,
                'alumnos': alumnos})
    else:
        return redirect('Error', comprobacion)
@csrf_protect
@login_required(login_url='Login')
def Fase1(request, codigo, idFase):
    layout = LlenarLayout(request)
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comprobacion = ComprobarCodigoUsuario(request, codigo)
    if comprobacion == 'No inscrito':
        return redirect('EntrarProyecto', codigo)
    elif comprobacion == 'Inscrito':
        try:
            with connection.cursor() as cursor:
                if tipo_usuario == "Alumno":
                    alumno = Alumno.objects.get(id_usuario_id=usuario.id)
                    id_alumno = alumno.id

                    cursor.callproc('obtener_actividades_por_alumno', [idFase, id_alumno])
                    actividades = cursor.fetchall()
                else:
                    cursor.callproc('obtener_actividades_por_fase', [idFase])
                    actividades = cursor.fetchall()

                cursor.callproc('BuscarProyectoByCodigo', [codigo])
                proyectoDetails = cursor.fetchall()

                cursor.callproc('buscarProyectoPorCodigo', [codigo])
                proyectoCodigo = cursor.fetchone()[0]

                cursor.callproc('ListasFasesByProyecto', [proyectoCodigo])
                fases = cursor.fetchall() 

                cursor.callproc('listaMateriales', [idFase])
                materiales = cursor.fetchall()

                
                cursor.callproc('BuscarProyectoAlumnos', [proyectoCodigo])
                alumnos = cursor.fetchall()
            return render(request, 'pages/FasesCoil/fase1.html', {
                'enlace_activo': 'tareas',
                'enlace_activo1': idFase,
                'proyectoDetails': proyectoDetails,
                'codigo': codigo,
                'usuario': usuario,
                'layout': layout,
                'fases': fases,
                'materiales': materiales,
                'actividades': actividades,
                'alumnos': alumnos
            })
        except Exception as e:
            return redirect('Error', str(e))
    else:
        return redirect('Error', comprobacion)
@csrf_protect
@login_required(login_url='Login')
def ListaAlumnosProfesores(request, codigo):
    layout = LlenarLayout(request)
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comprobacion = ComprobarCodigoUsuario(request, codigo)
    
    if comprobacion == 'No inscrito':
        return redirect('EntrarProyecto', codigo)
    elif comprobacion == 'Inscrito':
        with connection.cursor() as cursor:
            # Obtener detalles del proyecto
            cursor.callproc('BuscarProyectoByCodigo', [codigo])
            proyectoDetails = cursor.fetchall()
            
            # Obtener código del proyecto
            cursor.callproc('buscarProyectoPorCodigo', [codigo])
            proyectoCodigo = cursor.fetchone()[0]
            
            # Obtener profesores
            cursor.callproc('BuscarProyectoProfesores', [proyectoCodigo])
            profesores = cursor.fetchall()
            
            # Obtener alumnos
            cursor.callproc('BuscarProyectoAlumnos', [proyectoCodigo])
            alumnos = cursor.fetchall()
            
            return render(request, 'pages/Proyectos/ListaAlumnosProfesores.html', {
                'enlace_activo': 'personas',
                'proyectoDetails': proyectoDetails,
                'codigo': codigo,
                'usuario': usuario,
                'layout': layout,
                'profesores': profesores,
                'alumnos': alumnos
            })
    else:
        return redirect('Error', comprobacion)
@csrf_protect
@login_required(login_url='Login')
def ProyectoDetail(request, codigo):
    layout = LlenarLayout(request)
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comprobacion = ComprobarCodigoUsuario(request,codigo)
    if comprobacion == 'No inscrito':
        return redirect('EntrarProyecto', codigo)
    elif comprobacion == 'Inscrito':
        with connection.cursor() as cursor:
            cursor.callproc('BuscarProyectoByCodigo', [codigo])
            proyectoDetails = cursor.fetchall()
            cursor.callproc('buscarProyectoPorCodigo', [codigo])
            proyectoId = cursor.fetchone()[0]
            cursor.callproc('obtener_anuncios', [proyectoId])
            anuncios = cursor.fetchall()
            archivos_dict = {}
            for anuncio in anuncios:
                cursor.callproc('verArchivosAnuncio', [anuncio[0]])
                archivos = cursor.fetchall()
                archivos_dict[anuncio[0]] = archivos
            archivos_list = [(anuncio_id, archivos) for anuncio_id, archivos in archivos_dict.items()]

            enlaces_dict = {}
            for anuncio in anuncios:
                cursor.callproc('verEnlacesAnuncios', [anuncio[0]])
                enlaces = cursor.fetchall()
                enlaces_dict[anuncio[0]] = enlaces
            enlaces_list = [(anuncio_id, enlaces) for anuncio_id, enlaces in enlaces_dict.items()]
            comentarios_dict = {}
            for anuncio in anuncios:
                cursor.callproc('obtener_comentarios', [anuncio[0]])
                comentarios = cursor.fetchall()
                comentarios_dict[anuncio[0]] = comentarios
            comentarios_list = [(anuncio_id, comentarios) for anuncio_id, comentarios in comentarios_dict.items()]
            return render(request,'pages/Proyectos/ProyectoDetail.html',{
                'enlace_activo': 'tablon',
                'proyectoDetails': proyectoDetails,
                'codigo': codigo,
                'usuario' : usuario,
                'layout' : layout,
                'proyectoId': proyectoId,
                'anuncios': anuncios,
                'comentarios': comentarios_list,
                'enlaces': enlaces_list,
                'archivos':archivos_list})
    else:
        return redirect('Error', comprobacion)
@csrf_protect
@login_required(login_url='Login')
def ListaActividadesPorFases(request):
    return render(request,'pages/Actividades/ListaActividadesPorFases.html',{'enlace_activo': 'tareas'})
@csrf_protect
@login_required(login_url='Login')
def ConfiguracionProyecto(request, codigo):
    layout = LlenarLayout(request)
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comprobacion = ComprobarCodigoUsuario(request,codigo)
    if comprobacion == 'No inscrito':
        return redirect('EntrarProyecto', codigo)
    elif comprobacion == 'Inscrito':
        if tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            id_profesor = profesor.id
            with connection.cursor() as cursor:
                cursor.callproc('BuscarProyectoByCodigo', [codigo])
                proyectoDetails = cursor.fetchall()
                cursor.callproc('buscarProyectoPorCodigo', [codigo])
                proyectoId = cursor.fetchone()[0]
                fecha_inicio = str(proyectoDetails[0][5])
                fecha_fin = str(proyectoDetails[0][6])
                return render(request,'pages/Proyectos/ConfiguracionProyecto.html',{
                    'enlace_activo': 'configurar',
                    'proyectoDetails': proyectoDetails,
                    'codigo': codigo,
                    'usuario' : usuario,
                    'layout' : layout,
                    'fecha_inicio': fecha_inicio,
                    'fecha_fin': fecha_fin,
                    'usuario_id': id_profesor,
                    'proyectoId': proyectoId})
        else:
            return redirect('Error', 'Sin permisos')
    else:
        return redirect('Error', comprobacion)
@csrf_protect
@login_required(login_url='Login')
def SeguimientoActividad(request, codigo):
    layout = LlenarLayout(request)
    usuario = request.user
    comprobacion = ComprobarCodigoUsuario(request, codigo)
    
    if comprobacion == 'No inscrito':
        return redirect('EntrarProyecto', codigo=codigo)
    elif comprobacion == 'Inscrito':
        with connection.cursor() as cursor:
            cursor.callproc('BuscarProyectoByCodigo', [codigo])
            proyectoDetails = cursor.fetchall()
            
            cursor.callproc('buscarProyectoPorCodigo', [codigo])
            proyectoCodigo = cursor.fetchone()[0]
            
            
            cursor.callproc('BuscarProyectoAlumnos', [proyectoCodigo])
            alumnos = cursor.fetchall()
            
            return render(request, 'pages/Actividades/SeguimientoActividad.html', {
                'enlace_activo': 'calificaciones',
                'proyectoDetails': proyectoDetails,
                'codigo': codigo,
                'usuario': usuario,
                'layout': layout,
                'alumnos': alumnos
            })
    else:
        return redirect('Error', mensaje=comprobacion)

@csrf_protect
@login_required(login_url='Login')
def ViAlActividades(request, actividad_id):
    layout = LlenarLayout(request)
    with connection.cursor() as cursor:
        cursor.callproc('obtener_actividad_por_id', [actividad_id])
        resultado = cursor.fetchone()  
        cursor.callproc('verEnlacesActividades', [actividad_id])
        links = cursor.fetchall()

        cursor.callproc('obtener_comentarios_actividades', [actividad_id])
        comentarios = cursor.fetchall()
        if layout[0] == "Profesor":
            cursor.callproc('obtener_comentarios_actividad_profesor', [actividad_id])
            comenPriv = cursor.fetchall()
        elif layout[0] == "Alumno":
            cursor.callproc('obtener_comentarios_actividad_alumno', [actividad_id, layout[8]])
            comenPriv = cursor.fetchall()
    # Obtener los archivos adjuntos relacionados con la actividad
    archivos = SubirArchivos_Actividades.objects.filter(id_actividad=actividad_id)
    return render(request, 'pages/Actividades/ViAlActividades.html', {
        'layout': layout,
        'actividad': resultado,
        'archivos': archivos,
        'mostrar_comentarios': comentarios,
        'mostrar_links': links,
        'comenPriv': comenPriv

    })


@csrf_protect
@login_required(login_url='Login')
def ViAlMateriales(request, material_id):
    layout = LlenarLayout(request)
    
    with connection.cursor() as cursor:
        cursor.callproc('obtener_material_por_id', [material_id])
        resultado = cursor.fetchone()
    
    # Obtener los archivos adjuntos relacionados con el material
    archivos = SubirArchivos_Materiales.objects.filter(id_material=material_id)
    
    # Obtener comentarios y enlaces relacionados con el material
    with connection.cursor() as cursor:
        cursor.callproc('obtener_comentarios_materiales', [material_id])
        comentarios = cursor.fetchall()

        cursor.callproc('enlacesMateriales', [material_id])
        links = cursor.fetchall()
        if layout[0] == "Profesor":
            cursor.callproc('obtener_comentarios_material_profesor', [material_id])
            comenPriv = cursor.fetchall()
        elif layout[0] == "Alumno":
            cursor.callproc('obtener_comentarios_material_alumno', [material_id, layout[8]])
            comenPriv = cursor.fetchall()
    return render(request, 'pages/Materiales/ViAlMateriales.html', {
        'layout': layout,
        'material': resultado,
        'mostrar_comentarios': comentarios,
        'mostrar_links': links,
        'archivos': archivos,
        'comenPriv': comenPriv
    })

@csrf_protect
@login_required(login_url='Login')
def RegistroAlumno(request):
    usuario = request.user

    if usuario.rol.nombre != "Alumno" or usuario.is_firstLogin == False:
        logout(request)
        return redirect('Login')

    if request.method == 'POST':
        form = RegistroAlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.id_usuario_id = usuario
            alumno.save()
            usuario.is_firstLogin = False
            usuario.save()
            messages.success(request, "Alumno registrado correctamente")
            # return redirect('ListaProyectos')  # Redirigir a la vista deseada después del registro
    else:
        form = RegistroAlumnoForm()

    return render(request, 'pages/Registro/FormularioAlumno.html', {'form': form, 'nombre_usuario': usuario.nombre_usuario})
@csrf_protect
@login_required(login_url='Login')
def RegistroProfesor(request):
    usuario = request.user
    
    if usuario.rol.nombre != "Profesor" or usuario.is_firstLogin == False:
        logout(request)
        return redirect('Login')

    if request.method == 'POST':
        form = RegistroProfesorForm(request.POST)
        if form.is_valid():
            profesor = form.save(commit=False)
            profesor.id_usuario_id = usuario
            usuario.is_firstLogin = False
            usuario.save()
            profesor.save()
            messages.success(request, "Profesor registrado correctamente")
            # return redirect('ListaProyectos')  # Redirigir a la vista deseada después del registro
    else:
        form = RegistroProfesorForm()

    return render(request, 'pages/Registro/FormularioProfesor.html', {'form': form, 'nombre_usuario': usuario.nombre_usuario})

@csrf_protect
@login_required(login_url='Login')
def ProfesorDatosPersonales(request):
    usuario = request.user
    if usuario.rol.nombre != "Profesor" or not usuario.is_firstRegister:
        logout(request)
        return redirect('Login')

    profesor = get_object_or_404(Profesor, id_usuario_id=usuario)

    if request.method == 'POST':
        form = RegisterProfesorForm(request.POST, request.FILES, instance=profesor)
        if form.is_valid():
            form.save()
            usuario.is_firstRegister = False
            usuario.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    else:
        form = RegisterProfesorForm(instance=profesor)

    return render(request, 'pages/Registro/DatosProfesor.html', {'form': form, 'profesor_nombre': profesor.nombre})
@csrf_protect
def Registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Guardar datos del formulario en la sesión para usar después
            request.session['registro_form_data'] = {
                'nombre_usuario': form.cleaned_data['nombre_usuario'],
                'correo_institucional': form.cleaned_data['correo_institucional'],
                'password': form.cleaned_data['password'],
                'rol': form.cleaned_data['rol'].id,  # Guardar el ID del rol
            }

            # Generar el código de verificación
            codigo_verificacion = get_random_string(6, allowed_chars='0123456789')

            # Construir la URL de verificación
            verification_url = request.build_absolute_uri(reverse('verify_code'))

            # Enviar el correo de verificación con el enlace
            mensaje = (
                f'Tu código de verificación es: {codigo_verificacion}.\n'
                f'Para verificar tu cuenta, por favor sigue este enlace: {verification_url}'
            )
            send_mail(
                'Código de verificación',
                mensaje,
                'from@example.com',
                [form.cleaned_data['correo_institucional']],
                fail_silently=False,
            )

            # Guardar el código de verificación en la sesión
            request.session['codigo_verificacion'] = codigo_verificacion
            request.session['correo_institucional'] = form.cleaned_data['correo_institucional']

            messages.success(request, "Se envió un código para la verificación del correo. Serás redirigido a una página para verificar tu código.")
            # # Redirigir a la vista de verificación de código
    else:
        form = RegistroForm()

    return render(request, 'pages/Registro/Registro.html', {'form': form})

def verify_code(request):
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            codigo_ingresado = form.cleaned_data['code']
            codigo_correcto = request.session.get('codigo_verificacion')

            if codigo_ingresado == codigo_correcto:
                # Obtener datos de registro del usuario de la sesión
                registro_data = request.session.get('registro_form_data')

                if registro_data:
                    # Obtener el objeto Rol
                    rol_id = registro_data['rol']
                    rol = Rol.objects.get(id=rol_id)

                    # Guardar el usuario en la base de datos con el rol obtenido
                    usuario = Usuario.objects.create_user(
                        nombre_usuario=registro_data['nombre_usuario'],
                        password=registro_data['password'],
                        rol=rol  # Asignar la instancia de Rol obtenida
                    )
                    
                    usuario.correo_institucional = registro_data['correo_institucional']

                    usuario.save()  # Guardar el usuario con el correo institucional

                    # Enviar correo de bienvenida
                    url_sistema = request.build_absolute_uri(reverse('Login'))  # Ajusta 'home' al nombre de tu vista principal
                    mensaje_bienvenida = (
                        f'Bienvenido al sistema, {usuario.nombre_usuario}.\n\n'
                        f'Puedes acceder al sistema utilizando el siguiente enlace: {url_sistema}\n\n'
                        'Gracias por unirte a nosotros.'
                    )
                    send_mail(
                        'Bienvenido al Sistema',
                        mensaje_bienvenida,
                        'from@example.com',
                        [usuario.correo_institucional],
                        fail_silently=False,
                    )

                    messages.success(request, "Código correcto. Usuario registrado correctamente. Serás redirigido a una página para iniciar sesión.")
                    del request.session['registro_form_data']
                    del request.session['codigo_verificacion']
                    del request.session['correo_institucional']

                    #return redirect('Login')  # Redirigir a la página deseada después del registro

            else:
                form.add_error('code', 'Código de verificación incorrecto.')
    else:
        form = VerificationCodeForm()

    return render(request, 'pages/Registro/VerificarCodigo.html', {'form': form})
@csrf_protect
@login_required(login_url='Login')
def save_other_university(request):
    usuario = request.user
    if request.method == 'POST':
        nombre_universidad = request.POST.get('nombre_universidad')
        pais = request.POST.get('pais')

        # Guarda en la base de datos
        nueva_universidad = Catalogo(nombre_universidad=nombre_universidad, pais=pais)
        nueva_universidad.save()
        if usuario.rol.nombre == "Alumno":
            return redirect('registro_alumno')
        elif usuario.rol.nombre == "Profesor":
            return redirect('registro_profesor')

    return render(request, 'pages/Modals/AgregarUniversidad.html')
@csrf_protect
def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data['nombre_usuario']
            password = form.cleaned_data['password']
            usuario = authenticate(request, username=nombre_usuario, password=password)
            if usuario is not None:
                login(request, usuario)
                if usuario.rol.nombre == "Alumno":
                    if usuario.is_firstLogin == True:
                        return redirect('registro_alumno')
                    else:
                        return redirect('ListaProyectos')       
                elif usuario.rol.nombre == "Profesor":
                        if usuario.is_firstLogin == True:
                            return redirect('registro_profesor')
                        elif usuario.is_firstRegister == True:
                            return redirect('ProfesorDatosPersonales')
                        else:
                            return redirect('ListaProyectos')
            
                    
                
            else:
                print(f"Autenticación fallida para: {nombre_usuario}")
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos')
        else:
            print("Formulario no es válido")
    else:
        form = LoginForm()
    return render(request, 'pages/Login/Login.html', {'form': form})
@csrf_protect
@login_required(login_url='Login')
def Home(request):
    usuario = request.user  # Obtener el usuario autenticado
    nombre_completo = None
    tipo_usuario = usuario.rol.nombre
    id_user = usuario.id
    if usuario.rol.nombre == "Alumno":
        
        alumno = Alumno.objects.get(id_usuario_id=usuario.id)
        nombre_completo = f"{alumno.nombre} {alumno.apellidos}"
    elif usuario.rol.nombre == "Profesor":
        profesor = Profesor.objects.get(id_usuario_id=usuario.id)
        nombre_completo = f"{profesor.nombre} {profesor.apellidos}"
            
    
    return render(request, 'pages/Home/Home.html', {'nombre_completo': nombre_completo, 'tipo_usuario': tipo_usuario, 'id_user': id_user})

def logout_view(request):
    logout(request)
    return redirect('Login')

class CustomPasswordResetView(FormView):
    template_name = 'registration/password_reset_form.html'
    form_class = EmailForm
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        
        usuario = Usuario.objects.filter(correo_institucional=email).first()
        
        if usuario:
            self.send_password_reset_email(usuario)
            return super().form_valid(form)
        else:
            form.add_error('email', 'Correo no encontrado.')
            return self.form_invalid(form)

    def send_password_reset_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        url = reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        reset_link = f"{self.request.scheme}://{self.request.get_host()}{url}"
        
        subject = 'Restablece tu contraseña'
        message = render_to_string('registration/password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })
        send_mail(subject, message, 'tu_correo@example.com', [user.correo_institucional])

def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': Usuario.objects.filter(nombre_usuario__iexact=username).exists()
    }
    return JsonResponse(data)

@csrf_protect
def validate_credentials(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user_exists = Usuario.objects.filter(nombre_usuario__iexact=username).exists()
        user = authenticate(request, username=username, password=password)
        credentials_valid = user is not None
        return JsonResponse({
            'user_exists': user_exists,
            'credentials_valid': credentials_valid
        })


@csrf_protect
@login_required(login_url='Login')
def EditDatosProfesor(request, codigo):
    usuario = request.user
    layout = LlenarLayout(request)
    comprobacion = ComprobarCodigoUsuario(request, codigo)
    
    if comprobacion == 'No inscrito':
        return redirect('EntrarProyecto', codigo)
    elif comprobacion == 'Inscrito':
        if usuario.rol.nombre == "Alumno":
            alumno = get_object_or_404(Alumno, id_usuario_id=usuario.id)
            with connection.cursor() as cursor:
                cursor.callproc('BuscarProyectoByCodigo', [codigo])
                proyectoDetails = cursor.fetchall()
                cursor.callproc('buscarProyectoPorCodigo', [codigo])
                proyectoCodigo = cursor.fetchone()[0]
                cursor.callproc('BuscarProyectoProfesores', [proyectoCodigo])
                profesores = cursor.fetchall()
            context = {
                'profesores': profesores,
                'codigo': codigo,
                'layout': layout,
                'enlace_activo': 'active',
                'proyectoDetails': proyectoDetails,
            }
            return render(request, 'pages/Proyectos/ProfesoresProyecto.html', context)
        else:
            profesor = get_object_or_404(Profesor, id_usuario_id=usuario.id)

            if request.method == 'POST':
                form = UpdateProfesorForm(request.POST, request.FILES, instance=profesor)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Datos actualizados correctamente")
                    return redirect('EditDatosProfesor', codigo)
            else:
                form = UpdateProfesorForm(instance=profesor)
            
            with connection.cursor() as cursor:
                cursor.callproc('BuscarProyectoByCodigo', [codigo])
                proyectoDetails = cursor.fetchall()
            
            context = {
                'form': form,
                'profesor': profesor,
                'codigo': codigo,
                'enlace_activo': 'active',
                'layout': layout,
                'proyectoDetails': proyectoDetails
            }
            return render(request, 'pages/Proyectos/EditDatosProfesor.html', context)
    else:
        return redirect('Error', comprobacion)

@csrf_protect
def Error(request,error):
    layout = LlenarLayout(request)
    return render(request, 'pages/error.html',{'error':error,'layout':layout})
@csrf_protect
@login_required(login_url='Login')
def editarProyecto(request,proyecto,codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    try:
        if tipo_usuario == "Alumno":
            return redirect('Error', 'sin permisos')
        elif tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
        else:
            return redirect('Error', 'Datos no válidos')
        nombre = request.POST.get('nombre')
        materia = request.POST.get('materia')
        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        ciclo_escolar = request.POST.get('ciclo_escolar')
        color = request.POST.get('color')
        with connection.cursor() as cursor:
            cursor.callproc('EditarProyecto', [
                proyecto,
                str(nombre),
                str(materia),
                str(descripcion),
                datetime.strptime(fecha_inicio, '%Y-%m-%d').date(),
                datetime.strptime(fecha_fin, '%Y-%m-%d').date(),
                str(ciclo_escolar),
                str(color)
            ])
            resultado = cursor.fetchone()[0]
        if resultado == 'Agregado exitosamente':
            return redirect('ConfiguracionProyecto', codigo)
        else:
            return redirect('Error', resultado)
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')
@csrf_protect
@login_required(login_url='Login')
def zoomProyecto(request,proyecto,codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    try:
        if tipo_usuario == "Alumno":
            return redirect('Error', 'sin permisos')
        elif tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
        else:
            return redirect('Error', 'Datos no válidos')
        zoom = request.POST.get('zoom')
        with connection.cursor() as cursor:
            cursor.callproc('ZoomProyecto', [
                proyecto,
                str(zoom)
            ])
            resultado = cursor.fetchone()[0]
        if resultado == 'Agregado exitosamente':
            return redirect('ConfiguracionProyecto', codigo)
        else:
            return redirect('Error', resultado)
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')
@csrf_protect
@login_required(login_url='Login')
def ArchivarProyecto(request,proyecto,codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    try:
        if tipo_usuario == "Alumno":
            return redirect('Error', 'sin permisos')
        elif tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
        else:
            return redirect('Error', 'Datos no válidos')
        with connection.cursor() as cursor:
            cursor.callproc('ArchivoProyecto', [
                proyecto
            ])
            resultado = cursor.fetchone()[0]
        if resultado == 'Agregado exitosamente':
            return redirect('ConfiguracionProyecto', codigo)
        else:
            return redirect('Error', resultado)
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')
@csrf_protect
@login_required(login_url='Login')
def ReactivarProyecto(request,proyecto,codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    try:
        if tipo_usuario == "Alumno":
            return redirect('Error', 'sin permisos')
        elif tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
        else:
            return redirect('Error', 'Datos no válidos')
        with connection.cursor() as cursor:
            cursor.callproc('ReactivarProyecto', [
                proyecto
            ])
            resultado = cursor.fetchone()[0]
        if resultado == 'Agregado exitosamente':
            return redirect('ConfiguracionProyecto', codigo)
        else:
            return redirect('Error', resultado)
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')
@csrf_protect
@login_required(login_url='Login')
def PublicarComentario(request, proyecto, codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comentario = request.POST.get('comentario')
    titulos = request.POST.getlist('linkname')
    paths = request.POST.getlist('link')
    combinados = zip(titulos, paths)
    try:
        if tipo_usuario == "Alumno":
            alumno = Alumno.objects.get(id_usuario_id=usuario.id)
            id_alumno = alumno.id
            with connection.cursor() as cursor:
                cursor.callproc('AnuncioAlumno', [
                    str(comentario),
                    id_alumno,
                    proyecto
                ])
                anucio_id = cursor.fetchone()[0]
                if anucio_id != 'Error no se publico el anuncio' :
                    if titulos:
                        for titulo, path in combinados:
                            cursor.callproc('enlacesAnuncio', [
                                str(titulo),
                                str(path),
                                anucio_id
                            ])
                    if request.method == 'POST':
                        if 'files' in request.FILES:
                            files = request.FILES.getlist('files')
                            for uploaded_file in files:
                                # Guardar cada archivo en el modelo
                                anuncio_archivo = Anuncios_archivos(
                                    path=uploaded_file,
                                    fecha=datetime.now().date(),
                                    id_anuncio_id=anucio_id
                                )
                                anuncio_archivo.save()
                            print('Archivo subido correctamente')
                    return redirect('ProyectoDetail', codigo)
                else:
                    return redirect('Error', anucio_id)
        elif tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            id_profesor = profesor.id
            with connection.cursor() as cursor:
                cursor.callproc('AnuncioProfesor', [
                    str(comentario),
                    id_profesor,
                    proyecto
                ])
                anucio_id = cursor.fetchone()[0]
                if anucio_id != 'Error no se publico el anuncio' :
                    if titulos:
                        for titulo, path in combinados:
                            cursor.callproc('enlacesAnuncio', [
                                str(titulo),
                                str(path),
                                anucio_id
                            ])
                    if request.method == 'POST':
                        if 'files' in request.FILES:
                            files = request.FILES.getlist('files')
                            for uploaded_file in files:
                                # Guardar cada archivo en el modelo
                                anuncio_archivo = Anuncios_archivos(
                                    path=uploaded_file,
                                    fecha=datetime.now().date(),
                                    id_anuncio_id=anucio_id
                                )
                                anuncio_archivo.save()
                            print('Archivo subido correctamente')
                    return redirect('ProyectoDetail', codigo)
                else:
                    return redirect('Error', anucio_id)
        else:
            return redirect('Error', 'Datos no válidos')
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')
@csrf_protect
@login_required(login_url='Login')
def ComentarPublicacion(request, publicacion, codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comentario = request.POST.get('comentar')
    try:
        if tipo_usuario == "Alumno":
            alumno = Alumno.objects.get(id_usuario_id=usuario.id)
            id_alumno = alumno.id
            with connection.cursor() as cursor:
                cursor.callproc('ComentarAnuncioAlumno', [
                    str(comentario),
                    id_alumno,
                    publicacion
                ])
                resultado = cursor.fetchone()[0]
            if resultado == 'Agregado exitosamente':
                return redirect('ProyectoDetail', codigo)
            else:
                return redirect('Error', resultado)
        elif tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            id_profesor = profesor.id
            with connection.cursor() as cursor:
                cursor.callproc('ComentarAnuncioProfesor', [
                    str(comentario),
                    id_profesor,
                    publicacion
                ])
                resultado = cursor.fetchone()[0]
            if resultado == 'Agregado exitosamente':
                return redirect('ProyectoDetail', codigo)
            else:
                return redirect('Error', resultado)
        else:
            return redirect('Error', 'Datos no válidos')
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')
@csrf_protect
@login_required(login_url='Login')
def eliminarComentario(request,id_coment, codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    try:
        if tipo_usuario == 'Alumno':
            alumno = Alumno.objects.get(id_usuario_id=usuario.id)
            id_alumno = alumno.id
            with connection.cursor() as cursor:
                cursor.callproc('BuscarAlumnoComentariobyID', [id_coment])
                r = cursor.fetchone()[0]
                if id_alumno == r:
                    cursor.callproc('EliminarComentario', [id_coment])
                    resultado = cursor.fetchone()[0]
                    if resultado == 'Eliminar exitosamente':
                        return redirect('ProyectoDetail', codigo)
                    else:
                        return redirect('Error', resultado)
                else:
                    return redirect('Error', 'Tu usuario no coincide con el comentario')
        elif tipo_usuario == 'Profesor':
            with connection.cursor() as cursor:
                cursor.callproc('EliminarComentario', [id_coment])
                resultado = cursor.fetchone()[0]
                if resultado == 'Eliminar exitosamente':
                    return redirect('ProyectoDetail', codigo)
                else:
                    return redirect('Error', resultado)
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')
@csrf_protect
@login_required(login_url='Login')
def editarComentario(request,id_coment, codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comentario = request.POST.get('comentariopost')
    try:
        if tipo_usuario == 'Alumno':
            alumno = Alumno.objects.get(id_usuario_id=usuario.id)
            id_alumno = alumno.id
            with connection.cursor() as cursor:
                cursor.callproc('BuscarAlumnoComentariobyID', [id_coment])
                r = cursor.fetchone()[0]
                if id_alumno == r:
                    cursor.callproc('EditarComentario', [id_coment, str(comentario)])
                    resultado = cursor.fetchone()[0]
                    if resultado == 'Editado exitosamente':
                        return redirect('ProyectoDetail', codigo)
                    else:
                        return redirect('Error', resultado)
                else:
                    return redirect('Error', 'Tu usuario no coincide con el comentario')
        elif tipo_usuario == 'Profesor':
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            id_profesor = profesor.id
            with connection.cursor() as cursor:
                cursor.callproc('BuscarProfesorComentariobyID', [id_coment])
                r = cursor.fetchone()[0]
                if id_profesor == r:
                    cursor.callproc('EditarComentario', [id_coment, str(comentario)])
                    resultado = cursor.fetchone()[0]
                    if resultado == 'Editado exitosamente':
                        return redirect('ProyectoDetail', codigo)
                    else:
                        return redirect('Error', resultado)
                else:
                    return redirect('Error', 'Tu usuario no coincide con el comentario')
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')

#MATEO - PARTES 
@csrf_protect
def obtener_material_por_id(material_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM obtener_material_por_id(%s)", [material_id])
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in result]
    
@csrf_protect
@login_required(login_url='Login')
def AgregarMaterial(request):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    if request.method == 'POST':
        tema = request.POST.get('Tema')
        descripcion = request.POST.get('descripcion')
        titulos = request.POST.getlist('linkname')
        paths = request.POST.getlist('link')
        fases = request.POST.get('fase_publicacion_material')
        fecha = datetime.now().date()
        combinados = zip(titulos, paths)

        if tipo_usuario == "Alumno":
            messages.error(request, "Error: Los alumnos no pueden agregar material.")
            return redirect('Error', 'Error al intentar')

        try:
            if tipo_usuario == "Profesor":
                profesor = Profesor.objects.get(id_usuario_id=usuario.id)
                id_profesor = profesor.id

                with transaction.atomic():
                    with connection.cursor() as cursor:
                        cursor.callproc('insertarMaterial', [
                            str(tema),
                            str(descripcion),
                            fecha,
                            int(fases),
                            id_profesor
                        ])
                        resultado = cursor.fetchone()[0]

                        if resultado != 'Error no se publico el anuncio':
                            if titulos:
                                for titulo, path in combinados:
                                    cursor.callproc('EnlacesMaterial', [
                                        str(titulo),
                                        str(path),
                                        resultado
                                    ])

                            # Procesar archivos subidos
                            if 'files' in request.FILES:
                                files = request.FILES.getlist('files')
                                for uploaded_file in files:
                                    archivo = SubirArchivos_Materiales(
                                        path=uploaded_file,
                                        fecha=datetime.now().date(),
                                        id_material_id=resultado
                                    )
                                    archivo.save()

                            messages.success(request, "Material agregado correctamente.")
                            return redirect('ViAlMateriales', material_id=resultado)
                        else:
                            messages.error(request, "Error: No se pudo publicar el anuncio.")
                            return redirect('Error', 'Error al intentar')
            else:
                messages.error(request, "Error: Tipo de usuario no permitido.")
                return redirect('Error', 'Error desconocido')
        except Profesor.DoesNotExist:
            messages.error(request, "Error: Profesor no encontrado.")
            return redirect('Error', 'Error al intentar')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('Error', str(e))

    return render(request, 'pages/Materiales/AgregarMaterial.html')
######################################################################
#COMENTARIOS
@csrf_protect
@login_required(login_url='Login')
def MaterialComentarios(request, id_material):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comentario = request.POST.get('comentar')
    try:
        if tipo_usuario == "Alumno":
            alumno = Alumno.objects.get(id_usuario_id=usuario.id)
            id_alumno = alumno.id
            with connection.cursor() as cursor:
                cursor.callproc('Material_Comentario_Alumno', [
                    str(comentario),
                    id_alumno,
                    id_material
                ])
                resultado = cursor.fetchone()[0]
            if resultado == 'Agregado exitosamente':
                return redirect('ViAlMateriales', id_material)
            else:
                return redirect('Error', resultado)
        elif tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            id_profesor = profesor.id
            with connection.cursor() as cursor:
                cursor.callproc('Material_Comentario', [
                    str(comentario),
                    id_profesor,
                    id_material
                ])
                resultado = cursor.fetchone()[0]
            if resultado == 'Agregado exitosamente':
                return redirect('ViAlMateriales', id_material)
            else:
                return redirect('Error', resultado)
        else:
            return redirect('Error', 'Datos no válidos')
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')
    
@csrf_protect    
@login_required(login_url='Login')
def eliminarAnuncio(request,id_anuncio, codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    try:
        if tipo_usuario == 'Alumno':
            alumno = Alumno.objects.get(id_usuario_id=usuario.id)
            id_alumno = alumno.id
            with connection.cursor() as cursor:
                cursor.callproc('BuscarAlumnoComentariobyID', [id_anuncio])
                r = cursor.fetchone()[0]
                if id_alumno == r:
                    cursor.callproc('EliminarAnuncio', [id_anuncio])
                    resultado = cursor.fetchone()[0]
                    if resultado == 'Eliminado exitosamente':
                        return redirect('ProyectoDetail', codigo)
                    else:
                        return redirect('Error', resultado)
                else:
                    return redirect('Error', 'Tu usuario no coincide con el comentario')
        elif tipo_usuario == 'Profesor':
            with connection.cursor() as cursor:
                cursor.callproc('EliminarAnuncio', [id_anuncio])
                resultado = cursor.fetchone()[0]
                if resultado == 'Eliminado exitosamente':
                    return redirect('ProyectoDetail', codigo)
                else:
                    return redirect('Error', resultado)
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')
    

#APARTADO DE ACTIVIDADES 
    #AGREGAR UNA NUEVA ACTIVIDAD
@csrf_protect
@login_required(login_url='Login')
def AgregarActividad(request):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fase_id = request.POST.get('fase_publicacion_actividad')
        titulos = request.POST.getlist('linkname')
        paths = request.POST.getlist('link')
        fecha = datetime.now().date()
        combinados = zip(titulos, paths)
        alumnos = request.POST.getlist('alumnos')

        if tipo_usuario == "Alumno":
            return redirect('Error', 'Error al intentar')
        elif tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            id_profesor = profesor.id
            try:
                with transaction.atomic():
                    with connection.cursor() as cursor:
                        cursor.callproc('insertarActividad', [
                            str(titulo),
                            str(descripcion),
                            fecha,
                            int(fase_id),
                            id_profesor
                        ])
                        resultado = cursor.fetchone()[0]  # ID de la actividad creada

                        # Insertar enlaces si existen
                        if titulos:
                            for titulo, path in combinados:
                                cursor.callproc('Actividades_enlaces', [
                                    str(titulo),
                                    str(path),
                                    resultado
                                ])

                        # Procesar archivos subidos
                        if 'files' in request.FILES:
                            files = request.FILES.getlist('files')
                            for uploaded_file in files:
                                archivo = SubirArchivos_Actividades(
                                    path=uploaded_file,
                                    fecha=datetime.now().date(),
                                    id_actividad_id=resultado
                                )
                                archivo.save()
                        
                        #*Asignar actividades
                        for alumno in alumnos:
                            cursor.callproc('asignarActividad', [alumno, resultado])

                        
                    return redirect('ViAlActividades', resultado)
            except Profesor.DoesNotExist:
                return redirect('Error', 'Profesor no encontrado')
            except Exception as e:
                return redirect('Error', str(e))
        else:
            return redirect('Error', 'Error desconocido')

    return render(request, 'pages/Actividades/AgregarActividad.html')
##############################################################

#COMENTARIOS
@csrf_protect
@login_required(login_url='Login')
def ActividadComentarios(request, id_actividad):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comentario = request.POST.get('comentar')
    try:
        if tipo_usuario == "Alumno":
            alumno = Alumno.objects.get(id_usuario_id=usuario.id)
            id_alumno = alumno.id
            with connection.cursor() as cursor:
                cursor.callproc('Actividad_Comentario_Alumno', [
                    str(comentario),
                    id_alumno,
                    id_actividad
                ])
                resultado = cursor.fetchone()[0]
            if resultado == 'Agregado exitosamente':
                return redirect('ViAlActividades', id_actividad)
            else:
                return redirect('Error', resultado)
        elif tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            id_profesor = profesor.id
            with connection.cursor() as cursor:
                cursor.callproc('Actividad_Comentario', [
                    str(comentario),
                    id_profesor,
                    id_actividad
                ])
                resultado = cursor.fetchone()[0]
            if resultado == 'Agregado exitosamente':
                return redirect('ViAlActividades', id_actividad)
            else:
                return redirect('Error', resultado)
        else:
            return redirect('Error', 'Datos no válidos')
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')

##############################################################
#!Comentarios priv ACTIVIDAD
@login_required(login_url='Login')
def comentarioPrivActividad(request, id_actividad, id_alumno):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comentario = request.POST.get('comentPriv')

    if not comentario:
        return redirect('Error', 'El comentario no puede estar vacío.')

    try:
        if tipo_usuario == 'Alumno':
            alumno = Alumno.objects.get(id_usuario_id=usuario.id)
            id_alumno_log = alumno.id
            procedimiento = 'ComentarActividadPrivAlumno'
            parametros = [str(comentario), id_actividad,id_alumno_log]
        elif tipo_usuario == 'Profesor':
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            id_profesor = profesor.id
            procedimiento = 'ComentarActividadPrivProfesor'
            parametros = [str(comentario), id_profesor, id_actividad, id_alumno]
        else:
            return redirect('Error', 'Tipo de usuario no válido.')

        with connection.cursor() as cursor:
            cursor.callproc(procedimiento, parametros)
            resultado = cursor.fetchone()[0]

            if resultado == 'Agregado exitosamente':
                return redirect('ViAlActividades', id_actividad)
            else:
                return redirect('Error', resultado)

    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')

    except Exception as e:
        return redirect('Error', str(e))

##############################################################
@login_required(login_url='Login')
def invitarProyecto(request, codigo):
    correos = request.POST.getlist('correos')
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    url_proyecto = request.build_absolute_uri(reverse('EntrarProyecto', args=[codigo]))
    url_sistema = request.build_absolute_uri(reverse('Login'))
    try:
        if tipo_usuario == "Alumno":
            return redirect('Error', 'Tu usuario no puede realizar esto')
        elif tipo_usuario == "Profesor":
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            nombre= profesor.nombre
            with connection.cursor() as cursor:
                cursor.callproc('BuscarProyectoByCodigo', [codigo])
                proyectoDetails = cursor.fetchone()
                for email in correos:
                    cursor.callproc('obteneroCorreoUsuario', [email])
                    correoYUsuario = cursor.fetchone()
                    if correoYUsuario:
                        #Correo
                        mensaje_invitacion = (
                        f'Hola, {correoYUsuario[1]}.\n\n'
                        f'El profesor(a) {nombre}, te invitó a unirte al Proyecto COIL {proyectoDetails[1]}\n'
                        f'Puedes acceder al proyecto utilizando el siguiente enlace: {url_proyecto}\n'
                        f'Tambien puede utilizar el codigo: {codigo}.'
                        )
                    else:
                        mensaje_invitacion = (
                        f'Hola, te han invitado a unirte al Proyecto COIL {proyectoDetails[1]}\n\n'
                        f'Al parcer no tienes una cuenta utiliza este enlace para registrarte: {url_sistema}\n'
                        f'Puedes acceder al proyecto utilizando el siguiente enlace: {url_proyecto}\n'
                        f'Tambien puede utilizar el codigo: {codigo}.'
                        )
                    send_mail(
                        'Nueva invitacion a un proyecto',
                        mensaje_invitacion,
                        'from@example.com',
                        [email],
                        fail_silently=False,
                    )
                    
            return redirect('ListaAlumnosProfesores', codigo)
        else:
            return redirect('Error', 'Datos no válidos')
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
            return redirect('logout')
    
@login_required(login_url='Login')
def expulsarAlumno(request, id_alumno, codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    try:
        if tipo_usuario == 'Alumno':
            return redirect('Error', 'No tienes permisos parar realizar esto')
        elif tipo_usuario == 'Profesor':
            with connection.cursor() as cursor:
                cursor.callproc('buscarProyectoPorCodigo', [codigo])
                proyectoid = cursor.fetchone()[0]
                cursor.callproc('EliminarAlumnoDelProyecto', [id_alumno, proyectoid])
                resultado = cursor.fetchone()[0]
                if resultado == 'Eliminado exitosamente':
                    return redirect('ListaAlumnosProfesores', codigo)
                else:
                    return redirect('Error', resultado)
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')
    
@login_required(login_url='Login')
def expulsarProfesor(request, id_profesor, codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    try:
        if tipo_usuario == 'Alumno':
            return redirect('Error', 'No tienes permisos parar realizar esto')
        elif tipo_usuario == 'Profesor':
            with connection.cursor() as cursor:
                cursor.callproc('buscarProyectoPorCodigo', [codigo])
                proyectoid = cursor.fetchone()[0]
                cursor.callproc('EliminarProfesorDelProyecto', [id_profesor, proyectoid])
                resultado = cursor.fetchone()[0]
                if resultado == 'Eliminado exitosamente':
                    return redirect('ListaAlumnosProfesores', codigo)
                else:
                    return redirect('Error', resultado)
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')
    
@login_required(login_url='Login')
def adminProyecto(request, id_profesor, codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    try:
        if tipo_usuario == 'Alumno':
            return redirect('Error', 'No tienes permisos parar realizar esto')
        elif tipo_usuario == 'Profesor':
            with connection.cursor() as cursor:
                cursor.callproc('buscarProyectoPorCodigo', [codigo])
                proyectoid = cursor.fetchone()[0]
                cursor.callproc('superAdminDelProyecto', [id_profesor, proyectoid])
                resultado = cursor.fetchone()[0]
                if resultado == 'Actulizado exitosamente':
                    return redirect('ListaAlumnosProfesores', codigo)
                else:
                    return redirect('Error', resultado)
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')
    
@login_required(login_url='Login')
def editarPost(request,id_anuncio, codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comentario = request.POST.get('editPost')
    titulos = request.POST.getlist('linkname')
    paths = request.POST.getlist('link')
    editLinkID = request.POST.getlist('editedId')
    editLinkTitle = request.POST.getlist('editedTitleLink')
    editLinkPath = request.POST.getlist('editedLink')
    deleteLink = request.POST.getlist('deletedLink')
    deleteFiles = request.POST.getlist('deleted_files')
    editLinks = zip(editLinkID, editLinkTitle,editLinkPath)
    combinados = zip(titulos, paths)
    try:
        if tipo_usuario == 'Alumno':
            alumno = Alumno.objects.get(id_usuario_id=usuario.id)
            id_alumno = alumno.id
            with connection.cursor() as cursor:
                cursor.callproc('buscarAlumnoPostbyId', [id_anuncio])
                r = cursor.fetchone()[0]
                if id_alumno == r:
                    cursor.callproc('EditarAnuncio', [id_anuncio, str(comentario)])
                    resultado = cursor.fetchone()[0]
                    if editLinks:
                        for editLinkID, editLinkTitle,editLinkPath in editLinks:
                            cursor.callproc('EditarEnlacesPost', [
                                int(editLinkID),
                                str(editLinkPath),
                                str(editLinkTitle)
                            ])
                    if deleteLink:
                        for deletelink in deleteLink:
                            cursor.callproc('EliminarEnlacesPost', [int(deletelink)])
                    if deleteFiles:
                        for deleteFile in deleteFiles:
                            cursor.callproc('EliminarArchivosPost', [int(deleteFile)])
                    if titulos:
                        for titulo, path in combinados:
                            cursor.callproc('enlacesAnuncio', [
                                str(titulo),
                                str(path),
                                id_anuncio
                            ])
                    if 'files' in request.FILES:
                        files = request.FILES.getlist('files')
                        for uploaded_file in files:
                            # Guardar cada archivo en el modelo
                            anuncio_archivo = Anuncios_archivos(
                                path=uploaded_file,
                                fecha=datetime.now().date(),
                                id_anuncio_id=id_anuncio
                            )
                            anuncio_archivo.save()
                    if resultado == 'Editado exitosamente':
                        return redirect('ProyectoDetail', codigo)
                    else:
                        return redirect('Error', resultado)
                else:
                    return redirect('Error', 'Tu usuario no coincide con el comentario')
        elif tipo_usuario == 'Profesor':
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            id_profesor = profesor.id
            with connection.cursor() as cursor:
                cursor.callproc('buscarProfesorPostbyId', [id_anuncio])
                r = cursor.fetchone()[0]
                if id_profesor == r:
                    cursor.callproc('EditarAnuncio', [id_anuncio, str(comentario)])
                    resultado = cursor.fetchone()[0]
                    if editLinks:
                        for editLinkID, editLinkTitle,editLinkPath in editLinks:
                            cursor.callproc('EditarEnlacesPost', [
                                int(editLinkID),
                                str(editLinkPath),
                                str(editLinkTitle)
                            ])
                    if deleteLink:
                        for deletelink in deleteLink:
                            cursor.callproc('EliminarEnlacesPost', [int(deletelink)])
                    if deleteFiles:
                        for deleteFile in deleteFiles:
                            cursor.callproc('EliminarArchivosPost', [int(deleteFile)])
                    if titulos:
                        for titulo, path in combinados:
                            cursor.callproc('enlacesAnuncio', [
                                str(titulo),
                                str(path),
                                id_anuncio
                            ])
                    if 'files' in request.FILES:
                        files = request.FILES.getlist('files')
                        for uploaded_file in files:
                            # Guardar cada archivo en el modelo
                            anuncio_archivo = Anuncios_archivos(
                                path=uploaded_file,
                                fecha=datetime.now().date(),
                                id_anuncio_id=id_anuncio
                            )
                            anuncio_archivo.save()
                    if resultado == 'Editado exitosamente':
                        return redirect('ProyectoDetail', codigo)
                    else:
                        return redirect('Error', resultado)
                else:
                    return redirect('Error', 'Tu usuario no coincide con el comentario')
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')
    
@login_required(login_url='Login')
def editarPostVista(request,id_anuncio, codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    layout = LlenarLayout(request)
    try:
        if tipo_usuario == 'Alumno':
            alumno = Alumno.objects.get(id_usuario_id=usuario.id)
            id_alumno = alumno.id
            with connection.cursor() as cursor:
                cursor.callproc('buscarAlumnoPostbyId', [id_anuncio])
                r = cursor.fetchone()[0]
                if id_alumno == r:
                    cursor.callproc('buscarPostbyId', [id_anuncio])
                    anuncio = cursor.fetchall()
                    cursor.callproc('verArchivosAnuncio', [id_anuncio])
                    archivos = cursor.fetchall()
                    cursor.callproc('verEnlacesAnuncios', [id_anuncio])
                    enlaces = cursor.fetchall()
                    return render(request, 'pages/ForoProyecto/EditarAnuncio.html',{
                        'layout': layout,
                        'anuncio': anuncio[0],
                        'archivos': archivos,
                        'enlaces': enlaces,
                        'codigo': codigo
                    })
                else:
                    return redirect('Error', 'Tu usuario no coincide con el comentario')
        elif tipo_usuario == 'Profesor':
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            id_profesor = profesor.id
            with connection.cursor() as cursor:
                cursor.callproc('buscarProfesorPostbyId', [id_anuncio])
                r = cursor.fetchone()[0]
                if id_profesor == r:
                    cursor.callproc('buscarPostbyId', [id_anuncio])
                    anuncio = cursor.fetchall()
                    cursor.callproc('verArchivosAnuncio', [id_anuncio])
                    archivos = cursor.fetchall()
                    cursor.callproc('verEnlacesAnuncios', [id_anuncio])
                    enlaces = cursor.fetchall()
                    return render(request, 'pages/ForoProyecto/EditarAnuncio.html',{
                        'layout': layout,
                        'anuncio': anuncio[0],
                        'archivos': archivos,
                        'enlaces': enlaces,
                        'codigo': codigo
                    })
                else:
                    return redirect('Error', 'Tu usuario no coincide con el comentario')
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')
    
#!Comentarios priv
@login_required(login_url='Login')
def comentarioPrivMaterial(request, id_material, id_alumno):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    comentario = request.POST.get('comentPriv')

    if not comentario:
        return redirect('Error', 'El comentario no puede estar vacío.')

    try:
        if tipo_usuario == 'Alumno':
            alumno = Alumno.objects.get(id_usuario_id=usuario.id)
            id_alumno_log = alumno.id
            procedimiento = 'ComentarMaterialPrivAlumno'
            parametros = [str(comentario), id_alumno_log, id_material]
        elif tipo_usuario == 'Profesor':
            profesor = Profesor.objects.get(id_usuario_id=usuario.id)
            id_profesor = profesor.id
            procedimiento = 'ComentarMaterialPrivProfesor'
            parametros = [str(comentario), id_profesor, id_material, id_alumno]
        else:
            return redirect('Error', 'Tipo de usuario no válido.')

        with connection.cursor() as cursor:
            cursor.callproc(procedimiento, parametros)
            resultado = cursor.fetchone()[0]

            if resultado == 'Agregado exitosamente':
                return redirect('ViAlMateriales', id_material)
            else:
                return redirect('Error', resultado)

    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')

    except Exception as e:
        return redirect('Error', str(e))

@login_required(login_url='Login')
def subirActividad(request, id_actividad_parm):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    if tipo_usuario == 'Alumno':
        alumno = Alumno.objects.get(id_usuario_id=usuario.id)
        id_alumno_log = alumno.id
        if 'files' in request.FILES:
            files = request.FILES.getlist('files')
            for uploaded_file in files:
                # Guardar cada archivo en el modelo
                entregas_actividades = Entregas_Actividades(
                    path=uploaded_file,
                    fecha=datetime.now().date(),
                    id_actividad_id=id_actividad_parm,
                    id_alumno_id = id_alumno_log
                )
                entregas_actividades.save()
            with connection.cursor() as cursor:
                cursor.callproc('entregarActividad', [id_alumno_log, id_actividad_parm])
    return redirect('ViAlActividades', id_actividad_parm)

###########################}
#SEGUMINETO DE LAS ACTIVIDADES DEL ALUMNO
@csrf_protect
@login_required(login_url='Login')
def SeguimientoAct(request,codigo,id_alumno):
    layout = LlenarLayout(request)
    comprobacion = ComprobarCodigoUsuario(request,codigo)
    alumno = Alumno.objects.filter(id=id_alumno).values('nombre', 'apellidos').first()
    if comprobacion == 'No inscrito':
        return redirect('EntrarProyecto', codigo)
    elif comprobacion == 'Inscrito':

        with connection.cursor() as cursor:
            cursor.callproc('BuscarProyectoByCodigo', [codigo])
            proyectoDetails = cursor.fetchall()

            cursor.callproc('buscarProyectoPorCodigo', [codigo])
            proyectoCodigo = cursor.fetchone()[0]
            cursor.callproc('ListasFasesByProyecto', [proyectoCodigo])
            fases = cursor.fetchall()

            cursor.callproc('obtener_actividades_by_alumno', [id_alumno])
            actividades = cursor.fetchall()

            cursor.callproc('obtener_entregas_by_alumno', [id_alumno])
            entregas = cursor.fetchall()

        return render(request, 'pages/Actividades/Seguimiento_Act.html', {
            'codigo': codigo,
            'layout': layout,
            'proyectoDetails': proyectoDetails,
            'fases': fases,
            'actividades': actividades,
            'alumno': alumno,
            'entregas': entregas,
            'id_alumno': id_alumno
        })
    else:
        return redirect('Error', comprobacion)
    
@login_required(login_url='Login')
def calificarActividad(request, id_entrega, id_alumno, codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    try:
        if tipo_usuario == 'Alumno':
            return redirect('Error', 'No tienes permisos parar realizar esto')
        elif tipo_usuario == 'Profesor':
            with connection.cursor() as cursor:
                cursor.callproc('calificarActividad', [id_entrega])
                resultado = cursor.fetchone()[0]
                if resultado == 'Calificada con exito':
                    return redirect('SeguimientoAct', codigo, id_alumno)
                else:
                    return redirect('Error', resultado)
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')
    
@login_required(login_url='Login')
def anularCalificacionActividad(request, id_entrega, id_alumno, codigo):
    usuario = request.user
    tipo_usuario = usuario.rol.nombre
    try:
        if tipo_usuario == 'Alumno':
            return redirect('Error', 'No tienes permisos parar realizar esto')
        elif tipo_usuario == 'Profesor':
            with connection.cursor() as cursor:
                cursor.callproc('descalificarActividad', [id_entrega])
                resultado = cursor.fetchone()[0]
                if resultado == 'Anulada con exito':
                    return redirect('SeguimientoAct', codigo, id_alumno)
                else:
                    return redirect('Error', resultado)
    except (Alumno.DoesNotExist, Profesor.DoesNotExist):
        return redirect('logout')