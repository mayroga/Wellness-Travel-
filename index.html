<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>MAY ROGA LLC - Wellness App Sandbox</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #0d0d0d; color: #ffffff; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .container { max-width: 600px; width: 100%; background: #141414; padding: 25px; border-radius: 12px; border: 1px solid #222; }
        h1 { color: #A3704C; text-align: center; }
        .timer { font-size: 28px; text-align: center; margin: 20px 0; color: #ff4d4d; font-family: monospace; }
        .triangle-container { width: 200px; height: 180px; margin: 20px auto; position: relative; border-bottom: 2px solid #333; }
        .circle-pulse { width: 30px; height: 30px; border-radius: 50%; background-color: #ffaa00; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); transition: all 0.5s ease; box-shadow: 0 0 15px #ffaa00; }
        .status-box { padding: 15px; background: #1c1c1c; border-radius: 8px; margin-top: 20px; display: none; }
    </style>
</head>
<body>
<div class="container">
    <h1>MAY ROGA LLC</h1>
    <div id="legalSection">
        <p><b>Legal Disclaimer:</b> MAY ROGA LLC is not a medical institution. This 15-minute service operates strictly for lifestyle enhancement...</p>
        <button id="awakenBtn" disabled onclick="startService()">Lea los Términos para Despertar (10s)</button>
    </div>
    <div id="serviceSection" style="display:none;">
        <div class="timer" id="timeDisplay">15:00</div>
        <div class="triangle-container"><div class="circle-pulse" id="pulseCircle"></div></div>
        <div class="status-box" id="resultBox">
            <h3>Evaluación Final CRM</h3>
            <p id="resultDesc"></p>
            <button onclick="requestPDF()">Descargar Reporte PDF</button>
        </div>
    </div>
</div>
<script>
let countdown = 10; let timeRemaining = 15 * 60; let currentLang = 'ES';
let scores = { initial: 35, respiracion: 95, adivinanzas: 80 };
window.onload = function() {
    let interval = setInterval(() => {
        countdown--;
        if(countdown <= 0) { clearInterval(interval); document.getElementById('awakenBtn').disabled = false; document.getElementById('awakenBtn').innerText = "APRENDO, ACEPTO Y DESPIERTO"; }
        else { document.getElementById('awakenBtn').innerText = `Lea los Términos para Despertar (${countdown}s)`; }
    }, 1000);
};
function startService() {
    document.getElementById('legalSection').style.display = 'none';
    document.getElementById('serviceSection').style.display = 'block';
    setTimeout(() => { runCRMMath(); }, 2000); // Simulates calculation triggering at 14:30
}
function runCRMMath() {
    let actual = (scores.initial * 0.2) + (scores.respiracion * 0.5) + (scores.adivinanzas * 0.3);
    let iev = actual - scores.initial;
    let varText = iev > 5 ? "VAR1_MEJORIA" : "VAR2_IGUAL";
    localStorage.setItem('current_session', JSON.stringify({
        servicio_id: "MR-" + Math.floor(Math.random()*10000), lang: currentLang, score_inicial: scores.initial, score_actual: actual, respiracion_score: scores.respiracion, adivinanzas_score: scores.adivinanzas, iev: iev, variante: varText, destino_id: "HOT-ELITE-001"
    }));
    document.getElementById('resultBox').style.display = 'block';
    document.getElementById('resultDesc').innerText = `IEV: ${iev.toFixed(1)} | Variant: ${varText}`;
}
function requestPDF() {
    let session = JSON.parse(localStorage.getItem('current_session'));
    fetch('/generate-pdf', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(session) })
    .then(r => r.blob()).then(blob => {
        let url = window.URL.createObjectURL(blob); let a = document.createElement('a'); a.href = url; a.download = `Report_${session.servicio_id}.pdf`; a.click();
    });
}
</script>
</body>
</html>
