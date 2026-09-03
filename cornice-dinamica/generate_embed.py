#!/usr/bin/env python3
"""
Genera la cornice dinamica AUTOSUFFICIENTE di EQUAZIONI DI SECONDO GRADO:
embed-equazioni-secondo-grado.html con il design DEDICATO v3 (titolo centrato,
pulsanti Schermo intero / Ricarica, spinner, stato online/errore, ping periodico)
e i font OpenDyslexic incorporati in base64 (funziona anche offline).

Uso:  python3 generate_embed.py
Legge i font da client/public/fonts/ e il template dedicato da
cornice-dinamica/embed-equazioni-secondo-grado-dedicata.html, e scrive il
file HTML autosufficiente nella cartella cornice-dinamica/.
Ri-eseguibile in ogni momento (i font restano sincronizzati).
"""
import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = ROOT / "client" / "public" / "fonts"
DEDICATA = ROOT / "cornice-dinamica" / "embed-equazioni-secondo-grado-dedicata.html"
OUT = ROOT / "cornice-dinamica" / "embed-equazioni-secondo-grado.html"

regular_b64 = base64.b64encode((FONTS / "OpenDyslexic-Regular-v2.woff2").read_bytes()).decode()
bold_b64 = base64.b64encode((FONTS / "OpenDyslexic-Bold-v2.woff2").read_bytes()).decode()

template = DEDICATA.read_text(encoding="utf-8")

# 1) Sostituisci i due @font-face esterni (via CORS) con quelli base64
template = re.sub(
    r"src: url\('https://deploy-hook-eq2grado\.easy-peasy\.site/fonts/OpenDyslexic-Regular-v2\.woff2'\) format\('woff2'\);",
    f"src: url(data:font/woff2;base64,{regular_b64}) format('woff2');",
    template,
)
template = re.sub(
    r"src: url\('https://deploy-hook-eq2grado\.easy-peasy\.site/fonts/OpenDyslexic-Bold-v2\.woff2'\) format\('woff2'\);",
    f"src: url(data:font/woff2;base64,{bold_b64}) format('woff2');",
    template,
)

# 2) Aggiorna l'intestazione del commento
template = template.replace(
    "CORNICE DINAMICA — EQUAZIONI DI SECONDO GRADO (embed DEDICATO · v3 impermeabile)",
    "CORNICE DINAMICA — EQUAZIONI DI SECONDO GRADO (embed AUTOSUFFICIENTE · v3)",
)
template = template.replace(
    """     ⭐ Versione DEDICATA: serve SOLO «Equazioni di Secondo Grado».
        Nessun parametro, nessun riuso per altre app: URL, colori,
        font e testi sono fissi e allineati a quest'app.""",
    """     ⭐ Versione AUTOSUFFICIENTE: serve SOLO «Equazioni di Secondo Grado».
        Font OpenDyslexic INCORPORATI in base64: funziona anche se l'app
        è offline (i font restano) ed è robusta su qualsiasi piattaforma.""",
)

OUT.write_text(template, encoding="utf-8")
print(f"OK -> {OUT}")
print(f"  dimensione: {len(template)} byte (regular_b64={len(regular_b64)}, bold_b64={len(bold_b64)})")
