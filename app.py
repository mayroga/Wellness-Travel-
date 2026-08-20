# ====================================================================================================
#                                    MAY ROGA LLC
#                       Wellness Travel Architecture & Lifestyle Optimization
#                                   Miami, Florida | USA
#                               PRODUCTION BACKEND - AUDITED
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
    version="2.0.0"
)

# MONTAR LA CARPETA ESTÁTICA SÓLO SI EXISTE EN EL DISCO
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# 🌟 DICCIONARIO BILINGÜE DE ALTA PRECISIÓN Y TONO EJECUTIVO
DICTIONARY_BILINGUAL = {
    "ES": {
        "doc_title": "PASAPORTE DE SINTONÍA Y ITINERARIO PRIVADO",
        "folio": "Folio de Operación",
        "status": "Estado: Sintonía Concluida",
        "sec1_title": "1. MÉTRICAS DE ENTORNO Y CALIBRACIÓN",
        "m1": "Parámetro Evaluado", "m2": "Línea Base", "m3": "Estado Final",
        "m_pace": "Índice de Fricción por Rutina",
        "m_breathe": "Eficiencia de Sintonía Respiratoria",
        "m_logic": "Velocidad de Procesamiento Lógico",
        "sec2_title": "2. ENRUTAMIENTO EXCLUSIVO DE SALIDA (HOST AGENCY)",
        "stay_lbl": "Santuario Curado",
        "desc_lbl": "Especificación del Entorno",
        "air_lbl": "Aviación Ejecutiva",
        "sea_lbl": "Corredor Náutico",
        "consorcio": "Privilegios Consorcio Privado: Acceso automático a cortesías Virtuoso y créditos de resort por $100 gestionados mediante el folio de servicio.",
        "sec3_title": "3. ACTIVACIÓN DE ITINERARIO",
        "cta": "Para fijar las tarifas preferenciales y coordinar los traslados de este itinerario, remita este documento digital a su Conserje Ejecutivo de MAY ROGA LLC.",
        "sec4_title": "4. AVISO CORPORATIVO Y EXENCIÓN DE RESPONSABILIDAD",
        "disclaimer": "Emitido por MAY ROGA LLC como una directriz recreativa de consultoría de viajes de alta gama y estilo de vida. No constituye asesoría médica, clínica o terapéutica. Toda la información analizada opera de forma local y anónima en el navegador del usuario (localStorage). El usuario asume total autonomía y responsabilidad sobre sus decisiones.",
        "ai_foot": "Documento exclusivo para fines promocionales e informativos de viajes privados."
    },
    "EN": {
        "doc_title": "PRIVATE ITINERARY & WELLNESS PASSPORT",
        "folio": "Operation Folio",
        "status": "Status: Tuning Completed",
        "sec1_title": "1. ENVIRONMENT METRICS & CALIBRATION",
        "m1": "Parameter Evaluated", "m2": "Baseline", "m3": "Final State",
        "m_pace": "Routine Friction Index",
        "m_breathe": "Respiration Tuning Efficiency",
        "m_logic": "Logical Processing Speed",
        "sec2_title": "2. EXCLUSIVE GATEWAY ROUTING (HOST AGENCY)",
        "stay_lbl": "Curated Sanctuary",
        "desc_lbl": "Environment Specification",
        "air_lbl": "Executive Aviation",
        "sea_lbl": "Nautical Corridor",
        "consorcio": "Private Consortium Privileges: Automatic access to Virtuoso benefits and $100 resort credits managed securely via service folio credentials.",
        "sec3_title": "3. ITINERARY ACTIVATION",
        "cta": "To lock in preferential rates and coordinate your logistics, transmit this digital document to your dedicated MAY ROGA LLC Executive Concierge.",
        "sec4_title": "4. CORPORATE DISCLAIMER & LIABILITY WAIVER",
        "disclaimer": "Issued by MAY ROGA LLC as a recreational guidance tool for luxury travel and lifestyle consulting. Does not constitute medical, clinical, or therapeutic advice. All parameters are processed locally and anonymously via browser storage (localStorage). The user assumes full sole responsibility for their travel decisions.",
        "ai_foot": "Document strictly for private promotional and travel planning purposes."
    }
}

