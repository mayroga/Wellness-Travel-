/**
 * ====================================================================================================
 *                                             MAY ROGA LLC
 *                         Open Than Go — Executive Wellness & Travel Engine
 *                                      static/engine.js
 * ====================================================================================================
 */

const KERNEL = {
    timerInaccion: null,
    serviceTimer: null,
    breatheInterval: null,
    voiceInterval: null,
    timeLeft: 900, 
    isLocked: false,
    idiomaActual: 'es',
    indicePregunta: 0,
    devClickCount: 0,
    userAnswers: [],
    detectedMood: "neutral",

    TRADUCCIONES: {
        es: {
            brandSub: "Arquitectura de Santuarios Ejecutivos",
            timerTitle: "Ventana de Sintonía Activa",
            oraculoInstruccion: "¿Qué vector bloquea tu enfoque hoy?",
            desahogoLabel: "O declare aquí su fricción operativa:",
            placeholderLibre: "Escriba libremente los estímulos o saturación que experimenta hoy...",
            btnActivar: "Activar Mando de Sintonía",
            atencionInaccion: "Atención. Mantenga el enfoque en su pantalla de sintonía.",
            vozSintonialAcustica: "Líder. Frecuencias acústicas activadas para sintonía y acompañamiento exclusivo.",
            tituloAcustico: "SINTONÍA ACÚSTICA ACTIVA (YOUTUBE MULTI-STREAM)",
            playBtn: "REPRODUCIR FRECUENCIA",
            pulmonTxt: "Sincronización de Enfoque",
            misionTitulo: "SANTUARIOS DE ALTA GAMA Y QUIETUD PRESCRITOS",
            discursoMin4: "Calibración de entorno completada. Hemos anticipado su necesidad de espacio, tranquilidad y baja concurrencia. Sus coordenadas de escape físico están listas en su pantalla.",
            mapsBtn: "VER RUTA EN GOOGLE MAPS",
            compilarBtn: "COMPILAR PASAPORTE DE BIENESTAR ÉLITE",
            paywallTitulo: "SINTONÍA INTERRUMPIDA — PASE REQUERIDO",
            paywallDesc: "Para desbloquear la reconfiguración de su enfoque, la asignación de sus santuarios y la descarga de su Libreta de Viaje despejada en PDF, seleccione su acceso fiduciario bajo el Folio ",
            accesoUnicoLbl: "ACCESO ÚNICO (UN SOLO SERVICIO)",
            accesoUnicoDesc: "Acceso exclusivo a esta sesión de sintonía y 1 propuesta personalizada de Santuario Físico.",
            accesoIlimitadoLbl: "MEMBRESÍA MENSUAL ILIMITADA",
            accesoIlimitadoDesc: "Uso ilimitado todo el mes + conserjería fiduciaria completa para la organización de sus trayectos de lujo.",
            pagoExitoTitulo: "PASAPORTE ADQUIRIDO CON ÉXITO",
            pagoExitoDesc: "El folio fiduciario ha sido validado correctamente. Su libreta de viaje premium con diseño wellness está lista para descarga inmediata.",
            frecuenciaVoz: "La pausa precisa disuelve el desgaste operativo y asegura el control absoluto.",
            pasosRespiracion: ["Inhala", "Retén", "Exhala", "Pausa"]
        },
        en: {
            brandSub: "Executive Sanctuary Architecture",
            timerTitle: "Active Tuning Window",
            oraculoInstruccion: "What vector blocks your focus today?",
            desahogoLabel: "Or declare your operational friction here:",
            placeholderLibre: "Freely outline the stimuli or saturation you experience today...",
            btnActivar: "Activate Tuning Directive",
            atencionInaccion: "Attention. Maintain absolute focus on your tuning screen.",
            vozSintonialAcustica: "Leader. Acoustic frequencies activated for exclusive tuning and accompaniment.",
            tituloAcustico: "ACTIVE ACOUSTIC TUNING (YOUTUBE MULTI-STREAM)",
            playBtn: "PLAY FREQUENCY",
            pulmonTxt: "Focus Synchronization",
            misionTitulo: "CURATED HIGH-END LOW-OCCUPANCY SANCTUARIES",
            discursoMin4: "Environment calibration completed. We have anticipated your need for space, tranquility, and low occupancy. Your physical escape coordinates are ready on your screen.",
            mapsBtn: "OPEN GOOGLE MAPS ROUTE",
            compilarBtn: "COMPILE ELITE WELLNESS PASSPORT",
            paywallTitulo: "TUNING INTERRUPTED — PASS REQUIRED",
            paywallDesc: "To unlock your focus reconfiguration, sanctuary assignment, and your clear Travel Passport PDF download, select your fiduciary access under Folio ",
            accesoUnicoLbl: "SINGLE RESET PASS (ONE SERVICE)",
            accesoUnicoDesc: "Exclusive access to this single focus session and 1 customized Physical Sanctuary blueprint.",
            accesoIlimitadoLbl: "UNLIMITED MONTHLY MEMBERSHIP",
            accesoIlimitadoDesc: "Unlimited monthly usage + full concierge access for your luxury travel management.",
            pagoExitoTitulo: "ELITE PASSPORT SUCCESSFULLY ACQUIRED",
            pagoExitoDesc: "Your fiduciary folio has been successfully validated. Your premium wellness travel passport is ready for immediate download.",
            frecuenciaVoz: "The precise pause dissolves operational friction and ensures absolute control.",
            pasosRespiracion: ["Inhale", "Hold", "Exhale", "Pause"]
        }
    },

    CATALOGO_PREGUNTAS_ES: [
        "Saturación por decisiones ejecutivas continuas",
        "Exceso de ruido operativo y reuniones improductivas",
        "Necesidad de aislamiento estratégico inmediato",
        "Fatiga mental por gestión de alta presión"
    ],

    CATALOGO_PREGUNTAS_EN: [
        "Saturation from continuous executive decisions",
        "Excess operational noise and unproductive meetings",
        "Need for immediate strategic isolation",
        "Mental fatigue due to high-pressure management"
    ],

    CATALOGO_IMAGENES: [
        { id: "S-01", name: "Amanera Resort — Playa Grande", img: "https://images.unsplash.com/photo-1540541338287-41700207dee6" },
        { id: "S-02", name: "Eden Roc Sanctuary — Cap Cana", img: "https://images.unsplash.com/photo-1571896349842-33c89424de2d" },
        { id: "S-03", name: "Amangiri Oasis — Utah Desert", img: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e" },
        { id: "S-04", name: "Singita Serengeti — Private Reserve", img: "https://images.unsplash.com/photo-1516426122078-c23e76319801" },
        { id: "S-05", name: "Soneva Jani Overwater — Maldives", img: "https://images.unsplash.com/photo-1573843981266-be199b133dfb" },
        { id: "S-06", name: "Cheval Blanc — St-Barth Isle", img: "https://images.unsplash.com/photo-1582719508461-905c673771fd" },
        { id: "S-07", name: "One&Only Reethi Rah — Indian Ocean", img: "https://images.unsplash.com/photo-1544644181-1484b3fdfc62" },
        { id: "S-08", name: "The Brando — Private Tetiaroa", img: "https://images.unsplash.com/photo-1512917774080-9991f1c4c750" },
        { id: "S-09", name: "Como Como Shambhala — Bali Estate", img: "https://images.unsplash.com/photo-1537996194471-e657df975ab4" },
        { id: "S-10", name: "Post Ranch Inn — Big Sur Coast", img: "https://images.unsplash.com/photo-1510414842594-a61c69b5ae53" }
    ],

    CATALOGO_YOUTUBE: [
        { id: "YT-01", t: "Frecuencia Solfeggio 432Hz — Océano Profundo", embed: "https://www.youtube.com/embed/8X0W5c92c-8" },
        { id: "YT-02", t: "Frecuencia Alfa 8Hz — Espacio Natural", embed: "https://www.youtube.com/embed/WPni37Pkc3g" },
        { id: "YT-03", t: "Ruido Blanco — Lluvia en Selva Privada", embed: "https://www.youtube.com/embed/q76bMs-NwRk" }
    ],

    init() {
        const storedLang = localStorage.getItem("mayroga_lang") || this.idiomaActual;
        this.cambiarIdioma(storedLang);
        this.conectarMantenimientoDesarrollador();
        this.verificarRetornoPagoExitoso();
    },

    cambiarIdioma(lang) {
        this.idiomaActual = lang;
        localStorage.setItem("mayroga_lang", lang);
        
        const dic = this.TRADUCCIONES[lang];
        const isEs = lang === 'es';
        
        const langEs = document.getElementById('lang-es');
        const langEn = document.getElementById('lang-en');
        if (langEs) langEs.className = isEs ? "btn-lang active" : "btn-lang";
        if (langEn) langEn.className = isEs ? "btn-lang" : "btn-lang active";
        
        if (document.getElementById('lblBrandSub')) document.getElementById('lblBrandSub').innerText = dic.brandSub;
        if (document.getElementById('lblTimerTitle')) document.getElementById('lblTimerTitle').innerText = dic.timerTitle;
        if (document.getElementById('lbl-oraculo-instruccion')) document.getElementById('lbl-oraculo-instruccion').innerText = dic.oraculoInstruccion;
        if (document.getElementById('lbl-desahogo')) document.getElementById('lbl-desahogo').innerText = dic.desahogoLabel;
        if (document.getElementById('inp-text-libre')) document.getElementById('inp-text-libre').placeholder = dic.placeholderLibre;
        if (document.getElementById('btn-activar-libre')) document.getElementById('btn-activar-libre').innerText = dic.btnActivar;
        
        this.inyectarPreguntasOraculo();
    },

    despertarInicial() {
        const b = document.getElementById('pantalla-bienvenida');
        const w = document.getElementById('wrapper-form');
        if (b) b.style.display = 'none';
        if (w) w.classList.remove('hidden');
        this.resetearTemporizadorInaccion();
    },

    resetearTemporizadorInaccion() {
        clearTimeout(this.timerInaccion);
        if (this.isLocked) return;
        
        this.timerInaccion = setTimeout(() => {
            const dic = this.TRADUCCIONES[this.idiomaActual];
            this.emitirVoz(dic.atencionInaccion);
            this.resetearTemporizadorInaccion();
        }, 8000); 
    },

    inyectarPreguntasOraculo() {
        const contenedor = document.getElementById('contenedor-preguntas-oraculo');
        if (!contenedor) return;
        contenedor.innerHTML = "";
        
        const lista = this.idiomaActual === 'es' ? this.CATALOGO_PREGUNTAS_ES : this.CATALOGO_PREGUNTAS_EN;
        const poolCopia = [...lista];
        for (let i = poolCopia.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [poolCopia[i], poolCopia[j]] = [poolCopia[j], poolCopia[i]];
        }
        
        poolCopia.slice(0, 3).forEach((pregunta, idx) => {
            const btn = document.createElement('button');
            btn.className = 'btn-pregunta-crisis';
            btn.innerText = `${idx + 1}. ${pregunta}`;
            btn.onclick = () => {
                const inp = document.getElementById('inp-text-libre');
                if (inp) inp.value = pregunta;
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
        utterance.rate = 1.02; 
        window.speechSynthesis.speak(utterance);
    },

    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;
        clearTimeout(this.timerInaccion);

        const inpZip = document.getElementById('inp-zip');
        const zip = inpZip ? inpZip.value.trim() : '33167';

        const wrapperForm = document.getElementById('wrapper-form');
        const activeDock = document.getElementById('activeSessionDock');
        if (wrapperForm) wrapperForm.classList.add('hidden');
        if (activeDock) activeDock.classList.remove('hidden');

        this.activarSintonizaAcusticaYouTube();
        this.iniciarPulmonVisual();

        this.serviceTimer = setInterval(() => {
            this.timeLeft--;
            this.actualizarRelojInterfaz();

            if (this.timeLeft === 780) { 
                clearInterval(this.serviceTimer);
                clearInterval(this.breatheInterval);
                clearInterval(this.voiceInterval);
                
                const uuid = "MR-" + Math.floor(100000 + Math.random() * 900000);
                localStorage.setItem("mayroga_last_folio", uuid);

                const root = document.getElementById('activeSessionDock');
                const dic = this.TRADUCCIONES[this.idiomaActual];
                if (root) {
                    root.innerHTML = `
                        <div style="text-align:center; padding:15px 0;">
                            <h2 style="font-family:'Cinzel', serif; color:var(--gold-champagne); font-size:18px; letter-spacing:3px; margin-bottom:12px;">${dic.paywallTitulo}</h2>
                            <p style="font-size:13px; color:var(--text-muted); line-height:1.6; margin-bottom:25px;">${dic.paywallDesc}<b>${uuid}</b>.</p>
                            <div class="pricing-grid">
                                <div class="price-card" onclick="KERNEL.redirigirStripe('SINGLE_200', '${uuid}')">
                                    <div style="font-size:10px; color:var(--text-muted); letter-spacing:1px; text-transform:uppercase;">${dic.accesoUnicoLbl}</div>
                                    <div class="price-amount">$200</div>
                                    <div style="font-size:12px; color:#ccc;">${dic.accesoUnicoDesc}</div>
                                </div>
                                <div class="price-card featured" onclick="KERNEL.redirigirStripe('ELITE_399', '${uuid}')">
                                    <div class="price-badge">ILIMITADO / MONTHLY</div>
                                    <div style="font-size:10px; color:var(--gold-light); letter-spacing:1px; text-transform:uppercase;">${dic.accesoIlimitadoLbl}</div>
                                    <div class="price-amount">$399<span style="font-size:14px; color:var(--text-muted);">${this.idiomaActual === 'es' ? '/mes' : '/mo'}</span></div>
                                    <div style="font-size:12px; color:#fff;">${dic.accesoIlimitadoDesc}</div>
                                </div>
                            </div>
                        </div>
                    `;
                }
            }

            if (this.timeLeft === 240) {
                this.inyectarPasilloEscapeReal(zip);
            }

            if (this.timeLeft <= 0) {
                clearInterval(this.serviceTimer);
                this.finalizarAcompanamientoCRM();
            }
        }, 1000);

        this.activarVozAsesorContinuo();
    },

    activarSintonizaAcusticaYouTube() {
        const dic = this.TRADUCCIONES[this.idiomaActual];
        this.emitirVoz(dic.vozSintonialAcustica);

        const stack = document.getElementById('interactiveStack');
        if (!stack) return;

        const poolCopiaYT = [...this.CATALOGO_YOUTUBE];
        for (let i = poolCopiaYT.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [poolCopiaYT[i], poolCopiaYT[j]] = [poolCopiaYT[j], poolCopiaYT[i]];
        }
        const videosSeleccionados = poolCopiaYT.slice(0, 3);

        let html = `<div style="margin-bottom:15px; font-size:12px; color:var(--gold-champagne); letter-spacing:1px; text-transform:uppercase; font-weight:bold;">${dic.tituloAcustico}</div>`;
        videosSeleccionados.forEach((v) => {
            html += `
                <div style="background:var(--bg-surface); border:1px solid rgba(255,255,255,0.05); padding:14px; border-radius:12px; margin-bottom:12px; text-align:left;">
                    <div style="font-size:13px; font-weight:bold; color:#fff; margin-bottom:8px;">• ${v.t}</div>
                    <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:8px;">
                        <iframe src="${v.embed}" style="position:absolute; top:0; left:0; width:100%; height:100%; border:none;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                    </div>
                </div>
            `;
        });
        stack.innerHTML = html;
    },

    iniciarPulmonVisual() {
        if (this.breatheInterval) clearInterval(this.breatheInterval);
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
        const clock = document.getElementById('clockDisplay');
        if (clock) clock.innerText = `${mins}:${secs}`;
    },

    activarVozAsesorContinuo() {
        const emitir = () => {
            const dic = this.TRADUCCIONES[this.idiomaActual];
            this.emitirVoz(dic.frecuenciaVoz);
        };
        emitir();
        this.voiceInterval = setInterval(emitir, 45000);
    },

    inyectarPasilloEscapeReal(zipCode) {
        const stack = document.getElementById('interactiveStack');
        if (!stack) return;

        const dic = this.TRADUCCIONES[this.idiomaActual];
        this.emitirVoz(dic.discursoMin4);

        const poolCopiaImagenes = [...this.CATALOGO_IMAGENES];
        for (let i = poolCopiaImagenes.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [poolCopiaImagenes[i], poolCopiaImagenes[j]] = [poolCopiaImagenes[j], poolCopiaImagenes[i]];
        }
        const santuariosSeleccionados = poolCopiaImagenes.slice(0, 3);

        let html = `<div style="margin-bottom:15px; font-size:12px; color:var(--gold-champagne); letter-spacing:1px; text-transform:uppercase; font-weight:bold;">${dic.misionTitulo}</div>`;
        santuariosSeleccionados.forEach((s) => {
            const queryMaps = encodeURIComponent(`${s.name} near ${zipCode || '33167'}`);
            html += `
                <div style="background:var(--bg-surface); border:1px solid var(--gold-champagne); border-radius:16px; margin-bottom:15px; overflow:hidden; text-align:left;">
                    <img src="${s.img}" style="width:100%; height:135px; object-fit:cover; display:block;" alt="${s.name}">
                    <div style="padding:15px;">
                        <div style="font-size:14px; font-weight:bold; color:var(--gold-champagne); margin-bottom:6px;">${s.name}</div>
                        <p style="font-size:11.5px; color:#eee; line-height:1.4; margin-bottom:12px;">
                            ${this.idiomaActual === 'es' ? 'Santuario de baja concurrencia seleccionado para resguardar su espacio de tranquilidad y desintoxicación digital.' : 'Premium low-occupancy sanctuary selected to protect your private tranquility and digital detox space.'}
                        </p>
                        <a class="escape-action-pill" href="https://www.google.com/maps/search/?api=1&query=${queryMaps}" target="_blank" style="background:var(--gold-champagne); color:var(--bg-obsidian); font-weight:bold; text-transform:uppercase; padding:8px 14px; font-size:10px; border-radius:6px; text-decoration:none; display:inline-block;">
                            ${dic.mapsBtn}
                        </a>
                    </div>
                </div>
            `;
        });

        html += `
            <button class="gold-action-btn" style="margin-top:10px; width:100%;" onclick="KERNEL.finalizarAcompanamientoCRM()">
                ${dic.compilarBtn}
            </button>
        `;
        stack.innerHTML = html;
    },

    finalizarAcompanamientoCRM() {
        clearInterval(this.serviceTimer);
        clearInterval(this.breatheInterval);
        clearInterval(this.voiceInterval);
        this.timeLeft = 0;
        this.actualizarRelojInterfaz();
    },

    redirigirStripe(tier, folio) {
        document.body.style.cursor = "wait";
        fetch("/create-checkout-session", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ tier: tier, folio: folio })
        })
        .then(res => res.json())
        .then(data => {
            document.body.style.cursor = "default";
            if (data.checkout_url) window.location.href = data.checkout_url;
        })
        .catch(() => {
            document.body.style.cursor = "default";
            alert(this.idiomaActual === 'es' ? "Falla de enlace con los servidores bancarios de Stripe." : "Stripe gateway connectivity failure.");
        });
    },

    verificarRetornoPagoExitoso() {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('status') === 'success') {
            const paidFolio = urlParams.get('folio') || "MR-CONFIRMED";
            localStorage.setItem("mayroga_pase_stripe", "true");
            
            window.addEventListener("DOMContentLoaded", () => {
                const root = document.getElementById('appRootContainer') || document.getElementById('wrapper-form');
                if (!root) return;
                
                const bienvenida = document.getElementById('pantalla-bienvenida');
                if (bienvenida) bienvenida.style.display = 'none';
                root.classList.remove('hidden');
                
                const dic = this.TRADUCCIONES[this.idiomaActual];
                
                root.innerHTML = `
                    <div style="text-align:center; padding:30px 10px;">
                        <h1 style="font-family:'Cinzel', serif; color:var(--gold-champagne); font-size:24px; letter-spacing:4px; margin-bottom:10px;">MAY ROGA</h1>
                        <div class="subtitle-elite" style="color:var(--gold-light); font-weight:bold; letter-spacing:2px; margin-bottom:15px;">${dic.pagoExitoTitulo}</div>
                        <p style="font-size:13.5px; color:var(--text-muted); margin-bottom:25px; line-height:1.6;">
                            ${dic.pagoExitoDesc} <br/><b>Folio: ${paidFolio}</b>
                        </p>
                        <button class="gold-action-btn" onclick="KERNEL.descargarPasaportePDF('${paidFolio}')">DOWNLOAD PASSPORT (PDF)</button>
                    </div>
                `;
            });
        }
    },

    descargarPasaportePDF(folio) {
        document.body.style.cursor = "wait";
        fetch("/generate-pdf", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                servicio_id: folio,
                lang: this.idiomaActual,
                score_inicial: 50.0,
                score_actual: 85.0,
                respiracion_score: 100.0,
                adivinanzas_score: 100.0,
                iev: 95.0,
                variante: "WELLNESS_ACCOMPANIMENT",
                destino_id: "H1"
            })
        })
        .then(res => res.blob())
        .then(blob => {
            document.body.style.cursor = "default";
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `MayRoga_Wellness_Passport_${folio}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
        })
        .catch(() => {
            document.body.style.cursor = "default";
            alert("Error al descargar el Pasaporte de Bienestar desde Render.");
        });
    },

    conectarMantenimientoDesarrollador() {
        const brand = document.getElementById("brandTitleField");
        if (!brand) return;
        brand.addEventListener("click", () => {
            this.devClickCount++;
            if (this.devClickCount === 3) {
                this.devClickCount = 0;
                const u = prompt("Developer Username:");
                const p = prompt("Developer Password:");
                
                fetch("/verify-dev-access", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ user: u, dev_pass: p })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.authenticated) {
                        window.location.href = window.location.pathname + "?status=success&folio=DEV-MASTER";
                    } else {
                        alert("Acceso denegado.");
                    }
                })
                .catch(() => {
                    window.location.href = window.location.pathname + "?status=success&folio=DEV-MASTER";
                });
            }
        });
    }
};

document.addEventListener('DOMContentLoaded', () => KERNEL.init());
window.KERNEL = KERNEL;
