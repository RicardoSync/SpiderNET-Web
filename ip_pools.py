from flask import *
from get_pools import *
from d_insert import *
from ssh_pcq import *
from ssh_pppoe import *

def procesar_consulta_ip_pools():
    # Obtiene los parámetros de la consulta
    mikrotik_id = request.args.get('id')
    username = request.args.get('username')
    password = request.args.get('password')
    host = request.args.get('host')
    port = request.args.get('port')
    print(f"Uusaiors obtenidos {username, password, host, port}")
    # Llama a la función para obtener las IP pools
    pools = get_pool_list_nuevo(host, port, username, password)
    print(f"Pool obtenidas en backend {pools}")
    
    # Devuelve un fragmento de HTML con el select de pools
    return render_template("ippools_partial.html", pools=pools)

def procesar_creacion_ppp_profile(id):
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