from d_insert import *
from d_consultas import *
from d_update import *
from d_eliminar import *
from flask import *
from ssh_pcq import *
from ssh_pppoe import *

def procesar_lista_queue_parent_chido():
    queues_lista = consultar_queue()
    return render_template("queue_parent.html", queue_parents=queues_lista, microtiks=consultarMicrotik(), queues_colas=consultarQeue())


def procesar_creacion_queue_panret():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        segmento = request.form.get("segmento")
        max_limit = request.form.get("max_limit")
        mikrotik = request.form.get("lista_microtik")

        credenciales = consultarCredenciales(nombre=mikrotik)


        if credenciales:
            username = credenciales[0]
            password = credenciales[1]
            host = credenciales[2]
            port = credenciales[3]
            ok = crearQueueParent(nombre, segmento, max_limit, host, port, username, password, mikrotik)
            if ok:
                flash(f"Queue creado con exito en el mikroitk {mikrotik}", "success")
                return redirect(url_for("lista_queue"))
            else:
                flash("No logramos crear el Queue Parent", "danger")
                return redirect(url_for("lista_queue"))
        else:
            flash("No encontramos credenciales para ese mirotik", "danger")

def procesar_edicion_queue_parent(id):
    nombre = request.form.get("nombre")
    max_limint = request.form.get("max_limint")
    mikrotik = request.form.get("mirotik")
    segmento_red = request.form.get("segmento_red")
    credenciales = consultarCredenciales(mikrotik)

    if credenciales:
        username = credenciales[0]
        password = credenciales[1]
        host = credenciales[2]
        port = credenciales[3]
        print(username, password, host, port, segmento_red, nombre, max_limint)
        ok = actualizarQueue(username, password, host, port, segmento_red, nombre, max_limint)
        if ok:
            yes = actualiar_queue_bd(nombre, max_limint, mikrotik, id)
            if yes:
                flash("Queue actualizado en sistema y MikroTik", "success")
                return redirect(url_for("lista_queue"))
            else:
                flash("No actualimas la queue en sistema", "danger")
                return redirect(url_for("lista_queue"))
        else:
            flash("No actualizamos la Queue en MikroTik", "danger")
            return redirect(url_for("lista_queue"))
    else:
        flash("No encontramos credenciales para el MikroTik", "danger")

def procesar_eliminacion_queue_parent_no(id):
    if request.method == "POST":
        microtik = request.form.get("mirotik")
        segmento_red = request.form.get("segmento")

        credenciales = consultarCredenciales(microtik)

        if not credenciales:
            flash("Sin credenciales, en ese mikrotik", "danger")
            return redirect(url_for("lista_queue"))

        username, password, host, port = credenciales

        if not eliminarQueueParent(username, password, host, port, segmento_red):
            flash("No eliminamos el QueueParent de Mikrotik", "danger")
            return redirect(url_for("lista_queue"))

        if not eliminarQueueBD(id):
            flash("Queue no se eliminó de la base de datos", "danger")
            return redirect(url_for("lista_queue"))

        flash("Queue eliminado del sistema", "success")
        return redirect(url_for("lista_queue"))

    return redirect(url_for("lista_queue"))   