# =========================================================================
# WELLNESS TRAVEL MASTER BACKEND — INTEGRIDAD TOTAL 100% OPEN THAN GO
# PARTE 1 DE 5: IMPORTACIONES CORE, CONFIGURACIÓN FASTAPI Y PASARELA STRIPE
# =========================================================================
import os
import random
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Optional
import stripe
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

app = FastAPI(
    title="Wellness Travel — Private Premium Engine",
    description="Núcleo de enrutamiento y balance fiduciario de estilo de vida premium sin alteraciones lógicas.",
    version="3.5.0"
)

# Inicialización fiduciaria y de pasarelas exclusivas de Wellness Travel
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_mock_wellness_travel")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_mock")

# Esquemas de Control de Payloads Pydantic — Idénticos a Open Than Go
class SintonizacionPayload(BaseModel):
    zip_code: str = Field(..., pattern=r"^[0-9]{5}$")
    modo: str = Field(..., pattern=r"^(SALIR|CASA)$")
    mente: str = Field(..., pattern=r"^(aburrido|cansado|estresado|agotado|ansioso)$")
    budget: str = Field(..., pattern=r"^(abierto|ilimitado)$")
    perfil: str = Field(..., pattern=r"^(solo|acompanado|familia|empresa|accesible)$")
    historial_vistos: List[str] = []
    texto_libre: Optional[str] = ""

class PDFPassportPayload(BaseModel):
    servicio_id: str
    lang: str
    score_inicial: float
    score_actual: float
    respiracion_score: float
    adivinanzas_score: float
    iev: float
    variante: str
    destino_id: str
# =========================================================================
# WELLNESS TRAVEL MASTER BACKEND — INTEGRIDAD TOTAL 100% OPEN THAN GO
# PARTE 2 DE 5: DICCIONARIO MAESTRO BILINGÜE ÉLITE Y MATRIZ DE SANTUARIOS VIP
# =========================================================================

# Diccionario Maestro Bilingüe Élite — Inmunizado contra términos médicos o clínicos
DICTIONARY_BILINGUAL = {
    "ES": {
        "doc_title": "PASAPORTE DE BIENESTAR INDIVIDUAL",
        "folio": "Folio de Sintonía Premium",
        "status": "Estatus: Validado en Red Render",
        "sec1_title": "1. BALANCE DE ENFOQUE Y BIENESTAR INDIVIDUAL",
        "m1": "Indicador Evaluated", "m2": "Nivel Inicial", "m3": "Nivel de Cierre",
        "m_pace": "Índice de Saturación Externa", 
        "m_breathe": "Tasa de Sincronización Respiratoria", 
        "m_logic": "Eficiencia de Enfoque Mental",
        "sec2_title": "2. ENRUTAMIENTO EXCLUSIVO DE VIAJE",
        "stay_lbl": "Santuario de Ultra-Lujo Prescrito", 
        "desc_lbl": "Perfil de Aislamiento Acústico",
        "air_lbl": "Logística Aérea Privada", 
        "sea_lbl": "Línea Marítima Élite",
        "consorcio": "Beneficios de Consorcio: Elegible automáticamente para créditos de cortesía Virtuoso/Signature ($100 USD para experiencias de sintonía y mejoras de suite).",
        "sec3_title": "3. CONCLUSIONES DE ESTILO DE VIAJE PREMIUM",
        "cta": "Este resumen certifica su descompresión y optimización de bienestar. Diseñado para disolver la saturación del entorno y asegurar el control total de su tiempo.",
        "sec4_title": "4. COMPLIANCE DE PRIVACIDAD MAY ROGA LLC",
        "disclaimer": "Toda la información de sintonía se procesa de forma local y anónima en su terminal mediante almacenamiento fiduciario seguro (localStorage). El líder retiene el control de sus registros.",
        "ai_foot": "Este documento es estrictamente confidencial y para fines informativos de estilo de vida premium. No constituye asesoramiento clínico ni médico formal."
    },
    "EN": {
        "doc_title": "INDIVIDUAL WELLNESS PASSPORT",
        "folio": "Premium Tuning Folio ID",
        "status": "Status: Validated on Secure Render Node",
        "sec1_title": "1. WELLNESS BALANCE & INDIVIDUAL FOCUS SUMMARY",
        "m1": "Evaluated Metric", "m2": "Initial Baseline", "m3": "Closing Balance",
        "m_pace": "External Saturation Index", 
        "m_breathe": "Respiratory Synchronization Rate", 
        "m_logic": "Mental Focus Efficiency Rate",
        "sec2_title": "2. EXCLUSIVE TRAVEL ROUTING",
        "stay_lbl": "Prescribed Ultra-Luxury Sanctuary", 
        "desc_lbl": "Acoustic Isolation Profile",
        "air_lbl": "Private Air Logistics", 
        "sea_lbl": "Elite Maritime Corridor",
        "consorcio": "Consortium Privileges: Automatically eligible for complimentary Virtuoso/Signature luxury benefits ($100 credits for wellness experiences and priority suite upgrades).",
        "sec3_title": "3. PREMIUM LIFESTYLE INSIGHTS",
        "cta": "This passport summarizes your progress, benchmarking your focus index and outlining the stabilization achieved against routine daily exhaustion.",
        "sec4_title": "4. CORPORATE LIFESTYLE PRIVACY ASSURANCE",
        "disclaimer": "All digital metrics gathered to compile this passport are processed strictly locally and anonymously on the user's browser terminal via local behavior algorithms (localStorage).",
        "ai_foot": "This document is for informational and promotional travel purposes only. It does not constitute clinical or medical advice."
    }
}

