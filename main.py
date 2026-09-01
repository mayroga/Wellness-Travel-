# =========================================================================
# WELLNESS TRAVEL MASTER BACKEND — INTEGRIDAD TOTAL 100% EXCLUSIVIDAD ÉLITE
# ACTUALIZACIÓN MAESTRA: NÚCLEO PREDICTIVO SIN ESTADOS PERSONALES Y ROTACIÓN INFINITA
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
    description="Motor fiduciario de descompresión soberana y enrutamiento exclusivo sin fricción.",
    version="4.0.0"
)

# Inicialización fiduciaria y pasarelas de alta seguridad
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_mock_wellness_travel")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_mock")

# Esquemas de Control — Presupuesto asumido como ilimitado; cero estados emocionales personales
class SintonizacionPayload(BaseModel):
    zip_code: str = Field(..., pattern=r"^[0-9]{5}$")
    modo: str = Field(..., pattern=r"^(SALIR|CASA)$")
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
# DICCIONARIO MAESTRO BILINGÜE ÉLITE & POOL AMPLIADO DE MEDIOS / VÍDEOS
# =========================================================================

DICTIONARY_BILINGUAL = {
    "ES": {
        "doc_title": "PASAPORTE DE SINTONÍA Y DESCOMPRESIÓN SOBERANA",
        "folio": "Folio Ejecutivo de Enrutamiento",
        "status": "Estatus: Validado en Red Fiduciaria Local",
        "sec1_title": "1. MÉTRICAS DE OPTIMIZACIÓN DE TIEMPO Y ENFOQUE",
        "m1": "Indicador Evaluated", "m2": "Línea Base", "m3": "Nivel de Cierre",
        "m_pace": "Índice de Saturación Ambiental", 
        "m_breathe": "Tasa de Sincronización Acústica (432Hz)", 
        "m_logic": "Eficiencia de Decisión Ejecutiva",
        "sec2_title": "2. ENRUTAMIENTO DE ULTRA-LUJO PRESCRITO",
        "stay_lbl": "Santuario Asignado", 
        "desc_lbl": "Perfil de Aislamiento",
        "air_lbl": "Logística Aérea Privada", 
        "sea_lbl": "Corredor Marítimo",
        "consorcio": "Privilegios de Consorcio: Elegible automáticamente para créditos preferenciales y mejoras prioritarias de suite.",
        "sec3_title": "3. CONCLUSIONES DE ESTILO DE VIDA PREMIUM",
        "cta": "Este resumen certifica la descompresión del entorno y la optimización del activo más valioso: su tiempo soberano.",
        "sec4_title": "4. CUMPLIMIENTO Y PRIVACIDAD MAY ROGA LLC",
        "disclaimer": "Toda la información se procesa localmente en su terminal mediante almacenamiento seguro. El líder retiene el control absoluto de sus registros.",
        "ai_foot": "Documento exclusivo para fines informativos de estilo de vida premium. No constituye asesoramiento médico ni clínico."
    },
    "EN": {
        "doc_title": "SOVEREIGN WELLNESS & TUNING PASSPORT",
        "folio": "Executive Routing Folio ID",
        "status": "Status: Validated on Secure Node",
        "sec1_title": "1. TIME & EXECUTIVE FOCUS OPTIMIZATION METRICS",
        "m1": "Evaluated Metric", "m2": "Initial Baseline", "m3": "Closing Balance",
        "m_pace": "Environmental Saturation Index", 
        "m_breathe": "Acoustic Synchronization Rate (432Hz)", 
        "m_logic": "Executive Decision Efficiency",
        "sec2_title": "2. PRESCRIBED ULTRA-LUXY ROUTING",
        "stay_lbl": "Assigned Sanctuary", 
        "desc_lbl": "Isolation Profile",
        "air_lbl": "Private Air Logistics", 
        "sea_lbl": "Elite Maritime Corridor",
        "consorcio": "Consortium Privileges: Automatically eligible for preferred executive credits and priority suite upgrades.",
        "sec3_title": "3. PREMIUM LIFESTYLE INSIGHTS",
        "cta": "This document certifies environmental decompression and the optimization of your most valuable asset: sovereign time.",
        "sec4_title": "4. CORPORATE PRIVACY ASSURANCE — MAY ROGA LLC",
        "disclaimer": "All digital metrics are processed strictly locally on your browser terminal. The principal retains total control over records.",
        "ai_foot": "Exclusive document for premium lifestyle and travel informational purposes only. Not clinical advice."
    }
}

