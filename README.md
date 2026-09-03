# 📐 EQUAZIONI DI SECONDO GRADO

> **App clonata dal WIDGET MATEMATICO SORGENTE** con **grado 2 (k = 1)**.
> Risolve le equazioni quadratiche `a·x² + b·x + c = 0` passo-passo, senza
> sostituzione né estrazione di radice: si calcola direttamente il delta e le due
> soluzioni `x₁` e `x₂` con la formula risolutiva.

Questa cartella è il **pacchetto completo ed esportabile** dell'app
**EQUAZIONI DI SECONDO GRADO** (5 passi, pensata per studenti BES/DSA). Contiene il codice
sorgente dell'app, i file di embed per il blog (`embed.html`, `embed-blogger.html`, `cornice-dinamica/`), la
guida completa (`GUIDA-UNICA.html`), le istruzioni per GitHub (`ISTRUZIONI-GITHUB.txt`),
la **guida per l'IA** (`GUIDA-IA.md`), la **sezione ACCESSIBILITÀ** (`ACCESSIBILITA.md`),
la guida per **Render** (`DEPLOY-RENDER.md`) e il Blueprint `render.yaml`.

---

## ♿ ACCESSIBILITÀ (sezione portabile)

> ⚠️ **SEZIONE ACCESSIBILITÀ** — questa app include **TUTTE** le misure di accessibilità
> e inclusione per studenti **BES/DSA** (dislessia, disortografia) e **ipovedenti**,
> portate dall'app di riferimento **LATINO FACILE**:

- **Font OpenDyslexic** auto-ospitato su tutta l'app (`client/public/fonts/` + `@font-face`);
- **Barra di accessibilità** fissa: dimensione testo 80%–160%, interlinea 1.65–2.6,
  righello di lettura, modalità ad alto contrasto, **lettura ad alta voce** in italiano;
- **Preferenze persistenti** (`localStorage` → `wms_access`), **focus visibile** da
  tastiera, rispetto di **`prefers-reduced-motion`**, **ARIA** (`role="toolbar"`,
  `aria-label`, `aria-live`);
- **PDF del quaderno in OpenDyslexic** (con fallback Cambria Math per le formule KaTeX);
- **CORS sui font** per l'embed cross-origin e **cornice dinamica** con OpenDyslexic;
- **Prima pagina a margini pareggiati** (card subito sotto la barra, niente vuoto da
  100vh; in embed l'iframe aderisce al contenuto, ~486 px — regole `lf-welcome-top` /
  `lf-embedded` in `index.css` + `initHeightSync` in `main.tsx`).

📄 Dettaglio completo con checklist di verifica: **[`ACCESSIBILITA.md`](ACCESSIBILITA.md)**
📄 Come portarle su altre app: **`ACCESSIBILITA.md`** e **`GUIDA-IA.md`** (sezione 9).

---

## 🎯 La filosofia (pensata per studenti BES/DSA)

L'app ha un unico obiettivo: **accompagnare lo studente passo-passo** nella risoluzione di
un'equazione di secondo grado, **lasciandogli fare soltanto i conti finali più semplici**.

Tutti i passaggi "difficili" (delta, formula risolutiva) sono già mostrati e spiegati.
Lo studente deve scrivere a mano **solo** i numeri essenziali: il discriminante `Δ`, le
radici `x₁` e `x₂` e la verifica finale. Per questo l'app è particolarmente adatta a
studenti con Bisogni Educativi Speciali (BES) e DSA:

- **5 passi chiari e numerati**, uno alla volta (divulgazione progressiva);
- **box "RICOPIA SUL QUADERNO"** con lo svolgimento completo da copiare;
- **feedback immediato** CORRETTO / SBAGLIATO a ogni passo;
- **PDF finale** con Cognome, Nome, Classe e Data, pronto per la valutazione;
- **input a mano** (canvas + riconoscimento ONNX) per chi fatica con la tastiera;
- **casi particolari gestiti**: Δ = 0 (soluzioni coincidenti, 4 passi) e Δ < 0
  (nessuna soluzione reale, il flusso si conclude con il messaggio dedicato).

---

## 📋 I 5 passi dell'app

1. **Equazione inserita** — lo studente scrive (o digita) l'equazione `a·x² + b·x + c = 0`;
2. **Calcolo delta Δ** — viene mostrata la formula `Δ = b² − 4ac` con i valori
   sostituiti; lo studente calcola e inserisce `Δ`;
3. **CALCOLO x₁** — formula `x₁ = (−b + √Δ) / (2a)` con i valori sostituiti;
4. **CALCOLO x₂** — formula `x₂ = (−b − √Δ) / (2a)` con i valori sostituiti;
5. **Verifica del risultato** — lo studente reinserisce `x₁` e `x₂` e l'app conferma
   con "CORRETTO! ✅ LE SOLUZIONI SONO: …" e il box finale **Soluzioni finali**.

