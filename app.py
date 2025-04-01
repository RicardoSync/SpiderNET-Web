from flask import Flask, render_template, redirect, session, request, url_for, flash, send_file, jsonify
from d_consultas import *
from d_insert import *
from d_eliminar import *
from d_update import *
from ssh_pcq import *
from d_login import login
from d_contador import *
from monitor import obtener_trafico_mikrotik
from dhcp_leases import get_dhcp_leases
from bloqueos_bd import estado_bloqueado
from ssh_pppoe import *
from get_pools import *
from pppoe import *


from dashboard import *
from clientes import *
from bloqueos import *
from mikrotik import *
from interfaces import *
from config_pcq import *
from parent import *
from mikrotik_toosl import *
from ip_pools import *
from paquetes import *
from servicios import *
from equipos import *
from queue_parent import *
from pppoe_profile import *
from ticket import *

app = Flask(__name__)
app.secret_key = 'zerocuatro04/2025'  # Necesario para usar flash
#------------------------------------------------RUTAS CUANDO OCURRE UN ERROR----------------------------------

# Error 404 (Página no encontrada)
@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("error.html"), 404

# Error 500 (Error interno del servidor)
@app.errorhandler(500)
def error_interno(error):
    return render_template("error.html"), 500
#------------------------------------------------RUTAS CUANDO OCURRE UN ERROR----------------------------------

#AQUI ES A DONDE NOS VAMOS CUANDO SE ENTRA AL SERVIDOR
@app.route("/")
def raiz():
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    return procesar_dashboard_raiz()

@app.route("/iniciar_sesion", methods=["POST"])
def iniciar_sesion():
    return procesar_dashboard_inicio_sesion()

#------------------------------------------------RUTA DE LOS CLIENTES CRUD----------------------------------
@app.route("/crear_cliente", methods=["POST"])
def crear_cliente():
    return procesar_cliente_creacion()
            
@app.route("/lista_clientes")
def lista_clientes():
    return procesar_lista_clientes()

@app.route("/eidtar_cliente<int:id>", methods=["POST"])
def eidtar_cliente(id):
    return procesar_edicion_del_cliente(id)

@app.route("/eliminar_cliente<int:id>", methods=["POST"])
def eliminar_cliente(id):
    return procesar_elimiacion_del_cliente(id)


@app.route('/bloquear_cliente_pcq/<int:id>', methods=["POST"])
def bloquear_cliente_pcq(id):
    return procesar_bloqueo_clinete(id)

@app.route("/desbloquear_cliente_pcq/<int:id>", methods=["POST"])
def desbloquear_cliente_pcq(id):
    return procesar_desbloqueo_cliente(id)

@app.route("/clientes_bloqueados")
def clientes_bloqueados():
    return procesar_lista_bloqueados()
#------------------------------------------------RUTA DE LOS CLIENTES CRUD----------------------------------

#------------------------------------------------RUTA DE LOS MICROTIKS CRUD----------------------------------
@app.route("/crear_mikrotik", methods=["POST"])
def crear_mikrotik():
    return procesar_creacion_mikrotik()

@app.route("/lista_microtiks")
def lista_microtiks():
    return procesar_lista_mickrotiks()

@app.route("/editar_mikrotik<int:id>", methods=["POST"])
def editar_mikrotik(id):
    return procesar_edicion_mikrotik(id)

@app.route("/eliminar_mikrotik<int:id>", methods=["POST"])
def eliminar_mikrotik(id):
    return procesar_eliminacion_mikrotik(id)

@app.route("/consultar_interfaces")
def consultar_interfaces():
    return procesar_consulta_interfaces()

@app.route("/consultar_interfaces_chido")
def consultar_interfaces_chido():
    return procesar_interfaces_chido()

@app.route("/configuracion_pcq", methods=["POST"])
def configuracion_pcq():
    return procesar_configuracion_pcq()

@app.route("/crear_queue_parent", methods=["POST"])
def crear_queue_parent():
    return procesar_creacion_queue_parent_del_bueno()

@app.route("/cargar_queue", methods=["POST"])
def cargar_queue():
    return procesar_cargar_queue()
 
@app.route("/eliminar_queue_simple/<int:id>", methods=["POST"])
def eliminar_queue_simple(id):
    return procesar_eliminar_queue_simple(id)

@app.route("/aplicar_reglas", methods=["POST"])
def aplicar_reglas():
    return procesar_aplicacion_firewall()

@app.route('/reiniciar_mikrotik/<int:id>', methods=["POST"])
def reiniciar_mikrotik(id):
    return procesar_reinicio_mikrotid(id)

