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

# RESPALDO INTERNO (FALLBACK) EN CASO DE DISCREPANCIAS EN LOS JSON
BACKEND_EVALUATION = {
    "VAR1_MEJORIA_GENERAL": { "color": "#3D9970", "es": "ARMONÍA LOGRADA", "en": "HARMONY ACHIEVED", "body_es": "Tu Figura Humana muestra una respuesta excepcional al estímulo de bienestar de 15 minutos. El Círculo de Desprendimiento ha regresado al centro geométrico del Triángulo de Balance.", "body_en": "Your Vitality Silhouette displays an exceptional response to the 15-minute wellness alignment. The Center Circle has successfully anchored back into the core of your Balance Triangle." },
    "VAR2_IGUAL_ESTACIONARIO": { "color": "#C5A059", "es": "BALANCE ESTACIONARIO", "en": "STATIONARY BALANCE", "body_es": "Tu Figura Humana se mantiene en una meseta de energía adaptativa. Tras los 15 minutos de servicio, el Círculo de Desprendimiento sigue inclinado hacia uno de los vértices del Triángulo.", "body_en": "Your Vitality Silhouette remains on an adaptive energy plateau. Following the 15-minute service, the Center Circle remains tilted toward one of the Triangle's vertices." },
    "VAR3_EMPEORAMIENTO_SATURACION": { "color": "#E04F4F", "es": "SATURACIÓN ACUMULADA", "en": "ACCUMULATED SATURATION", "body_es": "Tu Figura Humana refleja una resistencia activa a la desconexión digital. Los datos recolectados localmente muestran que el Círculo de Desprendimiento ha sido desplazado con fuerza.", "body_en": "Your Vitality Silhouette reflects an active resistance to digital disconnection. The local metrics indicate that the Center Circle has been forcefully pushed to the outer edge." }
}

