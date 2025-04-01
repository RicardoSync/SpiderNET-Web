from d_insert import *
from d_consultas import *
from d_update import *
from d_eliminar import *
from flask import *

def procesar_creacion_tikcet():
    if request.method == "POST":
        cliente = request.form.get("lista_clientes")
        tipo = request.form.get("lista_categorias")
        descripcion = request.form.get("ticket")
        usuario = request.form.get("lista_usuarios")
        
        if insertar_ticket(cliente, tipo, descripcion, usuario):
            flash("Ticket generado de manera exitosa", "success")
            return redirect(url_for("fallas"))
        else:
            flash("Ocurrio un error, no generado", "danger")
            return redirect(url_for("fallas"))      

def procesar_renderizado_fallas():
    categoria = ["Soporte técnico",
                 "Facturación",
                 "Instalación",
                 "Otro"]
    
    return render_template("fallas.html", clientes=consularNombreClientes(), reportes=categoria,
                           usuarios=consultarUsuarios(), tickets=consultar_tickets())

def procesar_edicion_ticket(id):
    if request.method == "POST":
        tipo = request.form.get("lista_categorias")
        descripcion = request.form.get("ticket")        
        usuario = request.form.get("lista_usuarios")
        if actualizar_ticket(tipo, descripcion, usuario, id):
            flash("Ticket actualizado con éxito", "success")
            return redirect(url_for("fallas"))
        else:
            flash("No actualizamos el ticket", "danger")
            return redirect(url_for("fallas"))
        
    return redirect(url_for("fallas"))

def procesar_acrualizacion_estado_ticket(id):
    if actualizar_ticket_finalizado(id):
        flash("Ticket finalizado", "success")
        return redirect(url_for("fallas"))
    else:
        flash("Ocurrio un error en la finalizacion", "danger")
        return redirect(url_for("fallas"))