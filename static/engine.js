const KERNEL = {
    idiomaActual: 'es',
    devClickCount: 0,
    cierreTimeLeft: 60,
    cierreTimerInterval: null,
    historialVistos: [],
    
    TRADUCCIONES: {
        es: {
            discursoMin4: "Ajustando sintonía ejecutiva y aislamiento acústico ambiental...",
            mapsBtn: "Abrir Ubicación Satelital",
            cierreFinalizado: "Ciclo de estabilización completado con éxito.",
            compilarBtn: "Compilar Pasaporte PDF Fiduciario"
        },
        en: {
            discursoMin4: "Adjusting executive tuning and environmental acoustic isolation...",
            mapsBtn: "Open Satellite Location",
            cierreFinalizado: "Stabilization cycle completed successfully.",
            compilarBtn: "Compile Fiduciary PDF Passport"
        }
    },

    SVGS: {
        S1: `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--gold-champagne)" stroke-width="1.5"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>`,
        S2: `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--gold-champagne)" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>`,
        S3: `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--gold-champagne)" stroke-width="1.5"><path d="M12 2a10 10 0 1 0 10 10H12V2z"/></svg>`,
        S4: `<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--gold-champagne)" stroke-width="1.5"><polygon points="12 2 2 22 22 22 12 2"/></svg>`
    },

    CATALOGO_RETOS: [
        {
            id: 'S1',
            titulo_es: 'Aislamiento Acústico Activo',
            titulo_en: 'Active Acoustic Isolation',
            desc_es: 'Desconecte todos los dispositivos de comunicación durante 10 minutos para restablecer el pulso sináptico.',
            desc_en: 'Disconnect all communication devices for 10 minutes to restore synaptic pulse.'
        },
        {
            id: 'S2',
            titulo_es: 'Sintonización de Enfoque Directivo',
            titulo_en: 'Executive Focus Tuning',
            desc_es: 'Concentre su respiración en ciclos de 4 segundos de inhalación y 6 segundos de exhalación.',
            desc_en: 'Focus your breath in cycles of 4 seconds inhalation and 6 seconds exhalation.'
        }
    ],

    init() {
        this.conectarMantenimientoDesarrollador();
        this.inyectarDestinoOpcionalRojo();
    },

    emitirVoz(texto) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(texto);
            utterance.lang = this.idiomaActual === 'es' ? 'es-ES' : 'en-US';
            window.speechSynthesis.speak(utterance);
        }
    },

    inyectarDestinoOpcionalRojo() {
        const stack = document.getElementById('interactiveStack');
        if (!stack) return;
        const dic = this.TRADUCCIONES[this.idiomaActual];
        this.emitirVoz(dic.discursoMin4);
        
        const divDestino = document.createElement('div');
        divDestino.style = "background:rgba(192,57,43,0.15); border:2px solid var(--alert-crimson); padding:16px; border-radius:16px; margin-top:15px; text-align:left; cursor:pointer;";
        
        divDestino.onclick = () => window.open(`https://google.com/search?q=${encodeURIComponent('Luxury Resort Amanera Playa Grande')}`, '_blank');
        
        divDestino.innerHTML = `
            <div style="font-size:11px; color:var(--alert-crimson); font-weight:bold; letter-spacing:1px; text-transform:uppercase; margin-bottom:4px;">💥 SANTUARIO EXCLUSIVO PROPUESTO</div> 
            <div style="font-size:14px; font-weight:bold; color:#fff; margin-bottom:4px;">Amanera Resort — Luxury Oasis</div> 
            <p style="font-size:12px; color:#eee; line-height:1.4; margin-bottom:8px;"> 
                ${this.idiomaActual === 'es' ? 'Haga clic para abrir la ruta directa hacia el aislamiento absoluto.' : 'Click to open the direct route towards absolute environmental isolation.'} 
            </p> 
            <span style="font-size:10px; background:var(--alert-crimson); color:#fff; padding:4px 8px; border-radius:4px; font-weight:bold; text-transform:uppercase;">${dic.mapsBtn}</span>
        `;
        stack.insertBefore(divDestino, stack.firstChild);

        // Activamos simulación de flujo para demostración de cierre tras 10s
        setTimeout(() => this.activarCierreConscienteCronometrado(), 10000);
    },

    activarCierreConscienteCronometrado() {
        const dock = document.getElementById('activeSessionDock');
        const cierre = document.getElementById('pantalla-cierre');
        if (!dock || !cierre) return;

        dock.classList.add('hidden');
        cierre.classList.remove('hidden');
        
        const retoSeleccionado = this.CATALOGO_RETOS[Math.floor(Math.random() * this.CATALOGO_RETOS.length)];
        const contenedorMensaje = document.getElementById('cierre-message');
        
        if (contenedorMensaje) {
            contenedorMensaje.innerHTML = `
                <div style="margin-bottom:15px;">${this.SVGS[retoSeleccionado.id] || ''}</div> 
                <h3 id="reto-titulo" style="text-transform: uppercase; font-family:'Cinzel', serif; color:var(--gold-champagne); margin-bottom:10px;"> 
                    ${this.idiomaActual === 'es' ? retoSeleccionado.titulo_es : retoSeleccionado.titulo_en} 
                </h3> 
                <p id="reto-descripcion" style="font-size:0.95rem; color:#eee; line-height:1.5; margin-bottom:20px;"> 
                    ${this.idiomaActual === 'es' ? retoSeleccionado.desc_es : retoSeleccionado.desc_en} 
                </p>
            `;
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
        
        const btnRecomenzar = document.getElementById('btn-recomenzar-experiencia');
        if (btnRecomenzar) btnRecomenzar.classList.remove('hidden');
        
        const root = document.getElementById('cierre-message');
        const folio = "MR-" + Math.floor(100000 + Math.random() * 900000);
        
        if (root) {
            root.innerHTML = `
                <div style="text-align:center; padding:10px 0;"> 
                    <p style="font-size:14px; color:var(--text-muted); margin-bottom:20px;"> 
                        ${this.idiomaActual === 'es' ? 'Su documentación de sintonía ejecutiva ha sido estructurada.' : 'Your executive tuning passport has been fully structured.'} 
                    </p> 
                    <button class="gold-action-btn" onclick="KERNEL.descargarPDF('${folio}')">${dic.compilarBtn}</button> 
                </div>
            `;
        }
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
                variante: "ELITE_WELLNESS",
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
