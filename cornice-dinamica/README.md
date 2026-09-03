# CORNICE DINAMICA — EQUAZIONI DI SECONDO GRADO (embed per Blogger)

Questa cartella contiene la **cornice dinamica** dell'app EQUAZIONI DI SECONDO GRADO:
un blocco HTML autonomo da incollare su Blogger (o su qualsiasi sito) che mostra
l'app dentro un iframe con **altezza automatica**, **font OpenDyslexic** e — nella
versione dedicata — **schermo intero, ricarica, spinner e stato online/errore**.

Il design replica la cornice dinamica di **LATINO FACILE**
(https://github.com/andreakeating1982/LATINO-FACILE → `cornice-dinamica/`):
titolo centrato in OpenDyslexic Bold con letter-spacing, **pulsanti sulla stessa riga
del titolo** (v3), colori carta `#f8f1e4` / inchiostro `#2e2018`.

## File contenuti

| File | Descrizione |
|---|---|
| `embed-equazioni-secondo-grado-dedicata.html` | ⭐ **Versione DEDICATA (~15 KB, v3)**: serve **solo** «Equazioni di Secondo Grado» (URL fisso). 🛡️ **IMPERMEABILE**: funziona anche se il blog ha altre cornici simili nella stessa pagina — ogni istanza è un'isola (id univoci con token, scoping DOM, filtro `e.source`, nessuna app può apparire dentro l'iframe di un'altra). Layout v3: **titolo e pulsanti SULLA STESSA RIGA**, tutto centrato (`flex-wrap` su schermi stretti). Pulsanti **Schermo intero** e **Ricarica**, **spinner**, **stato online/errore** con Riprova (timeout 15 s), ping periodico ogni 3 s + altezza al resize. Font OpenDyslexic via CORS. **La versione consigliata per questo blog** — la sua copia per il post è `embed-blogger.html` alla root del pacchetto. |
| `verifica-embed-produzione.html` | **Pagina di verifica**: copia della dedicata + pannello di debug che mostra in tempo reale i messaggi `labvisivo:height` dell'app e l'altezza applicata all'iframe. Aprila in un browser locale per verificare il comportamento "come su Blogger" (nella sandbox Easy-Peasy gli iframe cross-origine sono bloccati dal COEP del proxy). |
| `test-impermeabile.html` | **Pagina di test**: simula il blog con 2 cornici + una cornice «estranea» che tenta il furto dell'iframe e posta altezze false. Apri il file in un browser per verificare che ogni cornice mostri solo la propria app (le istruzioni di verifica sono nella pagina). |
| `test-dedicata.html` | **Pagina di test**: simula un post del blog con la cornice dedicata dentro un iframe. |
| `embed-equazioni-secondo-grado-lite.html` | **Versione leggera (~5 KB)**: font OpenDyslexic caricati dall'app via CORS. Codice piccolo e leggibile, ideale da incollare nel post. **Riutilizzabile**: per un'altra app basta cambiare la riga `APP_URL` (o passare `?app=URL` nella pagina). Richiede che l'app sia online. |
| `embed-universale.html` | **Template universale per altre app**: identico alla versione lite ma con URL segnaposto (`https://LA-TUA-APP.example.com/`). Copia il file, cambia `APP_URL` e `APP_TITLE` e incollalo dove vuoi. |
| `embed-equazioni-secondo-grado.html` | **Versione autosufficiente (~124 KB)**: font incorporati in base64. Funziona anche se l'app è offline (i font restano) ed è robusta su qualsiasi piattaforma. |
| `generate_embed.py` | Rigenera la versione autosufficiente (base64) dal template dedicato. |
| `generate_test_impermeabile.py` | Rigenera `test-impermeabile.html` (incolla 2 volte il template dedicato + intruso). |
| `README.md` | Questo file |

## Come si usa

1. Apri il post in Blogger e passa alla **vista HTML**.
2. Incolla l'intero contenuto di `embed-equazioni-secondo-grado-dedicata.html` (⭐ consigliata)
   oppure di `embed-equazioni-secondo-grado-lite.html` (minima) o di
   `embed-equazioni-secondo-grado.html` (autosufficiente).
3. Pubblica. L'iframe mostra l'app e si adatta da solo all'altezza del contenuto
   (desktop, tablet, cellulare).

## 🛡️ Anti-loop su mobile (altezza stabile)

Tutte le versioni della cornice includono la protezione **anti-loop**: su cellulare
l'iframe NON si allunga ripetutamente a dismisura. Tre livelli di difesa:

1. **Nessuna transizione CSS** sull'altezza (durante l'animazione l'app misurerebbe
   altezze intermedie e le rinvierebbe, auto-amplificando il loop);
