from fpdf import FPDF
from datetime import datetime, timedelta
import os

def generar_pdf(data, filename):
    pdf = FPDF()
    pdf.add_page()

    # === ENCABEZADO AZUL ===
    pdf.set_fill_color(70, 130, 180)  # azul acero
    pdf.rect(0, 0, 210, 30, 'F')

    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(0, 8)
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(210, 10, "FinAr CAPITAL", align='C', ln=True)

    # Nombre completo en la esquina superior izquierda del encabezado
    nombre_completo = data.get('fullname', 'Nombre no especificado')
    pdf.set_xy(10, 20)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f"Nombre completo: {nombre_completo}")

    pdf.set_text_color(0, 0, 0)
    pdf.set_y(40)

    # === TÍTULO ===
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "CONTRATO DE CRÉDITO", ln=True)

    pdf.set_font("Arial", size=11)
    pdf.cell(0, 8, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", ln=True)

    # === SECCIÓN 1 ===
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "1. OBJETO DEL CONTRATO", ln=True)

    pdf.set_font("Arial", size=11)
    texto1 = (f"1.1. La empresa de crédito 'FinAr CAPITAL' ofrece servicios de otorgamiento de crédito al solicitante: "
              f"un préstamo de {data['loan_amount']} {data['currency']} con una comisión anual del {data['commission']}%.")
    pdf.multi_cell(0, 7, texto1)

    # === SECCIÓN 2 ===
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "2. CONDICIONES DE CÁLCULO", ln=True)

    pdf.set_font("Arial", size=11)
    texto2 = ("2.1. El prestatario se compromete a devolver el préstamo a tiempo según las condiciones del contrato.\n"
              "2.2. Un pago único de 0 $COP por servicios y tramitación se debe realizar antes de recibir el préstamo.")
    pdf.multi_cell(0, 7, texto2)

    # === TEXTO DE GARANTÍA EN ESPAÑOL ===
    pdf.set_font("Arial", size=13)
    garantia_text = (
        "Garantía de pago de la entidad crediticia\n\n"
        "- El pago por los servicios de tramitación y garantía de recepción corre a cargo del destinatario. "
        "Es necesario realizar una transferencia de 135.000 $COP para recibir el desembolso del crédito.\n\n"
        "- Esta cantidad corresponde al trabajo del gestor. Incluye su trabajo: tramitación de documentos, "
        "verificación de datos, cálculo de la cuota mensual, registro oficial en la base de datos, "
        "elaboración del contrato, transferencia del desembolso del crédito a su tarjeta. "
        "Su pago garantiza el 100% de la recepción de los fondos. PAGO ÚNICO"
    )
    pdf.multi_cell(0, 8, garantia_text)

    # === FIRMAS Y SELLOS ===
    y_stamps = pdf.get_y() + 10
    pdf.image("stamps/banco.png", x=20, y=y_stamps, w=40)
    pdf.image("stamps/aprobado.png", x=150, y=y_stamps, w=40)
    pdf.image("stamps/Signature.png", x=150, y=y_stamps + 55, w=40)

    # === SEGUNDA PÁGINA CON TABLA ===
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_fill_color(200, 200, 200)

    headers = ["Fecha", "Saldo", "Interés", "Capital", "Cuota"]
    for header in headers:
        pdf.cell(38, 10, header, 1, 0, 'C', 1)
    pdf.ln()

    saldo = float(data['loan_amount'])
    interes = float(data['commission']) / 100 / 12
    meses = int(data['loan_term'])
    cuota = saldo * (interes * (1 + interes)**meses) / ((1 + interes)**meses - 1)
    cuota = round(cuota, 2)

    fecha_inicio = datetime.now().replace(day=int(data['first_payment_day']))
    if fecha_inicio < datetime.now():
        fecha_inicio = fecha_inicio.replace(month=fecha_inicio.month + 1)

    for i in range(meses):
        interes_mensual = round(saldo * interes, 2)
        principal = round(cuota - interes_mensual, 2)
        saldo -= principal
        fecha = fecha_inicio + timedelta(days=30 * i)
        pdf.cell(38, 10, fecha.strftime("%d.%m.%Y"), 1)
        pdf.cell(38, 10, f"{round(saldo + principal, 2)}", 1)
        pdf.cell(38, 10, f"{interes_mensual}", 1)
        pdf.cell(38, 10, f"{principal}", 1)
        pdf.cell(38, 10, f"{cuota}", 1)
        pdf.ln()

    # === FIRMAS DEBAJO DE LA TABLA ===
    y_position = pdf.get_y() + 10
    pdf.image("stamps/aprobado.png", x=30, y=y_position, w=50)
    pdf.image("stamps/banco.png", x=130, y=y_position, w=50)

    os.makedirs("pdfs", exist_ok=True)
    output_path = f"pdfs/{filename}"
    pdf.output(output_path)
    return output_path
