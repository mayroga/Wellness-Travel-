// =========================================================================
// WELLNESS TRAVEL FRONTEND ENGINE — EDICIÓN COMPLETA ULTRA-PREMIUM (SIN ERRORES)
// =========================================================================

const KERNEL = {
    timerInaccion: null,
    serviceTimer: null,
    breatheInterval: null,
    voiceInterval: null,
    cierreTimerInterval: null,
    timeLeft: 600,          
    cierreTimeLeft: 60,    
    isLocked: false,
    idiomaActual: 'es',
    devClickCount: 0,
    historialVistos: [],    

    TRADUCCIONES: {
        es: {
            brandSub: "Arquitectura de Santuarios Ejecutivos y Bienestar",
            timerTitle: "Ventana de Sintonía Activa",
            oraculoInstruccion: "¿Qué vector bloquea tu sintonía hoy?",
            desahogoLabel: "O declare aquí su saturación ambiental o exigencia de viaje:",
            placeholderLibre: "Escriba libremente sobre su destino de lujo, hotel, yate o estímulo del entorno...",
            btnActivar: "Activar Mando de Sintonía",
            atencionInaccion: "Atención. Mantenga el enfoque en su pantalla de sintonía ejecutiva.",
            vozSintonialAcustica: "Líder. Frecuencias acústicas activadas para aislamiento total y máximo bienestar.",
            tituloAcustico: "SINTONÍA ACÚSTICA ACTIVA (432HZ / ALFA)",
            misionTitulo: "SANTUARIOS Y VIAJES DE LUJO CURADOS DISPONIBLES",
            discursoMin4: "Calibración completada. Santuario de ultra-lujo e itinerario VIP listo.",
            mapsBtn: "ABRIR RUTA EXCLUSIVA",
            compilarBtn: "COMPILACIÓN PASAPORTE DE BIENESTAR Y VIAJE",
            frecuenciaVoz: "La pausa precisa disuelve el desgaste y asegura el control absoluto sobre su experiencia de viaje y estilo de vida.",
            cierreFinalizado: "Calibración completada con éxito. Su pasaporte premium de bienestar y viajes está listo.",
            fases: [
                { texto: "Inhala", desc: "Expande tu diafragma. Introduce oxígeno puro para resetear el enfoque y claridad mental." },
                { texto: "Retén", desc: "Mantén el aire. Siente la quietud interna y estabiliza tu ritmo cardíaco." },
                { texto: "Exhala", desc: "Suelta despacio. Elimina la presión del entorno y disuelve la fatiga ejecutiva." },
                { texto: "Pausa", desc: "Vacío absoluto. Permanece en silencio antes de diseñar su próxima travesía de lujo." }
            ]
        },
        en: {
            brandSub: "Executive Sanctuary & Luxury Travel Architecture",
            timerTitle: "Active Tuning Window",
            oraculoInstruccion: "What vector blocks your tuning today?",
            desahogoLabel: "Or declare your environmental saturation or travel requirements here:",
            placeholderLibre: "Freely outline your luxury destination, hotel, yacht or ambient stimuli...",
            btnActivar: "Activate Tuning Directive",
            atencionInaccion: "Attention. Maintain absolute focus on your executive tuning screen.",
            vozSintonialAcustica: "Leader. Acoustic frequencies activated for complete isolation and elite wellbeing.",
            tituloAcustico: "ACTIVE ACOUSTIC TUNING (432HZ / ALPHA)",
            misionTitulo: "CURATED SANCTUARIES & LUXURY TRAVEL AVAILABLE",
            discursoMin4: "Calibration completed. Ultra-luxury sanctuary and VIP itinerary fully unlocked.",
            mapsBtn: "OPEN EXCLUSIVE ROUTE",
            compilarBtn: "COMPILE WELLNESS & TRAVEL PASSPORT",
            frecuenciaVoz: "The precise pause dissolves exhaustion and ensures absolute control over your travel experience and lifestyle.",
            cierreFinalizado: "Calibration successfully completed. Your premium wellness and travel passport is ready.",
            fases: [
                { texto: "Inhale", desc: "Expand your chest. Introduce pure oxygen to reset focus index." },
                { texto: "Hold", desc: "Sustain breath. Feel internal quietness and balance heart rate." },
                { texto: "Exhale", desc: "Release smoothly. Discharging environmental saturation and tension." },
                { texto: "Pause", desc: "Absolute void. Remain in perfect stillness before designing your next luxury journey." }
            ]
        }
    },

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

    CATALOGO_PREGUNTAS_ES: [
        "¿Sientes que los estímulos del entorno saturan tu capacidad de contemplar la calma?",
        "¿Se diluye tu enfoque en redes digitales buscando llenar vacíos de desconexión?",
        "¿Buscas un refugio de ultra-lujo, hotel exclusivo o experiencia de entretenimiento privado?",
        "¿El exceso de control sobre tu agenda te priva de disfrutar el entorno en paz?",
        "¿Deseas planificar tu próximo viaje ejecutivo con estándares de élite inquebrantables?",
        "¿Percibes que el ritmo acelerado del entorno nubla tu claridad mental hoy?"
    ],

    CATALOGO_PREGUNTAS_EN: [
        "Do you feel environmental stimuli saturate your ability to contemplate calm?",
        "Does your strategic focus dissolve in digital networks trying to fill moments of friction?",
        "Are you seeking an ultra-luxury sanctuary, exclusive hotel or private entertainment experience?",
        "Does excessive schedule control deprive you of calmly observing your environment?"
    ],

    init() {
        this.cambiarIdioma(this.idiomaActual);
        this.conectarMantenimientoDesarrollador();
    },

    cambiarIdioma(lang) {
        this.idiomaActual = lang;
        const diccionario = this.TRADUCCIONES[lang];

        const lblBrandSub = document.getElementById('lblBrandSub');
        if (lblBrandSub) lblBrandSub.innerText = diccionario.brandSub;

        const lblTimerTitle = document.getElementById('lblTimerTitle');
        if (lblTimerTitle) lblTimerTitle.innerText = diccionario.timerTitle;

        const lblOraculo = document.getElementById('lbl-oraculo-instruccion');
        if (lblOraculo) lblOraculo.innerText = diccionario.oraculoInstruccion;

        const lblDesahogo = document.getElementById('lbl-desahogo');
        if (lblDesahogo) lblDesahogo.innerText = diccionario.desahogoLabel;

        const inpTextLibre = document.getElementById('inp-text-libre');
        if (inpTextLibre) inpTextLibre.placeholder = diccionario.placeholderLibre;

        const btnActivarLibre = document.getElementById('btn-activar-libre');
        if (btnActivarLibre) btnActivarLibre.innerText = diccionario.btnActivar;

        const lblZip = document.getElementById('lbl-zip');
        if (lblZip) {
            lblZip.innerText = lang === 'es' ? "Código Postal" : "Zip Code";
        }

        this.inyectarPreguntasOraculo();
    },

    despertarInicial() {
        const pBienvenida = document.getElementById('pantalla-bienvenida');
        if (pBienvenida) pBienvenida.style.display = 'none';

        const wrapperForm = document.getElementById('wrapper-form');
        if (wrapperForm) wrapperForm.classList.remove('hidden');

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
                const inpLibre = document.getElementById('inp-text-libre');
                if (inpLibre) inpLibre.value = pregunta;
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
        utterance.rate = 0.90;
        window.speechSynthesis.speak(utterance);
    },

    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;
        clearTimeout(this.timerInaccion);
        
        const zipInput = document.getElementById('inp-zip');
        const modoSelector = document.getElementById('modo-selector');
        const menteSelector = document.getElementById('mente-selector');
        const budgetSelector = document.getElementById('budget-selector');
        const perfilSelector = document.getElementById('perfil-selector');
        const textLibreInput = document.getElementById('inp-text-libre');

        const zipCode = zipInput ? zipInput.value : "33139";
        const modoActivo = modoSelector ? modoSelector.value : "SALIR";
        const menteActiva = menteSelector ? menteSelector.value : "SILENCIO";
        const budgetActivo = budgetSelector ? budgetSelector.value : "ILIMITADO";
        const perfilActivo = perfilSelector ? perfilSelector.value : "solo";
        const textoLibreStr = textLibreInput ? textLibreInput.value : "";
        
        const wrapperForm = document.getElementById('wrapper-form');
        if (wrapperForm) wrapperForm.classList.add('hidden');

        const activeDock = document.getElementById('activeSessionDock');
        if (activeDock) activeDock.classList.remove('hidden');
        
        this.activarSintonizaAcusticaYouTube();
        this.iniciarPulmonVisual();
        
        this.serviceTimer = setInterval(() => {
            this.timeLeft--;
            this.actualizarRelojInterfaz();
            
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

        try {
            const respuesta = await fetch("/api/sintonizar", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
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

            if (!respuesta.ok) throw new Error("Error en red.");
            const data = await respuesta.json();

            if (data.opciones_escape_vip) {
                data.opciones_escape_vip.forEach(d => {
                    if (!this.historialVistos.includes(d.id)) this.historialVistos.push(d.id);
                });
            }
        } catch (error) {
            console.error("[CRITICAL] Fallo en motor:", error);
            if (this.historialVistos.length === 0) this.historialVistos.push("S1");
        }
    },

    activarSintonizaAcusticaYouTube() {
        const dic = this.TRADUCCIONES[this.idiomaActual];
        this.emitirVoz(dic.vozSintonialAcustica);
        const stack = document.getElementById('interactiveStack');
        if (!stack) return;

        const poolVideos = [
            { t: "Frecuencia Solfeggio 432Hz — Océano Profundo", id: "1ZYbU82GVz4" },
            { t: "Frecuencia Alfa 8Hz — Ondas de Espacio Natural", id: "WPni755-Krg" }
        ];

        let html = `<div style="margin-bottom:10px; font-size:11px; color:var(--gold-champagne); font-weight:bold; letter-spacing:1px; text-transform:uppercase;">${dic.tituloAcustico}</div>`;
        
        poolVideos.forEach((v) => {
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
        let segundoInterno = 0;
        const dic = this.TRADUCCIONES[this.idiomaActual];
        const circle = document.getElementById('lungCircle');
        const txtPulmon = document.getElementById('txt-pulmon');
       
        this.breatheInterval = setInterval(() => {
            segundoInterno++;
            
            if (segundoInterno >= 4) {
                segundoInterno = 0;
                paso = (paso + 1) % 4;
            }

            const faseActual = dic.fases[paso];
            if (circle) circle.innerText = `${faseActual.texto}\n(${4 - segundoInterno}s)`;
            if (txtPulmon) txtPulmon.innerText = faseActual.desc;
           
            if (circle) {
                if (paso === 0) {
                    circle.className = "lung-circle-master lung-inhale-state";
                } else if (paso === 2) {
                    circle.className = "lung-circle-master lung-exhale-state";
                } else {
                    circle.className = "lung-circle-master";
                }
            }
        }, 1000);
    },

    actualizarRelojInterfaz() {
        const clockDisplay = document.getElementById('clockDisplay');
        if (!clockDisplay) return;
        let mins = Math.floor(this.timeLeft / 60).toString().padStart(2, '0');
        let secs = (this.timeLeft % 60).toString().padStart(2, '0');
        clockDisplay.innerText = `${mins}:${secs}`;
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
        divDestino.style.cssText = "background:rgba(192,57,43,0.15); border:2px solid var(--alert-crimson); padding:16px; border-radius:16px; margin-top:15px; text-align:left; cursor:pointer;";
        
        divDestino.onclick = () => window.open(`https://www.google.com/search?q=${encodeURIComponent('Amanera Resort Luxury Travel & Hotel')}`, '_blank');

        divDestino.innerHTML = `
            <div style="font-size:11px; color:var(--alert-crimson); font-weight:bold; letter-spacing:1px; text-transform:uppercase; margin-bottom:4px;">💥 SANTUARIO Y HOTEL VIP PROPUESTO</div> 
            <div style="font-size:14px; font-weight:bold; color:#fff; margin-bottom:4px;">Amanera Resort & Elite Travel Oasis</div> 
            <p style="font-size:12px; color:#eee; line-height:1.4; margin-bottom:8px;"> 
                ${this.idiomaActual === 'es' ? 'Haga clic para abrir la ruta exclusiva hacia el hotel y santuario de lujo.' : 'Click to open the exclusive route towards the luxury hotel and sanctuary.'} 
            </p> 
            <span style="font-size:10px; background:var(--alert-crimson); color:#fff; padding:4px 8px; border-radius:4px; font-weight:bold; text-transform:uppercase;">${dic.mapsBtn}</span>
        `;
        stack.insertBefore(divDestino, stack.firstChild);
    },

    activarCierreConscienteCronometrado() {
        const activeDock = document.getElementById('activeSessionDock');
        if (activeDock) activeDock.classList.add('hidden');

        const pantallaCierre = document.getElementById('pantalla-cierre');
        if (pantallaCierre) pantallaCierre.classList.remove('hidden');
        
        const retoSeleccionado = this.CATALOGO_RETOS[Math.floor(Math.random() * this.CATALOGO_RETOS.length)];
        const contenedorMensaje = document.getElementById('cierre-message');
        if (!contenedorMensaje) return;
       
        contenedorMensaje.innerHTML = `
            <div style="margin-bottom:15px;">${this.SVGS[retoSeleccionado.id]}</div> 
            <h3 id="reto-titulo" style="text-transform: uppercase; font-family:'Cinzel', serif; color:var(--gold-champagne); margin-bottom:10px;"> 
                ${this.idiomaActual === 'es' ? retoSeleccionado.titulo_es : retoSeleccionado.titulo_en} 
            </h3> 
            <p id="reto-descripcion" style="font-size:0.95rem; color:#eee; line-height:1.5; margin-bottom:20px;"> 
                ${this.idiomaActual === 'es' ? retoSeleccionado.desc_es : retoSeleccionado.desc_en} 
            </p>
        `;

        this.cierreTimerInterval = setInterval(() => {
            this.cierreTimeLeft--;
            const cierreTimerEl = document.getElementById('cierre-timer');
            if (cierreTimerEl) cierreTimerEl.innerText = this.cierreTimeLeft;
            
            if (this.cierreTimeLeft <= 0) {
                clearInterval(this.cierreTimerInterval);
                this.finalizarCierreYMostrarDescarga();
            }
        }, 1000);
    },

    finalizarCierreYMostrarDescarga() {
        const dic = this.TRADUCCIONES[this.idiomaActual];
        this.emitirVoz(dic.cierreFinalizado);

        const cierreTimerEl = document.getElementById('cierre-timer');
        if (cierreTimerEl) cierreTimerEl.classList.add('hidden');

        const msgFinal = document.getElementById('cierre-mensaje-final');
        if (msgFinal) {
            msgFinal.innerText = dic.cierreFinalizado;
            msgFinal.classList.remove('hidden');
        }
        
        const btnRecomenzar = document.getElementById('btn-recomenzar-experiencia');
        if (btnRecomenzar) btnRecomenzar.classList.remove('hidden');
        
        const root = document.getElementById('cierre-message');
        if (!root) return;

        const folio = "WT-" + Math.floor(100000 + Math.random() * 900000);
        
        root.innerHTML = `
            <div style="text-align:center; padding:10px 0;"> 
                <p style="font-size:14px; color:var(--text-muted); margin-bottom:20px;"> 
                    ${this.idiomaActual === 'es' ? 'Su pasaporte de bienestar y viajes de lujo ha sido estructurado.' : 'Your wellness and luxury travel passport has been fully structured.'} 
                </p> 
                <button class="gold-action-btn" onclick="KERNEL.descargarPDF('${folio}')">${dic.compilarBtn}</button> 
            </div>
        `;
    },

    descargarPDF(folio) {
        document.body.style.cursor = "wait";
        const destinoPrescrito = this.historialVistos.length > 0 ? this.historialVistos[this.historialVistos.length - 1] : "S1";
       
        fetch("/api/pdf", {
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
                variante: "WELLNESS_TRAVEL_ELITE", 
                destino_id: destinoPrescrito
            })
        })
        .then(res => {
            if (!res.ok) throw new Error("Error.");
            return res.blob();
        })
        .then(blob => {
            document.body.style.cursor = "default";
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `Wellness_Travel_Elite_Passport_${folio}.pdf`;
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