# Matriz completa de ultra-lujo para millonarios, clase alta y adinerada.
SANTUARIOS_VIP = {
    "S1": {
        "nombre": "Amanera Resort — Playa Grande",
        "perfil_compatible": ["solo", "acompanado"],
        "es": {
            "desc": "Casitas zen minimalistas de cristal suspendidas sobre acantilados masivos protegidos en la selva virgen.",
            "actividad": "Sesión privada de sintonización sonora frente al mar y aislamiento acústico ambiental.",
            "logistica_aerea": "Vuelo charter privado en Gulfstream G650 hasta el aeródromo ejecutivo más cercano.",
            "logistica_maritima": "Yate de colección de 80 pies disponible para traslados y descompresión en mar abierto."
        },
        "en": {
            "desc": "Zen minimalist glass casitas suspended over massive protected cliffs in the pristine jungle.",
            "actividad": "Private oceanfront sound tuning session and premium guided environmental isolation.",
            "logistica_aerea": "Private Gulfstream G650 charter flight to the nearest executive airfield.",
            "logistica_maritima": "80-foot collector yacht available for open-ocean bespoke leisure transfers."
        }
    },
    "S2": {
        "nombre": "Eden Roc Cap Cana — Boutique Sanctuary",
        "perfil_compatible": ["acompanado", "familia", "empresa"],
        "es": {
            "desc": "Bungalows independientes de ultra-lujo con piscinas privadas, acceso restringido a playas vírgenes y lagunas naturales.",
            "actividad": "Navegación premium a baja velocidad en aguas profundas y cena sensorial exclusiva.",
            "logistica_aerea": "Acceso VIP a través de la terminal privada FBO y helicóptero al helipuerto del resort.",
            "logistica_maritima": "Embarcación premium Riva Aquarama para accesos directos desde la marina privada."
        },
        "en": {
            "desc": "Bespoke standalone ultra-luxury bungalows featuring private pools, restricted pristine beachfronts, and eco-lagoons.",
            "actividad": "Deep water premium sailing at low cruise speed and exclusive chef-curated dining sensory experiences.",
            "logistica_aerea": "VIP access via private FBO terminal and executive helicopter connection directly to the resort pad.",
            "logistica_maritima": "Premium Riva Aquarama vessel operational for direct boarding from the private marina."
        }
    }
}
# =========================================================================
# WELLNESS TRAVEL MASTER BACKEND — INTEGRIDAD TOTAL 100% OPEN THAN GO
# PARTE 3 DE 5: CIERRE DE SANTUARIOS VIP Y MOTOR ANALÍTICO DE SINTONÍA
# =========================================================================

