from flask import *

from bloqueos import *
from clientes import *
from config_pcq import *
from dashboard import *
from equipos import *
from interfaces import *
from ip_pools import *
from mikrotik import *
from mikrotik_toosl import *
from paquetes import *
from panel_clientes import *
from parent import *
from pagos import *
from pppoe_profile import *
from queue_parent import *
from registro_simplequeue import *
from servicios import *
from ticket import *
from usuarios import *
from cortes_clientes_programar import *

app = Flask(__name__)
app.secret_key = 'zerocuatro04/2025'  # Necesario para usar flash

#------------------------------------------------ ERRORES ----------------------------------

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("error.html"), 404

@app.errorhandler(500)
def error_interno(error):
    return render_template("error.html"), 500

#------------------------------------------------ LOGIN Y DASHBOARD ----------------------------------

@app.route("/")
def raiz():
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    return procesar_dashboard_raiz()

@app.route("/iniciar_sesion", methods=["POST"])
def iniciar_sesion():
    return procesar_dashboard_inicio_sesion()

@app.route("/cliente/<int:id_cliente>")
def cliente_panel(id_cliente):
    return procesar_el_cliente(id_cliente=id_cliente)

@app.route("/logout")
def logout():
    session.clear()  # <- si estás usando sesión
    return redirect(url_for("raiz"))  # raíz puede ser tu login
#------------------------------------------------ CRUD CLIENTES ----------------------------------

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

@app.route("/registrar_pago/<int:id>", methods=["POST"])
def registrar_pago(id):
    return procesar_registro_pago(id)

@app.route("/pagos", methods=["GET"])
def pagos():
    return procesar_lista_de_pagos()

@app.route("/programar_tarea/<int:id>", methods=["POST"])
def programar_tarea(id):
    return procesar_programacion_tarea_corte(id)

#------------------------------------------------ CRUD MIKROTIK ----------------------------------

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

@app.route("/probar_coneion/<int:id>", methods=["POST"])
def probar_coneion_mk(id):
    print("pruba de conexion")
    return redirect(url_for("lista_microtiks"))

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

@app.route("/cargar_queues/<int:id>", methods=["POST"])
def cargar_queues(id):
    obtener_datos_mikrotik_cargar_simple_queue(id)
    return redirect(url_for("lista_microtiks"))

#------------------------------------------------ CRUD PAQUETES ----------------------------------

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

#------------------------------------------------ CRUD SERVICIOS ----------------------------------

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

#------------------------------------------------ EQUIPOS ----------------------------------

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

#------------------------------------------------ QUEUE PARENT ----------------------------------

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

#------------------------------------------------ PPPoE PROFILES ----------------------------------

@app.route("/pppoe_profiles")
def pppoe_profiles():
    return procesar_render_profile()

@app.route("/crear_profile", methods=["POST"])
def crear_profile():
    return procesar_creacion_ppp_profile_chido()

#------------------------------------------------ TICKETS ----------------------------------

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

#------------------------------------------------ USUARIOS ----------------------------------

@app.route("/usuarios")
def usuarios():
    return procesar_rendender_usuarios()

@app.route("/creacion_usuario", methods=["POST"])
def creacion_usuario():
    return procesar_creacion_usuario()

@app.route("/editar_usuario/<int:id>", methods=["POST"])
def editar_usuario(id):
    return procesar_actualizacion_usuario(id)

@app.route("/eliminar_usuario/<int:id>", methods=["GET"])
def eliminar_usuario(id):
    return procesar_eliminacion_usuario(id)

#------------------------------------------------ INICIAR APP ----------------------------------

app.run(debug=True)
