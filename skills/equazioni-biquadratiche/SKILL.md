---
name: equazioni-biquadratiche
description: "Manutenzione completa e personalizzazione dell'app WIDGET MATEMATICO SORGENTE (già Equazioni Biquadratiche, in /home/user/equazioni-biquadratiche; Vite + React + TypeScript + Tailwind, scaffold web-static). Usare per: modificare UI studente, personalizzare i passi guidati, deploy preview/produzione, correggere riconoscimento scrittura (ONNX/ink-on), personalizzare il NotebookGuide (RICOPIA SUL QUADERNO), modificare generazione PDF, aggiornare l'embed HTML per Blogger. L'app guida lo studente passo-passo nella risoluzione di equazioni biquadratiche con input tramite scrittura a mano e PDF scaricabile. NON usare per clonare l'app con un grado diverso o per le disequazioni — usare la skill widget-matematico-sorgente."
---

# Widget Matematico Sorgente — Skill di Manutenzione

## Overview

App in `/home/user/equazioni-biquadratiche` (ora chiamata **WIDGET MATEMATICO SORGENTE**).

> **Clonazione / grado diverso / disequazioni**: NON usare questa skill. Usare la skill
> `widget-matematico-sorgente`, che clona l'app cambiando solo il grado dell'equazione
> (2, 4, 6, 8...) e adatta l'app alle disequazioni. Scaffold **`web-static`** (NON `web-db-user`). Stack: Vite + React 18 + TypeScript + TailwindCSS 4 + shadcn/ui + KaTeX. **Nessun backend**, **nessun database** — tutta la logica è lato client.

**URL produzione**: `https://equazioni-biquadratiche.easy-peasy.site`

