"""Elementinventar eines oder mehrerer TEI-Files: je Element die Zahl der
Vorkommen und die Attribute daran, mit Haeufigkeit. Fremde Namespaces werden
gemeldet, nicht uebergangen. Das ist das Werkzeug, mit dem docs/DATA-MODEL.md
gemessen wurde; wer eine Aussage ueber das Modell macht, misst sie hier nach.

Aufruf: python scripts/inventar.py ../cantus/TEIs/brixen_current_tei.xml [...]
"""
import sys
from collections import Counter, defaultdict
from pathlib import Path

from lxml import etree

sys.stdout.reconfigure(encoding="utf-8")
TEI = "http://www.tei-c.org/ns/1.0"
if len(sys.argv) < 2:
    sys.exit("Aufruf: inventar.py DATEI [DATEI...]")
for pfad in sys.argv[1:]:
    baum = etree.parse(pfad)
    elemente = Counter()
    attribute = defaultdict(Counter)
    fremd = Counter()
    for el in baum.iter():
        if not isinstance(el.tag, str):
            continue
        ns, _, name = el.tag[1:].partition("}") if el.tag.startswith("{") else ("", "", el.tag)
        if ns != TEI:
            fremd[ns or "(kein Namespace)"] += 1
            continue
        elemente[name] += 1
        for a in el.attrib:
            attribute[name][a.replace("{http://www.w3.org/XML/1998/namespace}", "xml:")] += 1
    gesamt = sum(elemente.values())
    print(f"=== {Path(pfad).name}: {gesamt} TEI-Elemente, {len(elemente)} Elementnamen ===")
    for name, n in elemente.most_common():
        attrs = ", ".join(f"@{a} x{c}" for a, c in attribute[name].most_common())
        print(f"  {name:20} {n:7}  {attrs}")
    if fremd:
        print("  Fremde Namespaces:", dict(fremd))
    if gesamt == 0:
        sys.exit(f"FEHLER: {pfad}: keine TEI-Elemente gefunden")
