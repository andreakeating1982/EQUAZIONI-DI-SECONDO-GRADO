# ♿ ACCESSIBILITÀ — Equazioni di Secondo Grado

> ⚠️ **SEZIONE ACCESSIBILITÀ** — Questa è la sezione che riassume **TUTTE** le misure di
> accessibilità/inclusione dell'app. Ogni misura è **portabile su altre app simili**:
> nella tabella è indicato il file da copiare. Il riepilogo operativo "come portarle su
> un'altra app" è in fondo a questa pagina e in `GUIDA-IA.md` (sezione 9).

> Misure di accessibilità/inclusione portate dall'app di riferimento **LATINO FACILE**
> (https://github.com/andreakeating1982/LATINO-FACILE) e dalla **repository sorgente**
> delle equazioni trinomie (EQUAZIONI-DI-QUARTO-GRADO-TRINOMIE-BIQUADRATICHE, da cui
> è allineata la barra a 5 moduli con colori fissi stile Cornice Universale). Pensate
> per studenti con **BES**, **DSA (dislessia, disortografia)** e **ipovisione**.

**Principio guida**: *ogni comando raggiungibile da tastiera; preferenze persistenti;
testo grande e ad alta leggibilità; contrasto regolabile; rispetto di
`prefers-reduced-motion`.*

---

## Panoramica delle misure

| # | Misura | Dove vive nel codice |
|---|--------|----------------------|
| 1 | **Font OpenDyslexic** (auto-ospitato) su tutta l'app | `client/public/fonts/` + `@font-face` in `client/src/index.css` |
| 2 | **Barra di accessibilità** a 5 moduli (Font, Interlinea, Righello, Modalità, Ascolto), colori fissi stile Cornice Universale, gruppi `role="group"` + live region | `client/src/components/AccessibilityToolbar.tsx` |
| 3 | **Dimensione testo regolabile** 80%–160% | `client/src/contexts/AccessibilityContext.tsx` → `--lf-scale` |
| 4 | **Interlinea regolabile** 1.65 / 1.9 / 2.2 / 2.6 | `AccessibilityContext.tsx` → `--lf-lh` |
| 5 | **Righello di lettura** (banda che segue il mouse) | `index.css` (`.lf-ruler-band`) + context |
| 6 | **Modalità ad alto contrasto** | `index.css` (`html.lf-hc`) |
| 7 | **Focus visibile** (tastiera / ipovedenti) | `index.css` (`:focus-visible`) |
| 8 | **`prefers-reduced-motion`** rispettato | `index.css` (`@media (prefers-reduced-motion)`) |
| 9 | **Testo base 18 px + selezione ad alto contrasto** | `index.css` (`body`, `::selection`) |
| 10 | **ARIA e accessibilità da tastiera** | `AccessibilityToolbar.tsx`, `WelcomePage.tsx` |
| 11 | **PDF esportato in OpenDyslexic** | `client/src/pages/QuadraticExercises.tsx` (`handleScaricaPdf`) |
| 12 | **Preferenze persistenti** (`localStorage`) | `AccessibilityContext.tsx` (chiave `wms_access`) |
| 13 | **CORS sui font** (per embed Blogger cross-origin) | `server/index.ts` (`app.use("/fonts", ...)`) |
| 14 | **Lettura ad alta voce** (text-to-speech in italiano) | `client/src/hooks/useReadAloud.ts` + pulsante "Ascolto" nella barra |

---

## Dettaglio

### Font OpenDyslexic
- Quattro `@font-face` (Regular 400, Bold 700, Italic 400, Bold Italic 700) con
  `font-display: swap` in `client/src/index.css`.
- File auto-ospitati in `client/public/fonts/` (TTF, OTF, WOFF2). Nessun CDN esterno.
- Applicato a `html, body, #root` e alle classi `.font-sans/.font-serif/.font-mono`
  (con fallback `'Cambria Math', Cambria, serif`).
- **La notazione matematica (KaTeX) conserva il proprio font** (KaTeX_Main ecc.), non
  sovrascritto: le formule restano perfettamente allineate.

### Barra di accessibilità
Barra fissa in alto, visibile su **tutte** le pagine (`App.tsx`), con **5 moduli**:
- **Font** (`A−` / `A+`): scala 80%–160%, passo 10%, percentuale annunciata con `aria-live`.
- **Interlinea**: cicla 1.65 → 1.9 → 2.2 → 2.6.
- **Righello**: banda gialla di lettura che segue il mouse (`pointer-events: none`).
- **Modalità**: alterna Normale ↔ Alto contrasto.
- **Ascolto**: pulsante **Leggi** / **Stop** che legge ad alta voce il contenuto della
  pagina in italiano (Web Speech API `speechSynthesis`, voce italiana).

**Colori fissi stile Cornice Universale** (allineati alla repository di quarto grado):
barra bianco caldo `#fdfbf8` con bordo `#dedbd6`, capsule crema `#f5f0e6`, testo
marrone scuro `#2e2118`, focus `#b71c1c`. La barra NON usa le variabili del tema:
resta invariata anche se l'app cambia palette.

**Accessibilità della barra stessa (screen reader)**: ogni modulo è un gruppo
`role="group"` con `aria-label` (Font, Interlinea, Righello, Modalità, Ascolto); le
icone decorative sono `aria-hidden`; una **live region** `role="status"` annuncia
all'avvio "Barra di accessibilità pronta" e ad ogni cambiamento (percentuale font,
interlinea, stato righello/modalità, lettura avviata/fermata); i pulsanti sono
raggiungibili da tastiera con `:focus-visible`.

