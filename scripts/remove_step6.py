#!/usr/bin/env python3
"""Rimuove il blocco 'Step 6: Extract x from t' (non serve per k=1, x = t)."""

path = "/home/user/equazioni-secondo-grado/client/src/pages/BiquadraticExercises.tsx"

with open(path, "r", encoding="utf-8") as f:
    testo = f.read()

start_marker = "      {/* Step 6: Extract x from t */}"
end_marker = "      {/* Step 7 (or 6 when \u0394=0): Verification */}"

i = testo.find(start_marker)
j = testo.find(end_marker)

if i == -1 or j == -1 or j <= i:
    print(f"[ERRORE] marker non trovati: i={i}, j={j}")
    raise SystemExit(1)

rimosso = testo[i:j]
testo = testo[:i] + testo[j:]
with open(path, "w", encoding="utf-8") as f:
    f.write(testo)

print(f"[OK] Rimosso blocco Step 6 ({len(rimosso)} caratteri)")