@app.route("/dios_ayudame")
def dios_ayudame():
    microtiks = consultarMicrotik()
    return render_template("monitor.html", microtiks=microtiks)

@app.route('/monitor_traffic', methods=["POST"])
def monitor_traffic():
    return procesar_monito_trafico()

@app.route("/consultar_ip_pools")
def consultar_ip_pools():
    return procesar_consulta_ip_pools()

@app.route("/crear_ppp_profile/<int:id>", methods=["POST"])
def crear_ppp_profile(id):
    return procesar_creacion_ppp_profile(id)
#------------------------------------------------RUTA DE LOS MICROTIKS CRUD----------------------------------



#------------------------------------------------RUTA DE LOS PAQUETES CRUD----------------------------------
@app.route('/lista_paquetes')
def lista_paquetes():
    return procesar_lista_paquetes()

@app.route('/crear_paquete', methods=['POST'])
def crear_paquete():
    return procesar_creacion_paquete()

@app.route('/editar_paquete/<int:id>', methods=['POST'])
def editar_paquete(id):
    return procesar_editar_paquete(id)

@app.route('/eliminar_paquete/<int:id>')
def eliminar_paquete(id):
    return procesar_eliminar_paquete(id)
#------------------------------------------------RUTA DE LOS PAQUETES CRUD----------------------------------


#------------------------------------------------RUTA DE LOS SERVICIOS CRUD----------------------------------
@app.route("/creacion_servicio", methods=["POST"])
def creacion_servicio():
    return procesar_creacion_servicio()

@app.route("/lista_servicios")
def lista_servicios():
    return procesar_lista_servicios()

@app.route("/editar_servicio/<int:id>", methods=["POST"])
def editar_servicio(id):
    return procesar_edicion_servicios(id)

@app.route("/eliminar_servicio/<int:id>")
def eliminar_servicio(id):
    return procesar_eliminar_servicio(id)
#------------------------------------------------RUTA DE LOS SERVICIOS CRUD----------------------------------

#=======================================ASIGNACION DE LOS EQUIPOS==============================
# Ruta para procesar la asignación del equipo
@app.route('/asignar_equipo/<int:id>', methods=['POST'])
def asignar_equipo(id):
    return procesar_asignacion_equipo(id)

@app.route("/consultar_equipos")
def consultar_equipos():
    return procesar_consulta_equipos()

@app.route("/editar_equipo/<int:id>", methods=["POST"])
def editar_equipo(id):
    return procesar_edicion_equipo(id)

@app.route("/eliminar_equipo/<int:id>")
def eliminar_equipo(id):
    return procesar_eliminar_equipos(id)
#=======================================ASIGNACION DE LOS EQUIPOS==============================

#=======================================FUNCION DE QUEUE PARENT==============================
@app.route("/creacion_queue_parent", methods=["POST"])
def creacion_queue_parent():
    return procesar_creacion_queue_panret()

@app.route("/lista_queue")
def lista_queue():
    return procesar_lista_queue_parent_chido()

@app.route("/editar_queue_parent/<int:id>", methods=["POST"])
def editar_queue_parent(id):
    return procesar_edicion_queue_parent(id)

@app.route("/eliminar_queue_parent/<int:id>", methods=["POST"])
def eliminar_queue_parent(id):
    return procesar_eliminacion_queue_parent_no(id)     
#=======================================FUNCION DE QUEUE PARENT==============================



#=======================================FUNCION DE DHCP LEASES==============================

# Ruta para renderizar la página de perfiles PPPoE
@app.route("/pppoe_profiles")
def pppoe_profiles():
    return procesar_render_profile()
# Ruta para crear un nuevo perfil PPPoE
@app.route("/crear_profile", methods=["POST"])
def crear_profile():
    return procesar_creacion_ppp_profile_chido()


#=======================================FUNCION DE DHCP LEASES==============================


#=======================================FUNCION DE DHCP LEASES==============================
@app.route("/crear_ticket", methods=["POST"])
def crear_ticket():
    return procesar_creacion_tikcet()

@app.route("/fallas")
def fallas():
    return procesar_renderizado_fallas()

@app.route("/editar_ticket/<int:id>", methods=["POST"])
def editar_ticket(id):
    return procesar_edicion_ticket(id)
    
@app.route("/actualizar_finalizado/<int:id>", methods=["POST"])
def actualizar_finalizado(id):
    return procesar_acrualizacion_estado_ticket(id)
#================================""=======FUNCION DE DHCP LEASES==============================

app.run(debug=True)