### Dimensione testo e interlinea
Il provider imposta su `<html>`: `font-size: 16px × scala` (scala le unità `rem`) e le
variabili `--lf-scale` / `--lf-lh`. Il `body` usa `font-size: calc(18px * var(--lf-scale))`
e `line-height: var(--lf-lh)`. Tutto scala in modo proporzionale.

### Alto contrasto
`html.lf-hc` applica `filter: contrast(1.3) saturate(1.15)` e sfondo bianco
(+ override dello sfondo `.paper-grain`).

### Lettura ad alta voce (text-to-speech)
Il pulsante **Ascolto → Leggi** nella barra legge ad alta voce **tutta la pagina** in
italiano (Web Speech API `speechSynthesis`, `lang="it-IT"`, migliore voce italiana
disponibile). **Stop** interrompe la lettura.

Caratteristiche della lettura (`useReadAloud.ts`):
- legge **tutto il contenuto**: header, guida del quaderno, sezioni comprimibili e passaggi;
- **converte le formule KaTeX dal LaTeX in italiano parlato**: esponenti ("x²" → "x al
  quadrato", "x³" → "x al cubo"), frazioni ("fratto"), radici ("radice quadrata di"),
  "più o meno", "delta";
- legge anche **etichette e valori dei campi di input** (Cognome, Nome, Data, Classe),
  con le **date lette in forma naturale** ("01/09/2026" → "primo settembre duemilaventisei");
- converte le **parole MAIUSCOLE in minuscolo** per evitare accenti sbagliati o lettura
  lettera-per-lettera;
- ignora toolbar, pulsanti, canvas e script (niente rumore).

### Focus e riduzione movimento
- `:focus-visible { outline: 3px solid var(--ring); outline-offset: 2px }` — anello
  visibile solo alla navigazione da tastiera.
- `::selection { background: var(--primary); color: var(--primary-foreground) }`.
- `@media (prefers-reduced-motion: reduce)` azzera animazioni e transizioni.

### ARIA e struttura
- Le pagine usano il landmark `<main>` (WelcomePage e QuadraticExercises) per la
  navigazione con screen reader e come sorgente per la lettura ad alta voce.
- `html { scroll-behavior: smooth }` per uno scorrimento morbido.
- Barra: `role="toolbar"`, `aria-label`, `aria-pressed` sui toggle, `aria-live` sulla
  percentuale.
- Campi di ingresso `Cognome` / `Nome` / `Data` / `Classe`: `aria-label` (`WelcomePage.tsx`).
- Il canvas di scrittura a mano è affiancato dal pulsante **✎ digita l'equazione**
  (input da tastiera), alternativa per chi non può usare il tratto.

### PDF
Il PDF del quaderno (`handleScaricaPdf`) ora usa **OpenDyslexic** (con `<base>` e
`@font-face` inline nel documento di stampa), mantenendo il fallback Cambria Math per
le formule KaTeX.

### Persistenza
Le impostazioni sono salvate in `localStorage` (chiave `wms_access`) e ricaricate
all'avvio, su tutte le pagine.

### Cornice dinamica (embed per Blogger)
La cartella `cornice-dinamica/` contiene l'embed che mostra l'app dentro un iframe con
**altezza automatica** (protocollo `labvisivo:height` + ping), **titolo in OpenDyslexic**
e — nella versione dedicata v3 — pulsanti **Schermo intero** e **Ricarica** (utili su
LIM/proiettore/tablet), **spinner** rispettoso di `prefers-reduced-motion`, **stato
online/errore** con Riprova, e **impermeabilità** (ogni cornice è un'isola: id con
token, scoping DOM, filtro `e.source`, token `cornice` rispecchiato dall'app —
vedi `client/src/main.tsx`). Il design replica la cornice di LATINO-FACILE. I font sono
caricati dall'app via CORS (versioni dedicata e lite) o incorporati in base64 (versione
autosufficiente). L'accessibilità vale anche dentro l'embed.

