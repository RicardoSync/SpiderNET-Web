from d_insert import *
from d_consultas import *
from d_update import *
from d_eliminar import *
from flask import *

def procesar_consulta_equipos():
    dedos = consultarEquipos()
    return render_template("equipos.html", equipos=dedos)

def procesar_asignacion_equipo(id):
    if request.method == "POST":
        nombre_equipo = request.form.get("nombre_equipo")
        tipo_equipo = request.form.get("tipo_equipo")
        marca_equipo = request.form.get("marca_equipo")
        modelo_equipo = request.form.get("modelo_equipo")
        estado_equipo = request.form.get("estado_equipo")
        
        ok = insertarEquipo(nombre_equipo, tipo_equipo, marca_equipo, modelo_equipo, estado_equipo, id)
        if ok:
            flash("Equipo asignado con exito", "success")
            return redirect(url_for("lista_clientes"))
        else:
            flash("No asignamos el equipo al cliente", "danger")
            return redirect(url_for("lista_clientes"))

def procesar_edicion_equipo(id):
    if request.method == "POST":
        nombre = request.form.get("nombre")
        tipo = request.form.get("tipo_equipo")
        marca = request.form.get("marca")
        modelo = request.form.get("modelo")
        estado_equipo = request.form.get("estado_equipo")
        
        ok = actualizarEquipo(nombre, tipo, marca, modelo, estado_equipo, id)
        if ok:
            flash("El equipo se actualizo", "success")
            return redirect(url_for("consultar_equipos"))
        else:
            flash("No actualizamos el equipo", "danger")
            return redirect(url_for("consultar_equipos"))
        
def procesar_eliminar_equipos(id):
    ok = eliminarEquipo(id)
    if ok:
        flash("Equipo eliminado", "success")
        return redirect(url_for("consultar_equipos"))
    else:
        flash("Equipo no eliminado", "danger")
        return redirect(url_for("consultar_equipos"))