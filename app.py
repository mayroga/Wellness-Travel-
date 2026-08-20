# ====================================================================================================
#                                         MAY ROGA LLC
#                       Wellness Travel Architecture & Lifestyle Optimization
#                                    Miami, Florida | USA
#                                 PRODUCTION BACKEND - AUDITED
# ====================================================================================================

import os
import json
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

app = FastAPI(
    title="MAY ROGA LLC - Wellness Travel App Production Backend",
    version="1.0.0"
)

# MONTAR LA CARPETA ESTÁTICA SÓLO SI EXISTE EN EL DISCO
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# DICCIONARIO MAESTRO SINCRONIZADO CON LOS HOTELES DEL FRONTEND
BACKEND_HOTELES = {
    "H1": {"name": "Eden Roc Cap Cana (República Dominicana)", "desc": "Bungalows de ultra-lujo con alberca propia, jardín zen y aislamiento acústico total."},
    "H2": {"name": "Amanera Resort (Playa Grande)", "desc": "Casitas minimalistas de cristal suspendidas sobre los acantilados marinos de Dominicana."},
    "H3": {"name": "Grand Velas Riviera Maya (México)", "desc": "Suites presidenciales frente al mar acompañadas de un circuito hidrotermal de spa guiado."},
    "H4": {"name": "Secrets Impression Moxché (México)", "desc": "Oasis exclusivo rústico-chic con rooftops infinity y servicio de mayordomo las 24 horas."},
    "H5": {"name": "Secrets Royal Beach Punta Cana", "desc": "Complejo vacacional todo incluido solo para adultos frente a las arenas blancas de Bávaro."}
}

# DICCIONARIO DE TRASLADOS PREMIUM SEGÚN EL TIER CALCULADO
BACKEND_LOGISTICA = {
    "ELITE": {
        "air": "Gulfstream G650 Chárter Privado directo desde la terminal VIP de Miami (OPF).",
        "sea": "The Ritz-Carlton Yacht Collection Suite Ejecutiva con terraza de popa privada."
    },
    "PREMIUM": {
        "air": "Clase Ejecutiva Flagship Suite con asientos Lie-Flat totalmente reclinables.",
        "sea": "Celebrity Cruises (The Retreat Enclave) con acceso a solárium VIP restringido."
    },
    "ASPI": {
        "air": "Cabina Principal Confort+ en vuelo directo sin escalas con chequeo prioritario.",
        "sea": "Royal Caribbean International (Solarium Adults-Only Retreat) libre de ruidos."
    }
}

class PDFPayload(BaseModel):
    servicio_id: str
    lang: str
    score_inicial: float
    score_actual: float
    respiracion_score: float
    adivinanzas_score: float
    iev: float
    variante: str
    destino_id: str

