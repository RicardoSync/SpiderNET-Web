from flask import *
from d_insert import *
from d_consultas import *
from d_update import *
from d_eliminar import *


def procesar_rendender_usuarios():
    return render_template("usuarios.html", usuarios=consultar_usuarios())

def procesar_creacion_usuario():
    rol = None  # Inicializamos rol en None para evitar errores
    if request.method == "POST":
        nombre = request.form.get("nombre")
        usuario = request.form.get("usuario")
        password = request.form.get("password")
        tipo = request.form.get("tipo_permisos")

        # Asignar el rol basado en el tipo de usuario
        if tipo == "Administrador":
            rol = 0
        elif tipo == "Tecnico":
            rol = 1
        elif tipo == "Cliente":
            rol = 2

        print(nombre, usuario, password, tipo, rol)  # Debugging

    return redirect(url_for("usuarios"))