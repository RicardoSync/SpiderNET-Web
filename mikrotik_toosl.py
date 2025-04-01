from flask import *
from ssh_pcq import *
from ssh_pppoe import *
from monitor import *

def procesar_aplicacion_firewall():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        host = request.form.get("direccion_ip")
        port = request.form.get("port")
        
        ok = aplicarFirewall(host, port, username, password)
        if ok:
            flash("Reglas aplicadas con exito", "success")
            return redirect(url_for("lista_microtiks"))
        else:
            flash("No logramos aplicar las reglas", "danger")
            return redirect(url_for("lista_microtiks"))
        
def procesar_reinicio_mikrotid(id):
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        host = request.form.get("ip")
        port = request.form.get("port")
        reicniar_mikrotik(username, password, host, port)
        
    return redirect(url_for("lista_microtiks"))

def procesar_monito_trafico():
    if request.method == "POST":
        mikrotik = request.form.get("lista_microtik")
        # Obtén la interfaz seleccionada del formulario
        interface = request.form.get("interface", "ether1")
        credenciales = consultarCredenciales(nombre=mikrotik)

        if credenciales:
            username = credenciales[0]
            password = credenciales[1]
            host = credenciales[2]
            port = credenciales[3]
            
            try:
                output = obtener_trafico_mikrotik(host, port, username, password, interface)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

            # Procesa la salida para convertirla en un diccionario:
            data = {}
            for line in output.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    data[key.strip()] = value.strip()
    
    return jsonify(data)