# Pool ampliado de 12 Santuarios VIP con variantes de vídeos y protocolos únicos de descompresión
SANTUARIOS_VIP = {
    "S1": {
        "nombre": "Amanera Resort — Playa Grande",
        "perfil_compatible": ["solo", "acompanado"],
        "video_url": "https://www.youtube.com/embed/mock_amanera_432hz",
        "es": {
            "desc": "Casitas zen minimalistas suspendidas sobre acantilados protegidos en la selva virgen.",
            "actividad": "Protocolo acústico de 432Hz y aislamiento ambiental absoluto frente al mar.",
            "logistica_aerea": "Vuelo charter privado en Gulfstream G650 hasta el aeródromo ejecutivo.",
            "logistica_maritima": "Yate de colección de 80 pies disponible para descompresión en alta mar."
        },
        "en": {
            "desc": "Minimalist zen casitas suspended over protected cliffs in the pristine jungle.",
            "actividad": "432Hz acoustic protocol and absolute oceanfront environmental isolation.",
            "logistica_aerea": "Private Gulfstream G650 charter flight to executive airfield.",
            "logistica_maritima": "80-foot collector yacht available for open-ocean leisure."
        }
    },
    "S2": {
        "nombre": "Eden Roc Cap Cana — Boutique Sanctuary",
        "perfil_compatible": ["acompanado", "familia", "empresa"],
        "video_url": "https://www.youtube.com/embed/mock_edenroc_biohacking",
        "es": {
            "desc": "Bungalows independientes con piscinas privadas y acceso restringido a lagunas naturales.",
            "actividad": "Sincronización hemisférica y cena sensorial curada por chef ejecutivo.",
            "logistica_aerea": "Acceso VIP mediante FBO privado y helicóptero directo al helipuerto.",
            "logistica_maritima": "Embarcación Riva Aquarama para accesos directos desde la marina."
        },
        "en": {
            "desc": "Standalone bungalows with private pools and restricted natural lagoon access.",
            "actividad": "Hemispheric synchronization and executive chef-curated sensory dining.",
            "logistica_aerea": "VIP access via private FBO and direct helicopter transfer.",
            "logistica_maritima": "Riva Aquarama vessel for direct boarding from private marina."
        }
    },
    "S3": {
        "nombre": "Amangiri Sanctuary — Desert Solitude",
        "perfil_compatible": ["solo", "acompanado", "empresa"],
        "video_url": "https://www.youtube.com/embed/mock_amangiri_silence",
        "es": {
            "desc": "Arquitectura monolítica oculta en cañones desérticos. Diseñado para recuperar el control del silencio.",
            "actividad": "Sesión nocturna de aislamiento acústico total sin contaminación lumínica.",
            "logistica_aerea": "Charter privado Bombardier Global 7500 con tripulación dedicada.",
            "logistica_maritima": "No aplica. Logística terrestre con flota de vehículos blindados de confort."
        },
        "en": {
            "desc": "Monolithic architecture hidden inside deep desert canyons. Engineered to regain quietness.",
            "actividad": "Nightly total acoustic isolation session shielded from light pollution.",
            "logistica_aerea": "Private Bombardier Global 7500 flight with dedicated vetted crew.",
            "logistica_maritima": "Not applicable. Secured luxury ground transport fleet."
        }
    },
    "S4": {
        "nombre": "Singita Lebombo — Private Wilderness Lodge",
        "perfil_compatible": ["familia", "empresa", "accesible"],
        "video_url": "https://www.youtube.com/embed/mock_singita_focus",
        "es": {
            "desc": "Villas de cristal suspendidas sobre parajes naturales con accesibilidad total y diseño de vanguardia.",
            "actividad": "Inmersión guiada de claridad estratégica y rastreo de alta fidelidad.",
            "logistica_aerea": "Conexión directa en jet privado intercontinental y avioneta monomotor exclusiva.",
            "logistica_maritima": "Exploración fluvial en embarcación privada eco-sustentable de alta gama."
        },
        "en": {
            "desc": "Elevated glass villas hovering over wild nature fields with full accessibility.",
            "actividad": "Guided strategic clarity immersion and high-fidelity tracking.",
            "logistica_aerea": "Direct private intercontinental jet routing linking with exclusive aircraft.",
            "logistica_maritima": "River exploration on a private bespoke high-end vessel."
        }
    },
    "S5": {
        "nombre": "The Brando — Tetiaroa Private Atoll",
        "perfil_compatible": ["solo", "acompanado", "familia"],
        "video_url": "https://www.youtube.com/embed/mock_brando_atoll",
        "es": {
            "desc": "Santuario polinesio ultra-exclusivo accesible únicamente por aire privado.",
            "actividad": "Hidroterapia de alta frecuencia y recalibración de ritmos circadianos.",
            "logistica_aerea": "Air Tetiaroa privado desde Faa'a International Airport en Papeete.",
            "logistica_maritima": "Catamarán privado de apoyo logístico para navegación en atolón."
        },
        "en": {
            "desc": "Ultra-exclusive Polynesian sanctuary accessible solely via private air routing.",
            "actividad": "High-frequency hydrotherapy and circadian rhythm recalibration.",
            "logistica_aerea": "Private Air Tetiaroa routing directly from Papeete International.",
            "logistica_maritima": "Private logistics catamaran for atoll navigation."
        }
    },
    "S6": {
        "nombre": "Laucala Island — Private Hill Estate",
        "perfil_compatible": ["solo", "empresa", "acompanado"],
        "video_url": "https://www.youtube.com/embed/mock_laucala_island",
        "es": {
            "desc": "Propiedad insular masiva con selva tropical, playas de arena blanca y máxima privacidad.",
            "actividad": "Protocolo de desconexión ejecutiva y optimización de oxígeno hiperbárico.",
            "logistica_aerea": "King Air privado directo a la pista de aterrizaje asfaltada de la isla.",
            "logistica_maritima": "Submarino personal DeepFlight Super Falcon para expediciones submarinas."
        },
        "en": {
            "desc": "Massive island estate featuring tropical jungle, white beaches, and supreme privacy.",
            "actividad": "Executive disconnection protocol and hyperbaric oxygen optimization.",
            "logistica_aerea": "Private King Air direct to the island's paved air strip.",
            "logistica_maritima": "Personal DeepFlight Super Falcon submarine for deep-sea exploration."
        }
    },
    "S7": {
        "nombre": "Clayoquot Wilderness Lodge — Vancouver Island",
        "perfil_compatible": ["solo", "acompanado", "empresa"],
        "video_url": "https://www.youtube.com/embed/mock_clayoquot_lodge",
        "es": {
            "desc": "Campamento de lona de lujo elevado sobre fiordos remotos en la selva templada de Canadá.",
            "actividad": "Terapia de aislamiento en bosque antiguo y flotación en aguas glaciales.",
            "logistica_aerea": "Hidroavión privado ejecutivo desde el puerto de Vancouver directo al muelle.",
            "logistica_maritima": "Crucero privado de expedición por fiordos protegidos."
        },
        "en": {
            "desc": "Luxury canvas encampment elevated over remote fjords in the temperate rainforest.",
            "actividad": "Old-growth forest isolation therapy and glacial water floating.",
            "logistica_aerea": "Private executive seaplane from Vancouver harbor direct to dock.",
            "logistica_maritima": "Private expedition cruiser through protected fjords."
        }
    },
    "S8": {
        "nombre": "Nihi Sumba — Edge of Wildness",
        "perfil_compatible": ["solo", "acompanado", "familia"],
        "video_url": "https://www.youtube.com/embed/mock_nihi_sumba",
        "es": {
            "desc": "Resort costero remoto enfocado en la libertad soberana y el surf de clase mundial sin presencia de masas.",
            "actividad": "Ecualización mental mediante frecuencias oceánicas y retiro ecuestre privado.",
            "logistica_aerea": "Vuelo charter interno en turbohélice privado y helicóptero de enlace.",
            "logistica_maritima": "Yate motovelero de expedición para navegación costera exclusiva."
        },
        "en": {
            "desc": "Remote coastal sanctuary focused on sovereign freedom and world-class surf without crowds.",
            "actividad": "Mental equalization via ocean frequencies and private equestrian retreat.",
            "logistica_aerea": "Internal private turboprop charter and connecting executive helicopter.",
            "logistica_maritima": "Expedition motor-sailer yacht for exclusive coastal cruising."
        }
    },
    "S9": {
        "nombre": "Fogo Island Inn — Newfoundland Edge",
        "perfil_compatible": ["solo", "acompanado", "empresa"],
        "video_url": "https://www.youtube.com/embed/mock_fogo_island",
        "es": {
            "desc": "Arquitectura brutalista flotante al borde de la tierra, frente al Atlántico Norte.",
            "actividad": "Contemplación estática y protocolo de enfoque estratégico contra tormentas.",
            "logistica_aerea": "Jet ejecutivo hasta Gander y conexión privada en bimotor.",
            "logistica_maritima": "Bote de investigación costera adaptado para observación de icebergs."
        },
        "en": {
            "desc": "Floating brutalist architecture on the edge of the earth facing the North Atlantic.",
            "actividad": "Static contemplation and storm-resistant strategic focus protocol.",
            "logistica_aerea": "Executive jet to Gander and private twin-engine connection.",
            "logistica_maritima": "Coastal research vessel adapted for iceberg observation."
        }
    },
    "S10": {
        "nombre": "And Beyond Mnemba Island — Zanzibar Atoll",
        "perfil_compatible": ["solo", "acompanado"],
        "video_url": "https://www.youtube.com/embed/mock_mnemba_island",
        "es": {
            "desc": "Isla privada desierta con diez bandas de lujo rústico y arrecife de coral protegido.",
            "actividad": "Sintonía subacuática y aislamiento sensorial marina sin interrupciones.",
            "logistica_aerea": "Helicóptero ejecutivo desde el aeropuerto internacional de Zanzíbar.",
            "logistica_maritima": "Lancha rápida privada de alta velocidad y dhow tradicional de colección."
        },
        "en": {
            "desc": "Deserted private island featuring ten rustic luxury bandas and protected coral reef.",
            "actividad": "Underwater tuning and uninterrupted marine sensory isolation.",
            "logistica_aerea": "Executive helicopter directly from Zanzibar International Airport.",
            "logistica_maritima": "Private high-speed launch and traditional collector dhow."
        }
    },
    "S11": {
        "nombre": "North Island — Seychelles Sanctuary",
        "perfil_compatible": ["familia", "acompanado", "empresa"],
        "video_url": "https://www.youtube.com/embed/mock_north_island",
        "es": {
            "desc": "Diez villas hiper-privadas integradas en la naturaleza granítica de una isla conservada.",
            "actividad": "Restauración biológica y mapeo de claridad ejecutiva en entorno virgen.",
            "logistica_aerea": "Helicóptero bimotor directo desde la terminal VIP de Mahe.",
            "logistica_maritima": "Yate catamarán de lujo operativo 24/7 para traslados insulares."
        },
        "en": {
            "desc": "Ten hyper-private villas integrated into the granitic nature of a preserved island.",
            "actividad": "Biological restoration and executive clarity mapping in a pristine setting.",
            "logistica_aerea": "Twin-engine executive helicopter direct from Mahe VIP terminal.",
            "logistica_maritima": "Luxury catamaran yacht operational 24/7 for island transfers."
        }
    },
    "S12": {
        "nombre": "Quasar Expeditions — Galapagos Yacht Sanctuary",
        "perfil_compatible": ["solo", "acompanado", "empresa", "familia"],
        "video_url": "https://www.youtube.com/embed/mock_quasar_galapagos",
        "es": {
            "desc": "Yate expedicionario privado de ultra-lujo navegando en archipiélago protegido de señales.",
            "actividad": "Descompresión en mar abierto con desconexión satelital selectiva.",
            "logistica_aerea": "Vuelo ejecutivo privado hasta Baltra o San Cristóbal.",
            "logistica_maritima": "Yate privado de expedición con tripulación y naturalistas expertos."
        },
        "en": {
            "desc": "Private ultra-luxury expedition yacht cruising a signal-protected archipelago.",
            "actividad": "Open-ocean decompression featuring selective satellite disconnection.",
            "logistica_aerea": "Private executive flight to Baltra or San Cristobal.",
            "logistica_maritima": "Private expedition yacht with dedicated expert crew."
        }
    }
}