BACKEND_DESTINATIONS = {
    "HOT-ELITE-001": {"es": "Eden Roc Cap Cana (Punta Cana)", "en": "Eden Roc Cap Cana (Punta Cana)", "desc_es": "Villas de ultra-lujo con piscinas privadas y club de playa privado.", "desc_en": "Ultra-luxury villas with private pools and a private beach club."},
    "HOT-PREM-001": {"es": "Grand Velas Riviera Maya (México)", "en": "Grand Velas Riviera Maya (Mexico)", "desc_es": "Todo incluido premium con circuito hidrotermal de spa.", "desc_en": "Premium all-inclusive featuring an immersive hydrothermal spa."},
    "HOT-ASPI-001": {"es": "Secrets Royal Beach Punta Cana", "en": "Secrets Royal Beach Punta Cana", "desc_es": "Oasis todo incluido solo para adultos frente al mar Caribe.", "desc_en": "Adults-only all-inclusive oasis facing the Caribbean sea."}
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
    
    # ENCABEZADO CORPORATIVO
    story.append(Paragraph("<b>MAY ROGA LLC</b>", title_style))
    story.append(Paragraph("Wellness Travel Architecture & Lifestyle Optimization<br/>Miami, Florida | USA", subtitle_style))
    story.append(Spacer(1, 15))
    
    is_es = payload.lang.upper() == "ES"
    
    t_report = "REPORTE DE BALANCE DE VITALIDAD Y PRESCRIPCIÓN DE VIAJE" if is_es else "VITALITY BALANCE REPORT & TRAVEL PRESCRIPTION"
    story.append(Paragraph(f"<b>{t_report}</b>", ParagraphStyle('RepTitle', parent=styles['Heading3'], fontSize=11, leading=14, alignment=1, textColor=color_primary, spaceAfter=15)))
    
    meta_text = f"<b>Folio de Servicio / Service ID:</b> {payload.servicio_id} | <b>Status:</b> Completado Localmente / Locally Completed"
    story.append(Paragraph(meta_text, body_style))
    story.append(Spacer(1, 12))
    
    # SECCIÓN 1: DIAGNÓSTICO MATEMÁTICO DEL CRM
    s1_title = "1. DIAGNÓSTICO DEL CRM WELLNESS / WELLNESS CRM DIAGNOSTIC"
    story.append(Paragraph(s1_title, h2_style))
    
    metrics_data = [
        [Paragraph("<b>Métrica de Estilo de Vida / Lifestyle Metric</b>", body_style), Paragraph("<b>Inicial</b>", body_style), Paragraph("<b>Actual (14:30)</b>", body_style)],
        [Paragraph("Índice de Ritmo de Vida / Lifestyle Pace Index", body_style), f"{payload.score_inicial}%", f"{payload.score_actual}%"],
        [Paragraph("Reserva Energética / Energy Reserves", body_style), f"{payload.score_inicial}%", f"{payload.respiracion_score}%"],
        [Paragraph("Flujo Creativo / Creative Flow", body_style), f"{payload.score_inicial}%", f"{payload.adivinanzas_score}%"]
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
    
    # 🌟 MAPEO INDESTRUCTIBLE DE LA FIGURA HUMANA
    var_key = payload.variante if payload.variante in BACKEND_EVALUATION else "VAR2_IGUAL_ESTACIONARIO"
    fallback_node = BACKEND_EVALUATION[var_key]
    titulo_estado = fallback_node["es"] if is_es else fallback_node["en"]
    cuerpo_estado = fallback_node["body_es"] if is_es else fallback_node["body_en"]
    
    # Intentar lectura asíncrona local desde la carpeta JSON
    base_dir = os.path.dirname(__file__)
    eval_file_path = os.path.join(base_dir, "static", "json", "evaluacion.json")
    if os.path.exists(eval_file_path):
        try:
            with open(eval_file_path, "r", encoding="utf-8") as f:
                data_eval = json.load(f)
                if payload.variante in data_eval:
                    node_eval = data_eval[payload.variante]
                    titulo_estado = node_eval.get("status_es" if is_es else "status_en", titulo_estado)
                    cuerpo_estado = node_eval.get("body_es" if is_es else "body_en", cuerpo_estado)
        except Exception:
            pass

    story.append(Paragraph(f"<b>ESTADO DE VITALIDAD / VITALITY SILHOUETTE STATUS:</b>", ParagraphStyle('StateH', parent=body_style, fontSize=10, textColor=color_primary)))
    story.append(Paragraph(f"👉 <u>{titulo_estado}</u>", ParagraphStyle('StateSub', parent=body_style, fontSize=10, textColor=color_gold, spaceBefore=4, spaceAfter=4)))
    story.append(Paragraph(cuerpo_estado, body_style))
    story.append(Spacer(1, 15))
    
    # SECCIÓN 2: PRESCRIPCIÓN DEL ITINERARIO GLOBAL
    s2_title = "2. ITINERARIO TURÍSTICO DE COMPENSACIÓN / COMPENSATORY TRAVEL ITINERARY"
    story.append(Paragraph(s2_title, h2_style))
    
    # Mapeo de Destino con Respaldo Inteligente contra errores de Clave
    dest_key = payload.destino_id
    if dest_key in BACKEND_DESTINATIONS:
        dest_name = BACKEND_DESTINATIONS[dest_key]["es" if is_es else "en"]
        dest_desc = BACKEND_DESTINATIONS[dest_key]["desc_es" if is_es else "desc_en"]
    else:
        dest_name = payload.destino_id
        dest_desc = "Curated luxury corridor requested dynamically via local selection."
        
    dest_file_path = os.path.join(base_dir, "static", "json", "destinos.json")
    if os.path.exists(dest_file_path):
        try:
            with open(dest_file_path, "r", encoding="utf-8") as f:
                data_dest = json.load(f)
                target_dest = next((d for d in data_dest if d["id"] == payload.destino_id), None)
                if target_dest:
                    dest_name = target_dest["name_es"] if is_es else target_dest["name_en"]
                    dest_desc = target_dest["desc_es"] if is_es else target_dest["desc_en"]
    except Exception:
        pass

    # Estructuración limpia de strings con formato HTML compatible para ReportLab
    dest_html = f"<b>Santuario Asignado / Curated Oasis:</b> {dest_name}<br/><br/>"
    dest_html += f"<b>Detalle del Entorno / Wellness Profile:</b> {dest_desc}<br/><br/>"
    dest_html += "• <b>Logística Aérea / Air Travel:</b> Premium routing synchronized from Miami Int. (MIA). Flight details locked against friction protocols.<br/><br/>"
    dest_html += "• <b>Estatus de Reserva / Consortium Privileges:</b> Eligible for Virtuoso/Signature luxury benefits ($100 resort credits and priority room upgrades processed locally via credentials)."
    
    story.append(Paragraph(dest_html, body_style))
    story.append(Spacer(1, 15))

    # SECCIÓN 3: ACTIVACIÓN COMERCIAL
    s3_title = "3. ACTIVACIÓN DE PRESCRIPCIÓN COMERCIAL / BOOKING GATEWAY"
    story.append(Paragraph(s3_title, h2_style))
    
    cta_text = "Para conservar este balance natural y fijar las tarifas exclusivas de este itinerario, póngase en contacto con su Conserje de Viajes corporativo. Presente este reporte digital en formato PDF junto con el Folio de Servicio para procesar los beneficios corporativos." if is_es else "To consolidate this natural balance and lock down the exclusive rates of this itinerary, contact your corporate Travel Concierge. Present this digital PDF report along with the attached Service ID to unlock your custom benefits."
    story.append(Paragraph(cta_text, body_style))
    story.append(Spacer(1, 20))

    # SECCIÓN 4: BLINDAJE JURÍDICO
    story.append(Paragraph("4. AVISO LEGAL Y EXENCIÓN DE RESPONSABILIDAD / LEGAL DISCLAIMER", ParagraphStyle('LegHeader', parent=styles['Normal'], fontSize=8, leading=11, textColor=color_primary, spaceAfter=6)))
    
    disc_es = "ESPAÑOL: Este documento es emitido exclusivamente por MAY ROGA LLC como una herramienta de orientación para el estilo de vida, el bienestar general y la consultoría de viajes premium. No constituye, ni reemplaza, un diagnóstico médico, psiquiátrico, psicológico o clínico de ninguna índole. MAY ROGA LLC no es una institución de salud ni un proveedor médico. Los datos utilizados para generar este reporte se procesan de forma estrictamente local y anónima en el dispositivo del usuario mediante algoritmos de comportamiento digital (localStorage). El usuario asume total responsabilidad sobre las decisiones de viaje y actividades derivadas de este reporte."
    disc_en = "ENGLISH: This document is issued exclusively by MAY ROGA LLC as a guidance tool for lifestyle enhancement, general wellness, and premium travel consulting. It does not constitute, nor does it replace, a medical, psychiatric, psychological, or clinical diagnosis of any kind. MAY ROGA LLC is not a healthcare institution nor a medical provider. The data utilized to generate this report is processed and stored strictly locally and anonymously on the user's device via digital behavior algorithms (localStorage). The user assumes full and sole responsibility for travel decisions and activities derived from this report."
    
    story.append(Paragraph(disc_es, disclaimer_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(disc_en, disclaimer_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("This document is for informational and promotional travel purposes only. For medical advice or diagnosis, consult a certified healthcare professional. AI responses may include mistakes.", ParagraphStyle('AIFoot', parent=disclaimer_style, fontName='Helvetica-Oblique', alignment=1)))
    story.append(Spacer(1, 15))
    story.append(Paragraph("© 2026 MAY ROGA LLC. All rights reserved. Miami, Florida.", ParagraphStyle('FootCopyright', parent=subtitle_style, fontSize=8)))
    
    doc.build(story)
    
    return FileResponse(pdf_path, media_type='application/pdf', filename=pdf_filename)

@app.get("/", response_class=HTMLResponse)
def index():
    base_dir = os.path.dirname(__file__)
    ruta_html = os.path.join(base_dir, "index.html")
    
    if os.path.exists(ruta_html):
        with open(ruta_html, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
            
    return HTMLResponse(content="<h1>MAY ROGA LLC</h1><p>Error crítico: index.html no encontrado en la raíz del servidor.</p>", status_code=404)

    
