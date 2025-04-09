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

        if insertar_usuario(nombre, usuario, password, rol):
            flash("Usuario almacenado con exito", "success")
            return redirect(url_for("usuarios"))
        else:
            flash("Existio un problema en la creacion del usuario", "danger")
            return redirect(url_for("usuarios"))
            
def procesar_actualizacion_usuario(id):
    if request.method == "POST":
        nombre = request.form.get("nombre")
        usuario = request.form.get("usuario")
        password = request.form.get("password")

        if actualizar_usuario(id, nombre, usuario, password):
            flash(f"El usuario {nombre} se actualizo con exito", "success")
            return redirect(url_for("usuarios"))
        else:
            flash(f"Hubo un error durante la actualizacion del usuario", "danger")
            return redirect(url_for("usuarios"))


def procesar_eliminacion_usuario(id):
    if eliminarUsuario(id):
        flash(f"El usuario se eliminó con éxito", "success")
    else:
        flash(f"Hubo un error durante la eliminación del usuario", "danger")
    return redirect(url_for("usuarios"))