# =========================================================================
# MOTOR ANALÍTICO DE ESTABILIZACIÓN SIN ESTADOS PERSONALES
# =========================================================================
def calcular_indice_estabilizacion(payload: SintonizacionPayload) -> dict:
    base_score = 50.0  # Baseline inicial estándar sin sesgo emocional
    
    # Modificadores basados estrictamente en el perfil y modo operativo
    modificadores_perfil = {
        "solo": 10.0,
        "acompanado": 5.0,
        "familia": -5.0,
        "empresa": -15.0,  # Alta densidad corporativa
        "accesible": 0.0
    }
    
    score_inicial = base_score + modificadores_perfil.get(payload.perfil, 0.0)
    score_inicial = max(15.0, min(90.0, score_inicial))
    
    # Análisis del texto libre o comando de voz para ajustar la métrica de entorno
    interceptor_friccion = 0.0
    if payload.texto_libre:
        palabras_saturacion = ["ruido", "saturacion", "agenda", "tiempo", "vuelo", "reunion", "entorno", "exceso", "reuniones", "mercado"]
        conteo = sum(1 for palabra in palabras_saturacion if palabra in payload.texto_libre.lower())
        interceptor_friccion = conteo * -4.0
        
    score_inicial = max(10.0, score_inicial + interceptor_friccion)
    score_cierre = min(100.0, score_inicial + 50.0)
    
    return {
        "score_inicial": round(score_inicial, 2),
        "score_cierre": round(score_cierre, 2),
        "eficiencia_respiratoria": 100.0,
        "enfoque_mental": 100.0
    }

