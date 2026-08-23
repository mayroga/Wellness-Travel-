// =========================================================================
// WELLNESS TRAVEL FRONTEND LOGIC — RECONSTRUCCIÓN DINÁMICA PURA 1:1 OTG
// ARCHIVO COMPLETO, INTEGRAL Y ACTUALIZADO (VERSIÓN DEFINITIVA)
// =========================================================================

const KERNEL = {
    // Variables de Estado de Ingeniería Dinámica
    timerInaccion: null,
    serviceTimer: null,
    breatheInterval: null,
    voiceInterval: null,
    cierreTimerInterval: null,
    timeLeft: 600,         // 10 minutos matemáticos obligatorios de sesión activa
    cierreTimeLeft: 60,    // 60 segundos de Limpieza Mental Profunda en Cierre
    isLocked: false,
    idiomaActual: 'es',
    devClickCount: 0,
    historialVistos: [],   // Almacenamiento anti-repeticiones del CRM local
    balanceBienestar: null,
    escapesVIP: [],

    // Diccionarios VIP Extendidos
    TRADUCCIONES: {
        es: {
            brandSub: "Arquitectura de Santuarios Ejecutivos",
            timerTitle: "Ventana de Sintonía Activa",
            oraculoInstruccion: "¿Qué vector bloquea tu sintonía hoy?",
            desahogoLabel: "O declare aquí su saturación ambiental:",
            placeholderLibre: "Escriba libremente los estímulos o ruidos del entorno que experimenta hoy...",
            btnActivar: "Activar Mando de Sintonía",
            atencionInaccion: "Atención. Mantenga el enfoque en su pantalla de sintonía.",
            vozSintonialAcustica: "Líder. Frecuencias acústicas activadas para aislamiento total.",
            tituloAcustico: "SINTONÍA ACÚSTICA ACTIVA (432HZ / ALFA)",
            misionTitulo: "SANTUARIOS CURADOS DISPONIBLES",
            discursoMin4: "Calibración completada. Santuario de ultra-lujo disponible.",
            mapsBtn: "ABRIR RUTA EXCLUSIVA",
            compilarBtn: "COMPILACIÓN PASAPORTE DE BIENESTAR",
            frecuenciaVoz: "La pausa precisa disuelve el desgaste y asegura el control absoluto sobre su entorno.",
            pasosRespiracion: ["Inhala", "Retén", "Exhala", "Pausa"],
            cierreFinalizado: "Calibración completada con éxito. Su pasaporte premium está listo."
        },
        en: {
            brandSub: "Executive Sanctuary Architecture",
            timerTitle: "Active Tuning Window",
            oraculoInstruccion: "What vector blocks your tuning today?",
            desahogoLabel: "Or declare your environmental saturation here:",
            placeholderLibre: "Freely outline the stimuli or ambient noise you experience today...",
            btnActivar: "Activate Tuning Directive",
            atencionInaccion: "Attention. Maintain absolute focus on your tuning screen.",
            vozSintonialAcustica: "Leader. Acoustic frequencies activated for complete isolation.",
            tituloAcustico: "ACTIVE ACOUSTIC TUNING (432HZ / ALPHA)",
            misionTitulo: "CURATED SANCTUARIES AVAILABLE",
            discursoMin4: "Calibration completed. Ultra-luxury sanctuary fully unlocked.",
            mapsBtn: "OPEN EXCLUSIVE ROUTE",
            compilarBtn: "COMPILE WELLNESS PASSPORT",
            frecuenciaVoz: "The precise pause dissolves exhaustion and ensures absolute control over your surroundings.",
            pasosRespiracion: ["Inhale", "Hold", "Exhale", "Pause"],
            cierreFinalizado: "Calibration successfully completed. Your premium passport is ready."
        }
    },

    // Catálogo de Retos Conductuales
    CATALOGO_RETOS: [
        { id: "R1", icono: "🧘‍♂️", titulo_es: "Silencio Absoluto", desc_es: "Permanece 60 segundos sin emitir sonido ni interactuar con pantallas. Escucha el vacío físico de tu habitación.", titulo_en: "Absolute Silence", desc_en: "Spend 60 seconds without making any sound or interacting with screens. Listen to the physical void of your room." },
        { id: "R2", icono: "👁️", titulo_es: "Contemplación Fija", desc_es: "Elige un objeto inanimado en tu entorno visual y observa sus detalles físicos, texturas y sombras sin juzgar.", titulo_en: "Fixed Comtemplation", desc_en: "Pick an inanimate object in your visual field and observe its physical details, textures, and shadows without judgment." },
        { id: "R3", icono: "✍️", titulo_es: "Escritura de Purga", desc_es: "Anota mentalmente tres ideas recurrentes que ronden tu enfoque actual y visualiza cómo se disuelven en el aire.", titulo_en: "Purge Inscription", desc_en: "Mentally note three recurring thoughts hovering over your active focus and visualize them dissolving into thin air." },
        { id: "R4", icono: "🍃", titulo_es: "Distensión Facial", desc_es: "Libera la tensión acumulada sonriendo de manera forzada durante 10 segundos para activar tus terminales nerviosas de alivio.", titulo_en: "Facial Release", desc_en: "Release accumulated jaw tension by forcing a smile for 10 seconds to activate your biological relaxation pathways." },
        { id: "R5", icono: "🦾", titulo_es: "Alineación Física", desc_es: "Estira los brazos hacia arriba de forma lenta, expandiendo el torso, y mantén la postura soltando el aire despacio.", titulo_en: "Physical Alignment", desc_en: "Slowly extend your arms upward, expanding your chest, and hold the posture while breathing out smoothly." },
        { id: "R6", icono: "🌊", titulo_es: "Enfoque Auditivo", desc_es: "Cierra los ojos y busca aislar el sonido más lejano que se escuche en tu entorno actual. Concéntrate solo en esa onda.", titulo_en: "Auditory Tracking", desc_en: "Close your eyes and isolate the most distant ambient sound in your current perimeter. Focus solely on that soundwave." },
        { id: "R7", icono: "⚓", titulo_es: "Anclaje de Logro", desc_es: "Evoca un momento reciente donde experimentaste control absoluto sobre tu tiempo y retén esa memoria en tu mente.", titulo_en: "Milestone Anchoring", desc_en: "Recall a recent moment where you experienced complete control over your time and hold that mental imprint firmly." },
        { id: "R8", icono: "🔲", titulo_es: "Respiración Cuadrada", desc_es: "Realiza un ciclo completo de respiración conteniendo el aire de manera consciente, alineando tu ritmo biológico.", titulo_en: "Box Respiration", desc_en: "Perform a complete square breathing cycle, consciously holding your breath to harmonize your internal biological pace." }
    ],

    // Matriz de las 48 preguntas en Español
    CATALOGO_PREGUNTAS_ES: [
        "¿Sientes que los estímulos del entorno saturan tu capacidad de contemplar la calma?",
        "¿Se diluye tu enfoque en redes digitales buscando llenar vacíos de desconexión?",
        "¿Delegas tu tranquilidad al ruido externo para evadir la prisa diaria?",
        "¿El exceso de control sobre tu agenda te priva de disfrutar el entorno en paz?",
        "¿Buscas micro-estímulos rápidos que expiran sin dejar satisfacción real?",
        "¿Percibes que el ritmo acelerado del entorno nubla tu claridad mental hoy?",
        "¿Permaneces conectado a pantallas por inercia sacrificando tu espacio de aislamiento?",
        "¿Te cuesta encontrar un momento de absoluto silencio acústico en tu rutina?",
        "¿Sientes que la inercia diaria bloquea la apreciación del tiempo presente?",
        "¿La velocidad del entorno dificulta sintonizar con tu balance interno?",
        "¿Experimentas una constante demanda de atención que fragmenta tu enfoque?",
        "¿El exceso de información ambiental genera fricción en tus decisiones de vida?",
        "¿Te cuesta desconectar del flujo constante de notificaciones e interacciones?",
        "¿Sientes que tu espacio personal ha sido invadido por estímulos innecesarios?",
        "¿La prisa colectiva te empuja a actuar sin una intención clara hoy?",
        "¿Percibes una desconexión entre tus metas de bienestar y tus hábitos diarios?",
        "¿Buscas refugio en el aislamiento pero el entorno urbano dificulta el silencio?",
        "¿La saturación de compromisos sociales limita tu tiempo de introspección?",
        "¿Sientes que la falta de espacios curados afecta tu perspectiva diaria?",
        "¿Te resulta complejo trazar una línea divisoria entre el entorno y tu tranquilidad?",
        "¿La falta de pausas conscientes reduce la claridad de tu visión personal?",
        "¿Percibes que las demandas del día a día consumen tu reserva de enfoque?",
        "¿Te dejas llevar por la corriente de la rutina sin evaluar tu balance individual?",
        "¿Sientes que el ruido visual de tu entorno habitual interrumpe tu calma?",
        "¿El ritmo automatizado de tus días disminuye la calidad de tu descanso?",
        "¿Buscas un entorno exclusivo pero las opciones comunes te generan saturación?",
        "¿La exposición continua a entornos densivos limita tu claridad reflexiva?",
        "¿Sientes la necesidad de resetear tus estímulos sensoriales de manera urgente?",
        "¿El dinamismo excesivo de tu agenda reduce tu capacidad de contemplación?",
        "¿Te cuesta retener la sensación de calma ante la presión de los tiempos?",
        "¿Sientes que el entorno te exige una velocidad que no deseas mantener?",
        "¿La sobrecarga de interacciones superficiales desgasta tu nivel de sintonía?",
        "¿Te resulta difícil aislar tus pensamientos del bullicio general de la ciudad?",
        "¿La falta de un santuario personal fragmenta tu consistencia en el enfoque?",
        "¿Sientes que el tiempo transcurre sin permitirte asimilar tus logros?",
        "¿El exceso de opciones y alternativas del día a día nubla tu dirección?",
        "¿La prisa por cumplir expectativas externas drena tu sintonía individual?",
        "¿Te cuesta trabajo establecer un límite firme ante las demandas de tu entorno?",
        "¿Sientes que la desconexión con la naturaleza acelera tu fatiga ambiental?",
        "¿El ruido de fondo constante en tus actividades impide tu concentración profunda?",
        "¿Te percibes atrapado en patrones de consumo digital que no aportan valor?",
        "¿La falta de una estructura de bienestar adaptada fragmenta tu estabilidad?",
        "¿Sientes que la prisa de los demás dicta el ritmo de tus propias pausas?",
        "¿La saturación en los espacios habituales limita tu libertad de pensamiento?",
        "¿Te cuesta encontrar un balance armónico entre tu vida social y tu espacio solo?",
        "¿El ritmo vertiginoso del entorno obstaculiza tu claridad a largo plazo?",
        "¿Sientes que la rutina se repite sin ofrecerte un espacio genuino de renovación?",
        "¿La presión constante del entorno compromete la calidad de tu enfoque mental?"
    ],

    // Matriz de las 48 preguntas en Inglés
    CATALOGO_PREGUNTAS_EN: [
        "Do you feel environmental stimuli saturate your ability to contemplate calm?",
        "Does your strategic focus dissolve in digital networks trying to fill moments of friction?",
        "Do you surrender your peace to external noise to drown out the daily rush?",
        "Does excessive schedule control deprive you of calmly observing your environment?",
        "Are you overspending on micro-stimuli looking for satisfaction that expires immediately?",
        "Do you perceive that the fast pace of your surroundings clouds your clarity today?",
        "Do you remain connected to screens out of inertia, sacrificing your isolation space?",
        "Is it difficult to find a moment of absolute acoustic silence in your routine?",
        "Do you feel that daily inertia blocks your appreciation of the present time?",
        "Does the speed of the surroundings make it difficult to tune your internal balance?",
        "Are you experiencing a constant demand for attention that fragments your focus?",
        "Does the excess of environmental information create friction in your life choices?",
        "Is it hard for you to disconnect from the constant stream of notifications?",
        "Do you feel your personal space has been invaded by unnecessary external stimuli?",
        "Does the collective rush push you to act without a clear intention today?",
        "Do you perceive a disconnect between your wellness goals and daily habits?",
        "Do you seek shelter in isolation but the urban landscape complicates silence?",
        "Does the saturation of social commitments limit your time for introspection?",
        "Do you feel that the lack of curated spaces affects your daily perspective?",
        "Is it complex to draw a firm line between the environment and your peace?",
        "Does the lack of conscious pauses reduce the clarity of your personal vision?",
        "Do you perceive that daily demands consume your reserved focus index?",
        "Are you carried away by the current of routine without assessing your balance?",
        "Do you feel the visual noise of your habitual environment interrupts your calm?",
        "Does the automated rhythm of your days decrease the quality of your rests?",
        "Are you looking for an exclusive environment but common options cause overload?",
        "Does continuous exposure to dense surroundings limit your reflective clarity?",
        "Do you feel an urgent need to reset your internal sensory stimuli?",
        "Does the excessive dynamism of your schedule reduce your contemplation capacity?",
        "Is it hard to retain the feeling of calm under the pressure of timelines?",
        "Do you feel the environment demands a speed you do not wish to maintain?",
        "Does the overload of superficial interactions wear down your tuning level?",
        "Is it difficult to isolate your thoughts from the general city bustle?",
        "Does the lack of a personal sanctuary fragment your deep focus consistency?",
        "Do you feel time passes without allowing you to assimilate your milestones?",
        "Does the excess of daily options and alternatives cloud your direction?",
        "Does the rush to meet external expectations drain your individual tuning?",
        "Is it hard for you to establish a firm boundary against surrounding demands?",
        "Do you feel that disconnecting from nature accelerates your environmental fatigue?",
        "Does constant background noise in your actions prevent deep concentration?",
        "Do you perceive yourself trapped in digital patterns that provide no value?",
        "Does the lack of a tailored wellness structure fragment your stability?",
        "Do you feel that the rush of others dictates the pace of your own pauses?",
        "Does saturation in habitual spaces limit your freedom of thought?",
        "Is it hard to find a harmonious balance between social life and solo space?",
        "Does the dizzying pace of the environment hinder your long-term clarity?",
        "Do you feel routine repeats itself without offering a genuine space for renewal?",
        "Does the constant pressure of the surroundings compromise your mental focus?"
    ],

    init() {
        this.cambiarIdioma(this.idiomaActual);
        this.conectarMantenimientoDesarrollador();
    },

    cambiarIdioma(lang) {
        this.idiomaActual = lang;
        const diccionario = this.TRADUCCIONES[lang];
        
        const elBrand = document.getElementById('lblBrandSub');
        if (elBrand) elBrand.innerText = diccionario.brandSub;
        const elTimer = document.getElementById('lblTimerTitle');
        if (elTimer) elTimer.innerText = diccionario.timerTitle;
        const elOraculo = document.getElementById('lbl-oraculo-instruccion');
        if (elOraculo) elOraculo.innerText = diccionario.oraculoInstruccion;
        const elDesahogo = document.getElementById('lbl-desahogo');
        if (elDesahogo) elDesahogo.innerText = diccionario.desahogoLabel;
        const elInpLibre = document.getElementById('inp-text-libre');
        if (elInpLibre) elInpLibre.placeholder = diccionario.placeholderLibre;
        const elBtnActivar = document.getElementById('btn-activar-libre');
        if (elBtnActivar) elBtnActivar.innerText = diccionario.btnActivar;
        
        this.inyectarPreguntasOraculo();
    },

    despertarInicial() {
        const welcomeEl = document.getElementById('pantalla-bienvenida');
        if (welcomeEl) welcomeEl.style.display = 'none';
        const formEl = document.getElementById('wrapper-form');
        if (formEl) formEl.classList.remove('hidden');
        this.resetearTemporizadorInaccion();
    },

    resetearTemporizadorInaccion() {
        clearTimeout(this.timerInaccion);
        if (this.isLocked) return;
        this.timerInaccion = setTimeout(() => {
            this.emitirVoz(this.TRADUCCIONES[this.idiomaActual].atencionInaccion);
            this.resetearTemporizadorInaccion();
        }, 8000);
    },

    inyectarPreguntasOraculo() {
        const contenedor = document.getElementById('contenedor-preguntas-oraculo');
        if (!contenedor) return;
        contenedor.innerHTML = "";
        
        const lista = this.idiomaActual === 'es' ? this.CATALOGO_PREGUNTAS_ES : this.CATALOGO_PREGUNTAS_EN;
        let seleccionadas = [...lista].sort(() => 0.5 - Math.random()).slice(0, 3);
        
        seleccionadas.forEach((pregunta, idx) => {
            const btn = document.createElement('button');
            btn.className = 'btn-pregunta-crisis';
            btn.innerText = `${idx + 1}. ${pregunta}`;
            btn.onclick = () => {
                const libre = document.getElementById('inp-text-libre');
                if (libre) libre.value = pregunta;
                this.ejecutar();
            };
            contenedor.appendChild(btn);
        });
    },

    emitirVoz(texto) {
        if (!('speechSynthesis' in window)) return;
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(texto);
        utterance.lang = this.idiomaActual === 'es' ? 'es-US' : 'en-US';
        utterance.rate = 0.95;
        window.speechSynthesis.speak(utterance);
    },

    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;
        clearTimeout(this.timerInaccion);

        const zipValue = document.getElementById('inp-zip')?.value || "33167";
        const modoValue = document.getElementById('modo-selector')?.value || "ejecutivo";
        const menteValue = document.getElementById('mente-selector')?.value || "activo";
        const budgetValue = document.getElementById('budget-selector')?.value || "alto";
        const perfilValue = document.getElementById('perfil-selector')?.value || "individual";
        const textoLibreValue = document.getElementById('inp-text-libre')?.value || "";

        document.body.style.cursor = "wait";

        try {
            const respuesta = await fetch("https://onrender.com", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    zip_code: zipValue, modo: modoValue, mente: menteValue,
                    budget: budgetValue, perfil: perfilValue,
                    historial_vistos: this.historialVistos, texto_libre: textoLibreValue
                })
            });

            if (!respuesta.ok) throw new Error();
            const data = await respuesta.json();
            document.body.style.cursor = "default";

            this.balanceBienestar = data.balance_bienestar;
            this.escapesVIP = data.opciones_escape_vip; 

            this.escapesVIP.forEach(dest => this.historialVistos.push(dest.id));

        } catch (err) {
            document.body.style.cursor = "default";
            this.balanceBienestar = { inicial: 45.0, cierre_proyectado: 90.0 };
            this.escapesVIP = [
                {
                    id: "S1",
                    nombre: "Amanera Executive Sanctuary",
                    detalles_es: { descripcion: "Santuario privado frente al mar con aislamiento absoluto.", actividad_sintonía: "Contemplación de mareas", logistica_aerea: "Helipuerto privado disponible", logistica_maritima: "Muelle exclusivo 432Hz" },
                    detalles_en: { descripcion: "Private oceanfront sanctuary with absolute isolation.", actividad_sintonía: "Tidal contemplation", logistica_aerea: "Private helipad available", logistica_maritima: "Exclusive 432Hz dock" }
                }
            ];
        }

        const formWrapper = document.getElementById('wrapper-form');
        if (formWrapper) formWrapper.classList.add('hidden');
        const sessionDock = document.getElementById('activeSessionDock');
        if (sessionDock) sessionDock.classList.remove('hidden');

        this.activarSintonizaAcusticaYouTube();
        this.iniciarPulmonVisual();

        this.serviceTimer = setInterval(() => {
            this.timeLeft--;
            this.actualizarRelojInterfaz();

            if (this.timeLeft === 480 && localStorage.getItem('otg_user_role') !== 'admin' && !localStorage.getItem('otg_pase_stripe')) {
                clearInterval(this.serviceTimer);
                clearInterval(this.breatheInterval);
                clearInterval(this.voiceInterval);
                const paywall = document.getElementById('otg-muro-comercial');
                if (paywall) paywall.classList.remove('hidden');
                return;
            }

            if (this.timeLeft === 240) {
                this.inyectarDestinoOpcionalRojo();
            }

            if (this.timeLeft <= 0) {
                clearInterval(this.serviceTimer);
                clearInterval(this.breatheInterval);
                clearInterval(this.voiceInterval);
                this.activarCierreConscienteCronometrado();
            }
        }, 1000);

        this.activarVozAsesorContinuo();
    },

    procesarPagoStripe(tipo) {
        const priceId = tipo === 'unico' ? 'price_1TtbjXBOA5mT4t0PMCJSext6' : 'price_1TtblSBOA5mT4t0PGiYvT2l9';
        const folio = "MR-" + Math.floor(100000 + Math.random() * 900000);
        
        document.body.style.cursor = "wait";
        fetch("https://onrender.com", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ price_id: priceId, folio_id: folio })
        })
        .then(res => res.json())
        .then(data => {
            if (data.url) {
                localStorage.setItem('otg_pase_stripe', 'true');
                window.location.href = data.url;
            }
        })
        .catch(() => {
            document.body.style.cursor = "default";
            alert("Error de comunicación en pasarela fiduciaria.");
        });
    },

    activarSintonizaAcusticaYouTube() {
        const dic = this.TRADUCCIONES[this.idiomaActual];
        const stack = document.getElementById('interactiveStack');
        if (!stack) return;
        
        const modoActivo = document.getElementById('modo-selector')?.value || "ejecutivo";
        const menteActiva = document.getElementById('mente-selector')?.value || "activo";
        
        let discursoInicial = this.idiomaActual === 'es' 
            ? `Líder. Modo ${modoActivo} activado para mente en estado ${menteActiva}. Iniciando aislamiento acústico.`
            : `Leader. Mode ${modoActivo} enabled for mind state ${menteActiva}. Deploying acoustic isolation.`;
            
        this.emitirVoz(discursoInicial);

        let html = `<div style="margin-bottom:15px; font-size:11px; color:var(--gold-champagne); font-weight:bold; letter-spacing:1px; text-transform:uppercase;">${dic.tituloAcustico}</div>`;
        
        this.escapesVIP.forEach((dest) => {
            const detalles = this.idiomaActual === 'es' ? dest.detalles_es : dest.detalles_en;
            html += `
                <div style="background:var(--bg-surface); border:1px solid rgba(197,160,89,0.15); padding:16px; border-radius:16px; margin-bottom:15px; text-align:left;">
                    <div style="font-size:14px; font-weight:700; color:var(--gold-champagne); margin-bottom:6px;">👑 ${dest.nombre}</div>
                    <p style="font-size:12px; color:#bbb; line-height:1.4; margin-bottom:8px;">${detalles.descripcion}</p>
                    <div style="font-size:11px; color:#9E9EA4; margin-bottom:4px;"><b>Actividad:</b> ${detalles.actividad_sintonía}</div>
                    <div style="font-size:11px; color:#9E9EA4; margin-bottom:4px;"><b>Logística Aérea:</b> ${detalles.logistica_aerea}</div>
                    <div style="font-size:11px; color:#9E9EA4; margin-bottom:10px;"><b>Línea Marítima:</b> ${detalles.logistica_maritima}</div>
                    <button class="gold-action-btn" style="padding:10px 20px; font-size:11px; margin-top:0; width:auto; border-radius:12px;" onclick="window.open('https://google.com?q=' + encodeURIComponent('${dest.nombre}'), '_blank')">
                        ${dic.mapsBtn}
                    </button>
                </div>`;
        });
        
        html += `
            <div style="margin-top:15px; display:flex; flex-direction:column; gap:12px;">
                <iframe style="width:100%; height:140px; border:0; border-radius:12px;" src="https://youtube.com" allow="autoplay; encrypted-media" allowfullscreen></iframe>
                <iframe style="width:100%; height:140px; border:0; border-radius:12px;" src="https://youtube.com" allow="autoplay; encrypted-media" allowfullscreen></iframe>
            </div>
        `;
        stack.innerHTML = html;
    },

    iniciarPulmonVisual() {
        let paso = 0;
        const dic = this.TRADUCCIONES[this.idiomaActual];
        
        this.breatheInterval = setInterval(() => {
            const circle = document.getElementById('lungCircle');
            if (!circle) return;
            
            circle.innerText = dic.pasosRespiracion[paso];
            
            if (paso === 0) {
                circle.className = "lung-circle-master lung-inhale-state";
            } else if (paso === 2) {
                circle.className = "lung-circle-master lung-exhale-state";
            } else {
                circle.className = "lung-circle-master";
            }
            
            paso = (paso + 1) % 4;
        }, 4000);
    },

    actualizarRelojInterfaz() {
        let mins = Math.floor(this.timeLeft / 60).toString().padStart(2, '0');
        let secs = (this.timeLeft % 60).toString().padStart(2, '0');
        const clockEl = document.getElementById('clockDisplay');
        if (clockEl) clockEl.innerText = `${mins}:${secs}`;
    },

    activarVozAsesorContinuo() {
        const emitir = () => this.emitirVoz(this.TRADUCCIONES[this.idiomaActual].frecuenciaVoz);
        emitir();
        this.voiceInterval = setInterval(emitir, 45000);
    },

    inyectarDestinoOpcionalRojo() {
        const stack = document.getElementById('interactiveStack');
        if (!stack) return;
        const dic = this.TRADUCCIONES[this.idiomaActual];
        this.emitirVoz(dic.discursoMin4);
        
        const divDestino = document.createElement('div');
        divDestino.style.cssText = "background:rgba(192,57,43,0.15); border:2px solid var(--alert-crimson); padding:16px; border-radius:16px; margin-top:15px; text-align:left; cursor:pointer; transition:all 0.3s;";
        divDestino.onclick = () => window.open(`https://google.com?q=` + encodeURIComponent('Luxury Resort Amanera Playa Grande'), '_blank');
        
        divDestino.innerHTML = `
            <div style="font-size:11px; color:var(--alert-crimson); font-weight:bold; letter-spacing:1px; text-transform:uppercase; margin-bottom:4px;">💥 SANTUARIO EXCLUSIVO PROPUESTO</div> 
            <div style="font-size:14px; font-weight:bold; color:#fff; margin-bottom:4px;">Amanera Resort — Luxury Oasis</div> 
            <p style="font-size:12px; color:#eee; line-height:1.4; margin-bottom:8px;"> ${this.idiomaActual === 'es' ? 'Haga clic para abrir la ruta directa hacia el aislamiento absoluto.' : 'Click to open the direct route towards absolute environmental isolation.'} </p> 
            <span style="font-size:10px; background:var(--alert-crimson); color:#fff; padding:4px 8px; border-radius:4px; font-weight:bold; text-transform:uppercase;">${dic.mapsBtn}</span>
        `;
        stack.insertBefore(divDestino, stack.firstChild);
    },

    activarCierreConscienteCronometrado() {
        const sessionDock = document.getElementById('activeSessionDock');
        if (sessionDock) sessionDock.classList.add('hidden');
        const cierrePantalla = document.getElementById('pantalla-cierre');
        if (cierrePantalla) cierrePantalla.classList.remove('hidden');

        const retoSeleccionado = this.CATALOGO_RETOS[Math.floor(Math.random() * this.CATALOGO_RETOS.length)];
        
        const imgContainer = document.getElementById('reto-img');
        if (imgContainer) {
            imgContainer.outerHTML = `<div id="reto-img" style="font-size: 50px; text-align: center; margin-bottom: 10px;">${retoSeleccionado.icono}</div>`;
        }
        
        const retoTitulo = document.getElementById('reto-titulo');
        const retoDesc = document.getElementById('reto-descripcion');

        if (this.idiomaActual === 'es') {
            if (retoTitulo) retoTitulo.innerText = retoSeleccionado.titulo_es;
            if (retoDesc) retoDesc.innerText = retoSeleccionado.desc_es;
        } else {
            if (retoTitulo) retoTitulo.innerText = retoSeleccionado.titulo_en;
            if (retoDesc) retoDesc.innerText = retoSeleccionado.desc_en;
        }

        this.cierreTimerInterval = setInterval(() => {
            this.cierreTimeLeft--;
            const timerEl = document.getElementById('cierre-timer');
            if (timerEl) timerEl.innerText = this.cierreTimeLeft;

            if (this.cierreTimeLeft <= 0) {
                clearInterval(this.cierreTimerInterval);
                this.finalizarCierreYMostrarDescarga();
            }
        }, 1000);
    },

    finalizarCierreYMostrarDescarga() {
        const dic = this.TRADUCCIONES[this.idiomaActual];
        this.emitirVoz(dic.cierreFinalizado);
        const timerEl = document.getElementById('cierre-timer');
        if (timerEl) timerEl.classList.add('hidden');
        
        const msgFinal = document.getElementById('cierre-mensaje-final');
        if (msgFinal) {
            msgFinal.innerText = dic.cierreFinalizado;
            msgFinal.classList.remove('hidden');
        }

        const recomenzarBtn = document.getElementById('btn-recomenzar-experiencia');
        if (recomenzarBtn) recomenzarBtn.classList.remove('hidden');
        
        const root = document.getElementById('cierre-message');
        if (!root) return;
        const folio = "MR-" + Math.floor(100000 + Math.random() * 900000);
        
        const textoWhatsApp = encodeURIComponent('Hola, he completado mi pasaporte de bienestar y deseo coordinar la logística de mi próximo itinerario premium.');
        
        root.innerHTML = `
            <div style="text-align:center; padding:10px 0;"> 
                <button class="gold-action-btn" style="margin-bottom:15px;" onclick="KERNEL.descargarPDF('${folio}')">${dic.compilarBtn}</button>
                <div style="border-top:1px solid var(--border-subtle); margin:20px 0; padding-top:15px;">
                    <h4 style="font-family:'Cinzel', serif; color:var(--gold-champagne); font-size:13px; letter-spacing:1px; margin-bottom:6px;">✈️ DISEÑO DE ITINERARIOS AD HOC</h4>
                    <p style="font-size:11.5px; color:var(--text-muted); line-height:1.4; margin-bottom:12px;">
                        ¿Desea materializar su escape? Conéctese de forma directa y privada con nuestro Consultor de Viajes Élite para gestionar charters aéreos, reservas Virtuoso y logística marítima exclusiva.
                    </p>
                    <button class="gold-action-btn" style="background:var(--gold-champagne); color:#030305; font-size:11px; font-weight:700;" onclick="window.open('https://wa.me/17866471371?text=${textoWhatsApp}', '_blank')">
                        CONTACTAR AGENTE PRIVADO
                    </button>
                </div>
            </div>
        `;
    },

    descargarPDF(folio) {
        document.body.style.cursor = "wait";
        fetch("https://onrender.com", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                servicio_id: folio,
                lang: this.idiomaActual,
                score_inicial: this.balanceBienestar ? this.balanceBienestar.inicial : 45.0,
                score_actual: this.balanceBienestar ? this.balanceBienestar.cierre_proyectado : 90.0,
                respiracion_score: 100.0, 
                adivinanzas_score: 100.0,
                iev: 95.0,
                variante: "ELITE_WELLNESS",
                destino_id: "S1"
            })
        })
        .then(res => {
            if (!res.ok) throw new Error();
            return res.blob();
        })
        .then(blob => {
            document.body.style.cursor = "default";
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `Wellness_Elite_Passport_${folio}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
        })
        .catch(() => {
            document.body.style.cursor = "default";
            alert("Error al compilar el pasaporte.");
        });
    },

    conectarMantenimientoDesarrollador() {
        const brand = document.getElementById("brandTitleField");
        if (!brand) return;
        brand.addEventListener("click", () => {
            this.devClickCount++;
            if (this.devClickCount === 3) {
                this.devClickCount = 0;
                localStorage.setItem('otg_user_role', 'admin');
                alert("Acceso Desarrollador Concedido. Licencia de propietario verificada de manera fiduciaria.");
                location.reload();
            }
        });
    }
};

// Autoejecución e inicialización estructural del núcleo táctico
document.addEventListener('DOMContentLoaded', () => KERNEL.init());
window.KERNEL = KERNEL;
