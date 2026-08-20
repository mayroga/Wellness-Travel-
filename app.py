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

# 🌟 TRADUCCIÓN ESPEJO INDESTRUCTIBLE PARA LOS REPORTES EN AMBOS IDIOMAS
DICTIONARY_BILINGUAL = {
    "ES": {
        "doc_title": "LIBRETA DE VIAJE INDIVIDUAL",
        "folio": "Folio de Acompañamiento",
        "status": "Estatus: Completado con Éxito",
        "sec1_title": "1. BALANCE DEL ACOMPAÑAMIENTO DE BIENESTAR",
        "m1": "Indicador Evaluado", "m2": "Nivel Inicial", "m3": "Nivel de Cierre",
        "m_pace": "Índice de Fatiga por Rutina",
        "m_breathe": "Optimización por Respiración",
        "m_logic": "Agilidad del Enfoque Lógico",
        "sec2_title": "2. TU ENRUTAMIENTO EXCLUSIVO DE VIAJE (CAMINO HOST AGENT)",
        "stay_lbl": "Santuario Recomendado",
        "desc_lbl": "Detalle del Espacio",
        "air_lbl": "Logística del Aire",
        "sea_lbl": "Pasillo Marítimo",
        "consorcio": "Beneficios Exclusivos Consorcio: Acceso preferencial a créditos de cortesía Virtuoso ($100 para spa y mejoras de habitación gestionadas de forma automática mediante tu folio).",
        "sec3_title": "3. CÓMO ACTIVAR TU ITINERARIO DE CALMA",
        "cta": "Para conservar este balance natural de calma y fijar las tarifas preferenciales de este itinerario, envíe este documento PDF a su Conserje de Viajes VIP de MAY ROGA LLC. Indique su Folio de Servicio para validar sus beneficios de cortesía.",
        "sec4_title": "4. AVISO CORPORATIVO DE BIENESTAR & EXENCIÓN DE RESPONSABILIDAD",
        "disclaimer": "Este documento es emitido exclusivamente por MAY ROGA LLC como una guía recreativa de orientación para el estilo de vida, el confort y la consultoría de viajes premium. No constituye, ni reemplaza en ninguna circunstancia, un diagnóstico, consulta o tratamiento médico, psicológico, psiquiátrico o clínico de ninguna índole. MAY ROGA LLC no provee servicios de salud ni es un proveedor médico. Toda la información recopilada para generar esta prescripción se procesa y almacena de forma estrictamente local y anónima en el navegador del dispositivo del usuario (localStorage). El usuario asume total control y responsabilidad sobre sus elecciones de viaje.",
        "ai_foot": "Este documento es estrictamente para fines informativos y promocionales de viajes de lujo. Para asesoramiento profesional o médico, consulte a un especialista certificado. Las respuestas de asistencia automatizada pueden contener imprecisiones."
    },
    "EN": {
        "doc_title": "PERSONAL TRAVEL ITINERARY REPORT",
        "folio": "Service ID Folio",
        "status": "Status: Successfully Completed",
        "sec1_title": "1. WELLNESS BALANCE & ENGAGEMENT OVERVIEW",
        "m1": "Wellness Metric Evaluated", "m2": "Initial Baseline", "m3": "Closing Balance",
        "m_pace": "Routine Friction & Pace Index",
        "m_breathe": "Breathing Calibration Rate",
        "m_logic": "Focus Clarity & Logic Rate",
        "sec2_title": "2. YOUR EXCLUSIVE TRAVEL ROUTING (HOST AGENCY GATEWAY)",
        "stay_lbl": "Curated Luxury Oasis",
        "desc_lbl": "Wellness Profile Detail",
        "air_lbl": "Premium Air Logistics",
        "sea_lbl": "Maritime Cruise Corridor",
        "consorcio": "Exclusive Consortium Privileges: Eligible for complimentary Virtuoso/Signature luxury benefits ($100 resort credits for relaxation therapies and priority room upgrades processed automatically via credentials).",
        "sec3_title": "3. HOW TO SECURE AND BOOK YOUR ITINERARY",
        "cta": "To consolidate this natural state of calm and lock in the exclusive promotional rates of this itinerary, please forward this digital PDF document to your dedicated MAY ROGA LLC Travel Concierge. Reference your Service ID to unlock premium amenities.",
        "sec4_title": "4. CORPORATE LIFESTYLE DISCLAIMER & LIABILITY WAIVER",
        "disclaimer": "This document is issued exclusively by MAY ROGA LLC as a recreational guidance and orientation tool for luxury lifestyle enhancement and custom travel consulting. It does not constitute, nor does it substitute under any circumstances, a clinical, psychiatric, psychological, or medical diagnosis, advice, or therapy. MAY ROGA LLC is not a healthcare institution nor a certified medical provider. All digital metrics gathered to compile this travel passport are processed strictly locally and anonymously on the user's browser terminal via local behavior algorithms (localStorage). The user assumes full and sole responsibility for travel decisions.",
        "ai_foot": "This document is for informational and promotional travel purposes only. For clinical or medical advice, consult a certified healthcare professional. Automated assistance responses may include machine-generated errors."
    }
}