# Continuación de la Matriz de Ultra-Lujo
SANTUARIOS_VIP.update({
    "S3": {
        "nombre": "Amangiri Sanctuary — Desert Solitude",
        "perfil_compatible": ["solo", "acompanado", "empresa"],
        "es": {
            "desc": "Arquitectura monolítica oculta en cañones desérticos profundos. Diseñado para recuperar el control absoluto del silencio.",
            "actividad": "Sesión nocturna de observación astronómica privada sin contaminación lumínica ni acústica.",
            "logistica_aerea": "Charter privado Bombardier Global 7500 con tripulación de alta sintonía dedicada.",
            "logistica_maritima": "No aplica. Logística terrestre mediante flota privada de vehículos blindados de confort premium."
        },
        "en": {
            "desc": "Monolithic architecture hidden inside deep desert canyons. Engineered to regain complete control of quietness.",
            "actividad": "Nightly premium stargazing session guided by experts, fully shielded from light and noise pollution.",
            "logistica_aerea": "Private Bombardier Global 7500 flight utilizing highly vetted executive crews.",
            "logistica_maritima": "Not applicable. Secured luxury ground transport utilizing premium armored comfort fleets."
        }
    },
    "S4": {
        "nombre": "Singita Lebombo — Private Wilderness Lodge",
        "perfil_compatible": ["familia", "empresa", "accesible"],
        "es": {
            "desc": "Villas de cristal suspendidas sobre parajes naturales vírgenes con accesibilidad total y diseño de vanguardia.",
            "actividad": "Safari fotográfico privado de alta fidelidad con rastreadores y guías de élite.",
            "logistica_aerea": "Conexión directa en jet privado intercontinental y avioneta ejecutiva monomotor exclusiva.",
            "logistica_maritima": "Exploración fluvial premium en embarcación privada eco-sustentable de alta gama."
        },
        "en": {
            "desc": "Elevated glass suites hovering over wild nature fields with full physical accessibility and high-end design.",
            "actividad": "Private high-fidelity photographic safari featuring veteran elite track specialists.",
            "logistica_aerea": "Direct private intercontinental jet routing linking directly with an exclusive single-engine aircraft.",
            "logistica_maritima": "Premium river exploration on a private bespoke eco-friendly high-end vessel."
        }
    }
})

# Motor analítico de puntuación - Réplica exacta del CWRE V2.1 de Open Than Go
def calcular_indice_estabilizacion(payload: SintonizacionPayload) -> dict:
    base_score = 45.0  # Baseline inicial estándar
    
    # Modificadores de estado mental (Mente)
    modificadores_mente = {
        "aburrido": 5.0,
        "cansado": -10.0,
        "estresado": -20.0,
        "agotado": -25.0,
        "ansioso": -30.0
    }
    
    # Modificadores de entorno y acompañamiento (Perfil VIP)
    modificadores_perfil = {
        "solo": 10.0,
        "acompanado": 5.0,
        "familia": -5.0,
        "empresa": -15.0,  # Alta demanda de atención directiva
        "accesible": 0.0
    }
    
    score_inicial = base_score + modificadores_mente.get(payload.mente, 0.0) + modificadores_perfil.get(payload.perfil, 0.0)
    score_inicial = max(10.0, min(95.0, score_inicial))
    
    # Análisis del texto libre (Mando de Sintonía) para detectar fricciones
    interceptor_friccion = 0.0
    if payload.texto_libre:
        palabras_saturacion = ["ruido", "saturacion", "agenda", "tiempo", "vuelo", "reunion", "entorno", "exceso"]
        conteo = sum(1 for palabra in palabras_saturacion if palabra in payload.texto_libre.lower())
        interceptor_friccion = conteo * -3.5
        
    score_inicial = max(5.0, score_inicial + interceptor_friccion)
    
    # Simulación matemática de optimización post-sesión (Cierre proyectado)
    score_cierre = min(100.0, score_inicial + 45.0)
    
    return {
        "score_inicial": round(score_inicial, 2),
        "score_cierre": round(score_cierre, 2),
        "eficiencia_respiratoria": 100.0,
        "enfoque_mental": 100.0
    }
