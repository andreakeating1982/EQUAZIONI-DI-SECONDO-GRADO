# 🤖 GUIDA-IA — Ricostruzione e variazione di "Equazioni di Secondo Grado"

> **Documento operativo per un'Intelligenza Artificiale** (MARKY su Easy-Peasy.AI,
> GitHub Copilot, Claude, ChatGPT, ecc.) o per uno sviluppatore, per **ricostruire**,
> **clonare** e **variare** questa app partendo dalla repository GitHub.
>
> **App**: EQUAZIONI DI SECONDO GRADO (variante grado 2, k = 1, del Widget Matematico)
> **Stack**: Vite + React 19 + TypeScript + TailwindCSS 4 + shadcn/ui + KaTeX + ONNX (ink-on)
> **Nessun backend, nessun database**: tutta la logica (generazione equazione, passi,
> verifica, PDF) è lato client. Il server Express serve solo i file statici.

---

## INDICE

1. [Che cos'è l'app](#1-che-cosè-lapp)
2. [Architettura e file critici](#2-architettura-e-file-critici)
3. [Ricostruire l'app da GitHub](#3-ricostruire-lapp-da-github)
4. [Variante A — cambiare il grado dell'equazione](#4-variante-a--cambiare-il-grado-dellequazione)
5. [Variante B — disequazioni di qualsiasi grado](#5-variante-b--disequazioni-di-qualsiasi-grado)
6. [Variante C — equazioni/disequazioni fratte](#6-variante-c--equazionidisequazioni-fratte)
7. [Build, verifica e deploy](#7-build-verifica-e-deploy)
8. [Trasferimento su Render (via GitHub)](#8-trasferimento-su-render-via-github)
9. [ACCESSIBILITÀ (sezione portabile)](#9-accessibilità-sezione-portabile)
10. [Regole d'oro](#10-regole-doro)

---

## 1. Che cos'è l'app

L'app guida uno studente nella risoluzione di un'**equazione di secondo grado**

```
a · x² + b · x + c = 0
```

calcolando il discriminante **Δ = b² − 4ac** e le due soluzioni `x₁`, `x₂` con la
formula risolutiva, senza sostituzione né estrazione di radice (k = 1).

Questa app è la **variante grado 2 (k = 1)** del WIDGET MATEMATICO SORGENTE
(che risolve le trinomie `a·x^(2k) + b·x^k + c = 0` con la sostituzione `t = x^k`).

Il flusso didattico è in **5 passi**, con input tramite **canvas di scrittura a mano**
(riconoscimento ONNX via ink-on) e un box **"RICOPIA SUL QUADERNO"** per ogni passo,
più un **PDF scaricabile** al termine:

1. Equazione inserita (canonica, con a, b, c riconosciuti dal parser)
2. Calcolo del delta Δ (formula con valori sostituiti)
3. Calcolo di x₁ (formula (−b + √Δ) / (2a) con valori sostituiti)
4. Calcolo di x₂ (formula (−b − √Δ) / (2a) con valori sostituiti)
5. Verifica finale e insieme delle soluzioni

Casi particolari gestiti: **Δ = 0** (soluzioni coincidenti, flusso a 4 passi) e
**Δ < 0** (nessuna soluzione reale, messaggio dedicato).

Tutto è pensato per studenti con **BES/DSA**: pochi passi chiari, colori, box da copiare,
feedback immediato CORRETTO/SBAGLIATO, PDF finale.

---

## 2. Architettura e file critici

| File | Ruolo |
|------|-------|
| `client/src/main.tsx` | **`initHeightSync`**: rileva l'iframe, aggiunge `lf-embedded` su `<html>`, misura l'altezza REALE del contenuto (capace di restringersi) e la invia alla cornice embed con il protocollo `labvisivo:height` + risposta al ping `labvisivo:ping` (token `?cornice=`) |
| `client/src/pages/QuadraticExercises.tsx` | **Tutta l'app**: generazione equazione, 5 passi, NotebookGuide, PDF, verifica |
| `client/src/pages/WelcomePage.tsx` | Schermata iniziale (Cognome, Nome, Data, Classe) — layout COMPATTO a margini pareggiati (24 px sopra/sotto la card in embed), classe `lf-welcome-top` su `<html>` in vista autonoma |
| `client/src/components/NumberInputCanvas.tsx` | Canvas input con riconoscimento ONNX, elaborazione LaTeX, display frazioni |
| `client/src/components/MathDrawCanvas.tsx` | Canvas disegno puro (penna, gomma), ResizeObserver, rendering stroke |
| `client/src/hooks/useMathRecognition.ts` | Hook gestione modello ONNX (COMER), init engine, recognize, repairLatex |
| `client/src/components/FractionDisplay.tsx` | Badge visualizzazione frazione riconosciuta |
| `client/src/contexts/AccessibilityContext.tsx` | Accessibilità: provider font/interlinea/righello/contrasto, localStorage `wms_access` |
| `client/src/components/AccessibilityToolbar.tsx` | Accessibilità: barra UI (Font A−/A+, Interlinea, Righello, Modalità, Ascolto) |
| `client/src/hooks/useReadAloud.ts` | **Lettura ad alta voce** (TTS italiano, converte formule KaTeX e MAIUSCOLE) |
| `client/public/fonts/` | **Font OpenDyslexic** (TTF/OTF/WOFF2) per dislessia/ipovedenti |
| `client/public/models/comer/` | Modelli ONNX (encoder/decoder int8) + `vocab.json` |
| `client/public/fonts/` | **Font OpenDyslexic** (TTF/OTF/WOFF2) — caricati dall'app e dalle cornici embed via CORS |
| `client/src/index.css` | Tema Tailwind, `@font-face` OpenDyslexic, stili accessibilità, **regole `lf-welcome-top` / `lf-embedded`** (prima pagina compatta: azzera i `min-h-screen`/100vh in iframe, margini 24/24 px, dissolvenza sul bianco in vista autonoma) |
| `server/index.ts` | Server Express: serving statico + header COOP/COEP + CORS `/fonts` |
| `ACCESSIBILITA.md` | Documentazione completa delle misure di accessibilità |
| `docs/grado.md` | Riferimento: **cambiare il grado** (mappa del codice) |
| `docs/disequazioni.md` | Riferimento: **adattare alle disequazioni** |
| `docs/fratte.md` | Riferimento: **adattare alle fratte** (C.E. + verifica) |
| `scripts/clone_app.py` | Script di clonazione meccanica: cambio grado (`--degree`) e tipo (`--kind`: equazioni, disequazioni, equazioni/disequazioni fratte) |
| `cornice-dinamica/` | Embed per Blogger — cornice **dedicata v3** (da incollare: `embed-blogger.html` alla root è la SUA copia) stile LATINO-FACILE: altezza automatica `labvisivo:height` + ping, schermo intero, ricarica, spinner, stato online/errore con Riprova (15 s), impermeabile (token + scoping DOM + filtro `e.source`), **anti-loop mobile** (niente transizione CSS, debounce ~200 ms, clamp 100–15000 px, conferma salti > 2×, congelamento) |
| `render.yaml` | Blueprint Render (deploy con un clic) |
| `.github/workflows/ci.yml` | CI su ogni push (install → check → test → build) |

### Pipeline del riconoscimento scrittura (ONNX)

```
User scrive sul canvas → MathDrawCanvas (stroke)
  → NumberInputCanvas.handleManualRecognize
    → useMathRecognition.recognize() → ink-on preprocessStrokes()
      → ONNX COMER (encoder_int8.onnx + decoder_int8.onnx)
        → token IDs → decodeToTokenArray() → repairLatex() → LaTeX
          → cleanLatex → evaluateLatex() → valore numerico
            → display frazione + decimale
```

### Embed: prima pagina COMPATTA e altezza reale (fix 09/2026)

La prima pagina (WelcomePage) è stata riallineata al modello LATINO-FACILE con
**margini pareggiati** (foto di verifica "Prima/Ora"): la card sta **subito sotto la
barra di accessibilità** e la pagina **termina subito dopo la card** — niente "grande
vuoto crema" da 100vh. Valori di riferimento misurati:

- **Embed (dentro la cornice del blog)**: 24 px sopra la card (20 px padding-top di
  `.lf-welcome` + 4 px `mb-1` della barra) e **24 px sotto** (simmetrici). L'iframe si
  restringe a **≈ 486 px** (non 640 px fissi).
- **Vista autonoma** (fuori dal blog): body **bianco** sotto la card, la pagina termina
  subito dopo (misurato: card 58→402, body 442 px) con una dissolvenza morbida.

Il meccanismo è in tre pezzi che viaggiano INSIEME (non rimuoverne uno solo):

1. **`main.tsx` → `initHeightSync`** — se l'app è in un iframe (`window.self !==
   window.top`, con try/catch cross-origin) aggiunge `lf-embedded` su `<html>` e invia
   l'altezza REALE con `labvisivo:height`. La misura **deve saper restringersi**:
   `Math.max(body.scrollHeight, body.offsetHeight, docEl.offsetHeight)` e si aggiunge
   `docEl.scrollHeight` **solo se** supera il viewport. NON usare `scrollHeight` assoluto
   come valore: dentro un iframe più alto del contenuto resta "gonfiato" e la cornice
   non potrebbe mai restringersi (il bug dei 640 px).
2. **`index.css` regole `lf-embedded`** — `min-h-screen`/`min-h-dvh`/`body` →
   `min-height: 0 !important`; `.lf-welcome` con `padding-top: 20px`, `padding-bottom:
   24px`, `justify-content: flex-start`; `> div:first-child { padding-top: 0 !important }`.
   **Mai `min-h-screen`/`100vh` dentro un iframe**: l'altezza misurata dipenderebbe
   dall'altezza dell'iframe → loop di crescita infinita.
3. **`WelcomePage.tsx` + regole `lf-welcome-top`** — in vista AUTONOMA
   (`window.self === window.top`) aggiunge su `<html>` la classe `lf-welcome-top`
   (body `#ffffff` + `::after` dissolvenza 48 px); in embed NON va aggiunta. Cleanup nel
   `useEffect` (`return () => html.classList.remove(...)`).

La cornice (genitore) risponde con debounce ~200 ms, clamp 100–15000 px, conferma salti
> 2× — vedi `cornice-dinamica/`.

---

## 3. Ricostruire l'app da GitHub

### 3.1 Localmente (qualsiasi macchina)

```bash
git clone https://github.com/<utente>/<repo>.git
cd <repo>            # se l'app è in una subfolder: cd <subfolder>
pnpm install
pnpm check           # type-check TypeScript — MAI saltare
pnpm dev             # avvia il dev server (http://localhost:5173)
```

> ⚠️ **Per ricostruire l'app IDENTICA** (stesso aspetto della prima pagina, stessi
> margini, embed che si restringe alla card ~486 px invece di 640 px fissi) servono
> TUTTI questi pezzi, non solo `QuadraticExercises.tsx`:
> 1. **`client/src/main.tsx`** → `initHeightSync` (misura che SA restringersi: `max(body.scrollHeight,
>    body.offsetHeight, docEl.offsetHeight)` + `docEl.scrollHeight` solo se supera il
>    viewport; NON mai `scrollHeight` assoluto come riferimento, dentro un iframe resta
>    gonfiato all'altezza del viewport e la cornice non può restringersi);
> 2. **`client/src/index.css`** → regole `html.lf-welcome-top` (body bianco in vista
>    autonoma + dissolvenza 48 px sotto la card) e `html.lf-embedded` (azzera
>    `min-h-screen`/`min-h-dvh`, `.lf-welcome` con `padding-top: 20px` + `padding-bottom:
>    24px`, `> div:first-child { padding-top: 0 }`);
> 3. **`client/src/pages/WelcomePage.tsx`** → `useEffect` che aggiunge/rimuove
>    `lf-welcome-top` su `<html>` SOLO quando `window.self === window.top` (mai in iframe).
>
> Senza questi tre pezzi la prima pagina torna a 100vh col "grande vuoto crema" e
> l'iframe embed resta a 640 px fissi.

### 3.2 Su Easy-Peasy.AI (MARKY)

Caricare la cartella nel sandbox e chiedere a MARKY di fare build, preview e deploy.
Oppure inizializzare un nuovo progetto `web-static` e copiare dentro i file `client/`,
`server/`, `shared/`, `package.json`, `tsconfig*.json`, `vite.config.ts`, `patches/`.

> **Nota**: lo scaffold è **`web-static`** (NON `web-db-user`). Non c'è database né
> autenticazione: non serve alcuna chiave API.

---

## 4. Variante A — cambiare il grado dell'equazione

La sorgente risolve `a·x² + b·x + c = 0` (grado 2, k = 1). Cambiare il grado significa
cambiare **k** e generalizzare a `a·x^(2k) + b·x^k + c = 0`:

| grado | k | sostituzione | radici x |
|-------|---|--------------|----------|
| **2** | **1** | **nessuna (t = x)** | **x = t *(sorgente)*** |
| 4  | 2 | t = x² | x = ±√t |
| 6  | 3 | t = x³ | x = ∛t |
| 8  | 4 | t = x⁴ | x = ±∜t |
| 2k | k | t = x^k | vedi sotto |

**Regola radici (passo finale):**
- k **pari**: `x = ±(t)^(1/k)` (due radici opposte, serve `t ≥ 0`).
- k **dispari**: `x = (t)^(1/k)` (una sola radice reale, `t` qualsiasi).
- k = 1: nessun passo di estrazione (x = t), i passi restano 5.

### Clonazione meccanica con lo script

```bash
python3 scripts/clone_app.py --name "equazioni-sesto-grado" --degree 6
# da repository GitHub invece della cartella locale:
python3 scripts/clone_app.py --source https://github.com/<utente>/<repo>.git \
    --name "equazioni-sesto-grado" --degree 6
```

Lo script accetta anche `--kind` per cambiare il **tipo di attività** (default
`equation`):

```bash
python3 scripts/clone_app.py --name "equazioni-sesto-grado" --degree 6 --kind equation
python3 scripts/clone_app.py --name "disequazioni-secondo-grado" --degree 2 --kind inequality
python3 scripts/clone_app.py --name "equazioni-fratte-quarto-grado" --degree 4 --kind fractional
python3 scripts/clone_app.py --name "disequazioni-fratte" --degree 2 --kind fractional-inequality
```

Il flag `--kind` aggiorna automaticamente titoli, numero di passi e testi visibili;
poi stampa una checklist specifica per il tipo scelto (studio del segno per le
disequazioni, C.E. per le fratte, ecc.).

Lo script copia la cartella e applica le sostituzioni meccaniche (potenze, titoli,
placeholder, testo della sostituzione). **Poi stampa una CHECKLIST dei passi manuali**:
leggerla e completarla (per k ≥ 2: aggiungere il passo 2 della sostituzione `t = x^k`,
il passo di estrazione radice — `Math.sqrt` → `Math.pow(t, 1/k)`, `\sqrt{t}` →
`\sqrt[k]{t}`, `±` solo per k pari — e rendere esplicita la potenza b nel builder:
`"x"` → `"x^{k}"`).

Per la **mappa esatta** di dove è codificato il grado (parser, builder, titoli, testi,
passo finale) leggere **[`docs/grado.md`](docs/grado.md)**.

> ⚠️ **Regola**: MAI fare replace globale delle cifre `2`/`1` — romperebbe `4ac`, `2a`,
> ecc. Sostituire solo i **token di grado** (vedi `clone_app.py` e `docs/grado.md`).

---

## 5. Variante B — disequazioni di qualsiasi grado

Stessa filosofia dell'app, ma la soluzione è un **intervallo** (o unione di intervalli)
con **studio del segno**. Forma: `a·x^(2k) + b·x^k + c ≷ 0` con `≷ ∈ {>, <, ≥, ≤}`.

Restano identici: input a mano ONNX, calcolo del delta, radici dell'equazione associata,
NotebookGuide, PDF, divulgazione progressiva, accessibilità.

La clonazione meccanica si avvia con `--kind inequality` (lo script aggiorna titoli,
passi e testi; la checklist indica i passi manuali). Va poi aggiunto:
1. **Parser del verso** (`>`, `<`, `≥`, `≤` → campo `verso`).
2. **Passo "studio del segno"** (parabola `y = at² + bt + c`, segno `+`/`−` con colori).
3. **Traduzione in x e intervallo finale** (`x < -2 ∨ x > 2`, notazione italiana).
4. **Input della risposta** come intervallo (o selettore strutturato per BES).

Per la **struttura passi completa**, la tabella dei segni e le linee guida BES leggere
**[`docs/disequazioni.md`](docs/disequazioni.md)**.

---

## 6. Variante C — equazioni/disequazioni fratte

Per le **fratte (razionali)** si aggiungono le **Condizioni di Esistenza (C.E.)**
(denominatore ≠ 0) e la verifica che le soluzioni non annullino i denominatori.

La clonazione meccanica si avvia con `--kind fractional` (o
`--kind fractional-inequality` per le disequazioni fratte). Forme trattate:
1. **Frazione unica = 0**: `N(x)/D(x) = 0` → `N(x) = 0` con `D(x) ≠ 0`.
2. **Somma/differenza di frazioni** → denominatore comune → `numeratore = 0`.
3. **Fratte che si riducono a una quadratica/trinomia di grado qualsiasi** → il numeratore
   è `a·x^(2k) + b·x^k + c`, quindi si **riusa TUTTA la logica dell'app** (per k=1 la
   formula quadratica; per k≥2 sostituzione `t = x^k`, delta, radici, estrazione x).
   Il grado può essere qualsiasi.

Passi aggiuntivi: **C.E.**, **numeratore = 0**, **verifica contro le C.E.** (badge
ACCETTABILE / NON ACCETTABILE), **insieme soluzione finale**.

Per la **struttura passi completa** e le linee guida BES leggere
**[`docs/fratte.md`](docs/fratte.md)**. La combinazione "fratte + disequazione" si ottiene
sommando i due riferimenti (C.E. + studio del segno).

---

## 7. Build, verifica e deploy

```bash
pnpm install                 # dipendenze (usa pnpm-lock.yaml)
pnpm check                   # type-check — MAI saltare prima del deploy
pnpm build                   # vite build + esbuild del server → dist/
pnpm dev                     # dev server locale
pnpm start                   # server di produzione (NODE_ENV=production node dist/index.js)
```

Su Easy-Peasy.AI:
- **Preview**: `webdev_deploy mode="preview" project_dir="<cartella>"`
- **Produzione**: prima `webdev_save_checkpoint`, poi (solo dopo conferma esplicita
  dell'utente) `webdev_deploy mode="production"`.

Verifica residui del grado (dopo una clonazione):

```bash
grep -rn "x^{2}\|x^{1}\|x²\|x¹" client/src
```

---

## 8. Trasferimento su Render (via GitHub)

Il progetto include già:
- **`render.yaml`** — Blueprint Render: crea il Web Service con un clic (Node 22,
  `pnpm install --frozen-lockfile && pnpm build`, `pnpm start`).
- **`.github/workflows/ci.yml`** — CI su ogni push (install → check → test → build).

Procedura completa passo-passo: **[`DEPLOY-RENDER.md`](DEPLOY-RENDER.md)**.

In sintesi:
1. Carica questa cartella su un repository GitHub (root del repo).
2. Su [render.com](https://render.com) → **New → Blueprint** → collega il repo.
3. Render legge `render.yaml` e crea il Web Service automaticamente.

> L'app NON ha database né chiavi API: il server Express serve solo i file statici +
> gli header COOP/COEP (richiesti da ONNX Runtime Web) + CORS su `/fonts` (per l'embed
> cross-origin). Non serve configurare nulla oltre a `NODE_VERSION`.

---

## 9. ACCESSIBILITÀ (sezione portabile)

> ⚠️ **SEZIONE ACCESSIBILITÀ** — questa è la sezione che riassume TUTTE le misure di
> accessibilità dell'app. Le stesse misure possono essere **portate su altre app simili**
> copiando i file indicati. Il dettaglio completo è in **[`ACCESSIBILITA.md`](ACCESSIBILITA.md)**.

### Misure implementate (riepilogo)

| # | Misura | File da copiare su altre app |
|---|--------|------------------------------|
| 1 | **Font OpenDyslexic** auto-ospitato | `client/public/fonts/` + `@font-face` in `client/src/index.css` |
| 2 | **Barra di accessibilità** (Font, Interlinea, Righello, Modalità, Ascolto) | `client/src/components/AccessibilityToolbar.tsx` |
| 3 | **Dimensione testo regolabile** 80%–160% | `client/src/contexts/AccessibilityContext.tsx` → `--lf-scale` |
| 4 | **Interlinea regolabile** 1.65 / 1.9 / 2.2 / 2.6 | `AccessibilityContext.tsx` → `--lf-lh` |
| 5 | **Righello di lettura** | `index.css` (`.lf-ruler-band`) |
| 6 | **Modalità ad alto contrasto** | `index.css` (`html.lf-hc`) |
| 7 | **Focus visibile** (`:focus-visible`) | `index.css` |
| 8 | **`prefers-reduced-motion`** rispettato | `index.css` |
| 9 | **Testo base 18px + selezione ad alto contrasto** | `index.css` |
| 10 | **ARIA / tastiera** (`role="toolbar"`, `aria-live`, `aria-label`) | `AccessibilityToolbar.tsx`, `WelcomePage.tsx` |
| 11 | **PDF esportato in OpenDyslexic** | `client/src/pages/QuadraticExercises.tsx` (`handleScaricaPdf`) |
| 12 | **Preferenze persistenti** (`localStorage` `wms_access`) | `AccessibilityContext.tsx` |
| 13 | **CORS sui font** (embed cross-origin) | `server/index.ts` |
| 14 | **Lettura ad alta voce** (TTS italiano) | `client/src/hooks/useReadAloud.ts` + pulsante "Ascolto" |
| 15 | **Cornice embed con OpenDyslexic** (v3: schermo intero, ricarica, stato, impermeabile, **anti-loop mobile**) | `cornice-dinamica/` (dedicata + lite + universale + autosufficiente) |

### Come portare l'accessibilità su un'altra app

1. Copiare `client/public/fonts/` (OpenDyslexic).
2. Copiare in `index.css`: i 4 `@font-face`, le classi `.lf-ruler-band`, `html.lf-hc`,
   `:focus-visible`, `::selection`, `@media (prefers-reduced-motion: reduce)`, e le
   variabili `--lf-scale` / `--lf-lh`.
3. Copiare `AccessibilityContext.tsx` + `AccessibilityToolbar.tsx` e montarli in `App.tsx`
   dentro un `<AccessibilityProvider>`, **prima** del router.
4. Copiare `useReadAloud.ts` per la lettura ad alta voce (voce italiana, converte formule
   ed esponenti in linguaggio naturale).
5. Aggiungere `aria-label` ai campi di input e `role="toolbar"` / `aria-live` alla barra.
6. Nel PDF: usare OpenDyslexic con `@font-face` inline nel documento di stampa.
7. Per l'embed: copiare `cornice-dinamica/` e adattare `APP_URL`/`APP_TITLE` nella sezione
   `⚙️ CONFIGURAZIONE` (la versione universale serve per altre app; quella dedicata è
   a URL fisso). **MANTENERE la funzione `applicaAltezza` e il commento anti-loop**:
   sono ciò che impedisce all'iframe di "allungarsi a dismisura" su mobile.

**Dettaglio completo**: **[`ACCESSIBILITA.md`](ACCESSIBILITA.md)** (con checklist di
verifica rapida).

---

## 10. Regole d'oro

1. **MAI saltare `pnpm check`** prima del deploy — gli errori TypeScript bloccano la build.
2. **Non fare replace globale delle cifre** `2`/`1` quando si cambia grado: sostituire solo
   i **token di grado** (vedi `clone_app.py` / `docs/grado.md`).
3. **Il calcolo di delta, x₁, x₂ è identico per ogni grado** — per k ≥ 2 cambia solo il
   passo di estrazione x (`Math.sqrt` → `Math.pow(t, 1/k)`, `±` solo per k pari).
4. **Per k ≥ 2 aggiungere il passo 2 (sostituzione `t = x^k`)** — nel sorgente k=1 non esiste.
5. **Il canale postMessage è `'labvisivo:height'`** (condiviso): NON cambiarlo negli embed.
6. **Il NotebookGuide DEVE mostrare la derivazione completa** (non versioni abbreviate).
7. **Le frazioni nei badge usano la freccia `→`** (non `=`): `⁴/₂ → 2`.
8. **Decimali con virgola `,`** (formato italiano), interi senza decimali.
9. **Font OpenDyslexic su `html, body, #root` e `.font-sans/.font-serif/.font-mono`**, ma
   **NON** su `.katex` (le formule restano in KaTeX).
10. **Prima del deploy produzione**: sempre `webdev_save_checkpoint` con descrizione.
11. **NON reintrodurre `transition: height` sulla cornice** e NON accettare altezze senza
    limiti nell'handler `labvisivo:height`: usare sempre `applicaAltezza()` (debounce +
    clamp + conferma). L'app, dal canto suo, aggiunge `lf-embedded` all'`<html>` quando
    è dentro un iframe (azzera i `min-h-screen`/100vh) — NON rimuovere quella riga.
12. **La misura dell'altezza (lato app) DEVE saper restringersi**: `max(body.scrollHeight,
    body.offsetHeight, docEl.offsetHeight)` + `docEl.scrollHeight` solo se > viewport.
    MAI `documentElement.scrollHeight` come valore assoluto (dentro un iframe resta
    gonfiato e la cornice non si restringe mai).
13. **`lf-welcome-top` SOLO in vista autonoma** (WelcomePage): in embed non va aggiunta,
    altrimenti il body bianco copre la card. Le regole `lf-embedded`/`lf-welcome-top` di
    `index.css` e `initHeightSync` di `main.tsx` sono il fix dei margini: copiarli SEMPRE
    quando si riclona l'app (vedi sezione 3.1).
14. **Test embed dentro la sandbox Easy-Peasy SOLO same-origin**: il proxy sandbox invia
    `Cross-Origin-Embedder-Policy: require-corp` su tutte le pagine → blocca QUALSIASI
    iframe cross-origine senza header `Cross-Origin-Resource-Policy: cross-origin`
    (verificato: persino `example.com` non si carica). **Non è un bug dell'app**: su
    Blogger il genitore non ha COEP e l'iframe carica. Per la verifica "da blog" usare la
    pagina locale `cornice-dinamica/verifica-embed-produzione.html` oppure controllare
    con `curl -sI <url>` l'assenza di `X-Frame-Options`/`frame-ancestors` sulla risposta.

---

*Documento generato per il pacchetto esportabile di "Equazioni di Secondo Grado" — Settembre 2026.*