L'app guida lo studente attraverso la risoluzione di un'equazione biquadratica random in 7 passi:
1. Forma canonica e coefficienti (a, b, c)
2. Delta (Δ = b² − 4ac)
3. Calcolo di t₁ (prima soluzione dell'equazione in t)
4. Calcolo di t₂ (seconda soluzione)
5. Calcolo di x₁ (da t₁: x = ±√t₁)
6. Calcolo di x₂ (da t₂: x = ±√t₂)
7. Verifica finale e soluzione

Ogni passo richiede input tramite **canvas di scrittura a mano** (riconoscimento ONNX via ink-on) e mostra un box **RICOPIA SUL QUADERNO** (NotebookGuide) per lo svolgimento completo da copiare. Al termine: PDF scaricabile.

## File Critici

| File | Ruolo | Righe |
|------|-------|-------|
| `client/src/pages/BiquadraticExercises.tsx` | **Tutta l'app**: generazione equazione, 7 passi, NotebookGuide, PDF, verifica | ~1472 |
| `client/src/components/NumberInputCanvas.tsx` | Canvas input con riconoscimento ONNX, elaborazione LaTeX, display frazioni | ~778 |
| `client/src/components/MathDrawCanvas.tsx` | Canvas disegno puro (penna, gomma), ResizeObserver, rendering stroke | 349 |
| `client/src/hooks/useMathRecognition.ts` | Hook gestione modello ONNX (COMER), init engine, recognize, repairLatex | 177 |
| `client/src/components/FractionDisplay.tsx` | Badge visualizzazione frazione riconosciuta (es. `⁴/₂ → 2`) | 43 |
| `client/src/index.css` | Tema Tailwind, font, animazioni, stili globali | — |
| `client/index.html` | `<html lang="it">`, titolo, meta viewport | — |
| `embed.html` | Codice embed per Blogger (iframe + postMessage altezza dinamica) | — |

## Architettura del Riconoscimento (ONNX)

### Pipeline

```
User scrive sul canvas → MathDrawCanvas (stroke collection)
    → NumberInputCanvas (handleManualRecognize)
        → useMathRecognition.recognize() → ink-on preprocessStrokes()
            → ONNX COMER model (encoder_int8.onnx + decoder_int8.onnx)
                → token IDs → decodeToTokenArray() → repairLatex() → LaTeX string
                    → cleanLatex (rimuove \pm, + iniziale)
                        → evaluateLatex() → valore numerico
                            → display frazione + decimale
```

### Modello ONNX

- **Modello**: COMER (encoder-decoder) per riconoscimento math handwriting
- **File**: `public/models/comer/encoder_int8.onnx`, `decoder_int8.onnx`, `vocab.json`
- **ONNX Runtime**: `onnxruntime-web` con WASM backend
- **Beam width**: 5 (configurato in `useMathRecognition.ts`)
- **Execution provider**: `wasm`

### Modalità di riconoscimento

In `handleManualRecognize` (NumberInputCanvas):
1. Prima prova `recognize(strokes, "expression")` — migliore per frazioni e struttura
2. Fallback: `recognize(strokes, "number")` — per digit puri

### Correzione errori di riconoscimento

**Livello 1 — `repairLatex`** (in `useMathRecognition.ts`): dopo il decode dei token, applica `repairLatex()` da ink-on che corregge errori comuni di formattazione LaTeX (brackets, spaziature, token malformati).

**Livello 2 — Digit correction** (in `NumberInputCanvas.tsx`): mappatura esplicita per caratteri comunemente confusi col 9:

```ts
const DIGIT_FIXES: Record<string, string> = {
  'g': '9', 'q': '9', 'G': '9', 'Q': '9',
  '\\gamma': '9', '\\Gamma': '9',
  '\\operatorname{g}': '9',
};
```

Applicata PRIMA di `cleanLatex` ed `evaluateLatex`. Se il LaTeX riconosciuto corrisponde esattamente a una chiave, viene sostituito.

### Preprocessing

`ink-on` gestisce internamente il preprocessing (`resamplePoints`, `isStrokeMeaningful`). Le funzioni sono importate dinamicamente (non bundle statico):

```ts
const mod = await import("ink-on/core");
InferenceEngine = mod.InferenceEngine;
preprocessStrokesFn = mod.preprocessStrokes;
isStrokeMeaningfulFn = mod.isStrokeMeaningful;
repairLatexFn = mod.repairLatex;
decodeToTokenArrayFn = mod.decodeToTokenArray;
```

### MathDrawCanvas — Dettagli implementativi

- **Canvas interno**: dimensione via `ResizeObserver` su `containerRef`, risoluzione a 700×N px (N = max(140, contentRect.height))
- **Container**: `h-full` per riempire il parent (importante: il parent in NumberInputCanvas ha `h-[170px] sm:h-[200px]`)
- **Stili**: `strokeStyle` nero, `lineWidth` dal tocco/mouse, `lineCap: 'round'`, `lineJoin: 'round'`
- **Gomma**: `globalCompositeOperation: 'destination-out'`
- **Tool**: `write` | `erase` | `select`
- **Griglia**: pattern leggero disegnato a ogni frame (`math-grid-pattern`)

## Flusso dei Passi (Step)

### Generazione Equazione

`useMemo` calcola `BiquadraticComputed` all'inizio. Genera coefficienti casuali garantendo:
- `a ≠ 0` (equazione di 4° grado effettiva)
- `Δ ≥ 0` (almeno una soluzione reale in t)
- Almeno un t positivo (per avere radici reali in x)
- Soluzioni entro range numerici ragionevoli

### Proprietà di `computed`

```ts
interface BiquadraticComputed {
  a, b, c: number;           // coefficienti
  delta: number;             // discriminante
  t1: number | null;         // (-b + √Δ) / (2a)
  t2: number | null;         // (-b - √Δ) / (2a)
  xValues: number[];         // tutte le x (±√t₁, ±√t₂)
  positiveRoots: number[];   // radici positive uniche (valori assoluti)
  positiveRootEntries: PositiveRootEntry[];  // array ordinato con radicali + flag per ogni radice
  solutionType: 'two_distinct' | 'one_double' | 'delta_negative';
  hasOneDoubleSolution: boolean;
  hasRealSolutions: boolean;
  // ...
}
```

### Validazione Step

- **Delta (step 2)**: `areNumbersApproximatelyEqual(deltaUtente, computed.delta, EPSILON * 100)`
- **t₁ (step 3)**: `areNumbersRoundedEqual(t1Utente, computed.t1)` (approssimazione 3 decimali)
- **t₂ (step 4)**: `areNumbersRoundedEqual(t2Utente, computed.t2)`
- **x₁, x₂ (step 5-6)**: confronto valori assoluti con `positiveRoots`, ordinamento crescente

### `PositiveRootEntry` — Struttura per soluzioni finali

```ts
interface PositiveRootEntry {
  value: number;           // valore numerico della radice
  radicalLatex: string;    // LaTeX radicale (es. "\\sqrt{1}", "\\sqrt{\\dfrac{9}{4}}")
  isRational: boolean;     // true se value è razionale
  isInteger: boolean;      // true se value è intero
}
```

**⚠️ IMPORTANTE**: usare UN array `PositiveRootEntry[]` (ordinato per valore crescente) invece di 3 array paralleli (`positiveRootRadicals`, `positiveRootIsRational`, `positiveRootIsInteger`). Gli array paralleli perdono l'accoppiamento quando ordinati separatamente — il bug produceva radicali scambiati tra radici diverse (es. `√1` accoppiato al valore `1,5`).

### `buildRootLine` — Rendering soluzioni finali

Definito inline in DUE punti: feedback verifica (linea ~1360) e NotebookGuide (linea ~1420). **Entrambi devono essere identici.**

Ogni linea è wrappata in `<span style="display:inline-flex;align-items:center;gap:6px;flex-wrap:wrap">` con le varianti separate da frecce `<span class="text-muted-foreground mx-1">→</span>`.

I decimali (es. `±1,50`) sono wrappati in `<span style="font-family:monospace;color:#1e40af;background:#eff6ff;padding:2px 8px;border-radius:8px;font-weight:bold">`.

**Regola**: `renderKatex(..., false)` (displayMode:false) dentro buildRootLine per mantenere le espressioni inline. MAI usare `\\rightarrow` — usare il carattere Unicode `→`.
- **Step 5-6 nascosti**: `allPreviousStepsCorrect` controlla che tutti gli step precedenti siano completati

### NotebookGuide (RICOPIA SUL QUADERNO)

Componente `NotebookGuide` definito inline in `BiquadraticExercises.tsx` (linea ~913). Props:
- `title`: titolo del box (es. "RICOPIA SUL QUADERNO:")
- `visible`: booleano — mostrato solo quando lo step è corretto
- `forceOpen`: `true` durante la generazione PDF
- `children`: contenuto LaTeX renderizzato con KaTeX via `renderKatex()`

**Regola**: il NotebookGuide DEVE mostrare la stessa derivazione completa mostrata fuori dal box (es. `x₁ = ±√t₁ = ±√9 = ±3`, non solo `x₁ = ±√9`).

### `renderKatex` — Funzione helper (ENTRAMBI i file)

**IMPORTANTE**: sia `BiquadraticExercises.tsx` che `NumberInputCanvas.tsx` hanno la propria funzione `renderKatex` locale. Entrambe accettano ora un parametro `displayMode` con default `true`:

```ts
function renderKatex(latex: string, displayMode: boolean = true): string {
  try {
    return katex.renderToString(latex, { displayMode, throwOnError: false, strict: false });
  } catch { return latex; }
}
```

**Regola**: `displayMode: true` (default) per le equazioni dei passi e badge — barra di frazione completa. `displayMode: false` SOLO dentro `buildRootLine` per le soluzioni finali (inline-flex).

**CSS override per badge ambra** (`NumberInputCanvas.tsx` linea ~687): quando si usa `displayMode: true` dentro un flex badge, `.katex-display` ha `display:block; margin:1em 0` che rompe il layout. Aggiungere al contenitore:
```
[&_.katex-display]:!m-0 [&_.katex-display]:!inline
```

Usa `dangerouslySetInnerHTML` in `<p>` o `<span>` per renderizzare LaTeX inline.

### `numberToLatex` — Formattazione numeri

Converte numeri in LaTeX:
- Interi: `"9"` → `"9"`
- Frazioni esatte: `2.25` → `\dfrac{9}{4}`
- Decimali irrazionali: approssimazione con `roundToPrecision`
- Include gestione segno negativo

## PDF Generation

Generato lato client tramite `window.print()` con CSS ottimizzato per singola pagina A4.

### Flusso

```ts
const handleScaricaPdf = () => {
  setGeneratingPdf(true);  // forza apertura di TUTTI i NotebookGuide
  setTimeout(() => {
    // Raccoglie TUTTI i .notebook-content dalla pagina
    // Costruisce HTML con CSS inline compatto
    // Apre nuova finestra e stampa
    const printWindow = window.open('', '_blank');
    printWindow.document.write(html);
    printWindow.document.close();
    printWindow.print();
    setGeneratingPdf(false);
  }, 100);
};
```

### CSS PDF (iniettato inline)

```css
body{font-family:'Cambria Math',Cambria,serif;color:#1a1a1a;padding:12px 18px;max-width:100%;margin:0 auto;text-align:center;line-height:1.65}
@media print{body{padding:8px;zoom:0.82}@page{size:A4;margin:0.6cm}}
/* Font ridotti per stare in una pagina */
.text-base{font-size:14px!important}
.text-lg{font-size:15px!important}
/* Spaziature compatte */
.mb-2{margin-bottom:6px!important}
.space-y-4>*+*{margin-top:14px!important}
/* etc. */
```

**Importante**: Ogni sezione ha `page-break-inside:avoid` per evitare rotture a metà sezione. Il CSS è progettato per comprimere tutto in UNA pagina A4.

## Deploy

```bash
cd /home/user/equazioni-biquadratiche
pnpm check    # verifica TypeScript (MAI saltare)
# Test:
webdev_deploy mode="preview" project_dir="/home/user/equazioni-biquadratiche"
# Produzione (solo dopo conferma utente esplicita):
webdev_save_checkpoint description="..." project_dir="/home/user/equazioni-biquadratiche"
webdev_deploy mode="production" project_dir="/home/user/equazioni-biquadratiche"
```

**Prima del deploy produzione**: sempre `webdev_save_checkpoint` con descrizione significativa.

## Modifiche Comuni

### Cambiare altezza canvas

In `NumberInputCanvas.tsx` (~linea 570): classe Tailwind `h-[170px] sm:h-[200px]`. Per cambiare anche l'area interna, il `MathDrawCanvas` ha già `h-full` sul container — basta cambiare l'altezza del parent in NumberInputCanvas.

### Aggiungere correzioni riconoscimento digit

In `NumberInputCanvas.tsx`, `handleManualRecognize` (~linea 395): aggiungere entry al `DIGIT_FIXES`.

### Modificare NotebookGuide

In `BiquadraticExercises.tsx`, cercare `<NotebookGuide` per ogni passo. Il pattern è:
1. Il contenuto fuori dal NotebookGuide mostra la formula completa
2. Il NotebookGuide DEVE mostrare LA STESSA derivazione (non una versione ridotta)
3. Tutto il LaTeX va renderizzato con `renderKatex()` via `dangerouslySetInnerHTML`

### Modificare generazione equazioni

In `BiquadraticExercises.tsx`, la funzione `useMemo` che calcola `computed` (~linea 415). Modifica i range dei coefficienti o la logica di generazione per cambiare la difficoltà.

### Modificare PDF

In `BiquadraticExercises.tsx`, funzione `handleScaricaPdf` (~linea 578). Il CSS inline è in una template string. Per regolare la compressione: `zoom`, `font-size`, `line-height`, margini `@page`.

### Aggiungere/rimuovere passi

Modificare `BiquadraticExercises.tsx` nella sezione appropriata. Aggiornare anche:
- `allPreviousStepsCorrect` (controlla le condizioni)
- Il `NotebookGuide` corrispondente
- La logica di avanzamento

## Embed Blogger

File `embed.html` nella root del progetto. Usa iframe con `postMessage` per altezza dinamica. L'app invia eventi `'equazionibiquadratiche:height'` via `ResizeObserver`.

## Dipendenze NPM Chiave

| Pacchetto | Ruolo |
|-----------|-------|
| `ink-on` | Riconoscimento scrittura a mano (ONNX COMER model) |
| `onnxruntime-web` | Runtime ONNX nel browser (WASM backend) |
| `katex` | Rendering LaTeX nelle formule |
| `framer-motion` | Animazioni UI |
| `wouter` | Routing lato client (con patch per hash routing) |
| `sonner` | Toast notifications |
| `html-to-image` | Cattura schermate (non usato nel flusso principale) |

## Patch e Configurazioni Particolari

- **`patches/wouter@3.7.1.patch`**: patch per supportare hash routing (`useHashLocation`)
- **`wouter` usa hash routing**: l'app usa `#/` per la navigazione (compatibile con Blogger embed)
- **`pnpm.overrides`**: `tailwindcss>nanoid: 3.3.7` per compatibilità

## Regole d'Oro

1. **MAI saltare `pnpm check`** prima del deploy — TypeScript errors bloccano la build
2. **Canvas interno DEVE avere `h-full`** — il parent in NumberInputCanvas imposta l'altezza
3. **`DIGIT_FIXES` in NumberInputCanvas** — mappatura per correggere errori comuni del modello ONNX
4. **NotebookGuide DEVE mostrare la derivazione completa** — non versioni abbreviate
5. **PDF CSS DEVE usare `page-break-inside:avoid`** sulle sezioni
6. **`repairLatex` si applica DOPO `decodeToTokenArray`, PRIMA di `join`**
7. **Le frazioni nei badge usano la freccia `→`** (non `=`): `⁴/₂ → 2`
8. **Decimali con virgola `,`** non punto (formato italiano)
9. **Interi senza decimali** — `2`, non `2,00` né `2{,}00` — MAI mostrare decimali nelle soluzioni finali
10. **Label canvas in `font-normal`**, non bold
11. **`numberToLatex`** per formattare numeri in LaTeX, **MAI** concatenazione diretta
12. **Template literals annidati**: attenzione all'escaping di `\` in stringhe LaTeX dentro JSX — usa `\\\\` per i backslash nelle regex
13. **`renderKatex` ha parametro `displayMode`** — default `true` per le equazioni dei passi, `false` solo dentro `buildRootLine`
14. **buildRootLine DEVE essere identico in entrambi i punti** (verifica feedback E NotebookGuide) — usa `inline-flex` wrapper con `gap:6px`
15. **MAI `\\rightarrow` in stringhe HTML** — non viene renderizzato da KaTeX, appare come testo letterale. Usare il carattere Unicode `→`
16. **Gli array paralleli causano bug** — usare `PositiveRootEntry[]` con ordine deterministico, MAI `positiveRootRadicals` + `positiveRootIsRational` + `positiveRootIsInteger` paralleli
17. **Il badge di riconoscimento NON mostra più la "FRAZIONE GENERATRICE"** — rimossa perché duplicava la frazione esatta già mostrata
18. **Pulsante ✎ digita l'equazione** presente sul canvas della prima pagina (input manuale via tastiera per l'equazione iniziale)
19. **Layout mobile pulsanti**: `flex-col sm:flex-row` — RICONOSCI su riga propria, GOMMA e CANCELLA affiancati sotto su schermi stretti
20. **Gap badge**: `gap-3` (12px) tra frazione → freccia → decimale (non `gap-2`)
21. **CSS KaTeX in flex badge**: `[&_.katex-display]:!m-0 [&_.katex-display]:!inline` per evitare che `displayMode:true` rompa il layout flex del badge ambra

## Note

- Nessun salvataggio stato — l'esercizio è effimero (refresh = nuova equazione)
- I modelli ONNX sono nella cartella `public/models/comer/` e vengono serviti staticamente
- `useMathRecognition` carica i modelli in modo asincrono al mount del componente
- `isModelReady` controlla se il modello è caricato prima di abilitare il riconoscimento
- La lingua è italiano (placeholder, testi UI, formato numerico)
