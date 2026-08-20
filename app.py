# ====================================================================================================
#                                         MAY ROGA LLC
#                       Wellness Travel Architecture & Lifestyle Optimization
#                                    Miami, Florida | USA
#                                       MAIN BACKEND
# ====================================================================================================

import os
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles # ◄── 1. AGREGAR ESTA IMPORTACIÓN
from pydantic import BaseModel
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

app = FastAPI(
    title="MAY ROGA LLC - Wellness Travel App Production Backend",
    version="1.0.0"
)

# ◄── 2. MONTAR LA CARPETA ESTÁTICA AQUÍ MISMO
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🏢 CATÁLOGO GLOBAL DE INFRAESTRUCTURA REAL Y COMPLETO (FASE 1)
CATALOGO_GLOBAL = [
    # --- BLOQUE 1: ULTRA-LUJO / ÉLITE (CRUCEROS) ---
    {
        "id": "CRU-ELITE-001", "tier": "ELITE", "tipo": "CRUCERO",
        "name_es": "The Ritz-Carlton Yacht Collection (Evrima / Ilma)",
        "name_en": "The Ritz-Carlton Yacht Collection (Evrima / Ilma)",
        "desc_es": "Suites con terrazas privadas sobre el mar, cenas de autor inspiradas por chefs de tres estrellas Michelin y una marina integrada en popa para deportes acuáticos en calas vírgenes del Caribe.",
        "desc_en": "Featuring private oceanfront terrace suites, signature dining inspired by three-Michelin-starred chefs, and an open-air aft marina for water sports in untouched Caribbean coves."
    },
    {
        "id": "CRU-ELITE-002", "tier": "ELITE", "tipo": "CRUCERO",
        "name_es": "Silversea Cruises (Silver Nova / Silver Ray)",
        "name_en": "Silversea Cruises (Silver Nova / Silver Ray)",
        "desc_es": "El pináculo del lujo todo incluido en el mar con servicio de mayordomo personalizado. Diseño arquitectónico asimétrico y cristal masivo. Incluye el programa gastronómico S.A.L.T.",
        "desc_en": "The pinnacle of ultra-luxury all-inclusive cruising with personalized butler service. Revolutionary asymmetrical design and massive glass. Features the S.A.L.T. culinary program."
    },
    {
        "id": "CRU-ELITE-003", "tier": "ELITE", "tipo": "CRUCERO",
        "name_es": "Explora Journeys (Explora I / Explora II)",
        "name_en": "Explora Journeys (Explora I / Explora II)",
        "desc_es": "Estética de hotel boutique europeo. Ofrece un santuario de bienestar de más de 700 metros cuadrados con spas hidrotermales al aire libre. Perfecto para equilibrar el Flujo Creativo.",
        "desc_en": "Sophisticated European boutique hotel aesthetic. Features a 7,000-square-foot wellness sanctuary with open-air hydrothermal spas. Perfect for balancing Creative Flow."
    },
    {
        "id": "CRU-ELITE-004", "tier": "ELITE", "tipo": "CRUCERO",
        "name_es": "Seabourn (Seabourn Ovation / Seabourn Venture)",
        "name_en": "Seabourn (Seabourn Ovation / Seabourn Venture)",
        "desc_es": "Ambiente exclusivo de club privado. Alianzas de bienestar con expertos internacionales en meditación consciente y spas galardonados, ideales para una desconexión total.",
        "desc_en": "Exclusive private club atmosphere. Wellness partnerships with international mindfulness experts and award-winning spas, ideal for complete executive decompression."
    },
    {
        "id": "CRU-ELITE-005", "tier": "ELITE", "tipo": "CRUCERO",
        "name_es": "Regent Seven Seas Cruises (Seven Seas Grandeur)",
        "name_en": "Regent Seven Seas Cruises (Seven Seas Grandeur)",
        "desc_es": "La línea más lujosa del mundo. Suites decoradas con arte original de Picasso. Inclusión total desde excursiones privadas ilimitadas hasta jets privados de conexión.",
        "desc_en": "The world's most luxurious cruise line. Suites adorned with original Picasso artwork. All-inclusive luxury from private excursions to connecting executive private jets."
    },
    # --- BLOQUE 2: ULTRA-LUJO / ÉLITE (HOTELES) ---
    {
        "id": "HOT-ELITE-001", "tier": "ELITE", "tipo": "HOTEL",
        "name_es": "Eden Roc Cap Cana (Punta Cana, República Dominicana)",
        "name_en": "Eden Roc Cap Cana (Punta Cana, Dominican Republic)",
        "desc_es": "Miembro exclusivo de Relais & Châteaux. Villas de ultra-lujo con piscinas privadas, duchas de spa tipo lluvia al aire libre y club de playa privado de arena blanca.",
        "desc_en": "Exclusive Relais & Châteaux member. Ultra-luxury villas with private pools, outdoor rain-spa showers, and a private white-sand beach club enclave."
    },
    {
        "id": "HOT-ELITE-002", "tier": "ELITE", "tipo": "HOTEL",
        "name_es": "Amanera (Playa Grande, República Dominicana)",
        "name_en": "Amanera (Playa Grande, Dominican Republic)",
        "desc_es": "Suspendido sobre acantilados. Combina arquitectura minimalista zen con la selva virgen. Casitas con techos verdes, piscinas infinitas y enfoque en el silencio absoluto.",
        "desc_en": "Perched above dramatic cliffs. Blends minimalist Zen architecture with raw jungle. Casitas feature green roofs, infinity pools, and absolute acoustic silence."
    },
    {
        "id": "HOT-ELITE-003", "tier": "ELITE", "tipo": "HOTEL",
        "name_es": "Chablé Maroma (Riviera Maya, México)",
        "name_en": "Chablé Maroma (Riviera Maya, Mexico)",
        "desc_es": "Santuario de ultra-lujo escondido en la mística jungla maya. Famoso por su spa enfocado en ceremonias de purificación maya y meditación de frecuencias.",
        "desc_en": "Ultra-luxury sanctuary hidden within the mystical Mayan jungle. Renowned for its world-class spa focused on ancestral purification rituals and frequency meditation."
    },
    {
        "id": "HOT-ELITE-004", "tier": "ELITE", "tipo": "HOTEL",
        "name_es": "Belmond Maroma Resort & Spa (Riviera Maya, México)",
        "name_en": "Belmond Maroma Resort & Spa (Riviera Maya, Mexico)",
        "desc_es": "El más alto nivel de sofisticación en la Riviera Maya. Ofrece un servicio hiper-personalizado donde cada huésped cuenta con un conserje de bienestar dedicado.",
        "desc_en": "The highest echelon of sophistication in the Riviera Maya. Delivers hyper-personalized service where every guest is paired with a dedicated wellness host."
    },
    {
        "id": "HOT-ELITE-005", "tier": "ELITE", "tipo": "HOTEL",
        "name_es": "One&Only Mandarina / One&Only Palmilla (México)",
        "name_en": "One&Only Mandarina / One&Only Palmilla (Mexico)",
        "desc_es": "Villas suspendidas en las copas de los árboles o frente a acantilados volcánicos. Santuarios de relajación profunda diseñados para la desconexión de altos ejecutivos.",
        "desc_en": "Ultra-luxury treehouse and cliffside compounds. Deep relaxation sanctuaries engineered specifically for high-profile corporate executive decompression."
    },
    # --- BLOQUE 3: PREMIUM / CLASE ALTA (CRUCEROS VIP) ---
    {
        "id": "CRU-PREM-001", "tier": "PREMIUM", "tipo": "CRUCERO",
        "name_es": "Celebrity Cruises (The Retreat)",
        "name_en": "Celebrity Cruises (The Retreat)",
        "desc_es": "Enclave exclusivo dentro de un megabarco. Restaurante privado de Daniel Boulud, solárium restringido con mayordomos de piscina y suites premium contemporáneas.",
        "desc_en": "A premium resort-within-a-resort enclave. Private restaurant by chef Daniel Boulud, restricted sundeck with pool butlers, and contemporary upscale suites."
    },
    # --- BLOQUE 4: PREMIUM / CLASE ALTA (HOTELES TODO INCLUIDO) ---
    {
        "id": "HOT-PREM-001", "tier": "PREMIUM", "tipo": "HOTEL",
        "name_es": "Grand Velas Riviera Maya (Riviera Maya, México)",
        "name_en": "Grand Velas Riviera Maya (Riviera Maya, Mexico)",
        "desc_es": "Todo incluido que redefine la alta cocina. Spa de más de 8,000 metros cuadrados con un circuito hidrotermal de 7 etapas y restaurantes galardonados con diamantes AAA.",
        "desc_en": "All-inclusive redefining fine dining. 80,000-square-foot spa featuring a 7-stage hydrothermal circuit and AAA Diamond-rated specialty restaurants."
    },
    # --- BLOQUE 5: ASPIRACIONAL / CLASE MEDIA (CRUCEROS CON CUBIERTA ADULTOS) ---
    {
        "id": "CRU-ASPI-001", "tier": "ASPI", "tipo": "CRUCERO",
        "name_es": "Royal Caribbean International (Solarium Enclave)",
        "name_en": "Royal Caribbean International (Solarium Enclave)",
        "desc_es": "Refugio acristalado exclusivo para adultos en la proa de los barcos más innovadores. Piscinas infinitas, jacuzzis colgantes y ambiente de paz total.",
        "desc_en": "Adults-only forward glass-domed paradise on the world's most innovative ships. Features infinity pools, cantilevered whirlpools, and total structural peace."
    },
    # --- BLOQUE 6: ASPIRACIONAL / CLASE MEDIA (RESORTS CONFIABLES) ---
    {
        "id": "HOT-ASPI-001", "tier": "ASPI", "tipo": "HOTEL",
        "name_es": "Secrets Royal Beach Punta Cana (República Dominicana)",
        "name_en": "Secrets Royal Beach Punta Cana (Dominican Republic)",
        "desc_es": "Resort todo incluido solo para adultos en Playa Bávaro. Ofrece ríos lentos tropicales y el concepto de Lujo Ilimitado sin necesidad de reservaciones previas.",
        "desc_en": "Adults-only, all-inclusive luxury value on Bávaro Beach. Features winding tropical lazy rivers and Unlimited-Luxury dining with zero reservations required."
    }
]
# 📝 VARIANTES DE TEXTO OFICIALES DEL CRM LOCAL DEL MINUTO 14:30
TEXTOS_CRM = {
    "VAR1_MEJORIA": {
        "title_es": "OPTIMIZACIÓN Y ARMONÍA NATURAL (MEJORÍA)",
        "title_en": "NATURAL OPTIMIZATION & HARMONY (IMPROVEMENT)","body_es": "Tu Figura Humana muestra una respuesta excepcional al estímulo de bienestar de 15 minutos. El Círculo de Desprendimiento ha regresado al centro geométrico del Triángulo de Balance. Tu Índice de Ritmo de Vida se ha desacelerado hacia una zona de calma, tu Reserva Energética se ha recargado en un 30% y tu Flujo Creativo se encuentra desbloqueado y receptivo.","body_en": "Your Vitality Silhouette displays an exceptional response to the 15-minute alignment. The Center Circle has anchored back into the core of your Balance Triangle. Your Lifestyle Pace Index has shifted into calm, your Energy Reserves have replenished by 30%, and your Creative Flow is unlocked."},"VAR2_IGUAL": {"title_es": "MESETA DE ENERGÍA ESTACIONARIA (IGUAL)","title_en": "STATIONARY ENERGY PLATEAU (UNCHANGED)","body_es": "Tu Figura Humana se mantiene en una meseta de energía adaptativa. El Círculo de Desprendimiento sigue inclinado hacia uno de los vértices, indicando que las presiones de la rutina cotidiana han generado una inercia que bloquea tu relajación natural. Tu reserva no ha empeorado, pero requieres un cambio radical de entorno.","body_en": "Your Vitality Silhouette remains on an adaptive energy plateau. The Center Circle remains tilted toward one vertex, indicating that routine pressures have created an inertia blocking your natural relaxation. Your reserves have not declined, but you require a radical change."},"VAR3_EMPEORAMIENTO": {"title_es": "SATURACIÓN POR RESISTENCIA ACTIVA (EMPEORAMIENTO)","title_en": "ACCUMULATED SATURATION (CRITICAL)","body_es": "Tu Figura Humana refleja una resistencia activa a la desconexión digital. El Círculo de Desprendimiento ha sido desplazado con fuerza hacia el exterior. Tu Índice de Ritmo de Vida se encuentra acelerado y tu Reserva Energética opera bajo mínimos, bloqueando tu Flujo Creativo. Se emite alerta de desconexión inmediata.","body_en": "Your Vitality Silhouette reflects active resistance to digital disconnection. The Center Circle has been forcefully pushed to the outer edge. Your Lifestyle Pace Index is over-accelerated, and Energy Reserves are operating at critical minimums. Immediate disconnection is advised."}}class PDFPayload(BaseModel):servicio_id: strlang: strscore_inicial: floatscore_actual: floatrespiracion_score: floatadivinanzas_score: floatiev: floatvariante: strdestino_id: str@app.post("/generate-pdf")def generate_pdf(payload: PDFPayload):pdf_filename = f"report_{payload.servicio_id}.pdf"pdf_path = os.path.join("temp", pdf_filename)os.makedirs("temp", exist_ok=True)# Configuración del documento en tamaño Carta (Letter) con márgenes pulcrosdoc = SimpleDocTemplate(pdf_path, pagesize=letter,rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45,title=f"Report {payload.servicio_id}")styles = getSampleStyleSheet()# 🎨 Paleta de colores corporativa MAY ROGA LLC (Minimalista, Lujo, Tierra)color_primary = colors.HexColor("#1A1A1A")   # Negro profundo corporativocomor_gold = colors.HexColor("#A3704C")      # Dorado / Bronce Wellnesscolor_text = colors.HexColor("#333333")      # Gris oscuro para lectura legiblecolor_legal = colors.HexColor("#777777")     # Gris claro para contratos/disclaimers# Estilos de Párrafo de Alta Gamatitle_style = ParagraphStyle('CorpTitle', parent=styles['Heading1'], fontSize=26, leading=30, textColor=color_primary, alignment=1)subtitle_style = ParagraphStyle('CorpSub', parent=styles['Normal'], fontSize=9, leading=13, textColor=color_legal, alignment=1)h2_style = ParagraphStyle('SectionHeader', parent=styles['Heading2'], fontSize=12, leading=16, textColor=color_gold, spaceBefore=18, spaceAfter=8)body_style = ParagraphStyle('CorpBody', parent=styles['Normal'], fontSize=10, leading=14, textColor=color_text)disclaimer_style = ParagraphStyle('LegalText', parent=styles['Normal'], fontSize=7.5, leading=10.5, textColor=color_legal, alignment=4)story = []

    # --- CONTINUACIÓN DIRECTA DEL PROCESAMIENTO ---
    
    # 1. Título e información del encabezado del documento
    story.append(Paragraph("MAY ROGA LLC", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"BIOMETRIC REPORT &bull; ID: {payload.servicio_id} &bull; DESTINATION: {payload.destino_id}", subtitle_style))
    story.append(Spacer(1, 24))

    # 2. Extracción dinámica de textos según el idioma ('es' o 'en')
    lang_key = payload.lang.lower() if payload.lang.lower() in ["es", "en"] else "en"
    textos_variante = TEXTOS_CRM.get(payload.variante, TEXTOS_CRM["VAR2_IGUAL"])
    
    title_text = textos_variante[f"title_{lang_key}"]
    body_text = textos_variante[f"body_{lang_key}"]

    story.append(Paragraph(title_text, h2_style))
    story.append(Paragraph(body_text, body_style))
    story.append(Spacer(1, 20))

    # 3. Construcción de Tabla Estructurada de Datos
    metric_label = "Métrica" if lang_key == "es" else "Metric"
    value_label = "Valor" if lang_key == "es" else "Value"
    
    th_style = ParagraphStyle('TH', parent=styles['Normal'], fontSize=10, leading=12, textColor=colors.white, fontName="Helvetica-Bold")
    td_style = ParagraphStyle('TD', parent=styles['Normal'], fontSize=9, leading=12, textColor=color_text)
    
    table_data = [
        [Paragraph(metric_label, th_style), Paragraph(value_label, th_style)],
        [Paragraph("Score Inicial" if lang_key == "es" else "Initial Score", td_style), Paragraph(str(payload.score_inicial), td_style)],
        [Paragraph("Score Actual" if lang_key == "es" else "Current Score", td_style), Paragraph(str(payload.score_actual), td_style)],
        [Paragraph("Score Respiración" if lang_key == "es" else "Breathing Score", td_style), Paragraph(str(payload.respiracion_score), td_style)],
        [Paragraph("Score Adivinanzas" if lang_key == "es" else "Riddles Score", td_style), Paragraph(str(payload.adivinanzas_score), td_style)],
        [Paragraph("Índice de Energía Vital (IEV)" if lang_key == "es" else "Vital Energy Index (IEV)", td_style), Paragraph(str(payload.iev), td_style)]
    ]
    
    # 522 pt es el ancho útil total disponible en tamaño Letter con márgenes de 45 pt
    metrics_table = Table(table_data, colWidths=[300, 222])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), color_primary),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9F9F9")]),
        ('LINEBELOW', (0, -1), (-1, -1), 1, color_gold),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 24))

    # 4. Cláusula Legal / Descargo de responsabilidad
    disclaimer_title = "AVISO LEGAL Y DE PRIVACIDAD" if lang_key == "es" else "LEGAL NOTICE & PRIVACY DISCLAIMER"
    story.append(Paragraph(disclaimer_title, h2_style))
    
    story.append(Paragraph(
        "Este documento contiene información automatizada y confidencial propiedad de MAY ROGA LLC. "
        "Las métricas representadas reflejan una simulación analítica de bienestar digital basada en respuestas operativas y no "
        "reemplazan en ningún caso una evaluación clínica o médica formal profesional." if lang_key == "es" else
        "This document contains automated and confidential information owned by MAY ROGA LLC. "
        "The metrics displayed reflect an analytical simulation of digital wellness based on operational responses and do "
        "not replace, under any circumstances, a formal professional clinical or medical evaluation.", 
        disclaimer_style
    ))

    # 5. Renderizado final del PDF en disco
    doc.build(story)
    
    return {"status": "success", "file_path": pdf_path}
    # --- CONTINUACIÓN DIRECTA DE TU HISTORIA (STORY) ---

    # ENCABEZADO CORPORATIVO
    story.append(Paragraph("MAY ROGA LLC", title_style))
    story.append(Paragraph("Wellness Travel Architecture & Lifestyle Optimization<br/>Miami, Florida | USA", subtitle_style))
    story.append(Spacer(1, 15))

    is_es = payload.lang.upper() == "ES"

    # TÍTULO DEL DOCUMENTO
    t_report = "REPORTE DE BALANCE DE VITALIDAD Y PRESCRIPCIÓN DE VIAJE" if is_es else "VITALITY BALANCE REPORT & TRAVEL PRESCRIPTION"
    story.append(Paragraph(f"{t_report}", ParagraphStyle('RepTitle', parent=styles['Heading3'], fontSize=11, leading=14, alignment=1, textColor=color_primary, spaceAfter=15)))

    # METADATOS LOCALES
    meta_text = f"Folio de Servicio / Service ID: {payload.servicio_id} | Status: Completado Localmente / Locally Completed"
    story.append(Paragraph(meta_text, body_style))
    story.append(Spacer(1, 12))

    # SECCIÓN 1: DIAGNÓSTICO MATEMÁTICO DEL CRM
    s1_title = "1. DIAGNÓSTICO DEL CRM WELLNESS / WELLNESS CRM DIAGNOSTIC"
    story.append(Paragraph(s1_title, h2_style))

    metrics_data = [
        [Paragraph("Métrica de Estilo de Vida / Lifestyle Metric", body_style), Paragraph("Inicial", body_style), Paragraph("Actual (14:30)", body_style)],
        [Paragraph("Índice de Ritmo de Vida / Lifestyle Pace Index", body_style), f"{payload.score_inicial}%", f"{payload.score_actual}%"],
        [Paragraph("Reserva Energética / Energy Reserves", body_style), f"{payload.score_inicial}%", f"{payload.respiracion_score}%"],
        [Paragraph("Flujo Creativo / Creative Flow", body_style), f"{payload.score_inicial}%", f"{payload.adivinanzas_score}%"]
    ]

    metrics_table = Table(metrics_data, colWidths=[280, 120, 120])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F9F9F9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E5E5")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 12))

    # ENCADENAR TEXTO VARIABLE DE LA FIGURA HUMANA DEL CRM
    var_key = payload.variante if payload.variante in TEXTOS_CRM else "VAR2_IGUAL"
    texto_activo = TEXTOS_CRM[var_key]

    titulo_estado = texto_activo["title_es"] if is_es else texto_activo["title_en"]
    cuerpo_estado = texto_activo["body_es"] if is_es else texto_activo["body_en"]

    story.append(Paragraph(f"ESTADO DE VITALIDAD / VITALITY SILHOUETTE STATUS:", ParagraphStyle('StateH', parent=body_style, fontSize=10, textColor=color_primary)))
    story.append(Paragraph(f"👉 {titulo_estado}", ParagraphStyle('StateSub', parent=body_style, fontSize=10, textColor=color_gold, spaceBefore=4, spaceAfter=4)))
    story.append(Paragraph(cuerpo_estado, body_style))
    story.append(Spacer(1, 15))

    # SECCIÓN 2: PRESCRIPCIÓN DEL ITINERARIO GLOBAL
    s2_title = "2. ITINERARIO TURÍSTICO DE COMPENSACIÓN / COMPENSATORY TRAVEL ITINERARY"
    story.append(Paragraph(s2_title, h2_style))

    # Búsqueda exacta de la propiedad inyectada por el algoritmo antirepetitivo local
    target_dest = next((d for d in CATALOGO_GLOBAL if d["id"] == payload.destino_id), None)

    if target_dest:
        dest_name = target_dest["name_es"] if is_es else target_dest["name_en"]
        dest_desc = target_dest["desc_es"] if is_es else target_dest["desc_en"]
    else:
        dest_name = payload.destino_id
        dest_desc = "Curated luxury corridor requested dynamically via local script selection."

    # Estructuración limpia de strings con formato HTML compatible para ReportLab
    dest_html = f"<b>Santuario Asignado / Curated Oasis:</b> {dest_name}<br/><br/>"
    dest_html += f"<b>Detalle del Entorno / Wellness Profile:</b> {dest_desc}<br/><br/>"
    dest_html += "• <b>Logística Aérea / Air Travel:</b> Premium routing synchronized from Miami Int. (MIA). Flight details locked against friction protocols.<br/><br/>"
    dest_html += "• <b>Estatus de Reserva / Consortium Privileges:</b> Eligible for Virtuoso/Signature luxury benefits ($100 resort credits and priority room upgrades processed locally via credentials)."

    story.append(Paragraph(dest_html, body_style))
    story.append(Spacer(1, 15))

    # --- CIERRE FINAL DEL DOCUMENTO Y DE LA FUNCIÓN DE FASTAPI ---
    
    # Renderizado físico en la carpeta temporal
    doc.build(story)

    return {
        "status": "success",
        "message": "PDF report generated successfully",
        "file_name": pdf_filename,
        "file_path": pdf_path
    }
    # --- CONTINUACIÓN DIRECTA DE TU HISTORIA (STORY) ---

    # SECCIÓN 3: ACTIVACIÓN COMERCIAL Y ACCESO DIRECTO HOST AGENCY
    s3_title = "3. ACTIVACIÓN DE PRESCRIPCIÓN COMERCIAL / BOOKING GATEWAY"
    story.append(Paragraph(s3_title, h2_style))
    
    cta_text = "Para consolidar este balance natural y fijar las tarifas exclusivas de este itinerario, póngase en contacto con su Conserje de Viajes corporativo. Presente este reporte digital en formato PDF junto con el Folio de Servicio adjunto para procesar los beneficios." if is_es else "To consolidate this natural balance and lock down the exclusive rates of this itinerary, contact your corporate Travel Concierge. Present this digital PDF report along with the attached Service ID to unlock your custom benefits."
    story.append(Paragraph(cta_text, body_style))
    story.append(Spacer(1, 20))

    # SECCIÓN 4: BLINDAJE JURÍDICO EXIGIDO POR EL ESTADO DE FLORIDA (AVISO LEGAL)
    story.append(Paragraph("4. AVISO LEGAL Y EXENCIÓN DE RESPONSABILIDAD / LEGAL DISCLAIMER", ParagraphStyle('LegHeader', parent=styles['Normal'], fontSize=8, leading=11, textColor=color_primary, spaceAfter=6)))
    
    disc_es = "ESPAÑOL: Este documento es emitido exclusivamente por MAY ROGA LLC como una herramienta de orientación para el estilo de vida, el bienestar general y la consultoría de viajes premium. No constituye, ni reemplaza, un diagnóstico médico, psiquiátrico, psicológico o clínico de ninguna índole. MAY ROGA LLC no es una institución de salud ni un proveedor médico. Los datos utilizados para generar este reporte se procesan de forma estrictamente local y anónima en el dispositivo del usuario mediante algoritmos de comportamiento digital (localStorage). El usuario asume total responsabilidad sobre las decisiones de viaje y actividades derivadas de este reporte."
    disc_en = "ENGLISH: This document is issued exclusively by MAY ROGA LLC as a guidance tool for lifestyle enhancement, general wellness, and premium travel consulting. It does not constitute, nor does it replace, a medical, psychiatric, psychological, or clinical diagnosis of any kind. MAY ROGA LLC is not a healthcare institution nor a medical provider. The data utilized to generate this report is processed and stored strictly locally and anonymously on the user's device via digital behavior algorithms (localStorage). El usuario asume full and sole responsibility for travel decisions and activities derived from this report."
    
    story.append(Paragraph(disc_es, disclaimer_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(disc_en, disclaimer_style))

    # Nota de pie de página de seguridad de IA obligatoria
    story.append(Spacer(1, 15))
    story.append(Paragraph("This document is for informational and promotional travel purposes only. For medical advice or diagnosis, consult a certified healthcare professional. AI responses may include mistakes.", ParagraphStyle('AIFoot', parent=disclaimer_style, fontName='Helvetica-Oblique', alignment=1)))
    story.append(Spacer(1, 15))
    story.append(Paragraph("© 2026 MAY ROGA LLC. All rights reserved. Miami, Florida.", ParagraphStyle('FootCopyright', parent=subtitle_style, fontSize=8)))

    doc.build(story)
    
    # Retorno del archivo PDF binario al cliente de forma directa
    from fastapi.responses import FileResponse
    return FileResponse(pdf_path, media_type='application/pdf', filename=pdf_filename)

# --- ENDPOINT INDEX HTML OFICIAL DE PRODUCCIÓN ---
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def index():
    # El servidor busca tu index.html real en la raíz y se lo entrega al usuario en Miami
    ruta_html = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(ruta_html):
        with open(ruta_html, "r", encoding="utf-8") as file:
            return HTMLResponse(content=file.read(), status_code=200)
    
    # Respaldo de seguridad en caso de que olvides subir el index.html a GitHub
    return HTMLResponse(
        content="<h1>MAY ROGA LLC</h1><p>Error crítico: index.html no encontrado en la raíz del servidor.</p>", 
        status_code=404
    )

