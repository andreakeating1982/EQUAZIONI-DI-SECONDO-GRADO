# Adattare l'app alle disequazioni — riferimento

Stessa filosofia dell'app sorgente: accompagnare lo studente passo-passo, lasciandogli
solo i conti finali più semplici. Per una **disequazione** (quadratica o trinomia) il
flusso si estende con lo **studio del segno** e la soluzione finale è un **intervallo**
(o unione di intervalli) invece di radici discrete.

## Forma generale trattata

```
a · x^(2k) + b · x^k + c  ≷  0      (con  ≷ ∈ {>, <, ≥, ≤})
```

- k = 1 (sorgente): disequazione quadratica `a·x² + b·x + c ≷ 0`, segno studiato
  direttamente sulla parabola in x.
- k ≥ 2: sostituzione `t = x^k` → disequazione quadratica `a·t² + b·t + c ≷ 0`,
  poi traduzione in x.

## Cosa resta identico all'app equazioni

- Input a mano (ONNX/ink-on), `NumberInputCanvas`, `MathDrawCanvas`.
- Calcolo del discriminante `Δ = b² − 4ac` e radici dell'equazione associata.
- `positiveRootEntries`, radicali, NotebookGuide "RICOPIA SUL QUADERNO", PDF.
- Logica di divulgazione progressiva (passi nascosti fino al passo corretto).
- Accessibilità (font OpenDyslexic, barra, lettura ad alta voce, PDF OpenDyslexic).

## Cosa cambia / va aggiunto

### 1) Parser del segno di disequazione
`parseQuadraticLaTeX` oggi normalizza via `.replace(/=0$/, '')`. Per le disequazioni
occorre riconoscere anche il **verso**:
- `> 0`, `< 0`, `\ge 0` / `\geq 0`, `\le 0` / `\leq 0`, `\geqslant`, `\leqslant`
- Salvare il verso in un campo tipo `verso: '>' | '<' | '>=' | '<='`.

Suggerimento: estrarre il verso PRIMA di rimuovere il membro destro, poi procedere
come oggi per i coefficienti a, b, c.

### 2) Nuovo passo: studio del segno della quadratica
Dopo aver ottenuto le radici, aggiungere un passo dedicato alla **parabola associata**
`y = ax² + bx + c` (o `y = at² + bt + c` in t):
- Se `a > 0`: parabola concava verso l'alto (valori positivi fuori dall'intervallo tra le radici).
- Se `a < 0`: concava verso il basso (positivi dentro l'intervallo).

Regola di segno da mostrare (per `a > 0`, con radici `r₁ < r₂`):
```
       r₁         r₂
  ++++++++0--------0++++++++   segno di a·x² + b·x + c
```
(segno `+` esterno all'intervallo, `−` interno; invertire se `a < 0`; per `Δ ≤ 0` segno
costante uguale ad `a`).

### 3) Traduzione in x e intervallo finale
Per k ≥ 2, da `t` a `x` con `x^k = t`:
- k **pari**: `x = ±(t)^(1/k)` solo per `t ≥ 0`; gli intervalli in t si riflettono simmetricamente.
- k **dispari**: `x = (t)^(1/k)` per ogni `t`; la radice k-esima conserva l'ordine (monotona).

Il risultato è scritto come intervallo, es. `x < -2 ∨ x > 2` oppure `]-∞, -2[ ∪ ]2, +∞[`,
oppure `-2 ≤ x ≤ 2`. Scegliere una notazione coerente (consigliata la forma con unione
di intervalli in notazione italiana).

### 4) Input della risposta finale
Per la verifica dello studente, accettare la **scrittura dell'intervallo** (o l'unione).
Opzioni implementative:
- `NumberInputCanvas` riconosce già espressioni; estendere il confronto a intervalli,
  oppure
- usare un selettore strutturato (due estremi + verso) per studenti BES, meno soggetto a
  errori di scrittura.

## Struttura passi per una disequazione (grado 2, k=1)

1. Disequazione inserita (con verso)
2. Calcolo delta Δ
3. Radici x₁, x₂ dell'equazione associata
4. **Studio del segno** (parabola / tabella segni)
5. **Intervallo soluzione** (con verso)
6. Verifica finale

Per k ≥ 2 i passi 2 (sostituzione `t = x^k`) e l'estrazione radice si intercalano come
nelle equazioni trinomie (vedi `grado.md`).

## Linee guida BES per le disequazioni

- **Tabella dei segni visiva**: usare colori distinti per `+` e `−` (es. verde/rosso),
  non solo simboli testuali.
- **Schema della parabola** disegnato (freccia verso alto/basso per `a>0`/`a<0`).
- **Evidenziare il verso richiesto** (`>0` = prendo i `+`, `<0` = prendo i `−`) con un
  riquadro colorato che si muove nella tabella.
- Tenere **NotebookGuide** con la derivazione completa da copiare, identica a quella
  mostrata fuori dal box.
- Fare scrivere allo studente **solo** il delta, le radici, e l'intervallo finale:
  lo studio del segno è mostrato e ragionato, non calcolato a mano.