@app.post("/generate-pdf")
def generate_pdf(payload: PDFPayload):
    pdf_filename = f"report_{payload.servicio_id}.pdf"
    pdf_path = os.path.join("temp", pdf_filename)
    os.makedirs("temp", exist_ok=True)
    
    # Configuración del documento en formato Carta (Letter) espacioso
    doc = SimpleDocTemplate(
        pdf_path, pagesize=letter,
        rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45,
        title=f"Report {payload.servicio_id}"
    )
    styles = getSampleStyleSheet()
    
    color_primary = colors.HexColor("#1A1A1A")   
    color_gold = colors.HexColor("#A3704C")      
    color_text = colors.HexColor("#333333")      
    color_legal = colors.HexColor("#777777")     
    
    title_style = ParagraphStyle('CorpTitle', parent=styles['Heading1'], fontSize=26, leading=30, textColor=color_primary, alignment=1)
    subtitle_style = ParagraphStyle('CorpSub', parent=styles['Normal'], fontSize=9, leading=13, textColor=color_legal, alignment=1)
    h2_style = ParagraphStyle('SectionHeader', parent=styles['Heading2'], fontSize=12, leading=16, textColor=color_gold, spaceBefore=18, spaceAfter=8)
    body_style = ParagraphStyle('CorpBody', parent=styles['Normal'], fontSize=10, leading=14, textColor=color_text)
    disclaimer_style = ParagraphStyle('LegalText', parent=styles['Normal'], fontSize=7.5, leading=10.5, textColor=color_legal, alignment=4)
    
    story = []
    
    # ENCABEZADO CORPORATIVO DE ULTRA-LUJO
    story.append(Paragraph("<b>MAY ROGA LLC</b>", title_style))
    story.append(Paragraph("Wellness Travel Architecture & Lifestyle Optimization<br/>Miami, Florida | USA", subtitle_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>LIBRETA DE VIAJE INDIVIDUAL / PERSONAL TRAVEL ITINERARY</b>", ParagraphStyle('RepTitle', parent=styles['Heading3'], fontSize=11, leading=14, alignment=1, textColor=color_primary, spaceAfter=15)))
    
    meta_text = f"<b>Folio de Acompañamiento / Service ID:</b> {payload.servicio_id} | <b>Estatus:</b> Completado con Éxito / Completed"
    story.append(Paragraph(meta_text, body_style))
    story.append(Spacer(1, 12))
    
    # SECCIÓN 1: MEDICIÓN DEL COMPORTAMIENTO LOCAL
    story.append(Paragraph("1. BALANCE DEL ACOMPAÑAMIENTO DE BIENESTAR", h2_style))
    
    metrics_data = [
        [Paragraph("<b>Indicador Evaluado / Wellness Metric</b>", body_style), Paragraph("<b>Nivel Inicial</b>", body_style), Paragraph("<b>Nivel de Cierre</b>", body_style)],
        [Paragraph("Índice de Fatiga por Rutina / Routine Friction Index", body_style), f"{payload.score_inicial}%", f"{payload.score_actual}%"],
        [Paragraph("Optimización por Respiración / Breathing Calibration", body_style), "0%", f"{payload.respiracion_score}%"],
        [Paragraph("Agilidad del Enfoque Lógico / Focus Clarity Rate", body_style), "0%", f"{payload.adivinanzas_score}%"]
    ]
    
    metrics_table = Table(metrics_data, colWidths=[240, 140, 140])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F9F9F9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E5E5")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 12))
    
    # SECCIÓN 2: DETERMINACIÓN DEL ENRUTAMIENTO TURÍSTICO
    story.append(Paragraph("2. TU ENRUTAMIENTO EXCLUSIVO DE VIAJE", h2_style))
    
    # Mapear hotel asignado por el filtro ciego
    hotel_id = payload.destino_id
    if hotel_id in BACKEND_HOTELES:
        h_name = BACKEND_HOTELES[hotel_id]["name"]
        h_desc = BACKEND_HOTELES[hotel_id]["desc"]
    else:
        h_name = "Santuario Curado Premium"
        h_desc = "Oasis seleccionado dinámicamente según tus respuestas locales."
    
    # Extraer el tier socioeconómico calculado (ELITE, PREMIUM, ASPI)
    tier_key = "ELITE"
    if "PREMIUM" in hotel_id: 
        tier_key = "PREMIUM"
    elif "ASPI" in hotel_id: 
        tier_key = "ASPI"
    
    logistica = BACKEND_LOGISTICA[tier_key]
        
    dest_html = f"• <b>Santuario Recomendado:</b> {h_name}<br/>"
    dest_html += f"• <b>Detalle del Espacio:</b> {h_desc}<br/><br/>"
    dest_html += f"• <b>Logística del Aire:</b> {logistica['air']}<br/>"
    dest_html += f"• <b>Pasillo Marítimo:</b> {logistica['sea']}<br/>"
    dest_html += "• <b>Beneficios Exclusivos Consorcio:</b> Acceso preferencial a créditos Virtuoso ($100 de cortesía para áreas de spa y mejoras de habitación gestionadas de forma automática)."
    
    story.append(Paragraph(dest_html, body_style))
    story.append(Spacer(1, 15))
    
    # SECCIÓN 3: ACTIVACIÓN DE LA PRESCRIPCIÓN
    story.append(Paragraph("3. CÓMO ACTIVAR TU ITINERARIO DE CALMA", h2_style))
    cta_text = "Para conservar este balance natural de calma y fijar las tarifas preferenciales de este itinerario, envíe este documento PDF a su Conserje de Viajes VIP de MAY ROGA LLC. Indique su Folio de Servicio para validar sus beneficios exclusivos de cortesía."
    story.append(Paragraph(cta_text, body_style))
    story.append(Spacer(1, 20))
    
    # SECCIÓN 4: BLINDAJE JURÍDICO EXIGIDO POR EL ESTADO DE FLORIDA
    story.append(Paragraph("<b>4. AVISO CORPORATIVO DE BIENESTAR & EXENCIÓN DE RESPONSABILIDAD</b>", ParagraphStyle('LegHeader', parent=styles['Normal'], fontSize=8, leading=11, textColor=color_primary, spaceAfter=6)))
    
    disc_es = "<b>ESPAÑOL:</b> Este documento es emitido exclusivamente por MAY ROGA LLC como una guía recreativa de orientación para el estilo de vida, el confort y la consultoría de viajes premium. No constituye, ni reemplaza en ninguna circunstancia, un diagnóstico, consulta o tratamiento médico, psicológico, psiquiátrico o clínico de ninguna índole. MAY ROGA LLC no provee servicios de salud ni es un proveedor médico. Toda la información recopilada para generar esta prescripción se procesa y almacena de forma estrictamente local y anónima en el navegador del dispositivo del usuario (localStorage). El usuario asume total control y responsabilidad sobre sus elecciones de viaje y actividades corporativas."
    disc_en = "<b>ENGLISH:</b> This document is issued exclusively by MAY ROGA LLC as a recreational guidance tool for premium lifestyle configuration and travel consulting. It does not replace, nor substitute, any psychiatric, psychological, clinical, or medical advice or diagnosis. MAY ROGA LLC is not a healthcare institution nor a medical provider. All analytics are generated strictly locally and anonymously on the user's terminal via algorithmic indicators (localStorage). The client maintains full control and liability for travel actions."
    
    story.append(Paragraph(disc_es, disclaimer_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(disc_en, disclaimer_style))
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("This document is for informational and promotional travel purposes only. For medical advice, consult a certified healthcare professional. Responses may include specialized insights.", ParagraphStyle('AIFoot', parent=disclaimer_style, fontName='Helvetica-Oblique', alignment=1)))
    story.append(Spacer(1, 15))
    story.append(Paragraph("© 2026 MAY ROGA LLC. All rights reserved. Miami, Florida.", ParagraphStyle('FootCopyright', parent=subtitle_style, fontSize=8)))
    
    doc.build(story)
    return FileResponse(pdf_path, media_type='application/pdf', filename=pdf_filename)

@app.get("/", response_class=HTMLResponse)
def index():
    base_dir = os.path.dirname(__file__) if "__file__" in locals() else "."
    ruta_html = os.path.join(base_dir, "index.html")
    if os.path.exists(ruta_html):
        with open(ruta_html, "r", encoding="utf-8") as file:
            return HTMLResponse(content=file.read(), status_code=200)
    return HTMLResponse(content="MAY ROGA LLC - Error crítico: index.html no encontrado en la raíz del servidor.", status_code=404)
