# AGENTS.md — Istruzioni per agenti IA che lavorano su questo repository

> Questo file orienta **qualsiasi IA** (GitHub Copilot, Claude, ChatGPT, MARKY su
> Easy-Peasy.AI, Cursor, ecc.) che apre questo repository. Leggilo PRIMA di modificare
> codice o di usare la repo come sorgente per una nuova app.

## Cosa è questo repository

**EQUAZIONI DI SECONDO GRADO** — app didattica (Vite + React 19 + TypeScript +
TailwindCSS 4 + shadcn/ui + KaTeX + ONNX/ink-on) che guida lo studente a risolvere
`a·x² + b·x + c = 0` in 5 passi con input a scrittura manuale, box "RICOPIA SUL
QUADERNO" e PDF scaricabile. Variante **grado 2 (k = 1)** del Widget Matematico.
È pensata per studenti BES/DSA (font OpenDyslexic, barra di accessibilità, TTS).

Struttura: `client/` (React), `server/index.ts` (Express statico: header COOP/COEP
solo su `.html` + CORS su `/fonts` + MIME wasm), `shared/`, `cornice-dinamica/`
(embed per Blogger), `docs/` (riferimenti grado/disequazioni/fratte), `scripts/`.

## Prima di toccare il codice — leggi SEMPRE

| File | Perché leggerlo |
|---|---|
| `GUIDA-IA.md` | La guida operativa completa: ricostruzione, clonazione, varianti (grado, disequazioni, fratte), build, deploy, regole d'oro. **Obbligatoria** se usi questa repo come sorgente per una nuova app. |
| `DEPLOY-RENDER.md` | Trasferimento su Render via GitHub (Blueprint `render.yaml`). |
| `ACCESSIBILITA.md` | Tutte le misure di accessibilità e come portarle su altre app. |
| `cornice-dinamica/README.md` | La cornice embed per Blogger (v3 impermeabile + anti-loop). |

## Regole NON negoziabili

1. **MAI saltare `pnpm check`** prima di un deploy — gli errori TypeScript bloccano la build.
2. **Non fare replace globale delle cifre** `2`/`1` per cambiare grado: usare
   `python3 scripts/clone_app.py --degree N --name <nome>` (token di grado, mai cifre nude).
3. **Non rimuovere** `initHeightSync` in `client/src/main.tsx` né le regole
   `html.lf-embedded` / `html.lf-welcome-top` in `client/src/index.css`: sono il fix dei
   margini della prima pagina (card compatta, embed ~486 px, niente vuoto da 100vh).
   Dentro un iframe **mai** `min-h-screen`/`100vh` (loop di crescita).
4. **Canale postMessage condiviso**: `labvisivo:height` e `labvisivo:ping` — non cambiarli.
5. **Nella cornice embed**: nessuna `transition: height` CSS, debounce ~200 ms, clamp
   100–15000 px, conferma salti > 2× (anti-loop mobile).
6. **Header server**: COOP/COEP solo sui `.html` (ONNX/SharedArrayBuffer); CORS su
   `/fonts`; MAI COEP su font/asset (rompe l'embed cross-origin su Blogger).
7. **Test embed nella sandbox Easy-Peasy**: solo same-origin (il proxy sandbox invia
   `Cross-Origin-Embedder-Policy: require-corp` e blocca gli iframe cross-origine senza
   CORP — non è un bug dell'app). Verifica "da blog" con la pagina locale
   `cornice-dinamica/verifica-embed-produzione.html` o `curl -sI` sull'URL.

## Flusso per creare una VARIANTE dalla repo

```bash
# clona e cambia grado (es. sesto)
python3 scripts/clone_app.py \
  --source https://github.com/<utente>/<repo>.git \
  --name equazioni-sesto-grado --degree 6

# tipo diverso (disequazioni / fratte / disequazioni fratte)
python3 scripts/clone_app.py --source <repo> --name disequazioni-secondo-grado \
  --degree 2 --kind inequality
```

Poi: completare la CHECKLIST stampata dallo script, `pnpm install`, `pnpm check`,
build, deploy, ZIP. Dettagli in `GUIDA-IA.md` (sezioni 3–6) e `docs/`.

## Deploy

- Preview su Easy-Peasy: `webdev_deploy mode="preview"`.
- Produzione Easy-Peasy: checkpoint → conferma utente → `webdev_deploy mode="production"`.
- Render: push su GitHub → Render Blueprint legge `render.yaml` → dopo il deploy
  aggiornare `APP_URL` in `embed-blogger.html`/`cornice-dinamica/` con il nuovo URL.
