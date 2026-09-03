# Cambiare il grado dell'equazione — riferimento completo

L'app sorgente risolve equazioni **quadratiche** della forma

```
a · x² + b · x + c = 0        (grado 2, k = 1)
```

in **5 passi**, senza sostituzione (t = x). Le trinomie di grado superiore si
ottengono generalizzando a

```
a · x^(2k) + b · x^k + c = 0
```

con sostituzione **`t = x^k`**, che riduce tutto a una quadratica `a·t² + b·t + c = 0`.
Il **grado** dell'equazione in `x` è `2k`. Il sorgente attuale è **k = 1 → grado 2**
(quadratica).

## Mappa grado → k

| grado | k | sostituzione | tipo | radici x |
|-------|---|--------------|------|----------|
| **2** | **1** | **nessuna (t = x)** | **quadratica *(sorgente)*** | **x = t** |
| 4  | 2 | t = x² | biquadratica | x = ±√t |
| 6  | 3 | t = x³ | bicubica | x = ∛t |
| 8  | 4 | t = x⁴ | — | x = ±∜t |
| 2k | k | t = x^k | trinomia | vedi sotto |

**Regola radici (passo finale):**
- k **pari**: `x = ±(t)^(1/k)` — due radici opposte, serve `t ≥ 0`.
- k **dispari**: `x = (t)^(1/k)` — una sola radice reale, `t` può essere qualsiasi reale.

## Dove è codificato il grado (code map)

File principale: `client/src/pages/QuadraticExercises.tsx`.
Righe indicative — possono slittare dopo modifiche, usare `grep` per conferma.

### 1) Parser dell'espressione scritta — `parseQuadraticLaTeX` (riga ~185)
Riconosce le potenze e assegna i coefficienti:
- `x^{2}` / `x^2` / `x²` → coefficiente **a** (potenza 2k)
- `x^{1}` / `x^1` / `x¹` (o `x` nuda) → coefficiente **b** (potenza k)
- costante → coefficiente **c**

Righe chiave: i blocchi `if (content.includes('x^{2}') ...)` (~239) e
`else if (content.includes('x^{1}') ...)` (~246), le assegnazioni `power = 2` /
`power = 1` (~241, 249), i flag `foundX2` / `foundX1` (~226, 287, 291), e le regex
di pulizia `.replace(/[xX]\^{2}/g, ...)`.

### 2) Builder dell'equazione — `buildEquationLatex` (riga ~808)
- `result += sign + coeffLatex + "x^{2}"` (~822) → potenza 2k
- `result += sign + coeffLatex + "x"` (~830) → potenza k (nuda nel sorgente!)

Per k ≥ 2 la potenza b deve diventare esplicita: `"x"` → `"x^{k}"`.

### 3) Titoli e testi visibili
- `<h1>` header: `EQUAZIONI DI SECONDO GRADO` (~850)
- `WelcomePage.tsx`: titolo `EQUAZIONI DI SECONDO GRADO` + `5 PASSI` (~71–75)
- Hint input: `SCRIVI L'EQUAZIONE ... 2x²−3x+1=0` (~876)
- placeholder: `es. 2x^{2}-3x+1=0` (~936)

### 4) Calcolo matematico (per k=1: resta direttamente in x)
- `delta = b*b - 4*a*c`
- `x1 = (-b + sqrt(delta)) / (2a)` e `x2`
- `positiveRootEntries` e i radicali x₁/x₂ (~343 `buildSolutionLine`)

Per k ≥ 2 lo stesso calcolo avviene sulla quadratica in t, poi si estrae x da t.

### 5) Passo finale — estrazione x da t (solo per k ≥ 2) — **cambia la logica**
- k=1 (attuale): x = t direttamente (nessuna estrazione) — vedi commento ~531.
- k=2: `x = ±√t` → `\pm\sqrt{t}` e `Math.sqrt(t)`.
- k pari ≥4: `±` + radice k-esima → `\pm\sqrt[k]{t}` e `Math.pow(t, 1/k)`.
- k dispari: solo radice k-esima → `\sqrt[k]{t}` (senza `±`) e `Math.pow(t, 1/k)`.

## Workflow di clonazione (riassunto)

1. **Clona** con lo script (sostituzioni meccaniche):
   ```bash
   python3 scripts/clone_app.py --name "equazioni-sesto-grado" --degree 6
   # oppure da repository GitHub:
   python3 scripts/clone_app.py --source https://github.com/<utente>/<repo>.git \
       --name "equazioni-sesto-grado" --degree 6
   ```
   Lo script copia la cartella, rinomina potenze/titoli/placeholder/testo sostituzione.

2. **Completa la logica** secondo la tabella radici qui sopra (lo script NON la tocca):
   - k=1: nessun cambio di logica.
   - k≥2: aggiungi il passo 2 (sostituzione `t = x^k`) e il passo di estrazione
     (`Math.sqrt` → `Math.pow(t, 1/k)`, `\pm\sqrt{` → `\sqrt[k]{`, ecc.), e rendi
     esplicita la potenza b nel builder (`"x"` → `"x^{k}"`).

3. **Verifica**:
   ```bash
   cd /home/user/<name> && pnpm install && pnpm check && pnpm dev
   grep -rn "x^{2}\|x^{1}\|x²\|x¹" client/src   # residui da sistemare
   ```

4. **Deploy** (stesso pattern dell'app sorgente):
   ```bash
   webdev_deploy mode="preview" project_dir="/home/user/<name>"
   # dopo conferma utente:
   webdev_save_checkpoint description="..." project_dir="/home/user/<name>"
   webdev_deploy mode="production" project_dir="/home/user/<name>"
   ```

## Coerenza dei nomi (facoltativo ma consigliato)

Per chiarezza interna, rinominare i simboli specifici del grado:
- `QuadraticExercises` → `Esercizi` / `TrinomieExercises`
- `QuadraticComputed` → `EquazioneComputed`
- `ParsedQuadratic` → `ParsedEquazione`
- `parseQuadraticLaTeX` → `parseEquazioneLaTeX`

Questi sono solo nomi interni (nessun impatto funzionale), ma riducono la confusione
quando si mantengono più cloni con gradi diversi.

## PostMessage e embed

Il canale postMessage è `'labvisivo:height'` (condiviso da tutte le app didattiche):
NON cambiarlo. L'embed Blogger (`cornice-dinamica/`) va rigenerato per la nuova app ma
il tipo messaggio resta `labvisivo:height`.

## Accessibilità

Qualunque variante conserva TUTTE le misure di accessibilità (font OpenDyslexic,
barra, lettura ad alta voce, PDF OpenDyslexic, CORS font): sono indipendenti dal grado.
Vedi `ACCESSIBILITA.md`.
