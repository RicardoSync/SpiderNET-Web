from d_consultas import consultarCredenciales
from flask import Flask, render_template, request, redirect, url_for, flash
from programacion_cortes import *

def procesar_programacion_tarea_corte(id):
    if request.method == "POST":
        nombre_cliente = request.form.get("name")
        direccion_ip = request.form.get("direccion_ip")
        dia_corte = int(request.form.get("dia_corte"))
        mikrotik = request.form.get("mikrotik_administrador")

        print(f"Datos obtenidos en programacion {nombre_cliente, direccion_ip, dia_corte, mikrotik}")

        credenciales = consultarCredenciales(nombre=mikrotik)
        if credenciales:
            username = credenciales[0]
            password = credenciales[1]
            host = credenciales[2]

            if create_task(name_cliente=nombre_cliente, address=direccion_ip, username=username, password=password,
                        host=host, dia_corte=dia_corte):
                
                flash("Tarea de corte programada con exito", "success")
                return redirect(url_for("lista_clientes"))
            
            else:
                flash("No se creo la tarea, existio algun error! Llama a Martha!!", "danger")
                return redirect(url_for("lista_clientes"))
            
        else:
            flash("No encontramos credenciales para ese mikrotik", "danger")
            return redirect(url_for("lista_clientes"))