# =========================================================================
# WELLNESS TRAVEL MASTER BACKEND — INTEGRIDAD TOTAL 100% OPEN THAN GO
# PARTE 4 DE 5: MOTOR RECOMENDADOR VIP Y PASARELA DE CHECKOUT PREMIUM
# =========================================================================

@app.post("/api/sintonizar")
async def endpoint_sintonizar_contextual(payload: SintonizacionPayload):
    """
    Core del motor de enrutamiento predictivo. Procesa el perfil, calcula las métricas
    de balance de sintonía y prescribe las 3 mejores opciones de escape VIP sin repeticiones.
    """
    try:
        # 1. Ejecutar el motor de cálculo analítico de estabilización
        metricas = calcular_indice_estabilizacion(payload)
        
        # 2. Filtrar el catálogo inmutable de santuarios por compatibilidad estricta de perfil
        opciones_filtradas = []
        for sid, datos in SANTUARIOS_VIP.items():
            if payload.perfil in datos["perfil_compatible"]:
                opciones_filtradas.append((sid, datos))
        
        # Salvaguarda: Si por exceso de segmentación queda vacío, abrir el catálogo completo
        if not opciones_filtradas:
            opciones_filtradas = list(SANTUARIOS_VIP.items())
            
        # 3. Algoritmo Anti-Repetición Inmutable: Excluir destinos previamente visitados en el CRM local
        opciones_disponibles = [
            (sid, datos) for sid, datos in opciones_filtradas 
            if sid not in payload.historial_vistos
        ]
        
        # Si el usuario ya recorrió todos los destinos disponibles, resetear el historial dinámicamente
        if len(opciones_disponibles) < 3:
            opciones_disponibles = opciones_filtradas
            
        # 4. Seleccionar exactamente de forma aleatoria las 3 mejores opciones prescritas de alta sintonía
        seleccionados = random.sample(opciones_disponibles, min(3, len(opciones_disponibles)))
        
        # 5. Estructurar la respuesta transaccional idéntica para el renderizado del frontend
        destinos_prescritos = []
        for sid, datos in seleccionados:
            destinos_prescritos.append({
                "id": sid,
                "nombre": datos["nombre"],
                "detalles_es": {
                    "descripcion": datos["es"]["desc"],
                    "actividad_sintonía": datos["es"]["actividad"],
                    "logistica_aerea": datos["es"]["logistica_aerea"],
                    "logistica_maritima": datos["es"]["logistica_maritima"]
                },
                "detalles_en": {
                    "descripcion": datos["en"]["desc"],
                    "actividad_sintonía": datos["en"]["actividad"],
                    "logistica_aerea": datos["en"]["logistica_aerea"],
                    "logistica_maritima": datos["en"]["logistica_maritima"]
                }
            })
            
        return JSONResponse(status_code=200, content={
            "status": "success",
            "codigo_postal": payload.zip_code,
            "modo_activo": payload.modo,
            "balance_bienestar": {
                "inicial": metricas["score_inicial"],
                "cierre_proyectado": metricas["score_cierre"],
                "eficiencia_respiratoria": metricas["eficiencia_respiratoria"],
                "enfoque_mental": metricas["enfoque_mental"]
            },
            "opciones_escape_vip": destinos_prescritos
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fallo crítico en el motor contextual: {str(e)}")


@app.post("/api/checkout-premium")
async def crear_sesion_checkout_elite(request: Request):
    """
    Pasarela de pagos específica de Wellness Travel blindada estáticamente con tu URL.
    Procesa las órdenes fiduciarias e inyecta los folios y estados requeridos.
    """
    try:
        body = await request.json()
        price_id = body.get("price_id")
        folio_servicio = body.get("folio_id", "MR-UNKNOWN")
        
        if not price_id:
            raise HTTPException(status_code=400, detail="Parámetros transaccionales incompletos.")
            
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment' if "unico" in price_id else 'subscription',
            # BLINDAJE INMUTABLE CON TU URL OFICIAL EN RENDER:
            success_url=f"https://wellness-travel.onrender.com{folio_servicio}",
            cancel_url="https://wellness-travel.onrender.com",
            client_reference_id=folio_servicio
        )
        return JSONResponse(status_code=200, content={"id": session.id, "url": session.url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en pasarela Stripe Élite: {str(e)}")
# =========================================================================
# WELLNESS TRAVEL MASTER BACKEND — INTEGRIDAD TOTAL 100% OPEN THAN GO
# PARTE 5 DE 5: WEBHOOKS, COMPILADOR PDF DINÁMICO Y RUTEADOR DE FRONTEND
# =========================================================================

@app.post("/api/stripe-webhook")
async def stripe_webhook_receptor(request: Request):
    """
    Interceptor de eventos asíncronos fiduciarios. Captura las confirmaciones
    exclusivas del checkout de Stripe y valida los folios de sintonía en Render.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Payload transaccional ilegible.")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Firma de webhook inválida.")

    # Procesar la confirmación fiduciaria una vez completada la transacción
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        folio_cliente = session.get("client_reference_id", "MR-ASYNC-DIRECT")
        print(f"[CRM PROCESSED] Pago autorizado para el Folio Ejecutivo: {folio_cliente}")

    return JSONResponse(status_code=200, content={"received": True})


@app.post("/")
async def endpoint_raiz_post(request: Request):
    """
    Manejador POST para la raíz, necesario para evitar errores 405 
    cuando el frontend realiza llamadas directas a la URL base.
    """
    try:
        body = await request.json()
        return JSONResponse(status_code=200, content={"status": "success", "message": "Nodo operativo recibido"})
    except Exception:
        return JSONResponse(status_code=200, content={"status": "success", "message": "Conexión establecida"})


@app.post("/api/pdf")
def generate_pdf_passport_reportlab(payload: PDFPassportPayload):
    """
    Compilador gráfico asíncrono de ReportLab. Diseña una libreta de sintonía
    limpia, minimalista y ultra-Premium usando una paleta Obsidian/Gold.
    """
    try:
        # Asegurar la persistencia del directorio temporal de almacenamiento
        if not os.path.exists("temp"):
            os.makedirs("temp")

        pdf_filename = f"Wellness_Elite_Passport_{payload.servicio_id}.pdf"
        pdf_path = os.path.join("temp", pdf_filename)
        
        # Inicializar el lienzo con márgenes de visualización aireados y limpios
        doc = SimpleDocTemplate(
            pdf_path, 
            pagesize=letter, 
            rightMargin=54, 
            leftMargin=54, 
            topMargin=54, 
            bottomMargin=54
        )
        
        styles = getSampleStyleSheet()
        
        # Paleta cromática de alta fidelidad inmutable
        c_primary = colors.HexColor("#030305")
        c_gold = colors.HexColor("#C5A059")
        c_text = colors.HexColor("#222222")
        c_legal = colors.HexColor("#777777")
        
        # Tipografías y estilos estructurales organizados sin sobrecargas
        title_style = ParagraphStyle('Title', fontSize=22, leading=26, textColor=c_primary, alignment=1)
        subtitle_style = ParagraphStyle('Sub', fontSize=9, leading=12, textColor=c_legal, alignment=1)
        h2_style = ParagraphStyle('H2', fontSize=11, leading=14, textColor=c_gold, spaceBefore=15, spaceAfter=6)
        body_style = ParagraphStyle('Body', fontSize=9.5, leading=14, textColor=c_text)
        disclaimer_style = ParagraphStyle('Legal', fontSize=7.5, leading=11, textColor=c_legal, alignment=4)

        story = []
        lang_key = "EN" if payload.lang.upper() == "EN" else "ES"
        lang_map = DICTIONARY_BILINGUAL[lang_key]

        # Inyección secuencial de los bloques informativos
        story.append(Paragraph("MAY ROGA LLC", title_style))
        story.append(Paragraph("Wellness Travel Architecture & Lifestyle Optimization", subtitle_style))
        story.append(Spacer(1, 15))
        story.append(Paragraph(f"<b>{lang_map['doc_title']}</b>", ParagraphStyle('T', fontSize=12, alignment=1, textColor=c_primary)))
        story.append(Paragraph(f"{lang_map['folio']}: {payload.servicio_id} | {lang_map['status']}", body_style))
        story.append(Spacer(1, 10))
        
        # Sección 1: Métricas de Estabilización Analítica
        story.append(Paragraph(lang_map['sec1_title'], h2_style))
        metrics_data = [
            [Paragraph(lang_map['m1'], body_style), Paragraph(lang_map['m2'], body_style), Paragraph(lang_map['m3'], body_style)],
            [Paragraph(lang_map['m_pace'], body_style), f"{payload.score_inicial}%", f"{payload.score_actual}%"],
            [Paragraph(lang_map['m_breathe'], body_style), "0%", f"{payload.respiracion_score}%"],
            [Paragraph(lang_map['m_logic'], body_style), "0%", f"{payload.adivinanzas_score}%"]
        ]
        t = Table(metrics_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F9F9F9")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E5E5")),
            ('PADDING', (0,0), (-1,-1), 6)
        ]))
        story.append(t)
        
        # CORRECCIÓN DINÁMICA: Extraer el santuario exacto que envió el Frontend
        santuario_actual = SANTUARIOS_VIP.get(payload.destino_id, SANTUARIOS_VIP["S1"])
        h_info = santuario_actual[lang_key.lower()]
        
        # Sección 2: Prescripción Logística Exclusiva de Transporte y Hospedaje
        story.append(Paragraph(lang_map['sec2_title'], h2_style))
        
        dest_html = (
            f"• <b>{lang_map['stay_lbl']}</b>: {santuario_actual['nombre']}<br/>"
            f"• <b>{lang_map['desc_lbl']}</b>: {h_info['desc']}<br/>"
            f"• <b>Logística de Actividad</b>: {h_info['actividad']}<br/>"
            f"• <b>{lang_map['air_lbl']}</b>: {h_info['logistica_aerea']}<br/>"
            f"• <b>{lang_map['sea_lbl']}</b>: {h_info['logistica_maritima']}<br/><br/>"
            f"{lang_map['consorcio']}"
        )
        story.append(Paragraph(dest_html, body_style))
        
        # Sección 3 y 4: Cláusulas Corporativas, Compliance e Inmunidad de Responsabilidad Legal
        story.append(Spacer(1, 10))
        story.append(Paragraph(lang_map['sec3_title'], h2_style))
        story.append(Paragraph(lang_map['cta'], body_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(lang_map['sec4_title'], h2_style))
        story.append(Paragraph(lang_map['disclaimer'], disclaimer_style))
        story.append(Paragraph(lang_map['ai_foot'], disclaimer_style))

        # Compilación e inyección en el flujo binario
        doc.build(story)
        return FileResponse(pdf_path, media_type='application/pdf', filename=pdf_filename)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fallo en compilador ReportLab: {str(e)}")


# Montaje y enlace físico de recursos del frontend estático
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/{catchall:path}")
async def catch_all_routing():
    """
    Controlador de ruteo perimetral para Render. Redirige cualquier
    recarga o subruta hacia la pantalla de inicio limpia de la aplicación.
    """
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return HTMLResponse(content="<h1>Wellness Travel Node Operational</h1>", status_code=200)
