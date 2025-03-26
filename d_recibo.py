from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import datetime
from flask import send_file

def creacion_recibo(mensualidad, meses_pagados, nombre_cliente, descuento, concepto, metodo):
        # Ejemplo de cálculos (ajusta según tu lógica)
        total_mensualidad = mensualidad * meses_pagados
        descuento_aplicado = total_mensualidad * (descuento / 100.0)
        total_pagar = total_mensualidad - descuento_aplicado

        # Genera el PDF en memoria
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Encabezado
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2, height - 50, "RECIBO DE PAGO")
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 80, f"Cliente: {nombre_cliente}")
        c.drawString(50, height - 100, f"Concepto: {concepto}")
        c.drawString(50, height - 120, f"Método: {metodo}")
        c.drawString(50, height - 140, f"Meses Pagados: {meses_pagados}")
        c.drawString(50, height - 160, f"Total Mensualidad: ${total_mensualidad:.2f}")
        c.drawString(50, height - 180, f"Descuento: {descuento}% (${descuento_aplicado:.2f})")
        c.drawString(50, height - 200, f"TOTAL A PAGAR: ${total_pagar:.2f}")
        c.drawString(50, height - 220, f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        c.showPage()
        c.save()
        buffer.seek(0)
        
        # Enviar el PDF para descarga
        return send_file(buffer,
                         as_attachment=True,
                         download_name=f"Recibo_{nombre_cliente.replace(' ', '_')}.pdf",
                         mimetype='application/pdf')
        