# DATA DE RESPALDO BILINGÜE SINCRO CON TU INDEX.HTML
BACKEND_HOTELES = {
    "H1": {
        "es": {"name": "Eden Roc Cap Cana (República Dominicana)", "desc": "Bungalows de ultra-lujo con alberca propia, jardín privado y aislamiento acústico absoluto."},
        "en": {"name": "Eden Roc Cap Cana (Dominican Republic)", "desc": "Ultra-luxury standalone bungalows with private pools, zen gardens, and total acoustic insulation."}
    },
    "H2": {
        "es": {"name": "Amanera Resort (Playa Grande)", "desc": "Casitas de ebanistería minimalista y cristal suspendidas sobre los acantilados marinos del Caribe."},
        "en": {"name": "Amanera Resort (Playa Grande)", "desc": "Minimalist Zen glass casitas perched beautifully above massive ocean-facing cliffs."}
    },
    "H3": {
        "es": {"name": "Grand Velas Riviera Maya (México)", "desc": "Suites presidenciales de alta gama con un circuito hidrotermal guiado de spa de 7 etapas."},
        "en": {"name": "Grand Velas Riviera Maya (Mexico)", "desc": "High-end oceanfront presidential suites paired with an immersive 7-stage guided hydrothermal circuit."}
    },
    "H4": {
        "es": {"name": "Secrets Impression Moxché", "desc": "Oasis premium solo para adultos con rooftops infinity y mayordomía dedicada las 24 horas."},
        "en": {"name": "Secrets Impression Moxché Enclave", "desc": "Adults-only rustic-chic sanctuary boasting endless rooftop infinity views and dedicated 24/7 butler services."}
    },
    "H5": {
        "es": {"name": "Secrets Royal Beach Punta Cana", "desc": "Complejo vacacional todo incluido de confort con swim-up suites frente a las arenas blancas de Bávaro."},
        "en": {"name": "Secrets Royal Beach Punta Cana", "desc": "Premium all-inclusive beach resort offering upscale swim-up suites directly fronting the white sands of Bávaro."}
    }
}

