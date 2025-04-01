from d_insert import *
from d_consultas import *
from d_update import *
from d_eliminar import *
from flask import *
from ssh_pcq import *
from ssh_pppoe import *

def procesar_consulta_interfaces():
    # Obtiene los parámetros de la consulta
    mikrotik_id = request.args.get('id')
    username = request.args.get('username')
    password = request.args.get('password')
    ip = request.args.get('ip')
    port = request.args.get('port')
    
    # Llama a la función para obtener las interfaces
    interfaces = get_interfaces(ip, port, username, password)
    
    # Devuelve un fragmento de HTML (por ejemplo, un select) con las interfaces
    return render_template("interfaces_partial.html", interfaces=interfaces)

def procesar_interfaces_chido():
    # Se obtiene el nombre del Mikrotik desde el parámetro 'mikrotik'
    mikrotik = request.args.get("mikrotik")
    credenciales = consultarCredenciales(nombre=mikrotik)
    if credenciales:
        username = credenciales[0]
        password = credenciales[1]
        ip = credenciales[2]
        port = credenciales[3]
    
    # Llama a la función para obtener las interfaces
    interfaces = get_interfaces(ip, port, username, password)
    
    # Devuelve un fragmento de HTML (por ejemplo, un select) con las interfaces
    return render_template("interfaces_partial.html", interfaces=interfaces)