BACKEND_HOTELES = {
    "H1": {
        "es": {"name": "Eden Roc Cap Cana (Punta Cana)", "desc": "Bungalows de ultra-lujo con alberca propia, club de playa privado y aislamiento acústico total."},
        "en": {"name": "Eden Roc Cap Cana (Dominican Republic)", "desc": "Ultra-luxury standalone bungalows with private pools, beach clubs, and total acoustic insulation."}
    },
    "H2": {
        "es": {"name": "Amanera Resort (Playa Grande)", "desc": "Casitas de cristal y ebanistería minimalista suspendidas sobre acantilados masivos frente al mar."},
        "en": {"name": "Amanera Resort (Playa Grande)", "desc": "Minimalist glass casitas perched on massive ocean cliffs blending with pure Caribbean jungle."}
    },
    "H3": {
        "es": {"name": "Grand Velas Riviera Maya (México)", "desc": "Suites de alta gama acompañadas de un circuito hidrotermal de spa guiado de 7 etapas."},
        "en": {"name": "Grand Velas Riviera Maya (Mexico)", "desc": "Upscale beachfront suites paired with an immersive 7-stage guided hydrothermal spa circuit."}
    }
}

BACKEND_LOGISTICA = {
    "ELITE": {
        "es": {
            "air": "Gulfstream G650 Chárter Privado directo desde la terminal VIP FBO de Miami.",
            "sea": "The Ritz-Carlton Yacht Collection Suite de popa con terraza privada sobre el océano."
        },
        "en": {
            "air": "Private Aviation Charter (Gulfstream G650) flying direct from Miami's VIP FBO private terminal.",
            "sea": "The Ritz-Carlton Yacht Collection ultra-luxury terrace suite with private ocean overviews."
        }
    },
    "PREMIUM": {
        "es": {
            "air": "Clase Ejecutiva Flagship Suite con asientos Lie-Flat totalmente reclinables en vuelo directo.",
            "sea": "Celebrity Cruises (The Retreat Enclave) con solárium y restaurante de autor VIP."
        },
        "en": {
            "air": "Flagship Business Class Non-Stop Suite configured with fully reclinable Lie-Flat premium seating.",
            "sea": "Celebrity Cruises (The Retreat Private Enclave) granting VIP sundeck access and fine dining."
        }
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
    os.makedirs("temp", exist_ok=True)
    pdf_path = os.path.join("temp", pdf_filename)
    
    # 📏 Ancho útil exacto de 522 puntos para carta con márgenes de 45pt
    doc = SimpleDocTemplate(
        pdf_path, pagesize=letter,
        rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45,
        title=f"MayRoga Passport {payload.servicio_id}"
    )
    styles = getSampleStyleSheet()
    
    color_primary = colors.HexColor("#0D0D0F")   # Negro Obsidiana
    color_gold = colors.HexColor("#C5A059")      # Oro Champaña
    color_text = colors.HexColor("#2C2C2C")      # Gris Oscuro Corporativo
    color_legal = colors.HexColor("#7A7A7A")     # Gris Atenuado Legal
    color_bg_table = colors.HexColor("#FAFAFA")  # Fondo Suave Tablas
    
    title_style = ParagraphStyle('CorpTitle', parent=styles['Heading1'], fontSize=22, leading=26, textColor=color_primary, alignment=1, fontName="Helvetica-Bold")
    subtitle_style = ParagraphStyle('CorpSub', parent=styles['Normal'], fontSize=8.5, leading=12, textColor=color_legal, alignment=1, fontName="Helvetica")
    h2_style = ParagraphStyle('SectionHeader', parent=styles['Heading2'], fontSize=11, leading=14, textColor=color_gold, spaceBefore=14, spaceAfter=6, fontName="Helvetica-Bold")
    body_style = ParagraphStyle('CorpBody', parent=styles['Normal'], fontSize=9.5, leading=13.5, textColor=color_text, fontName="Helvetica")
    disclaimer_style = ParagraphStyle('LegalText', parent=styles['Normal'], fontSize=7, leading=9.5, textColor=color_legal, alignment=4, fontName="Helvetica")
    
    story = []
    
    lang_key = "EN" if payload.lang.upper() == "EN" else "ES"
    lang_map = DICTIONARY_BILINGUAL[lang_key]
    
    # ENCABEZADO MINIMALISTA DE ALTA GAMA
    story.append(Paragraph("<b>MAY ROGA LLC</b>", title_style))
    story.append(Paragraph("Wellness Travel Architecture & Lifestyle Optimization | Miami, Florida", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"{lang_map['doc_title']}", ParagraphStyle('RepTitle', parent=styles['Heading3'], fontSize=10, leading=13, alignment=1, textColor=color_primary, spaceAfter=10, fontName="Helvetica-Bold")))
    
    meta_text = f"<b>{lang_map['folio']}</b>: {payload.servicio_id} &nbsp;|&nbsp; <b>{lang_map['status']}</b>"
    story.append(Paragraph(meta_text, ParagraphStyle('MetaLine', parent=body_style, fontSize=9, alignment=1, textColor=color_gold)))
    story.append(Spacer(1, 10))
    
    # SECCIÓN 1: MÉTRICAS
    story.append(Paragraph(lang_map['sec1_title'], h2_style))
    metrics_data = [
        [Paragraph(f"<b>{lang_map['m1']}</b>", body_style), Paragraph(f"<b>{lang_map['m2']}</b>", body_style), Paragraph(f"<b>{lang_map['m3']}</b>", body_style)],
        [Paragraph(lang_map['m_pace'], body_style), f"{payload.score_inicial}%", f"{payload.score_actual}%"],
        [Paragraph(lang_map['m_breathe'], body_style), "0%", f"{payload.respiracion_score}%"],
        [Paragraph(lang_map['m_logic'], body_style), "0%", f"{payload.adivinanzas_score}%"]
    ]
    
    metrics_table = Table(metrics_data, colWidths=[262, 130, 130])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), color_bg_table),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#EAEAEA")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 10))
    
    # SECCIÓN 2: ENRUTAMIENTO
    story.append(Paragraph(lang_map['sec2_title'], h2_style))
    hotel_id = payload.destino_id
    if hotel_id in BACKEND_HOTELES:
        h_name = BACKEND_HOTELES[hotel_id][lang_key.lower()]["name"]
        h_desc = BACKEND_HOTELES[hotel_id][lang_key.lower()]["desc"]
    else:
        h_name = "Eden Roc Cap Cana Enclave" if lang_key == "EN" else "Eden Roc Cap Cana (Punta Cana)"
        h_desc = "Premium custom oasis configured dynamically based on your behavioral profile vectors."
        
    tier_key = "ELITE" if "ELITE" in payload.variante or payload.score_inicial < 45 else "PREMIUM"
    logistica = BACKEND_LOGISTICA.get(tier_key, BACKEND_LOGISTICA["ELITE"])[lang_key.lower()]
    
    dest_html = f"• <b>{lang_map['stay_lbl']}</b>: {h_name}<br/>"
    dest_html += f"• <b>{lang_map['desc_lbl']}</b>: {h_desc}<br/>"
    dest_html += f"• <b>{lang_map['air_lbl']}</b>: {logistica['air']}<br/>"
    dest_html += f"• <b>{lang_map['sea_lbl']}</b>: {logistica['sea']}<br/><br/>"
    dest_html += f"<i>{lang_map['consorcio']}</i>"
    
    story.append(Paragraph(dest_html, body_style))
    story.append(Spacer(1, 10))
    
    # SECCIÓN 3: ACTIVACIÓN
    story.append(Paragraph(lang_map['sec3_title'], h2_style))
    story.append(Paragraph(lang_map['cta'], body_style))
    story.append(Spacer(1, 12))
    
    # SECCIÓN 4: BLINDAJE JURÍDICO Y EXENCIÓN DE RESPONSABILIDAD
    story.append(Paragraph(f"<b>{lang_map['sec4_title']}</b>", ParagraphStyle('LegHeader', parent=styles['Normal'], fontSize=7.5, leading=10, textColor=color_primary, spaceAfter=4, fontName="Helvetica-Bold")))
    story.append(Paragraph(lang_map['disclaimer'], disclaimer_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph(lang_map['ai_foot'], ParagraphStyle('AIFoot', parent=disclaimer_style, fontName='Helvetica-Oblique', alignment=1)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("© 2026 MAY ROGA LLC. All rights reserved. Miami, Florida.", ParagraphStyle('FootCopyright', parent=subtitle_style, fontSize=7.5)))
    
    doc.build(story)
    return FileResponse(pdf_path, media_type='application/pdf', filename=pdf_filename)

@app.get("/", response_class=HTMLResponse)
def index():
    base_dir = os.path.dirname(__file__)
    ruta_html = os.path.join(base_dir, "index.html")
    if os.path.exists(ruta_html):
        with open(ruta_html, "r", encoding="utf-8") as file:
            return HTMLResponse(content=file.read(), status_code=200)
    return HTMLResponse(content="MAY ROGA LLC Terminal Error: index.html not found.", status_code=404)
