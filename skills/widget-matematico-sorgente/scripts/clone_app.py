#!/usr/bin/env python3
"""
clone_app.py — Clona l'app EQUAZIONI DI SECONDO GRADO (equazioni-secondo-grado)
in una NUOVA app identica cambiando SOLO il grado dell'equazione.

L'app sorgente risolve equazioni quadratiche  a·x² + b·x + c = 0  (grado 2, k = 1),
in 5 passi, senza sostituzione. Da questa base si possono generare le trinomie
di grado superiore (che richiedono sostituzione t = x^k ed estrazione radice).

Grado → k:  2→1 (quadratica, sorgente), 4→2 (biquadratica), 6→3 (bicubica), 8→4, ...

USO:
  python3 clone_app.py --name "equazioni-sesto-grado" --degree 6
  python3 clone_app.py --source /home/user/equazioni-secondo-grado \
                       --name "mio-widget" --degree 4
  python3 clone_app.py --source https://github.com/utente/repo.git \
                       --name "mio-widget" --degree 6

ATTENZIONE: questo script esegue le sostituzioni MECCANICHE (potenze, titoli,
placeholder, testo della sostituzione). NON modifica la logica matematica dei passi
(sostituzione t = x^k per k≥2, estrazione radice). Al termine stampa una CHECKLIST
dei passi manuali rimasti — leggerla e completarli prima del build. Per i dettagli
vedere docs/grado.md.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys

SORGENTE_DEFAULT = "/home/user/equazioni-secondo-grado"

# Nome italiano del grado per i titoli
GRADO_NOME = {
    2: "SECONDO",
    4: "QUARTO",
    6: "SESTO",
    8: "OTTAVO",
    10: "DECIMO",
    12: "DODICESIMO",
}

# Nome della "trinomia" per il grado (solo per gradi ≥ 4 pari)
TRINOMIA_NOME = {
    4: "TRINOMIE BIQUADRATICHE",
    6: "TRINOMIE BICUBICHE",
    8: "TRINOMIE BIOCTICHE",
}

SUPERSCRIPT = {
    "0": "\u2070", "1": "\u00B9", "2": "\u00B2", "3": "\u00B3", "4": "\u2074",
    "5": "\u2075", "6": "\u2076", "7": "\u2077", "8": "\u2078", "9": "\u2079",
}


def sup(n: int) -> str:
    return "".join(SUPERSCRIPT[d] for d in str(n))


def copia_sorgente(source: str, dest: str) -> None:
    """Copia la sorgente (cartella locale o repo git) in dest."""
    if os.path.isdir(source):
        if os.path.exists(dest):
            print(f"[ERRORE] La destinazione esiste già: {dest}")
            sys.exit(1)
        shutil.copytree(
            source, dest,
            ignore=shutil.ignore_patterns(
                "node_modules", "dist", ".git", "dev-server.log",
                "__pycache__", "*.zip",
            ),
        )
        print(f"[OK] Cartella copiata da {source} → {dest}")
    else:
        # Assumiamo sia un URL git
        subprocess.run(
            ["git", "clone", source, dest], check=True,
        )
        print(f"[OK] Repo clonato da {source} → {dest}")


def trova_root_app(base: str) -> str:
    """Trova la cartella contenente package.json (a base o un livello sotto).

    Utile quando il repo GitHub ha l'app in una subfolder invece della root.
    """
    if os.path.isfile(os.path.join(base, "package.json")):
        return base
    try:
        entries = os.listdir(base)
    except OSError:
        return base
    for d in sorted(entries):
        full = os.path.join(base, d)
        if os.path.isdir(full) and os.path.isfile(os.path.join(full, "package.json")):
            return full
    return base


def build_replacements(k: int) -> list[tuple[str, str]]:
    """Restituisce le coppie (vecchio, nuovo) ordinate dalla più specifica.

    La sorgente è grado 2 (k=1): potenza a = x^{2}, potenza b = x (implicita) o
    x^{1}. L'ordine conta: i token lunghi vanno prima dei corti, e MAI fare
    replace di cifre singole '2'/'1' (romperebbe 2a, 4ac, ecc.).
    """
    deg = 2 * k
    d2 = str(deg)          # es. "6" per k=3
    kstr = str(k)          # es. "3" per k=3
    sup_deg = sup(deg)     # es. "⁶"
    sup_k = sup(k)         # es. "³"

    r = []

    # 1) Parser — include() sulle potenze (case x e X, con/senza braccia, unicode)
    for base in ("x", "X"):
        r.append((f"{base}^{{2}}", f"{base}^{{{d2}}}"))
        r.append((f"{base}^{{1}}", f"{base}^{{{kstr}}}"))
        r.append((f"{base}^2", f"{base}^{{{d2}}}"))
        r.append((f"{base}^1", f"{base}^{{{kstr}}}"))
        r.append((f"{base}\u00B2", f"{base}{sup_deg}"))
        r.append((f"{base}\u00B9", f"{base}{sup_k}"))

    # 2) Parser — power = 2 / power = 1 (assegnazione esplicita)
    r.append(("power = 2", f"power = {deg}"))
    r.append(("power = 1", f"power = {k}"))

    # 3) Parser — flag foundX2 / foundX1
    r.append(("foundX2", f"foundX{deg}"))
    r.append(("foundX1", f"foundX{k}"))

    # 4) Parser — regex di pulizia coefficiente
    r.append((r"[xX]\^\{2\}", rf"[xX]\^{{{d2}}}]"))
    r.append((r"[xX]\^\{1\}", rf"[xX]\^{{{kstr}}}]"))
    r.append((r"[xX]\^2", rf"[xX]\^{{{d2}}}"))
    r.append((r"[xX]\^1", rf"[xX]\^{{{kstr}}}"))
    r.append(("[xX]\u00B2", f"[xX]{sup_deg}"))
    r.append(("[xX]\u00B9", f"[xX]{sup_k}"))

    # 5) builder equazione — "x^{2}" (potenza a) e "x" nuda (potenza b)
    r.append(('"x^{2}"', f'"x^{{{d2}}}"'))
    # La "x" nuda del builder (potenza b) va gestita solo nei punti esatti:
    # il replace globale di "x" è pericoloso, lo fa la checklist manuale.

    # 6) Testo della sostituzione (per k≥2: il sorgente k=1 NON ha sostituzione)
    #    Il testo "t = x" (potenza 1) del sorgente va aggiornato solo se presente.
    r.append(("t = x\u00B9", f"t = x{sup_k}"))
    r.append(("t = x^{1}", f"t = x^{{{kstr}}}"))

    # 7) Titoli (header, WelcomePage)
    nome_grado = GRADO_NOME.get(deg, f"DI GRADO {deg}")
    r.append(("EQUAZIONI DI SECONDO GRADO", f"EQUAZIONI DI {nome_grado} GRADO"))
    if deg in TRINOMIA_NOME:
        r.append(("TRINOMIE BIQUADRATICHE", TRINOMIA_NOME[deg]))

    # 8) Hint e placeholder (esempio di equazione)
    r.append(("2x\u00B2\u22123x+1=0", f"2x{sup_deg}\u22123x{sup_k}+1=0"))
    r.append(("es. 2x^{2}-3x+1=0", f"es. 2x^{{{d2}}}-3x^{{{kstr}}}+1=0"))

    # 9) Numero di passi visibile (sorgente: 5 PASSI; con sostituzione+radice → 7)
    if k >= 2:
        r.append(("5 PASSI", "7 PASSI"))

    return r


def applica_sostituzioni(root: str, k: int) -> int:
    """Applica le sostituzioni ai file sorgente. Ritorna il numero di file toccati."""
    sost = build_replacements(k)
    target_ext = (".tsx", ".ts", ".html", ".md")
    count = 0

    for dirpath, _dirs, files in os.walk(root):
        if "node_modules" in dirpath or "dist" in dirpath or ".git" in dirpath:
            continue
        for fname in files:
            if not fname.endswith(target_ext):
                continue
            path = os.path.join(dirpath, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    testo = f.read()
            except UnicodeDecodeError:
                continue
            originale = testo
            for vecchio, nuovo in sost:
                testo = testo.replace(vecchio, nuovo)
            if testo != originale:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(testo)
                count += 1
    return count


def checklist_manuale(k: int, deg: int) -> str:
    """Restituisce la checklist dei passi manuali che lo script NON esegue."""
    kstr = str(k)
    righe = []

    if k == 1:
        righe += [
            "k=1 (grado 2, quadratica): è il sorgente — nessuna sostituzione, 5 passi.",
            "  - Nessuna modifica alla logica dei passi.",
        ]

    if k >= 2:
        righe += [
            f"AGGIUNGERE la VARIABILE AUSILIARIA (passo 2): t = x^{k}.",
            "  - Il sorgente k=1 NON ha la sostituzione: va aggiunto un passo che",
            "    mostra 't = x^{k}', 'x^{k} = t' e calcola il delta sulla quadratica in t.",
            f"AGGIUNGERE il PASSO di ESTRAZIONE radice (da t a x):",
            "  - k pari:  x = ±(t)^(1/k) → '\\pm\\sqrt[k]{t}' e Math.pow(t, 1/k).",
            "  - k dispari: x = (t)^(1/k) → '\\sqrt[k]{t}' e Math.pow(t, 1/k) (senza ±).",
            "  - Nel builder lato destro: la potenza b del sorgente è 'x' NUDO;",
            "    sostituire MANUALMENTE la riga del builder  result += ... + \"x\"  con",
            f"    \"x^{{{k}}}\" (o \"x^{{{kstr}}}\" nei formati espliciti).",
        ]

    righe += [
        "",
        "VERIFICA GENERALE:",
        "  - pnpm check  (TypeScript deve passare)",
        "  - Cercare residui '2'/'1' come potenze: grep -rn 'x^{2}\\|x^{1}\\|x²\\|x¹' client/src",
        "  - Aggiornare il titolo <h1> e WelcomePage se il nome 'TRINOMIA' non è corretto.",
        "  - Rinominare componenti/interface se serve coerenza (QuadraticExercises → Esercizi, ecc.).",
    ]
    return "\n".join(righe)


def main() -> None:
    p = argparse.ArgumentParser(description="Clona EQUAZIONI DI SECONDO GRADO con grado diverso")
    p.add_argument("--source", default=SORGENTE_DEFAULT,
                   help="Cartella locale o URL git della sorgente (default: %(default)s)")
    p.add_argument("--name", required=True,
                   help="Nome della nuova cartella/app (senza spazi, es. equazioni-sesto-grado)")
    p.add_argument("--degree", required=True, type=int,
                   help="Grado dell'equazione (pari, >= 2): 2, 4, 6, 8...")
    p.add_argument("--dest", default=None,
                   help="Percorso destinazione (default: /home/user/<name>)")
    args = p.parse_args()

    if args.degree < 2 or args.degree % 2 != 0:
        print("[ERRORE] Il grado deve essere un numero pari >= 2 (2, 4, 6, 8...).")
        sys.exit(1)

    k = args.degree // 2
    dest = args.dest or f"/home/user/{args.name}"

    print(f"[INFO] Clono con grado {args.degree} → k = {k} (t = x^{k})")
    copia_sorgente(args.source, dest)

    root = trova_root_app(dest)
    if root != dest:
        print(f"[INFO] App trovata in subfolder: {os.path.relpath(root, dest)}")
    else:
        print(f"[INFO] App trovata alla root del repository/percorso.")

    n = applica_sostituzioni(root, k)
    print(f"[OK] Sostituzioni applicate a {n} file.")

    print("\n" + "=" * 70)
    print("CHECKLIST PASSI MANUALI (leggerla e completarla PRIMA del build)")
    print("=" * 70)
    print(checklist_manuale(k, args.degree))
    print("=" * 70)
    print(f"\n[FATTO] App clonata in {dest}")
    print("Prossimi comandi:")
    print(f"  cd {dest} && pnpm install && pnpm check && pnpm dev")


if __name__ == "__main__":
    main()