BACKEND_LOGISTICA = {
    "ELITE": {
        "es": {
            "air": "Gulfstream G650 Chárter Privado directo sin filas desde la terminal VIP FBO de Miami.",
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
    },
    "ASPI": {
        "es": {
            "air": "Cabina Principal Confort+ en vuelo directo con prioridad de chequeo y equipaje express.",
            "sea": "Royal Caribbean International (Solarium Adults-Only Retreat) libre de ruidos."
        },
        "en": {
            "air": "Main Cabin Comfort Plus direct booking with priority boarding and express baggage logistics.",
            "sea": "Royal Caribbean International Solarium Adults-Only Retreat fully shielded from ambient noise."
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
    
    # DETECTAR IDIOMA SELECCIONADO POR EL BOTÓN DEL CLIENTE (ES / EN)
    lang_key = "EN" if payload.lang.upper() == "EN" else "ES"
    lang_map = DICTIONARY_BILINGUAL[lang_key]
    
    # ENCABEZADO CORPORATIVO
    story.append(Paragraph("MAY ROGA LLC", title_style))
    story.append(Paragraph("Wellness Travel Architecture & Lifestyle Optimization<br/>Miami, Florida | USA", subtitle_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph(f"{lang_map['doc_title']}", ParagraphStyle('RepTitle', parent=styles['Heading3'], fontSize=11, leading=14, alignment=1, textColor=color_primary, spaceAfter=15)))
    
    meta_text = f"{lang_map['folio']}: {payload.servicio_id} | {lang_map['status']}"
    story.append(Paragraph(meta_text, body_style))
    story.append(Spacer(1, 12))
    
    # SECCIÓN 1
    story.append(Paragraph(lang_map['sec1_title'], h2_style))
    metrics_data = [
        [Paragraph(f"<b>{lang_map['m1']}</b>", body_style), Paragraph(f"<b>{lang_map['m2']}</b>", body_style), Paragraph(f"<b>{lang_map['m3']}</b>", body_style)],
        [Paragraph(lang_map['m_pace'], body_style), f"{payload.score_inicial}%", f"{payload.score_actual}%"],
        [Paragraph(lang_map['m_breathe'], body_style), "0%", f"{payload.respiracion_score}%"],
        [Paragraph(lang_map['m_logic'], body_style), "0%", f"{payload.adivinanzas_score}%"]
    ]
    
    metrics_table = Table(metrics_data, colWidths=[302, 110, 110])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F9F9F9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E5E5")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 12))
    
    # SECCIÓN 2
    story.append(Paragraph(lang_map['sec2_title'], h2_style))
    hotel_id = payload.destino_id
    if hotel_id in BACKEND_HOTELES:
        h_name = BACKEND_HOTELES[hotel_id][lang_key.lower()]["name"]
        h_desc = BACKEND_HOTELES[hotel_id][lang_key.lower()]["desc"]
    else:
        h_name = "Eden Roc Cap Cana Enclave" if lang_key == "EN" else "Eden Roc Cap Cana (Punta Cana)"
        h_desc = "Premium custom oasis configured dynamically."
        
    tier_key = "ELITE"
    if "PREMIUM" in payload.variante or payload.score_inicial >= 40:
        tier_key = "PREMIUM"
    elif "ASPI" in payload.variante:
        tier_key = "ASPI"
        
    logistica = BACKEND_LOGISTICA.get(tier_key, BACKEND_LOGISTICA["ELITE"])[lang_key.lower()]
    
    dest_html = f"• <b>{lang_map['stay_lbl']}</b>: {h_name}<br/>"
    dest_html += f"• <b>{lang_map['desc_lbl']}</b>: {h_desc}<br/><br/>"
    dest_html += f"• <b>{lang_map['air_lbl']}</b>: {logistica['air']}<br/>"
    dest_html += f"• <b>{lang_map['sea_lbl']}</b>: {logistica['sea']}<br/>"
    dest_html += f"• <b>{lang_map['consorcio']}</b>"
    
    story.append(Paragraph(dest_html, body_style))
    story.append(Spacer(1, 15))
    
    # SECCIÓN 3
    story.append(Paragraph(lang_map['sec3_title'], h2_style))
    story.append(Paragraph(lang_map['cta'], body_style))
    story.append(Spacer(1, 20))
    
    # SECCIÓN 4
    story.append(Paragraph(f"<b>{lang_map['sec4_title']}</b>", ParagraphStyle('LegHeader', parent=styles['Normal'], fontSize=8, leading=11, textColor=color_primary, spaceAfter=6)))
    story.append(Paragraph(lang_map['disclaimer'], disclaimer_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(lang_map['ai_foot'], ParagraphStyle('AIFoot', parent=disclaimer_style, fontName='Helvetica-Oblique', alignment=1)))
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("© 2026 MAY ROGA LLC. All rights reserved. Miami, Florida.", ParagraphStyle('FootCopyright', parent=subtitle_style, fontSize=8)))
    
    doc.build(story)
    return FileResponse(pdf_path, media_type='application/pdf', filename=pdf_filename)

@app.get("/", response_class=HTMLResponse)
def index():
    base_dir = os.path.dirname(__file__)
    ruta_html = os.path.join(base_dir, "index.html")
    if os.path.exists(ruta_html):
        with open(ruta_html, "r", encoding="utf-8") as file:
            return HTMLResponse(content=file.read(), status_code=200)
    return HTMLResponse(content="MAY ROGA LLC Critical Error: index.html not found in root path.", status_code=404)