# =========================================================================
# ENDPOINTS DE EJECUCIÓN Y RUTEO ÉLITE
# =========================================================================

@app.post("/api/sintonizar")
async def endpoint_sintonizar_contextual(payload: SintonizacionPayload):
    """
    Core predictivo. Asume presupuesto ilimitado, omite estados personales y garantiza
    variabilidad infinita (combinando 12 santuarios y protocolos de vídeo únicos).
    """
    try:
        metricas = calcular_indice_estabilizacion(payload)
        
        # Filtrado por perfil de compatibilidad
        opciones_filtradas = [
            (sid, datos) for sid, datos in SANTUARIOS_VIP.items()
            if payload.perfil in datos["perfil_compatible"]
        ]
        if not opciones_filtradas:
            opciones_filtradas = list(SANTUARIOS_VIP.items())
            
        # Anti-Repetición Inmutable basado en CRM local
        opciones_disponibles = [
            (sid, datos) for sid, datos in opciones_filtradas 
            if sid not in payload.historial_vistos
        ]
        if len(opciones_disponibles) < 3:
            opciones_disponibles = opciones_filtradas
            
        # Selección aleatoria garantizada para que cada entrada sea completamente distinta
        seleccionados = random.sample(opciones_disponibles, min(3, len(opciones_disponibles)))
        
        destinos_prescritos = []
        for sid, datos in seleccionados:
            destinos_prescritos.append({
                "id": sid,
                "nombre": datos["nombre"],
                "video_url": datos["video_url"],
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
    Pasarela de pagos blindada con enrutamiento inmutable y URL oficial en Render.
    """
    try:
        body = await request.json()
        price_id = body.get("price_id")
        folio_servicio = body.get("folio_id", "MR-SOVEREIGN")
        
        if not price_id:
            raise HTTPException(status_code=400, detail="Parámetros transaccionales incompletos.")
            
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment' if "unico" in price_id else 'subscription',
            success_url=f"https://wellness-travel.onrender.com{folio_servicio}",
            cancel_url="https://wellness-travel.onrender.com",
            client_reference_id=folio_servicio
        )
        return JSONResponse(status_code=200, content={"id": session.id, "url": session.url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en pasarela Stripe Élite: {str(e)}")


@app.post("/api/stripe-webhook")
async def stripe_webhook_receptor(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Payload transaccional ilegible.")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Firma de webhook inválida.")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        folio_cliente = session.get("client_reference_id", "MR-ASYNC-DIRECT")
        print(f"[CRM PROCESSED] Orden ejecutada para el Folio: {folio_cliente}")

    return JSONResponse(status_code=200, content={"received": True})


@app.post("/")
async def endpoint_raiz_post(request: Request):
    try:
        await request.json()
        return JSONResponse(status_code=200, content={"status": "success", "message": "Nodo operativo recibido"})
    except Exception:
        return JSONResponse(status_code=200, content={"status": "success", "message": "Conexión establecida"})


@app.post("/api/pdf")
def generate_pdf_passport_reportlab(payload: PDFPassportPayload):
    """
    Compilador gráfico ReportLab optimizado para generar el Pasaporte de Sintonía Fiduciaria.
    """
    try:
        if not os.path.exists("temp"):
            os.makedirs("temp")

        pdf_filename = f"Sovereign_Passport_{payload.servicio_id}.pdf"
        pdf_path = os.path.join("temp", pdf_filename)
        
        doc = SimpleDocTemplate(
            pdf_path, 
            pagesize=letter, 
            rightMargin=54, 
            leftMargin=54, 
            topMargin=54, 
            bottomMargin=54
        )
        
        styles = getSampleStyleSheet()
        c_primary = colors.HexColor("#030305")
        c_gold = colors.HexColor("#C5A059")
        c_text = colors.HexColor("#222222")
        c_legal = colors.HexColor("#777777")
        
        title_style = ParagraphStyle('Title', fontSize=22, leading=26, textColor=c_primary, alignment=1)
        subtitle_style = ParagraphStyle('Sub', fontSize=9, leading=12, textColor=c_legal, alignment=1)
        h2_style = ParagraphStyle('H2', fontSize=11, leading=14, textColor=c_gold, spaceBefore=15, spaceAfter=6)
        body_style = ParagraphStyle('Body', fontSize=9.5, leading=14, textColor=c_text)
        disclaimer_style = ParagraphStyle('Legal', fontSize=7.5, leading=11, textColor=c_legal, alignment=4)

        story = []
        lang_key = "EN" if payload.lang.upper() == "EN" else "ES"
        lang_map = DICTIONARY_BILINGUAL[lang_key]

        story.append(Paragraph("MAY ROGA LLC", title_style))
        story.append(Paragraph("Sovereign Lifestyle Architecture & Time Optimization", subtitle_style))
        story.append(Spacer(1, 15))
        story.append(Paragraph(f"<b>{lang_map['doc_title']}</b>", ParagraphStyle('T', fontSize=12, alignment=1, textColor=c_primary)))
        story.append(Paragraph(f"{lang_map['folio']}: {payload.servicio_id} | {lang_map['status']}", body_style))
        story.append(Spacer(1, 10))
        
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
        
        santuario_actual = SANTUARIOS_VIP.get(payload.destino_id, SANTUARIOS_VIP["S1"])
        h_info = santuario_actual[lang_key.lower()]
        
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
        
        story.append(Spacer(1, 10))
        story.append(Paragraph(lang_map['sec3_title'], h2_style))
        story.append(Paragraph(lang_map['cta'], body_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(lang_map['sec4_title'], h2_style))
        story.append(Paragraph(lang_map['disclaimer'], disclaimer_style))
        story.append(Paragraph(lang_map['ai_foot'], disclaimer_style))

        doc.build(story)
        return FileResponse(pdf_path, media_type='application/pdf', filename=pdf_filename)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fallo en compilador ReportLab: {str(e)}")

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/{catchall:path}")
async def catch_all_routing(catchall: str):
    if catchall.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return HTMLResponse(content="<h1>Sovereign Wellness Node Operational</h1>", status_code=200)