2. **Debounce**: l'altezza viene applicata solo quando l'app smette di inviare
   valori per ~200 ms (layout stabilizzato);
3. **Clamp di sanità + conferma dei salti sospetti**: valori < 100 px o > 15000 px
   ignorati; una crescita > 2× (> 1000 px) viene accettata solo se l'app la
   conferma rinviando lo stesso valore entro 2 s. Un loop divergente invia valori
   sempre diversi → non viene mai confermato → l'iframe resta fermo.

Sul lato app, `client/src/main.tsx` aggiunge la classe `lf-embedded` quando rileva
un iframe: le regole in `index.css` azzerano i `min-h-screen` (100vh) che, dentro
un iframe, renderebbero l'altezza misurata dipendente dall'altezza dell'iframe
stesso (causa principale del loop).

## Riutilizzare la cornice per un'altra app

La cornice è **universale**: per usarla con un'altra app basta cambiare la riga
`APP_URL` nella sezione `⚙️ CONFIGURAZIONE` (e, facoltativamente, `APP_TITLE`).
Tutto il resto — iframe, font OpenDyslexic, altezza dinamica — si adatta da solo.

**Bonus (zero modifiche):** se l'URL è passato come parametro della pagina, ha la
precedenza su `APP_URL`:

```
https://tuosito.it/post?app=https://mia-altra-app.example.com/&title=LA MIA APP
```

- `app` (o `url`): l'URL dell'app da mostrare nella cornice
- `title`: (facoltativo) il titolo mostrato nella barra della cornice

Nota sui font: la cornice carica gli OpenDyslexic da `APP_URL/fonts/*`. Le app
della famiglia LabVisivo li servono con CORS abilitato; se l'app target non li
serve, si usano i font di riserva (Cambria/Georgia) senza alcun errore bloccante.

## Le versioni a confronto

| Caratteristica | `...-dedicata.html` | `...-lite.html` | `embed-equazioni-secondo-grado.html` |
|---|---|---|---|
| Dimensione | ~15 KB (v3 impermeabile) | ~5 KB | ~124 KB |
| Dedicata a Equazioni di Secondo Grado | ✅ sì (URL fisso) | riutilizzabile (`?app=`) | riutilizzabile |
| Schermo intero / Ricarica | ✅ sì | solo «Apri» | solo «Apri» |
| Stato online/errore + Riprova | ✅ sì (timeout 15 s) | no | no |
| Spinner di caricamento | ✅ sì (con `prefers-reduced-motion`) | no | no |
| Font OpenDyslexic | via `/fonts/*` (CORS) | via `/fonts/*` (CORS) | incorporati in base64 |
| App online richiesta | sì (font + contenuto) | sì (font + contenuto) | solo per il contenuto |
| Vantaggio | completa, dedicata, impermeabile (multi-embed sicuro), stato incluso | codice minimo e leggibile | funziona ovunque, zero dipendenze |

## 🛡️ Impermeabilità: perché ora ogni cornice vede solo la propria app

Prima (v1/v2) le cornici usavano **id fissi** (`lfIframe`, `lfCornice`) e
`document.getElementById` globale: se il blog aveva **più cornici simili nella
stessa pagina** (es. più post con app della stessa famiglia LabVisivo), gli
script si agganciavano al **primo** iframe trovato — e dentro una cornice
compariva l'app dell'altra. In più ogni cornice ascoltava **tutti** i messaggi
`postMessage` della pagina e applicava altezze arrivate da altre app.

La v3 rende ogni cornice **impermeabile e non comunicante**:

1. **Scoping DOM per istanza**: lo script trova il PROPRIO `<div class="lf-cornice">`
   risalendo da `document.currentScript` (non più per id globale).
2. **Id univoci con token**: a runtime gli id vengono rinominati con un suffisso
   casuale (`lfIframe-lf5ebjz6da`…). Nessun'altra cornice che cerchi `lfIframe`
   può più agganciare i nostri elementi (e viceversa).
3. **Filtro `e.source`**: il listener accetta messaggi **solo** se arrivano dal
   PROPRIO iframe (`e.source === iframe.contentWindow`). I messaggi di altezza
   delle altre app vengono ignorati.
