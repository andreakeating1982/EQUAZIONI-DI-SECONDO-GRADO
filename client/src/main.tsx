import { createRoot } from "react-dom/client";
import App from "./App";
import "./index.css";

/**
 * heightSync — sincronizzazione altezza con la cornice embed (protocollo labvisivo)
 *
 * 1) MODALITÀ EMBED: se l'app gira dentro un iframe (cornice dinamica del blog),
 *    aggiungiamo la classe `lf-embedded` su <html>. Le regole in index.css
 *    (html.lf-embedded .min-h-screen { min-height: 0 }, .lf-welcome pareggiato)
 *    azzerano i min-height in 100vh: DENTRO un iframe "100vh" equivale
 *    all'altezza corrente dell'iframe, quindi l'altezza misurata dipenderebbe
 *    dall'altezza dell'iframe stesso e si creerebbe un LOOP DI CRESCITA INFINITA
 *    (l'iframe cresce → 100vh cresce → l'altezza misurata cresce → ...), molto
 *    visibile su mobile. Con `lf-embedded` la pagina segue SOLO il contenuto.
 *
 * 2) MISURA "CHE SI RESTRINGE": NON usiamo documentElement.scrollHeight come
 *    riferimento assoluto. Quando il contenuto è più corto dell'iframe, lo
 *    scrollHeight del documento resta "gonfiato" all'altezza del viewport
 *    dell'iframe (mai meno), quindi la cornice non potrebbe MAI restringersi
 *    e la prima pagina mostrerebbe un grande vuoto. Usiamo invece l'altezza
 *    reale del contenuto (body + offsetHeight del documento) e aggiungiamo
 *    documentElement.scrollHeight SOLO quando il contenuto supera davvero il
 *    viewport. Risultato: la cornice segue la card (≈486px) invece di restare
 *    a 640px fissi con vuoti sopra/sotto.
 *
 * 3) PING della cornice v3 (impermeabile): quando il genitore invia
 *    { type: "labvisivo:ping", cornice: <token> }, misuriamo subito l'altezza
 *    reale e la rispediamo rispecchiando il token, così la cornice si aggiorna
 *    anche senza cambi di layout (es. al resize della finestra).
 */
(function initHeightSync() {
  if (typeof window === "undefined") return;

  // --- Modalità embed: attiva le regole CSS anti-loop (min-h-screen → 0) ---
  try {
    const inIframe = (() => {
      try {
        return window.self !== window.top;
      } catch {
        // cross-origin: se lancia, siamo comunque dentro un iframe
        return true;
      }
    })();
    if (inIframe) {
      document.documentElement.classList.add("lf-embedded");
    }
  } catch {
    /* ignora: senza la classe l'app resta comunque utilizzabile */
  }

  // --- Misura robusta dell'altezza REALE del contenuto (vedi nota 2) ---
  function misuraAltezza(): number {
    const docEl = document.documentElement;
    const body = document.body;
    const viewportH = window.innerHeight || (docEl ? docEl.clientHeight : 0);
    let h = Math.max(
      body ? body.scrollHeight : 0,
      body ? body.offsetHeight : 0,
      docEl ? docEl.offsetHeight : 0,
    );
    // Aggiungi docEl.scrollHeight SOLO se il contenuto supera davvero il
    // viewport: altrimenti resterebbe gonfiato all'altezza dell'iframe.
    if (docEl && docEl.scrollHeight > viewportH) {
      h = Math.max(h, docEl.scrollHeight);
    }
    return h;
  }

  // Token della cornice (parametro ?cornice=...): la cornice dinamica genera
  // un token per OGNI istanza e l'app lo rispecchia nei messaggi di altezza,
  // così la cornice accetta solo i messaggi del PROPRIO iframe.
  function corniceToken(): string {
    try {
      return new URLSearchParams(window.location.search).get("cornice") || "";
    } catch {
      return "";
    }
  }

  let ultimaInviata = 0;

  function sendHeight(token: string = corniceToken()): void {
    // Attivo solo quando siamo dentro un iframe
    if (window.self === window.top) return;
    const height = misuraAltezza();
    if (height < 100) return;
    // Soglia: invia solo se l'altezza è cambiata in modo significativo
    // (evita di rimbalzare valori identici o micro-oscillazioni < 2px)
    if (Math.abs(height - ultimaInviata) < 2) return;
    ultimaInviata = height;
    const msg: Record<string, unknown> = { type: "labvisivo:height", height };
    if (token) msg.cornice = token;
    try {
      if (window.parent && window.parent !== window) {
        window.parent.postMessage(msg, "*");
      }
    } catch {
      /* non in iframe: ignora */
    }
  }

  window.addEventListener("message", (e) => {
    if (!e.data || typeof e.data !== "object") return;
    if (e.data.type !== "labvisivo:ping") return;
    sendHeight(typeof e.data.cornice === "string" ? e.data.cornice : corniceToken());
  });

  // Al primo avvio e a caricamento avvenuto la cornice riceve subito l'altezza
  window.addEventListener("load", () => sendHeight());
  window.addEventListener("resize", () => sendHeight());

  // Osserva i cambi di layout: cambio pagina, dialoghi, font, ecc.
  if (typeof ResizeObserver !== "undefined") {
    const ro = new ResizeObserver(() => sendHeight());
    if (document.documentElement) ro.observe(document.documentElement);
    if (document.body) ro.observe(document.body);
    setTimeout(() => sendHeight(), 250);
  }

  // I font (OpenDyslexic) e i contenuti asincroni cambiano il layout dopo il
  // load: ricontrolliamo un paio di volte per mandare l'altezza definitiva.
  setTimeout(sendHeight, 500);
  setTimeout(sendHeight, 1500);
  if (typeof document.fonts !== "undefined") {
    document.fonts.ready.then(() => setTimeout(() => sendHeight(), 200)).catch(() => {});
  }
})();

createRoot(document.getElementById("root")!).render(<App />);