**Anti-loop mobile (stabilità dell'altezza)**: la cornice include la protezione che
impedisce all'iframe di "allungarsi ripetutamente a dismisura" su cellulare — nessuna
transizione CSS sull'altezza, **debounce** (l'altezza è applicata solo a layout
stabilizzato), **clamp di sanità** (valori < 100 px o > 15000 px ignorati), **conferma
dei salti sospetti** (crescita > 2× richiede che l'app rinvii lo stesso valore) e
**congelamento** (3 crescite consecutive bloccano gli aggiornamenti per 5 s). Sul lato
app, `main.tsx` aggiunge la classe `lf-embedded` quando rileva un iframe: le regole in
`index.css` azzerano i `min-h-screen` (100vh), che dentro un iframe renderebbero
l'altezza misurata dipendente dall'altezza dell'iframe stesso (causa del loop). In
aggiunta la **prima pagina è compatta** (`lf-welcome-top` solo in vista autonoma, body
bianco + dissolvenza): in embed la card sta a 24 px dalla barra e 24 px dal fondo
(margini simmetrici) e l'iframe si restringe a ~486 px. In vista autonoma la pagina
"termina" subito sotto la card (niente vuoto crema).

**Verifica embed in locale**: `cornice-dinamica/verifica-embed-produzione.html` è una
copia della cornice dedicata con pannello di debug (messaggi `labvisivo:height`,
altezza applicata, stato) — aprilo nel browser per verificare il comportamento "da
blog". NB: dentro la sandbox Easy-Peasy il proxy invia `Cross-Origin-Embedder-Policy:
require-corp` che blocca gli iframe cross-origine (non è un difetto dell'app): il test
va fatto same-origin o in locale.

### Come portare queste misure su un'altra app

1. Copiare la cartella `client/public/fonts/` (font OpenDyslexic).
2. Copiare in `index.css`: i 4 `@font-face`, le variabili `--lf-scale` / `--lf-lh`, le
   classi `.lf-ruler-band` e `html.lf-hc`, `:focus-visible`, `::selection` e
   `@media (prefers-reduced-motion: reduce)`.
3. Copiare `AccessibilityContext.tsx` + `AccessibilityToolbar.tsx` e montarli in `App.tsx`
   dentro un `<AccessibilityProvider>`, **prima** del router. La barra usa **colori
   fissi** (#fdfbf8, #f5f0e6, #2e2118, focus #b71c1c): non dipende dalla palette dell'app.
4. Copiare `useReadAloud.ts` per la lettura ad alta voce (voce italiana, converte formule
   ed esponenti in linguaggio naturale).
5. Aggiungere `aria-label` ai campi di input e `role="toolbar"` / `aria-live` alla barra
   (la barra a 5 moduli include già gruppi `role="group"` e una live region `role="status"`).
6. Nel PDF: usare OpenDyslexic con `@font-face` inline nel documento di stampa.
7. Per l'embed: copiare `cornice-dinamica/` e adattare URL, titolo e sottotitolo.
   **MANTENERE l'anti-loop**: niente `transition: height` sull'iframe, debounce ~200 ms,
   clamp 100–15000 px, conferma dei salti > 2× e congelamento dopo 3 crescite; sul lato
   app conservare la riga che aggiunge `lf-embedded` all'`<html>` quando è in iframe.

---

## Verifica rapida

- [ ] Il font OpenDyslexic si carica (DevTools → Network → `/fonts/OpenDyslexic-Regular.ttf` → 200).
- [ ] `Tab` sposta il focus con anello visibile; la barra si annuncia come "toolbar".
- [ ] `A−`/`A+` scala il testo (80%–160%) e la percentuale si aggiorna.
- [ ] Interlinea cicla 1,65 → 1,9 → 2,2 → 2,6.
- [ ] Righello ON/OFF mostra/nasconde la banda gialla senza bloccare i clic.
- [ ] Modalità Contrasto schiarisce lo sfondo e aumenta il contrasto.
- [ ] Le preferenze restano dopo il riavvio del browser (`localStorage` → `wms_access`).
- [ ] Il PDF usa OpenDyslexic.
- [ ] Il pulsante "Ascolto → Leggi" avvia la lettura ad alta voce in italiano; "Stop" la ferma.

---

## Riferimenti

- **OpenDyslexic** — font libero (licenza OFL) per la dislessia.
- **WCAG 2.1/2.2** (W3C): contrasto (1.4.3), ridimensionamento testo (1.4.4), focus
  visibile (2.4.7), tastiera (2.1), `prefers-reduced-motion` (2.3.3).
- **L. 170/2010 e Linee Guida MIUR (DSA)** — contesto normativo della didattica inclusiva.
