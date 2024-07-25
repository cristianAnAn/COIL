from django.urls import path, include
from . import views
from .views import CustomPasswordResetView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index,name='Index'),
    path('ListaProyectos/', views.ListaProyectos, name='ListaProyectos'),
    path('listaArchivoProyectos/', views.ListaArchivoProyectos, name='ListaArchivoProyectos'),
    path('crearProyecto/',views.crearProyecto,name="crearProyecto"),
    path('unirteProyecto/',views.UnirteProyecto,name="unirteProyecto"),
    path ('ListaAlumnosProfesores/<str:codigo>', views.ListaAlumnosProfesores,name="ListaAlumnosProfesores"),
    path('IntroduccionCoil/<str:codigo>', views.IntroduccionCoil,name="IntroduccionCoil"),
    path('Foro/<str:codigo>', views.ProyectoDetail,name="ProyectoDetail"),
    path('ListaActividadesPorFases/', views.ListaActividadesPorFases, name="ListaActividadesPorFases"),
    path('ConfiguracionProyecto/<str:codigo>',views.ConfiguracionProyecto, name="ConfiguracionProyecto"),
    path('SeguimientoActividad/<str:codigo>',views.SeguimientoActividad,name='SeguimientoActividad'),
    path('ViAlActividades/',views.ViAlActividades,name="ViAlActividades"),
    path('ViAlMateriales/<int:material>', views.ViAlMateriales, name='ViAlMateriales'),
    path('AgregarMaterial/', views.AgregarMaterial, name='AgregarMaterial'),
    path('MaterialComentarios/<int:id_material>', views.MaterialComentarios, name='MaterialComentarios'),
    
    
    path('Registro/', views.Registro, name='Registro'),
    path('Login/', views.Login, name='Login'),
    path('Home/', views.Home, name="Home"),
    path('Logout/', views.logout_view, name='logout'),
    path('verificationcode/', views.verify_code, name='verify_code'),
    path('EditarUsuario/', views.EditarUsuario, name='editar_usuario'),
    
    path('guardar_usuario/', views.guardar_usuario, name='guardar_usuario'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    
    
    
    
    path('registro_alumno/', views.RegistroAlumno, name='registro_alumno'),
    path('save_other_university/', views.save_other_university, name='save_other_university'),
    path('registro_profesor/', views.RegistroProfesor, name='registro_profesor'),
    path('ProfesorDatosPersonales/', views.ProfesorDatosPersonales, name='ProfesorDatosPersonales'),
    path('EditDatosProfesor/<str:codigo>', views.EditDatosProfesor, name="EditDatosProfesor"),
    
    
    path('Validatecredentials/', views.validate_credentials, name='validate_credentials'),
    path('Checkusername/', views.check_username, name='check_username'),
    path('fasesCoil/<str:codigo>',views.indexFases,name="FasesCoil"),
    path('fasesCoil/<str:codigo>/<int:idFase>',views.Fase1,name="Fase"),

    path('error/<str:error>',views.Error,name="Error"),
    path('Proyecto/<str:codigo>',views.UnirteProyectoPage, name="EntrarProyecto"),
    path('AgregarUsuarioProyecto/<int:proyecto>/<str:codigo>',views.AgregarUsuarioProyecto, name="AgregarUsuarioProyecto"),
    path('EditarProyecto/<int:proyecto>/<str:codigo>',views.editarProyecto, name="EditarProyecto"),
    path('ZoomProyecto/<int:proyecto>/<str:codigo>',views.zoomProyecto, name="ZoomProyecto"),
    path('ArchivarProyecto/<int:proyecto>/<str:codigo>',views.ArchivarProyecto, name="ArchivarProyecto"),
    path('ReactivarProyecto/<int:proyecto>/<str:codigo>',views.ReactivarProyecto, name="ReactivarProyecto"),
    path('CrearAnucio/<int:proyecto>/<str:codigo>',views.PublicarComentario,name="PublicarComentario"),
    path('ComentarAnucio/<int:publicacion>/<str:codigo>',views.ComentarPublicacion,name="ComentarPublicacion"),
    path('EliminarComentarioAnucio/<int:id_coment>/<str:codigo>',views.eliminarComentario,name="eliminarComentario"),
    path('EliminarAnucio/<int:id_anuncio>/<str:codigo>',views.eliminarAnuncio,name="eliminarAnuncio"),
    path('EditarComentarioAnucio/<int:id_coment>/<str:codigo>',views.editarComentario,name="editarComentario")
    # path('articulos/',views.articulos,name="articulos"),
    # path('articulo/',views.arcticulo,name="articulo"),

]