4. **Token `cornice`**: l'URL dell'iframe porta `?cornice=<token>`; l'app lo
   rispecchia nei messaggi (`main.tsx` → `initHeightSync`) e la cornice rifiuta
   token altrui.
5. **Ping sicuro**: in uscita usa `'*'` (destinatario = nostro iframe, sicuro)
   e in ricezione filtra per `e.source` + token.
6. **CSS scoped**: tutte le regole usano la classe `.lf-cornice` — nessun
   selettore globale che possa toccare il layout del blog o di altre cornici.

Puo' incollare la stessa cornice in **più post della stessa pagina**: ogni
istanza resta indipendente.

## Come funziona l'altezza dinamica

- L'app (dentro l'iframe) misura la propria altezza reale e la invia al genitore
  con un messaggio: `{ type: "labvisivo:height", height: <numero> }`.
- Il codice dell'app che fa questo è in `client/src/pages/WelcomePage.tsx` e
  `client/src/pages/QuadraticExercises.tsx` (ResizeObserver + MutationObserver),
  più il gestore del ping in `client/src/main.tsx` (`initHeightSync`).
- La cornice ascolta i messaggi e imposta `iframe.style.height`.
- La cornice invia anche un "ping" (`{ type: "labvisivo:ping", cornice: <token> }`)
  dopo il caricamento per richiedere l'altezza: l'app risponde con la sua
  altezza rispecchiando il token (gestore in `main.tsx`).

## CORS sui font

Per la versione leggera il server dell'app risponde a `/fonts/*` con
`Access-Control-Allow-Origin: *` (aggiunto in `server/index.ts`).
Senza questo header il browser bloccherebbe il `@font-face` cross-origin quando
la cornice è su un dominio diverso (Blogger).

## Come ricostruire la cornice (per l'IA o a mano)

0. **Nuova app, zero modifiche al codice**: parti da `embed-universale.html`
   (template con URL segnaposto), imposta `APP_URL` (e, facoltativo, `APP_TITLE`)
   nella sezione `⚙️ CONFIGURAZIONE` e incolla il file dove vuoi. L'iframe, i
   font OpenDyslexic e l'altezza dinamica derivano tutti da `APP_URL`: non c'è
   altro da cambiare. In alternativa, puoi passare `?app=URL&title=NOME` come
   parametri della pagina senza toccare il file.
1. **URL dell'app (file esistenti)**: nei file HTML cerca
   `https://deploy-hook-eq2grado.easy-peasy.site` e sostituiscilo con l'URL di
   produzione aggiornato (stessa cosa per eventuali altri domini).
2. **Font (versione autosufficiente)**: i WOFF2 incorporati provengono dai file in
   `../client/public/fonts/` (`OpenDyslexic-Regular-v2.woff2` e
   `OpenDyslexic-Bold-v2.woff2`). Per rigenerarli:
   ```bash
   python3 cornice-dinamica/generate_embed.py
   ```
   Lo script legge il template dedicato e sostituisce i due `@font-face` esterni
   con i data URI base64 dei font.
3. **Perché base64 (versione autosufficiente)?** Incorporando i font la cornice
   funziona ovunque anche senza CORS o con l'app momentaneamente offline.
   La versione leggera invece sfrutta il CORS di `/fonts/*` per restare minima.

## Accessibilità dell'embed

La cornice preserva l'accessibilità dell'app anche dentro un post: font
**OpenDyslexic** anche nella cornice (via CORS nella versione lite, in base64 in
quella autosufficiente), **altezza automatica** dell'iframe (protocollo
`labvisivo:height`, nessun contenuto tagliato), **prefers-reduced-motion**
rispettato (spinner e transizioni disattivati) e pulsanti con `aria-label`.
Il recap completo delle misure di accessibilità dell'app è in
[`../ACCESSIBILITA.md`](../ACCESSIBILITA.md).

## Note di stile

- La cornice riprende i colori dell'app: sfondo carta `#f8f1e4` **uniforme**
  (stesso colore di pagina e header; la barra di accessibilità interna
  all'app è bianco caldo `#fdfbf8` con capsule crema `#f5f0e6`, bordi
  `#dedbd6`, testo `#2e2118`), bordo morbido
  `rgba(46,32,24,.15)` + ombra leggera, titolo inchiostro `#2e2018` e link
  "Apri ↗" in alto a destra (versione lite/universale).
- Il titolo "EQUAZIONI DI SECONDO GRADO" è in **OpenDyslexic Bold** (17px,
  letter-spacing 2px), lo stesso font usato in tutta l'app
  (vedi `../client/src/index.css`).
