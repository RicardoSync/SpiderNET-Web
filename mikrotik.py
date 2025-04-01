from d_insert import *
from d_consultas import *
from d_update import *
from d_eliminar import *
from flask import *
from ssh_pcq import *
from ssh_pppoe import *

def procesar_creacion_mikrotik():
    if request.method == "POST":
        nombre = request.form.get("nombreNuevo")
        username = request.form.get("usernameNuevo")
        password = request.form.get("passwordNuevo")
        ip = request.form.get("ipNuevo")
        port = request.form.get("portNuevo")

        ok = insertMicrotik(nombre, ip, username, password, port)
        if ok:
            flash("Microtik registrado con exito", "success")
            return redirect(url_for("lista_microtiks"))
        else:
            flash("No se registro el microtik", "danger")
            return redirect(url_for("lista_microtiks"))


    return redirect(url_for("lista_microtiks"))

def procesar_lista_mickrotiks():
    micro = consultarMicrotikTodo()
    print(micro)
    return render_template("microtik.html", microtiks=micro, queues_colas=consultarQeue())

def procesar_edicion_mikrotik(id):
    if request.method == "POST":
        nombre = request.form.get("nombre")
        username = request.form.get("username")
        password = request.form.get("password")
        ip = request.form.get("ip")
        port = request.form.get("port")

        ok = actualizarMicrotik(nombre, ip, username, password, port, id)
        if ok:
            flash("Microtik actualizado exitosamente", "success")
            return redirect(url_for("lista_microtiks"))
        else:
            flash("Microtik no actualizado", "danger")
            return redirect(url_for("lista_microtiks"))


    return redirect(url_for("lista_microtiks"))

def procesar_eliminacion_mikrotik(id):
    ok = eliminarMicrotik(id)

    if ok:
        flash("Microtik eliminado de manera exitosa", "success")
        return redirect(url_for("lista_microtiks"))
    else:
        flash("No se logro eliminar el microtik", "danger")
        return redirect(url_for("lista_microtiks"))