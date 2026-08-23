// =========================================================================
// WELLNESS TRAVEL FRONTEND LOGIC — INTEGRIDAD TOTAL 99% OPEN THAN GO
// PARTE 1: ARQUITECTURA DE DATOS, DICCIONARIOS Y RETOS DE CIERRE CONSCIENTE
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

    // Matriz de Retos Conductuales del Cierre Consciente (Réplica exacta 1:1)
    CATALOGO_RETOS: [
        {
            id: "R1", img: "/static/silence.svg",
            titulo_es: "Silencio Absoluto", desc_es: "Permanece 60 segundos sin emitir sonido ni interactuar con pantallas. Escucha el vacío físico de tu habitación.",
            titulo_en: "Absolute Silence", desc_en: "Spend 60 seconds without making any sound or interacting with screens. Listen to the physical void of your room."
        },
        {
            id: "R2", img: "/static/observe.svg",
            titulo_es: "Contemplación Fija", desc_es: "Elige un objeto inanimado en tu entorno visual y observa sus detalles físicos, texturas y sombras sin juzgar.",
            titulo_en: "Fixed Contemplation", desc_en: "Pick an inanimate object in your visual field and observe its physical details, textures, and shadows without judgment."
        },
        {
            id: "R3", img: "/static/words.svg",
            titulo_es: "Escritura de Purga", desc_es: "Anota mentalmente tres ideas recurrentes que ronden tu enfoque actual y visualiza cómo se disuelven en el aire.",
            titulo_en: "Purge Inscription", desc_en: "Mentally note three recurring thoughts hovering over your active focus and visualize them dissolving into thin air."
        },
        {
            id: "R4", img: "/static/laugh.svg",
            titulo_es: "Distensión Facial", desc_es: "Libera la tensión acumulada sonriendo de manera forzada durante 10 segundos para activar tus terminales nerviosas de alivio.",
            titulo_en: "Facial Release", desc_en: "Release accumulated jaw tension by forcing a smile for 10 seconds to activate your biological relaxation pathways."
        },
        {
            id: "R5", img: "/static/stretch.svg",
            titulo_es: "Alineación Física", desc_es: "Estira los brazos hacia arriba de forma lenta, expandiendo el torso, y mantén la postura soltando el aire despacio.",
            titulo_en: "Physical Alignment", desc_en: "Slowly extend your arms upward, expanding your chest, and hold the posture while breathing out smoothly."
        },
        {
            id: "R6", img: "/static/nature_sound.svg",
            titulo_es: "Enfoque Auditivo", desc_es: "Cierra los ojos y busca aislar el sonido más lejano que se escuche en tu entorno actual. Concéntrate solo en esa onda.",
            titulo_en: "Auditory Tracking", desc_en: "Close your eyes and isolate the most distant ambient sound in your current perimeter. Focus solely on that soundwave."
        },
        {
            id: "R7", img: "/static/gratitude.svg",
            titulo_es: "Anclaje de Logro", desc_es: "Evoca un momento reciente donde experimentaste control absoluto sobre tu tiempo y retén esa memoria en tu mente.",
            titulo_en: "Milestone Anchoring", desc_en: "Recall a recent moment where you experienced complete control over your time and hold that mental imprint firmly."
        },
        {
            id: "R8", img: "/static/square_breath.svg",
            titulo_es: "Respiración Cuadrada", desc_es: "Realiza un ciclo completo de respiración conteniendo el aire de manera consciente, alineando tu ritmo biológico.",
            titulo_en: "Box Respiration", desc_en: "Perform a complete square breathing cycle, consciously holding your breath to harmonize your internal biological pace."
        }
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

    // Continuación Pool de Preguntas Analíticas — Segundo Bloque (25 a 48)
    CATALOGO_PREGUNTAS_ES_2: [
        "¿El ritmo automatizado de tus días disminuye la calidad de tus descansos?",
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
        // Unificar los dos bloques en español en un solo arreglo dinámico al arrancar
        this.CATALOGO_PREGUNTAS_ES = [...this.CATALOGO_PREGUNTAS_ES, ...this.CATALOGO_PREGUNTAS_ES_2];
        this.cambiarIdioma(this.idiomaActual);
        this.conectarMantenimientoDesarrollador();
    },

    cambiarIdioma(lang) {
        this.idiomaActual = lang;
        const diccionario = this.TRADUCCIONES[lang];
       
        document.getElementById('lblBrandSub').innerText = diccionario.brandSub;
        document.getElementById('lblTimerTitle').innerText = diccionario.timerTitle;
        document.getElementById('lbl-oraculo-instruccion').innerText = diccionario.oraculoInstruccion;
        document.getElementById('lbl-desahogo').innerText = diccionario.desahogoLabel;
        document.getElementById('inp-text-libre').placeholder = diccionario.placeholderLibre;
        document.getElementById('btn-activar-libre').innerText = diccionario.btnActivar;
       
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
       
        // Algoritmo inmutable de desordenamiento y extracción de 3 elementos flotantes en cascada
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
        utterance.rate = 0.95;
        window.speechSynthesis.speak(utterance);
    },

    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;
        clearTimeout(this.timerInaccion);

        // Bloqueo y transición estética de viewports
        document.getElementById('wrapper-form').classList.add('hidden');
        document.getElementById('activeSessionDock').classList.remove('hidden');

        this.activarSintonizaAcusticaYouTube();
        this.iniciarPulmonVisual();

        // Cronómetro maestro síncrono de 10 minutos (600s) idéntico a Open Than Go
        this.serviceTimer = setInterval(() => {
            this.timeLeft--;
            this.actualizarRelojInterfaz();

            // INYECCIÓN OBLIGATORIA DEL DESTINO EN ROJO 4 MINUTOS ANTES DE EXPIRAR (MINUTO 6 / 240s RESTANTES)
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
            // CORREGIDO: Se cambió de comillas simples a backticks y interpolación correcta ${v.id}
            html += `
                <div style="background:var(--bg-surface); border:1px solid rgba(197,160,89,0.1); padding:12px; border-radius:14px; margin-bottom:12px;">
                    <div style="font-size:12px; font-weight:600; color:#fff; margin-bottom:8px;">${v.t}</div>
                    <iframe style="width:100%; height:140px; border:0; border-radius:8px;" src="https://www.youtube.com/embed/${v.id}?autoplay=1&mute=0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
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

    // Inyección interactiva obligatoria destacada en ROJO a los 4 minutos finales
    inyectarDestinoOpcionalRojo() {
        const stack = document.getElementById('interactiveStack');
        const dic = this.TRADUCCIONES[this.idiomaActual];
        this.emitirVoz(dic.discursoMin4);
       
        const divDestino = document.createElement('div');
        divDestino.style = "background:rgba(192,57,43,0.15); border:2px solid var(--alert-crimson); padding:16px; border-radius:16px; margin-top:15px; text-align:left; cursor:pointer; transition:all 0.3s;";
       
        // CORREGIDO: Uso correcto de backticks para la URL de Google Search
        divDestino.onclick = () => window.open(`https://google.com/search?q=${encodeURIComponent('Luxury Resort Amanera Playa Grande')}`, '_blank');
       
        divDestino.innerHTML = `
            <div style="font-size:11px; color:var(--alert-crimson); font-weight:bold; letter-spacing:1px; text-transform:uppercase; margin-bottom:4px;">💥 SANTUARIO EXCLUSIVO PROPUESTO</div>
            <div style="font-size:14px; font-weight:bold; color:#fff; margin-bottom:4px;">Amanera Resort — Luxury Oasis</div>
            <p style="font-size:12px; color:#eee; line-height:1.4; margin-bottom:8px;"> ${this.idiomaActual === 'es' ? 'Haga clic para abrir la ruta directa hacia el aislamiento absoluto.' : 'Click to open the direct route towards absolute environmental isolation.'} </p>
            <span style="font-size:10px; background:var(--alert-crimson); color:#fff; padding:4px 8px; border-radius:4px; font-weight:bold; text-transform:uppercase;">${dic.mapsBtn}</span>
        `;
        stack.insertBefore(divDestino, stack.firstChild);
    },

    // MÓDULO COMPLETO CRONOMETRADO DEL CIERRE CONSCIENTE (99% OPEN THAN GO)
    activarCierreConscienteCronometrado() {
        // Desplegar viewport de cierre inyectando un reto conductual aleatorio
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
            document.getElementById('reto-descripcion').innerText = retoSeleccionado.desc_en;
        }

        // Ejecutar cuenta atrás obligatoria de 60 segundos
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

        const btnReiniciar = document.getElementById('btn-recomenzar-experiencia');
        btnReiniciar.classList.remove('hidden');

        // Transformación dinámica del contenedor para habilitar la descarga del PDF fiduciario
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
       
        // CONEXIÓN DIRECTA FIX A TU ENDPOINT EN RENDER
        fetch("https://wellness-travel.onrender.com", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                servicio_id: folio,
                lang: this.idiomaActual,
                score_inicial: 45.0, score_actual: 90.0, respiracion_score: 100.0, adivinanzas_score: 100.0,
                iev: 95.0, variante: "ELITE_WELLNESS", destino_id: "S1"
            })
        })
        .then(res => {
            if (!res.ok) throw new Error("Fallo transaccional");
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
                window.location.href = window.location.pathname + "?status=success&folio=DEV-MASTER";
            }
        });
    }
};

// Autoejecución e inicialización estructural del núcleo táctico
document.addEventListener('DOMContentLoaded', () => KERNEL.init());
window.KERNEL = KERNEL;
