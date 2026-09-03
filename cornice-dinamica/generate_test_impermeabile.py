#!/usr/bin/env python3
"""
Genera test-impermeabile.html per EQUAZIONI DI SECONDO GRADO:
simula un blog con 2 cornici dedicate (istanza A e B) + una cornice
«estranea» che tenta il furto dell'iframe e posta altezze false.

Uso:  python3 generate_test_impermeabile.py
Legge il template dedicato (embed-equazioni-secondo-grado-dedicata.html)
e lo incolla due volte dentro la pagina di test.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
DEDICATA = (ROOT / "embed-equazioni-secondo-grado-dedicata.html").read_text(encoding="utf-8")

HEADER = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>TEST impermeabilità cornice — 2 cornici + interferenza</title>
<style>
  body { font-family: Georgia, serif; background: #eee; margin: 0; padding: 20px; }
  h1 { text-align: center; font-size: 20px; }
  .post { background: #fff; border: 1px dashed #999; border-radius: 10px; margin: 20px auto; max-width: 860px; padding: 14px; }
  .post h2 { font-size: 15px; margin: 0 0 8px; color: #444; }
  #esito { position: fixed; top: 8px; right: 8px; background: #222; color: #0f0; font: 11px monospace; padding: 8px 12px; border-radius: 8px; max-width: 380px; white-space: pre-wrap; z-index: 999; }
</style>
</head>
<body>
<h1>🧪 Test impermeabilità — come sul blog (2 cornici + intruso)</h1>
<div id="esito">attendo verifiche…</div>

<script>
  /* Registra i messaggi di altezza ricevuti per la verifica automatica */
  window.__msgLog = [];
  window.addEventListener('message', function (e) {
    try { window.__msgLog.push({ source: (e.source === window ? 'SELF' : (e.source && e.source.location ? e.source.location.href : '?')), data: e.data }); } catch (err) {}
  });
  setInterval(function () {
    var el = document.getElementById('esito');
    if (el) el.textContent = 'messaggi: ' + window.__msgLog.length + '\\n' + JSON.stringify(window.__msgLog.slice(-6), null, 1);
  }, 1500);
</script>
"""

INTRUSO = """
<div class="post">
  <h2>👾 Post 0 — cornice ESTRANEA (tenta il furto e posta altezze false)</h2>
  <p>Questa cornice NON è una cornice LabVisivo: prova a impossessarsi degli iframe
  delle altre cornici e a postare altezze false. Le cornici v3 devono ignorarla.</p>
  <div id="intruso" style="border:2px dashed #c0392b;border-radius:12px;padding:12px;background:#fdf3f2;text-align:center;font-family:Georgia,serif;color:#7f1d1d;">
    <p style="margin:0 0 6px;font-weight:bold;">☠️ Cornice estranea</p>
    <p style="margin:0 0 6px;font-size:13px;">tenta di rubare iframe &lt;iframe id=&quot;lfIframe&quot;&gt; e di postare height=false</p>
    <button onclick="tentaFurto()" style="padding:6px 12px;cursor:pointer;">Tenta il furto ora</button>
  </div>
</div>

<script>
  /* 🕵️ ATTACCO: cerca per id globali (vecchio bug delle v1/v2) e prova a
     modificare l'iframe trovato e a postare altezze false. La cornice v3
     NON deve reagire. */
  function tentaFurto() {
    var trovati = document.querySelectorAll('iframe[id^="lfIframe"]');
    var msg = 'iframe agganciati per id: ' + trovati.length + '\\n';
    trovati.forEach(function (f) { msg += '  - ' + f.id + ' → ' + f.src + '\\n'; });
    try {
      if (trovati.length) {
        var primo = trovati[0];
        try { primo.style.height = '99999px'; } catch (err) {}
        try { primo.contentWindow.postMessage({ type: 'labvisivo:height', height: 99999 }, '*'); } catch (err) {}
      }
      window.parent.postMessage({ type: 'labvisivo:height', height: 99999 }, '*');
      msg += 'altezza falsa 99999 postata (al padre e agli iframe trovati)';
    } catch (err) { msg += 'errore: ' + err.message; }
    alert(msg);
  }
</script>
"""

POST_A = """
<div class="post">
  <h2>📄 Post 1 — cornice Equazioni di Secondo Grado (istanza A)</h2>
  <!-- ===== CORNICE A (v3 impermeabile) ===== -->
"""

POST_B = """
<div class="post">
  <h2>📄 Post 2 — cornice Equazioni di Secondo Grado (istanza B)</h2>
  <!-- ===== CORNICE B (v3 impermeabile) ===== -->
"""

FOOTER = """
</body>
</html>
"""

# La cornice dedicata inizia con un commento <!-- ... -->: lo teniamo (documentazione).
html = HEADER + INTRUSO + POST_A + DEDICATA + POST_B + DEDICATA + FOOTER
out = ROOT / "test-impermeabile.html"
out.write_text(html, encoding="utf-8")
print(f"OK -> {out}")
print(f"  dimensione: {len(html)} byte")
