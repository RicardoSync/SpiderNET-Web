from flask import request, render_template, redirect, url_for, flash
from ssh_pppoe import *
from d_insert import *

def procesado_creacion_profile():
    # Se obtienen los datos enviados desde el modal
    username = request.form.get('username')
    password = request.form.get('password')
    host = request.form.get('host')
    port = request.form.get('port')
    ippool = request.form.get('ippool')
    ppp_profile = request.form.get('ppp_profile')
    max_limit = request.form.get('max_limit')
    queue_parent = request.form.get('queueParent')


    if creacion_profile(ppp_profile, ippool, max_limit, username, password, host, port, queue_parent):
        if insertar_profile_pppoe(nombre=ppp_profile, local_address=ippool,remote_address=ippool, address_list="Internet", limit=max_limit, id_mikrotik=id):
            flash("PPP Profile creado en MikroTik y almacenado en el sistema", "success")
            return redirect(url_for("lista_microtiks"))
        else:
            flash("PPP Profile no se creo en el sistema")
            return redirect(url_for("lista_microtiks"))
    else:
        flash("PPP Profile no se creo en el MikroTik", "success")
        return redirect(url_for("lista_microtiks"))
