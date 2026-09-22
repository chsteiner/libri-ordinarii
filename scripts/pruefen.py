"""Prueft derived/ gegen die Konventionen. Laeuft ohne Modell und ohne Netz.

Harte Verstoesse (Exit 1):
  - derived/incipits.jsonl fehlt oder ist leer
  - eine incipit_id kommt in derselben Datei zweimal vor
  - eine Zeile hat nicht genau die Felder aus incipits-felder.md
  - data/vermerke.jsonl (falls vorhanden) hat einen Vermerk mit Status
    "geprueft" ohne geprueft_von und geprueft_am

Befunde (gemeldet, kein Exit 1), je mit Menge in derselben Zeile:
  - cantus_id, die nicht dem Muster einer Cantus-ID entspricht
  - Hora-Siglen ausserhalb der Menge, die im Bestand mehr als zehnmal vorkommt
  - Incipits ohne Hora, die kein Kommentar sind
  - n_roh-Werte, die wie eine verschriebene Cantus-ID aussehen

Ausserdem rendert es data/vermerke.jsonl nach derived/vermerke.md, falls die
Datei existiert. Die letzte Ausgabezeile ist das Ergebnis und gehoert
unveraendert in den PR.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HIER = Path(__file__).resolve().parent.parent
JSONL = HIER / "derived" / "incipits.jsonl"
VERMERKE = HIER / "data" / "vermerke.jsonl"
VERMERKE_MD = HIER / "derived" / "vermerke.md"

FELDER = ["handschrift", "kurztitel", "datei", "lfd", "incipit_id", "fest", "fest_id",
          "hora", "hora_id", "hora_text", "hora_typ", "gattung", "cantus_id", "n_roh",
          "konkordanz", "supplied", "kommentar", "varianten", "neume", "seite", "text"]
# Cantus-ID: sechs Ziffern, optional Buchstabe oder Suffix; dazu die Formen
# g01573a (Genre-IDs) und can9000. Alles andere ist ein Befund, kein Fehler.
CANTUS_ID = re.compile(r"^(\d{6}[a-z]?|\d{6}-\d{6}(/[a-z]\d+)?|g\d{5}[a-z]?|can\d{4}|[a-z]\d{5})$")
VERSCHRIEBEN = re.compile(r"^(cantusid|canutsid|caantusid|cantusi|chantid)", re.I)
VERMERK_STATUS = {"vorgeschlagen", "geprueft", "verworfen", "weitergegeben"}

hart = 0
befunde = 0

if not JSONL.exists():
    sys.exit(f"HART: {JSONL} fehlt, erst scripts/ableiten.py laufen lassen")

zeilen = []
with open(JSONL, encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        z = json.loads(line)
        if list(z.keys()) != FELDER:
            print(f"HART: Zeile {i}: Felder {list(z.keys())} statt {FELDER}")
            hart += 1
            break
        zeilen.append(z)
if not zeilen:
    sys.exit("HART: incipits.jsonl ist leer")

# Eindeutigkeit der xml:id je Datei
ids = defaultdict(Counter)
for z in zeilen:
    if z["incipit_id"]:
        ids[z["datei"]][z["incipit_id"]] += 1
doppelt = {d: [k for k, n in c.items() if n > 1] for d, c in ids.items()}
doppelt = {d: v for d, v in doppelt.items() if v}
if doppelt:
    for d, v in doppelt.items():
        print(f"HART: {d}: {len(v)} incipit_id mehrfach, z. B. {v[:3]}")
        hart += 1
ohne_id = sum(1 for z in zeilen if not z["incipit_id"])
print(f"Eindeutigkeit: {sum(len(c) for c in ids.values())} verschiedene incipit_id in "
      f"{len(ids)} Dateien, {ohne_id} Incipits ohne xml:id"
      + (f", davon in {Counter(z['datei'] for z in zeilen if not z['incipit_id'])}" if ohne_id else ""))

# Cantus-ID-Muster
mit_id = [z for z in zeilen if z["cantus_id"]]
schief = [z for z in mit_id if not all(CANTUS_ID.match(t) for t in z["cantus_id"].split())]
print(f"Cantus-IDs: {len(mit_id)} Incipits mit cantus_id, davon {len(schief)} ausserhalb des "
      f"Musters (Befund)")
if schief:
    befunde += 1
    for w, n in Counter(z["cantus_id"] for z in schief).most_common(8):
        print(f"    {n:5}  {w!r}")

# verschriebene CantusID in n_roh
verschr = Counter(z["n_roh"] for z in zeilen if z["n_roh"] and VERSCHRIEBEN.match(z["n_roh"]))
print(f"n_roh: {sum(1 for z in zeilen if z['n_roh'])} Incipits mit anderer Sigle, davon "
      f"{sum(verschr.values())} wie eine verschriebene Cantus-ID (Befund): "
      + (", ".join(f"{w!r}x{n}" for w, n in verschr.most_common()) or "keine"))
befunde += bool(verschr)

# Hora-Siglen
horen = Counter(z["hora"] for z in zeilen if z["hora"])
haeufig = {h for h, n in horen.items() if n > 10}
selten = {h: n for h, n in horen.items() if n <= 10}
print(f"Horen: {len(horen)} Siglen, {len(haeufig)} davon mehr als zehnmal "
      f"({', '.join(sorted(haeufig))}); selten (Befund): {selten or 'keine'}")
befunde += bool(selten)

# Reste ohne Hora
rest = [z for z in zeilen if z["hora"] is None and not z["kommentar"]]
print(f"Ohne Hora und kein Kommentar: {len(rest)} von {len(zeilen)} Incipits (Befund), in "
      f"{dict(Counter(z['datei'] for z in rest))}")
befunde += bool(rest)

# Vermerke
if VERMERKE.exists():
    vermerke = [json.loads(l) for l in open(VERMERKE, encoding="utf-8") if l.strip()]
    for v in vermerke:
        if v.get("status") not in VERMERK_STATUS:
            print(f"HART: Vermerk {v.get('id')}: Status {v.get('status')!r} nicht in {sorted(VERMERK_STATUS)}")
            hart += 1
        if v.get("status") == "geprueft" and not (v.get("geprueft_von") and v.get("geprueft_am")):
            print(f"HART: Vermerk {v.get('id')}: geprueft ohne geprueft_von/geprueft_am")
            hart += 1
    md = ["# Vermerke", "", "Erzeugt von `scripts/pruefen.py` aus `data/vermerke.jsonl`. Nicht von Hand aendern.",
          "", f"{len(vermerke)} Vermerke, nach Status: "
          + ", ".join(f"{s} {n}" for s, n in Counter(v.get('status') for v in vermerke).most_common()), "",
          "| Nr. | Datum | Datei | Stelle | Sachverhalt | Vorschlag | Von | Status | Geprueft |",
          "|---|---|---|---|---|---|---|---|---|"]
    for v in vermerke:
        gepr = f"{v.get('geprueft_von', '')} {v.get('geprueft_am', '')}".strip()
        md.append(f"| {v.get('id')} | {v.get('datum')} | `{v.get('datei')}` | `{v.get('stelle')}` | "
                  f"{v.get('sachverhalt')} | {v.get('vorschlag')} | {v.get('von')} | {v.get('status')} | {gepr} |")
    VERMERKE_MD.write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
    print(f"Vermerke: {len(vermerke)} nach derived/vermerke.md")
else:
    print("Vermerke: data/vermerke.jsonl fehlt, nichts gerendert")

print(f"ERGEBNIS: {'ROT' if hart else 'GRUEN'}, {hart} harte Verstoesse, {befunde} Befundklassen, "
      f"{len(zeilen)} Zeilen geprueft")
sys.exit(1 if hart else 0)
