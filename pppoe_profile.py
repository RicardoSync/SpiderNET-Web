from flask import *
from d_insert import *
from ssh_pppoe import *
from d_consultas import *

def procesar_creacion_ppp_profile_chido():
    lista_microtik = request.form.get("lista_microtik")
    nombre = request.form.get("nombre")
    pool = request.form.get("pool")
    pool_ranges = request.form.get("pool_ranges")
    max_limit = request.form.get("max_limit")
    
    creacion_profile(pool_ranges, pool, lista_microtik, nombre, max_limit)
    
    return redirect(url_for("pppoe_profiles"))

def procesar_render_profile():
    # En este ejemplo, se asume que 'microtiks' y 'pools' se obtienen previamente.
    # Podrías obtener la lista de mikrotiks desde una BD.
    microtiks = consultarMicrotik()
    # Por defecto, para mostrar pools, se utiliza el primer mikrotik seleccionado.

    pools = get_ip_pools(microtiks[0])
    profiles = []
    return render_template("monitor_profiles.html", microtiks=microtiks, pools=pools, profiles=profiles)
