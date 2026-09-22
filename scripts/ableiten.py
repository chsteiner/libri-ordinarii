"""Leitet aus den Cantus-TEIs die flache Schicht ab: eine Zeile je Incipit.

Schreibt derived/incipits.jsonl, derived/incipits-felder.md (was jedes Feld
bedeutet, samt Zaehlkonventionen) und derived/corpus-stats.md (Zahlen je
Handschrift, bei jedem Lauf neu gemessen). Alles unter derived/ ist erzeugt
und wird nicht von Hand geaendert.

Aufruf:  python scripts/ableiten.py [--tei-dir PFAD]
Default fuer --tei-dir ist ../cantus/TEIs, also ein Klon von
https://github.com/chsteiner/cantus neben diesem Repositorium.

Defensiv: eine Datei, die nicht auf _current_tei.xml endet, wird mit Namen
gemeldet und uebersprungen; ein Incipit ohne Fest oder ohne Hora wird gezaehlt
und im Bericht genannt; ein @n, das weder "CantusID <id>" noch eines der
bekannten Siglen-Muster ist, landet in n_roh und im Bericht. Null Incipits in
einer Datei sind ein harter Fehler.
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

from lxml import etree

sys.stdout.reconfigure(encoding="utf-8")
TEI = "{http://www.tei-c.org/ns/1.0}"
XMLID = "{http://www.w3.org/XML/1998/namespace}id"
# "CantusID 006583", auch "CantusID 006583 006584" (mehrere IDs, durch Leerzeichen
# getrennt). Schreibvarianten wie "CanutsID" oder "CantusiD" bleiben absichtlich
# in n_roh: das ist ein Befund ueber die Daten, keine Normalisierung.
CANTUS_ID = re.compile(r"^CantusID\s+(\S.*)$")
WS = re.compile(r"\s+")

HIER = Path(__file__).resolve().parent.parent
DERIVED = HIER / "derived"


def text_von(el):
    return WS.sub(" ", "".join(el.itertext())).strip()


def fest_von(seg):
    """Naechster Vorfahr-div mit einem head, das @corresp traegt."""
    for anc in seg.iterancestors(TEI + "div"):
        head = anc.find(TEI + "head")
        if head is not None and head.get("corresp"):
            return head.get("corresp").lstrip("#"), head.get(XMLID), text_von(head)
    return None, None, None


def hora_von(seg):
    """Naechster Vorfahr-div mit @type time:*; Hora aus dessen ab[@ana='#head']/label."""
    for anc in seg.iterancestors(TEI + "div"):
        typ = anc.get("type") or ""
        if typ.startswith("time"):
            label = anc.find(f"{TEI}ab[@ana='#head']/{TEI}label")
            if label is not None:
                return typ, label.get("n"), label.get(XMLID), text_von(label)
            return typ, None, None, None
    return None, None, None, None


def ableiten(datei):
    baum = etree.parse(str(datei))
    header = baum.find(TEI + "teiHeader")
    hs = header.get(XMLID) if header is not None else datei.stem
    kurz = baum.find(f".//{TEI}titleStmt/{TEI}title[@type='short']")
    kurz = text_von(kurz) if kurz is not None else hs
    body = baum.find(f".//{TEI}body")
    if body is None:
        sys.exit(f"FEHLER: {datei.name} hat keinen body")

    zeilen = []
    stat = Counter()
    ana_inventar = Counter()
    n_roh_inventar = Counter()
    seite = None
    lfd = 0
    for el in body.iter():
        if not isinstance(el.tag, str):
            continue
        if el.tag == TEI + "pb":
            seite = el.get("n")
            stat["seiten"] += 1
            continue
        if el.tag == TEI + "head" and el.get("corresp"):
            stat["feste"] += 1
            continue
        if el.tag == TEI + "div" and (el.get("type") or "").startswith("time"):
            stat["horen"] += 1
            continue
        if el.tag == TEI + "metamark":
            stat["varianten"] += 1
            continue
        if el.tag != TEI + "seg" or el.get("type") != "incipit":
            continue
        lfd += 1
        fest, fest_id, fest_head = fest_von(el)
        hora_typ, hora, hora_id, hora_text = hora_von(el)
        ana = (el.get("ana") or "").lstrip("#")
        n = el.get("n")
        cantus_id, n_roh = None, None
        if n:
            m = CANTUS_ID.match(n)
            if m:
                cantus_id = m.group(1).strip()
                stat["mehrere_cantus_ids"] += " " in cantus_id
            else:
                n_roh = n
                n_roh_inventar[n.split(" ")[0]] += 1
        supplied = el.get("subtype") == "supplied"
        # Incipits im Kommentarteil eines Fests tragen ".comment." in der xml:id
        # und stehen in keinem div type="time:*"; sie sind keine Fehlstellen.
        kommentar = ".comment." in (el.get(XMLID) or "")
        varianten = sum(1 for _ in el.iter(TEI + "metamark"))
        neume = el.find(f".//{TEI}phr[@type='neume']") is not None
        ana_inventar[ana or "(ohne)"] += 1
        stat["incipits"] += 1
        stat["supplied"] += supplied
        stat["mit_cantus_id"] += cantus_id is not None
        stat["mit_n_roh"] += n_roh is not None
        stat["ohne_fest"] += fest is None
        stat["ohne_hora"] += hora is None
        stat["kommentar"] += kommentar
        stat["ohne_hora_kein_kommentar"] += (hora is None and not kommentar)
        stat["mit_variante"] += varianten > 0
        stat["mit_neume"] += neume
        zeilen.append({
            "handschrift": hs,
            "kurztitel": kurz,
            "datei": datei.name,
            "lfd": lfd,
            "incipit_id": el.get(XMLID),
            "fest": fest,
            "fest_id": fest_id,
            "hora": hora,
            "hora_id": hora_id,
            "hora_text": hora_text,
            "hora_typ": hora_typ,
            "gattung": ana or None,
            "cantus_id": cantus_id,
            "n_roh": n_roh,
            "konkordanz": el.get("corresp"),
            "supplied": supplied,
            "kommentar": kommentar,
            "varianten": varianten,
            "neume": neume,
            "seite": seite,
            "text": text_von(el),
        })
    if stat["incipits"] == 0:
        sys.exit(f"FEHLER: {datei.name}: 0 Incipits, das Muster passt nicht")
    return hs, kurz, zeilen, stat, ana_inventar, n_roh_inventar


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tei-dir", default=str(HIER.parent / "cantus" / "TEIs"))
    args = ap.parse_args()
    tei_dir = Path(args.tei_dir)
    if not tei_dir.is_dir():
        sys.exit(f"FEHLER: {tei_dir} ist kein Verzeichnis (Klon von chsteiner/cantus fehlt?)")
    alle = sorted(tei_dir.glob("*.xml"))
    dateien = [d for d in alle if d.name.endswith("_current_tei.xml")]
    uebersprungen = [d.name for d in alle if d not in dateien]
    if not dateien:
        sys.exit(f"FEHLER: keine *_current_tei.xml in {tei_dir}")

    DERIVED.mkdir(exist_ok=True)
    zeilen_gesamt = []
    stats = {}
    ana_gesamt = Counter()
    n_roh_gesamt = Counter()
    for d in dateien:
        hs, kurz, zeilen, stat, ana_inv, n_roh_inv = ableiten(d)
        zeilen_gesamt.extend(zeilen)
        stats[hs] = (kurz, d.name, stat)
        ana_gesamt.update(ana_inv)
        n_roh_gesamt.update(n_roh_inv)
        print(f"{d.name}: {stat['incipits']} Incipits ({stat['supplied']} supplied, "
              f"{stat['mit_cantus_id']} mit CantusID), {stat['feste']} Feste, "
              f"{stat['horen']} Horen, {stat['varianten']} Varianten"
              + f", {stat['kommentar']} im Kommentar"
              + (f", {stat['ohne_fest']} ohne Fest" if stat["ohne_fest"] else "")
              + (f", {stat['ohne_hora_kein_kommentar']} ohne Hora und kein Kommentar"
                 if stat["ohne_hora_kein_kommentar"] else ""))

    with open(DERIVED / "incipits.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for z in zeilen_gesamt:
            f.write(json.dumps(z, ensure_ascii=False) + "\n")

    summe = Counter()
    for _, (_, _, s) in stats.items():
        summe.update(s)
    n_hs = len(stats)

    # corpus-stats.md
    # Das Messdatum gehoert in die Datei: eine Zahl ist am Tag ihrer Messung
    # richtig (CLAUDE.md, Regel 5). Die Quelle relativ zum Elternordner, damit
    # kein Pfad eines einzelnen Arbeitsplatzes in das Repositorium wandert.
    try:
        quelle = "../" + tei_dir.resolve().relative_to(HIER.parent).as_posix()
    except ValueError:
        quelle = tei_dir.as_posix()
    gemessen = datetime.now().strftime("%d.%m.%Y, %H:%M")
    k = ["# Der Bestand in Zahlen", "",
         "Erzeugt von `scripts/ableiten.py`, bei jedem Lauf neu gemessen. Nicht von",
         "Hand aendern. Quelle: die `*_current_tei.xml` unter `--tei-dir`.", "",
         f"Gemessen am {gemessen} Uhr aus `{quelle}`: {len(dateien)} Dateien "
         f"`*_current_tei.xml`.", "",
         f"**{n_hs} Handschriften** (Dateien, die auf `_current_tei.xml` enden; "
         f"{len(uebersprungen)} andere Dateien im Ordner uebersprungen: "
         + (", ".join(f"`{u}`" for u in uebersprungen) or "keine") + ").", "",
         f"**{summe['incipits']} Incipits** in allen {n_hs} Handschriften, davon "
         f"{summe['supplied']} `supplied` (vom Bearbeiter ergaenzt) und "
         f"{summe['incipits'] - summe['supplied']} im Original; "
         f"{summe['mit_cantus_id']} tragen eine Cantus-ID, {summe['mit_n_roh']} eine andere "
         f"Sigle in `@n`, {summe['incipits'] - summe['mit_cantus_id'] - summe['mit_n_roh']} keine. "
         f"{summe['mit_variante']} Incipits enthalten mindestens eine Variantenmarke; "
         f"{summe['mehrere_cantus_ids']} tragen mehr als eine Cantus-ID in einem `@n`.", "",
         "| Handschrift | Datei | Feste | Horen | Incipits | davon supplied | mit Cantus-ID | Varianten (ganze Datei) | Seiten |",
         "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for hs, (kurz, datei, s) in sorted(stats.items()):
        k.append(f"| {kurz} (`{hs}`) | `{datei}` | {s['feste']} | {s['horen']} | {s['incipits']} | "
                 f"{s['supplied']} | {s['mit_cantus_id']} | {s['varianten']} | {s['seiten']} |")
    k.append(f"| **zusammen** | {n_hs} Dateien | {summe['feste']} | {summe['horen']} | "
             f"{summe['incipits']} | {summe['supplied']} | {summe['mit_cantus_id']} | "
             f"{summe['varianten']} | {summe['seiten']} |")
    k += ["", "## Gattungen (`@ana` der Incipits, ueber alle Handschriften)", "",
          "| Gattung | Incipits |", "|---|---:|"]
    for g, n in ana_gesamt.most_common():
        k.append(f"| {g} | {n} |")
    k += ["", "## Andere Siglen in `@n` (erstes Wort), nicht als Cantus-ID gezaehlt", ""]
    if n_roh_gesamt:
        k += ["| Sigle | Incipits |", "|---|---:|"]
        for g, n in n_roh_gesamt.most_common():
            k.append(f"| {g} | {n} |")
    else:
        k.append("keine")
    k += ["", "## Incipits ausserhalb einer Hora", "",
          f"{summe['kommentar']} Incipits stehen im Kommentarteil eines Fests (`.comment.` in der "
          f"`xml:id`, kein `div type=\"time:*\"` als Vorfahr); das ist Struktur, keine Fehlstelle. "
          f"Dazu {summe['ohne_hora_kein_kommentar']} Incipits ohne Hora, die **nicht** Kommentar sind, "
          f"und {summe['ohne_fest']} ohne zuordenbares Fest (`head` ohne `@corresp` oder kein "
          "`head`). Beide Reste stehen in `docs/OFFENE-FRAGEN.md`; in `incipits.jsonl` haben "
          "sie ein leeres Feld.", ""]
    (DERIVED / "corpus-stats.md").write_text("\n".join(k), encoding="utf-8", newline="\n")

    # incipits-felder.md
    felder = [
        "# Felder von `incipits.jsonl`", "",
        "Eine Zeile je `seg type=\"incipit\"` in Dokumentreihenfolge, erzeugt von",
        "`scripts/ableiten.py`. Nicht von Hand aendern.", "",
        "| Feld | Herkunft im TEI | Bedeutung |", "|---|---|---|",
        "| `handschrift` | `teiHeader/@xml:id` | Kennung der Handschrift, z. B. `brixen` |",
        "| `kurztitel` | `titleStmt/title[@type='short']` | Kurzname |",
        "| `datei` | Dateiname | Quelle der Zeile |",
        "| `lfd` | gezaehlt | laufende Nummer des Incipits in der Datei, ab 1 |",
        "| `incipit_id` | `seg/@xml:id` | z. B. `incipit.01011000.V.9` |",
        "| `fest` | `head/@corresp` des naechsten Fest-`div` | Feastcode, z. B. `01011000` |",
        "| `fest_id` | `head/@xml:id` | |",
        "| `hora` | `label/@n` im `ab[@ana='#head']` des `div[@type='time:*']` | Horen-Sigle, z. B. `V` |",
        "| `hora_id`, `hora_text` | `label/@xml:id`, Labeltext | z. B. `Ad vesperam` |",
        "| `hora_typ` | `div/@type` | `time:1` oder `time:2` |",
        "| `gattung` | `seg/@ana` ohne `#` | Gattungssigle, z. B. `RP`, `AN`, `HY` |",
        "| `cantus_id` | `seg/@n`, wenn es mit `CantusID ` beginnt | die Cantus-ID; bei mehreren IDs alle, durch Leerzeichen getrennt |",
        "| `n_roh` | `seg/@n` sonst | andere Sigle, z. B. `AH 2-18` |",
        "| `konkordanz` | `seg/@corresp` | Konkordanzen, roh |",
        "| `supplied` | `seg/@subtype='supplied'` | vom Bearbeiter ergaenzt, nicht im Original |",
        "| `kommentar` | `.comment.` in `seg/@xml:id` | Incipit im Kommentarteil des Fests, nicht in einer Hora |",
        "| `varianten` | Zahl der `metamark[@function='variant']` im `seg` | |",
        "| `neume` | `phr[@type='neume']` im `seg` vorhanden | |",
        "| `seite` | letztes `pb/@n` vor dem `seg` | Folio |",
        "| `text` | Textinhalt des `seg`, Leerraum normalisiert | einschliesslich des Texts in Variantenmarken |",
        "", "## Zaehlkonventionen", "",
        "Dieselbe Frage hat je nach Konvention verschiedene Antworten. Wer eine Zahl nennt,",
        "nennt die Konvention dazu.", "",
        "- **Incipits** zaehlt jedes `seg type=\"incipit\"`, auch `supplied`. Wer nur den",
        "  Originalbestand will, zieht `supplied` ab; beide Zahlen stehen in `corpus-stats.md`.",
        "- **Mit Cantus-ID** zaehlt nur `@n` der Form `CantusID <id>`. Andere Siglen",
        "  (`AH`, `CAO` usw.) sind Belege, aber keine Cantus-ID.",
        "- **Varianten** zaehlt `metamark`-Elemente, nicht Lesarten: eine Marke kann",
        "  mehrere Zeugen buendeln. `varianten` je Zeile zaehlt nur die Marken innerhalb",
        "  des Incipits; die Spalte in `corpus-stats.md` zaehlt die ganze Datei.",
        "- **Feste** zaehlt `head` mit `@corresp`; ein Fest mit zwei `head` zaehlt zweimal.",
        "- **Horen** zaehlt `div` mit `@type`, das mit `time` beginnt.",
        "- **Handschriften** zaehlt Dateien mit der Endung `_current_tei.xml`, nicht",
        "  Ueberlieferungstraeger: `salzburg_sal`, `salzburg_ur`, `salzburg_ra`, `salzburg_vo`",
        "  sind vier Dateien einer Tradition.", ""]
    (DERIVED / "incipits-felder.md").write_text("\n".join(felder), encoding="utf-8", newline="\n")

    print(f"\n{summe['incipits']} Zeilen nach derived/incipits.jsonl aus {n_hs} Dateien "
          f"({len(uebersprungen)} uebersprungen: {', '.join(uebersprungen) or 'keine'})")
    print(f"Gattungen: {len(ana_gesamt)} verschiedene; andere Siglen in @n: {dict(n_roh_gesamt)}")
    print(f"ohne Fest: {summe['ohne_fest']}, ohne Hora: {summe['ohne_hora']}")


if __name__ == "__main__":
    main()
