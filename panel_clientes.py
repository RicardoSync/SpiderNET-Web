from flask import render_template, request
from conexion import conexion

def procesar_panel_cliente():
    id_cliente = 2
    con = conexion()
    cursor = con.cursor(dictionary=True)

    # Estado del cliente
    cursor.execute("SELECT estado, nombre FROM clientes WHERE id = %s", (id_cliente,))
    cliente = cursor.fetchone()

    # Pagos del cliente
    cursor.execute("SELECT nombre, monto, cantidad, fecha_pago FROM pagos WHERE id_cliente = %s ORDER BY fecha_pago DESC", (id_cliente,))
    pagos = cursor.fetchall()

    con.close()
    return render_template("panel_cliente.html", cliente=cliente, pagos=pagos, id_cliente=id_cliente)

def procesar_equipos_cliente(id_cliente):
    con = conexion()
    cursor = con.cursor(dictionary=True)

    cursor.execute("SELECT * FROM equipos WHERE id_cliente = %s", (id_cliente,))
    equipos_cliente = cursor.fetchall()

    con.close()
    return render_template("equipos_cliente.html", equipos=equipos_cliente)
