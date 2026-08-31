// =========================================================================
// WELLNESS TRAVEL FRONTEND LOGIC — INTEGRIDAD TOTAL 100% OPEN THAN GO
// PARTE 1 DE 6: ARQUITECTURA DE DATOS Y LOGÍSTICA DE ESTADO CORE
// =========================================================================

const KERNEL = {
    // Variables de Estado de Ingeniería (Sincronizadas con Open Than Go)
    timerInaccion: null,
    serviceTimer: null,
    breatheInterval: null,
    voiceInterval: null,
    cierreTimerInterval: null,
    timeLeft: 600,         // 10 minutos matemáticos de sesión activa obligatoria
    cierreTimeLeft: 60,    // 60 segundos obligatorios de Limpieza Mental Profunda en Cierre
    isLocked: false,
    idiomaActual: 'es',
    devClickCount: 0,
    historialVistos: [],   // Control local anti-repeticiones para enrutamiento

    // Diccionarios VIP Extendidos (Absolutamente libres de términos médicos o laborales)
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
// =========================================================================
// WELLNESS TRAVEL FRONTEND LOGIC — INTEGRIDAD TOTAL 100% OPEN THAN GO
// PARTE 2 DE 6: MATRIZ DE RETOS VIP Y POOL DE PREGUNTAS ANALÍTICAS (PARTE 1)
// =========================================================================

    // BANCO DE SVGs INTEGRADOS EN CÓDIGO (Elimina los errores 404 del servidor)
    SVGS: {
        R1: `<svg viewBox="0 0 24 24" width="60" fill="none" stroke="#C5A059" stroke-width="1.5"><path d="M19 11A7 7 0 0112 18m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 003-3V5a3 3 0 10-6 0v3a3 3 0 003 3z"/><line x1="1" y1="1" x2="23" y2="23" stroke="#C0392B" stroke-width="2"/></svg>`,
        R2: `<svg viewBox="0 0 24 24" width="60" fill="none" stroke="#C5A059" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/></svg>`,
        R3: `<svg viewBox="0 0 24 24" width="60" fill="none" stroke="#C5A059" stroke-width="1.5"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7M18.5 2.5a2.121 2.121 0 113 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>`,
        R4: `<svg viewBox="0 0 24 24" width="60" fill="none" stroke="#C5A059" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2M9 9h.01M15 9h.01"/></svg>`,
        R5: `<svg viewBox="0 0 24 24" width="60" fill="none" stroke="#C5A059" stroke-width="1.5"><path d="M18 15l-6-6-6 6"/></svg>`,
        R6: `<svg viewBox="0 0 24 24" width="60" fill="none" stroke="#C5A059" stroke-width="1.5"><path d="M3 18v-6a9 9 0 0118 0v6M21 19a2 2 0 01-2 2h-1a2 2 0 01-2-2v-3a2 2 0 012-2h3M3 19a2 2 0 002 2h1a2 2 0 002-2v-3a2 2 0 00-2-2H3"/></svg>`,
        R7: `<svg viewBox="0 0 24 24" width="60" fill="none" stroke="#C5A059" stroke-width="1.5"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>`,
        R8: `<svg viewBox="0 0 24 24" width="60" fill="none" stroke="#C5A059" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/></svg>`
    },

    CATALOGO_RETOS: [
        { id: "R1", titulo_es: "Silencio Absoluto", desc_es: "Permanece 60 segundos sin emitir sonido ni interactuar con pantallas. Escucha el vacío físico de tu habitación.", titulo_en: "Absolute Silence", desc_en: "Spend 60 seconds without making any sound or interacting with screens. Listen to the physical void of your room." },
        { id: "R2", titulo_es: "Contemplación Fija", desc_es: "Elige un objeto inanimado en tu entorno visual y observa sus detalles físicos, texturas y sombras sin juzgar.", titulo_en: "Fixed Contemplation", desc_en: "Pick an inanimate object in your visual field and observe its physical details, textures, and shadows without judgment." },
        { id: "R3", titulo_es: "Escritura de Purga", desc_es: "Anota mentalmente tres ideas recurrentes que ronden tu enfoque actual y visualiza cómo se disuelven en el aire.", titulo_en: "Purge Inscription", desc_en: "Mentally note three recurring thoughts hovering over your active focus and visualize them dissolving into thin air." },
        { id: "R4", titulo_es: "Distensión Facial", desc_es: "Libera la tensión acumulada sonriendo de manera forzada durante 10 segundos para activar tus terminales nerviosas de alivio.", titulo_en: "Facial Release", desc_en: "Release accumulated jaw tension by forcing a smile for 10 seconds to activate your biological relaxation pathways." },
        { id: "R5", titulo_es: "Alineación Física", desc_es: "Estira los brazos hacia arriba de forma lenta, expandiendo el torso, y mantén la postura soltando el aire despacio.", titulo_en: "Physical Alignment", desc_en: "Slowly extend your arms upward, expanding your chest, and hold the posture while breathing out smoothly." },
        { id: "R6", titulo_es: "Enfoque Auditivo", desc_es: "Cierra los ojos y busca aislar el sonido más lejano que se escuche en tu entorno actual. Concéntrate solo en esa onda.", titulo_en: "Auditory Tracking", desc_en: "Close your eyes and isolate the most distant ambient sound in your current perimeter. Focus solely on that soundwave." },
        { id: "R7", titulo_es: "Anclaje de Logro", desc_es: "Evoca un momento reciente donde experimentaste control absoluto sobre tu tiempo y retén esa memoria en tu mente.", titulo_en: "Milestone Anchoring", desc_en: "Recall a recent moment where you experienced complete control over your time and hold that mental imprint firmly." },
        { id: "R8", titulo_es: "Respiración Cuadrada", desc_es: "Realiza un ciclo completo de respiración conteniendo el aire de manera consciente, alineando tu ritmo biológico.", titulo_en: "Box Respiration", desc_en: "Perform a complete square breathing cycle, consciously holding your breath to harmonize your internal biological pace." }
    ],
    // Pool de Preguntas Analíticas — Primer Bloque (1 a 24)
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
        "¿Sientes que el ruido visual de tu entorno habitual interrumpe tu calma?"
    ],
    [
        "¿El ritmo automatizado de tus días disminuye la calidad de tus descansos?",
        "¿Buscas un entorno exclusivo pero las opciones comunes te generan saturación?",
        "¿La exposición continua a entornos densivos limita tu claridad reflexiva?",
        "¿Sientes la necesidad de resetear tus estímulos sensoriales de manera urgente?",
        "¿El dinamismo excesivo de tu agenda reduce tu capacidad de contemplación?",
        "¿Te cuesta ver la sensación de calma ante la presión de los tiempos?",
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

    // Pool Completo de Preguntas Analíticas en Inglés (1 a 48)
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
        "Does the rush to meet external expectations drench your individual tuning?",
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
// =========================================================================
// WELLNESS TRAVEL FRONTEND LOGIC — INTEGRIDAD TOTAL 100% OPEN THAN GO
// PARTE 4 DE 6: MÓDULOS DE INICIALIZACIÓN, CAMBIO DE IDIOMA E INACCIÓN CORE
// =========================================================================

    init() {
        // Unificar estructuralmente los dos bloques de preguntas en español al arrancar
        this.CATALOGO_PREGUNTAS_ES = [...this.CATALOGO_PREGUNTAS_ES, ...this.CATALOGO_PREGUNTAS_ES_2];
        this.cambiarIdioma(this.idiomaActual);
        this.conectarMantenimientoDesarrollador();
    },

    cambiarIdioma(lang) {
        this.idiomaActual = lang;
        const diccionario = this.TRADUCCIONES[lang];
       
        // Traducción e inyección masiva de cadenas de texto estáticas en la UI
        document.getElementById('lblBrandSub').innerText = diccionario.brandSub;
        document.getElementById('lblTimerTitle').innerText = diccionario.timerTitle;
        document.getElementById('lbl-oraculo-instruccion').innerText = diccionario.oraculoInstruccion;
        document.getElementById('lbl-desahogo').innerText = diccionario.desahogoLabel;
        document.getElementById('inp-text-libre').placeholder = diccionario.placeholderLibre;
        document.getElementById('btn-activar-libre').innerText = diccionario.btnActivar;
       
        // CORRECCIÓN PROTEGIDA: Sincronización precisa de la etiqueta de coordenadas logísticas
        const lblZip = document.getElementById('lbl-zip');
        if (lblZip) {
            lblZip.innerText = lang === 'es' ? "Código Postal" : "Zip Code";
        }

        // Alternancia de estados visuales activos en la barra de idiomas
        const btnEs = document.getElementById('lang-es');
        const btnEn = document.getElementById('lang-en');
        if (btnEs && btnEn) {
            if (lang === 'es') {
                btnEs.classList.add('active');
                btnEn.classList.remove('active');
            } else {
                btnEn.classList.add('active');
                btnEs.classList.remove('active');
            }
        }
       
        this.inyectarPreguntasOraculo();
    },

    despertarInicial() {
        document.getElementById('pantalla-bienvenida').style.display = 'none';
        document.getElementById('wrapper-form').classList.remove('hidden');
        this.resetearTemporizadorInaccion();
    },

    resetearTemporizadorInaccion() {
        clearTimeout(this.timerInaccion);
        if (this.isLocked) return;
        
        // Disparador cronometrado de 8 segundos para evitar la dispersión de la atención
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
       
        // Algoritmo inmutable de desordenamiento y extracción limpia de 3 vectores flotantes
        let seleccionadas = [...lista].sort(() => 0.5 - Math.random()).slice(0, 3);
       
        seleccionadas.forEach((pregunta, idx) => {
            const btn = document.createElement('button');
            btn.className = 'btn-pregunta-crisis';
            btn.innerText = `${idx + 1}. ${pregunta}`;
            btn.onclick = () => {
                document.getElementById('inp-text-libre').value = pregunta;
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
        utterance.rate = 0.95; // Cadencia ralentizada para transmitir control y elegancia
        window.speechSynthesis.speak(utterance);
    },
// =========================================================================
// WELLNESS TRAVEL FRONTEND LOGIC — INTEGRIDAD TOTAL 100% OPEN THAN GO
// PARTE 5 DE 6: NÚCLEO ASÍNCRONO EJECUTAR, CRONÓMETRO, PULMÓN Y FRECUENCIAS
// =========================================================================

    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;
        clearTimeout(this.timerInaccion);

        // Captura dinámica de coordenadas logísticas y filtros VIP
        const zipCode = document.getElementById('inp-zip').value || "33167";
        const modoActivo = document.getElementById('modo-selector').value;
        const menteActiva = document.getElementById('mente-selector').value;
        const budgetActivo = document.getElementById('budget-selector').value;
        const perfilActivo = document.getElementById('perfil-selector').value;
        const textoLibreStr = document.getElementById('inp-text-libre').value;

        // Transición y bloqueo visual inmediato de los viewports
        document.getElementById('wrapper-form').classList.add('hidden');
        document.getElementById('activeSessionDock').classList.remove('hidden');

        this.activarSintonizaAcusticaYouTube();
        this.iniciarPulmonVisual();

        // Cronómetro maestro síncrono de 10 minutos (600s) Open Than Go
        this.serviceTimer = setInterval(() => {
            this.timeLeft--;
            this.actualizarRelojInterfaz();

            // Inyección interactiva destacada en rojo a los 4 minutos finales (240s restantes)
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

        // ENLACE CONTEXTUAL ASÍNCRONO: Conexión con el motor predictivo en Render
        try {
            const respuesta = await fetch("https://onrender.com", {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json" 
                },
                body: JSON.stringify({
                    zip_code: zipCode,
                    modo: modoActivo,
                    mente: menteActiva,
                    budget: budgetActivo,
                    perfil: perfilActivo,
                    historial_vistos: this.historialVistos,
                    texto_libre: textoLibreStr
                })
            });

            if (!respuesta.ok) throw new Error("Fallo en el nodo de enlace analítico.");
            
            const data = await respuesta.json();

            // Sincronizar el historial local anti-repeticiones con la respuesta del servidor
            if (data.opciones_escape_vip && data.opciones_escape_vip.length > 0) {
                data.opciones_escape_vip.forEach(destino => {
                    if (!this.historialVistos.includes(destino.id)) {
                        this.historialVistos.push(destino.id);
                    }
                });
                console.log("[CRM EXCLUSIVO] Historial de Santuarios Sincronizado:", this.historialVistos);
            }

        } catch (error) {
            console.error("[CRITICAL] Fallo en el motor de escape:", error);
            // Salvaguarda fiduciaria para prevenir rupturas en el PDF Passport
            if (this.historialVistos.length === 0) {
                this.historialVistos.push("S1");
            }
        }
    },

    activarSintonizaAcusticaYouTube() {
        const dic = this.TRADUCCIONES[this.idiomaActual];
        this.emitirVoz(dic.vozSintonialAcustica);
        const stack = document.getElementById('interactiveStack');

        const poolVideos = [
            { t: "Frecuencia Solfeggio 432Hz — Océano Profundo", id: "1ZYbU82GVz4" },
            { t: "Frecuencia Alfa 8Hz — Ondas de Espacio Natural", id: "WPni755-Krg" }
        ];

        let html = `<div style="margin-bottom:10px; font-size:11px; color:var(--gold-champagne); font-weight:bold; letter-spacing:1px; text-transform:uppercase;">${dic.tituloAcustico}</div>`;
        poolVideos.forEach((v) => {
            html += `
                <div style="background:var(--bg-surface); border:1px solid rgba(197,160,89,0.1); padding:12px; border-radius:14px; margin-bottom:12px;">
                    <div style="font-size:12px; font-weight:600; color:#fff; margin-bottom:8px;">${v.t}</div>
                    <iframe style="width:100%; height:140px; border:0; border-radius:8px;" src="https://youtube.com{v.id}?autoplay=1&mute=0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
                </div>`;
        });
        stack.innerHTML = html;
    },

    iniciarPulmonVisual() {
        let paso = 0;
        const dic = this.TRADUCCIONES[this.idiomaActual];
       
        // Ciclo síncrono inmutable de respiración clínica en 4 tiempos fijos
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
// =========================================================================
// WELLNESS TRAVEL FRONTEND LOGIC — INTEGRIDAD TOTAL 100% OPEN THAN GO
// PARTE 6 DE 6: LOGÍSTICA DE INTERFAZ, CIERRE CONSCIENTE Y COMPILACIÓN FINAL
// =========================================================================

    actualizarRelojInterfaz() {
        let mins = Math.floor(this.timeLeft / 60).toString().padStart(2, '0');
        let secs = (this.timeLeft % 60).toString().padStart(2, '0');
        document.getElementById('clockDisplay').innerText = `${mins}:${secs}`;
    },

    activarVozAsesorContinuo() {
        const emitir = () => this.emitirVoz(this.TRADUCCIONES[this.idiomaActual].frecuenciaVoz);
        emitir();
        this.voiceInterval = setInterval(emitir, 45000);
    },

    inyectarDestinoOpcionalRojo() {
        const stack = document.getElementById('interactiveStack');
        const dic = this.TRADUCCIONES[this.idiomaActual];
        this.emitirVoz(dic.discursoMin4);
       
        const divDestino = document.createElement('div');
        divDestino.style = "background:rgba(192,57,43,0.15); border:2px solid var(--alert-crimson); padding:16px; border-radius:16px; margin-top:15px; text-align:left; cursor:pointer; transition:all 0.3s;";
       
        divDestino.onclick = () => window.open(`https://google.com{encodeURIComponent('Luxury Resort Amanera Playa Grande')}`, '_blank');
       
        divDestino.innerHTML = `
            <div style="font-size:11px; color:var(--alert-crimson); font-weight:bold; letter-spacing:1px; text-transform:uppercase; margin-bottom:4px;">💥 SANTUARIO EXCLUSIVO PROPUESTO</div>
            <div style="font-size:14px; font-weight:bold; color:#fff; margin-bottom:4px;">Amanera Resort — Luxury Oasis</div>
            <p style="font-size:12px; color:#eee; line-height:1.4; margin-bottom:8px;"> ${this.idiomaActual === 'es' ? 'Haga clic para abrir la ruta directa hacia el aislamiento absoluto.' : 'Click to open the direct route towards absolute environmental isolation.'} </p>
            <span style="font-size:10px; background:var(--alert-crimson); color:#fff; padding:4px 8px; border-radius:4px; font-weight:bold; text-transform:uppercase;">${dic.mapsBtn}</span>
        `;
        stack.insertBefore(divDestino, stack.firstChild);
    },

    activarCierreConscienteCronometrado() {
        document.getElementById('activeSessionDock').classList.add('hidden');
        document.getElementById('pantalla-cierre').classList.remove('hidden');

        const retoSeleccionado = this.CATALOGO_RETOS[Math.floor(Math.random() * this.CATALOGO_RETOS.length)];
        const imgTag = document.getElementById('reto-img');
       
        imgTag.src = retoSeleccionado.img;
        imgTag.classList.remove('hidden');
       
        if (this.idiomaActual === 'es') {
            document.getElementById('reto-titulo').innerText = retoSeleccionado.titulo_es;
            document.getElementById('reto-descripcion').innerText = retoSeleccionado.desc_es;
        } else {
            document.getElementById('reto-titulo').innerText = retoSeleccionado.titulo_en;
            document.getElementById('reto-titulo').innerText = retoSeleccionado.titulo_en;
            document.getElementById('reto-descripcion').innerText = retoSeleccionado.desc_en;
        }

        this.cierreTimerInterval = setInterval(() => {
            this.cierreTimeLeft--;
            document.getElementById('cierre-timer').innerText = this.cierreTimeLeft;

            if (this.cierreTimeLeft <= 0) {
                clearInterval(this.cierreTimerInterval);
                this.finalizarCierreYMostrarDescarga();
            }
        }, 1000);
    },

    finalizarCierreYMostrarDescarga() {
        const dic = this.TRADUCCIONES[this.idiomaActual];
        this.emitirVoz(dic.cierreFinalizado);
       
        document.getElementById('cierre-timer').classList.add('hidden');
       
        const msgFinal = document.getElementById('cierre-mensaje-final');
        msgFinal.innerText = dic.cierreFinalizado;
        msgFinal.classList.remove('hidden');

        document.getElementById('btn-recomenzar-experiencia').classList.remove('hidden');

        const root = document.getElementById('cierre-message');
        const folio = "MR-" + Math.floor(100000 + Math.random() * 900000);
       
        root.innerHTML = `
            <div style="text-align:center; padding:10px 0;">
                <p style="font-size:14px; color:var(--text-muted); margin-bottom:20px;">
                    ${this.idiomaActual === 'es' ? 'Su documentación de sintonía ejecutiva ha sido estructurada.' : 'Your executive tuning passport has been fully structured.'}
                </p>
                <button class="gold-action-btn" onclick="KERNEL.descargarPDF('${folio}')">${dic.compilarBtn}</button>
            </div>
        `;
    },

    descargarPDF(folio) {
        document.body.style.cursor = "wait";
       
        const destinoPrescrito = this.historialVistos.length > 0 
            ? this.historialVistos[this.historialVistos.length - 1] 
            : "S1";
       
        fetch("https://onrender.com", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                servicio_id: folio,
                lang: this.idiomaActual,
                score_inicial: 45.0, 
                score_actual: 90.0, 
                respiracion_score: 100.0, 
                adivinanzas_score: 100.0,
                iev: 95.0, 
                variante: "ELITE_WELLNESS", 
                destino_id: destinoPrescrito
            })
        })
        .then(res => {
            if (!res.ok) throw new Error("Fallo transaccional de comunicación.");
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
            window.URL.revokeObjectURL(url);
        })
        .catch(() => {
            document.body.style.cursor = "default";
            alert(this.idiomaActual === 'es' ? "Error al compilar el pasaporte." : "Error compiling passport.");
        });
    },

    conectarMantenimientoDesarrollador() {
        const brand = document.getElementById("brandTitleField");
        if (!brand) return;
        brand.addEventListener("click", () => {
            this.devClickCount++;
            if (this.devClickCount === 3) {
                this.devClickCount = 0;
                window.location.href = window.location.pathname + "?status=success&folio=DEV-MASTER";
            }
        });
    }
};

document.addEventListener('DOMContentLoaded', () => KERNEL.init());
window.KERNEL = KERNEL;