Il parser riconosce i coefficienti in molteplici formati (interi, decimali, frazioni,
`\frac{...}{...}`, coefficienti impliciti come `x^{2}` senza numero davanti).

---

## 📦 Cosa contiene questo pacchetto

```
equazioni-secondo-grado/
├── README.md                    ← questo file (guida generale)
├── AGENTS.md                    ← 🤖 istruzioni per agenti IA che aprono la repo
├── ISTRUZIONI-GITHUB.txt        ← come caricare il sorgente su GitHub
├── GUIDA-IA.md                  ← 🤖 guida operativa per l'IA (ricostruire/variare)
├── ACCESSIBILITA.md             ← ♿ SEZIONE ACCESSIBILITÀ completa (portabile)
├── DEPLOY-RENDER.md             ← 🚀 trasferire l'app su Render (via GitHub)
├── render.yaml                  ← Blueprint Render (deploy con un clic)
├── .github/workflows/ci.yml     ← CI su ogni push (check + build)
├── client/                      ← CODICE SORGENTE completo dell'app
│   └── src/pages/QuadraticExercises.tsx   ← app principale (5 passi)
├── server/                      ← server Express (serving statico)
├── shared/                      ← costanti condivise
├── docs/                        ← riferimenti: grado.md, disequazioni.md, fratte.md
├── scripts/clone_app.py         ← script clonazione con grado diverso
├── embed.html                   ← codice embed generico
├── embed-blogger.html           ← codice embed per Blogger (dedicata v3, ANTI-LOOP)
├── cornice-dinamica/             ← cornice embed OpenDyslexic v3 con ANTI-LOOP mobile
│                                   (dedicata + lite + universale + autosufficiente +
│                                   verifica-embed-produzione.html per il test locale)
├── GUIDA-UNICA.html             ← guida completa passo-passo
├── package.json                 ← dipendenze e script
└── skills/                      ← SKILL AI (da installare su Easy-Peasy.AI)
```

### 🤖 Ricostruire/variare l'app con l'IA

La **`GUIDA-IA.md`** è il documento operativo per qualsiasi IA (MARKY su Easy-Peasy.AI,
GitHub Copilot, Claude, ChatGPT…) o sviluppatore che voglia **ricostruire la stessa app**
partendo dalla repository GitHub, oppure generare una variante:

- **Variante A** — cambiare il **grado** dell'equazione (2 → 4, 6, 8…): `scripts/clone_app.py`
  + `docs/grado.md`;
- **Variante B** — trasformare tutto in **disequazioni di qualsiasi grado** (`docs/disequazioni.md`);
- **Variante C** — **equazioni/disequazioni fratte** di qualsiasi grado (`docs/fratte.md`).

### 🚀 Trasferimento su Render

Il pacchetto include **`render.yaml`** (Blueprint) e la guida **`DEPLOY-RENDER.md`**:
carica la cartella su GitHub, collega il repo su Render → **New → Blueprint**, e il Web
Service si crea da solo (Node 22, `pnpm install --frozen-lockfile && pnpm build`,
`pnpm start`).

---

## 🧮 L'app nel contesto del "grado"

L'app sorgente (WIDGET MATEMATICO SORGENTE) risolve **equazioni trinomie** della forma
`a·x^(2k) + b·x^k + c = 0` con la sostituzione `t = x^k`. Questa app è la **variante
grado 2 (k = 1)**: nessuna sostituzione necessaria, si applica direttamente la formula
risolutiva delle quadratiche.

| grado | k | sostituzione | tipo | radici x |
|-------|---|--------------|------|----------|
| **2** | **1** | **nessuna (t = x)** | **quadratica *(questa app)*** | **x = t** |
| 4 | 2 | t = x² | biquadratica *(sorgente)* | x = ±√t |
| 6 | 3 | t = x³ | bicubica | x = ∛t |
| … | k | t = x^k | trinomia | ±(k-esima radice) per k pari, (k-esima radice) per k dispari |

---

## 🚀 L'app è già online

La versione corrente (grado 2, 5 passi) è deployata e funzionante qui:

```
https://deploy-hook-eq2grado.easy-peasy.site
```

Puoi usarla subito, incorporarla nel blog (vedi `embed-blogger.html` o la cornice dinamica
in `cornice-dinamica/`) o personalizzarla.

---

## 🛠️ Sviluppo locale

```bash
pnpm install      # installa le dipendenze
pnpm dev          # avvia il server di sviluppo
pnpm check        # type check TypeScript (MAI saltare prima del deploy)
pnpm build        # build di produzione
```

---

## 🏗️ Tecnologie

React 19 + TypeScript · Vite · TailwindCSS 4 · Wouter · KaTeX · ONNX Runtime Web ·
Ink-ON (riconoscimento scrittura a mano) · Express.

---

*Pacchetto creato con ❤️ da MARKY su Easy-Peasy.AI · Agosto 2026*
