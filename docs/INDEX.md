# Libri ordinarii: die Wissensbasis

Libri ordinarii der Salzburger Kirchenprovinz aus dem Projekt Cantus Network
(2014 bis 2023), TEI-kodiert, mit Incipits, Cantus-IDs und Variantenapparat.
Dieses Repositorium ist die **Arbeitsschicht** darüber: was ein Team und seine
Agenten wissen müssen, um an den Daten weiterzuarbeiten, ohne die Edition in
GAMS zu verändern.

## Wo anfangen

| Wenn du ... | dann nimm |
|---|---|
| mit den Incipits arbeiten willst | `derived/incipits.jsonl`, eine flache Zeile je Incipit; liegt nicht im Repositorium, sondern kommt aus `python scripts/ableiten.py`. Was jedes Feld bedeutet: [`derived/incipits-felder.md`](../derived/incipits-felder.md) |
| eine Zahl nennen willst | [`derived/incipits-felder.md`](../derived/incipits-felder.md) → Zählkonventionen. Dieselbe Frage hat je nach Konvention verschiedene Antworten |
| wissen willst, was im Bestand steckt | [`derived/corpus-stats.md`](../derived/corpus-stats.md), bei jedem Lauf neu gemessen |
| das TEI verstehen willst | [DATA-MODEL.md](DATA-MODEL.md); daneben `Cantus-Dokumentation.pdf` im Quellrepositorium für den Word-Workflow von 2014 |
| wissen willst, was zu tun ist | die Issues, solange es sie nicht gibt [ANFORDERUNGEN.md](ANFORDERUNGEN.md): die Anforderungen als Issue-Entwürfe mit Autonomiestufe |
| wissen willst, was ein Sprachmodell an den Daten vorgeschlagen hat und wer es geprüft hat | [MASCHINELLE-EDITORIK.md](MASCHINELLE-EDITORIK.md), der Prüfstand in `derived/vermerke.md` |
| über eine Angabe stolperst, die niemand mehr erklären kann | [OFFENE-FRAGEN.md](OFFENE-FRAGEN.md) |
| wissen willst, warum etwas so ist und nicht anders | [DECISIONS.md](DECISIONS.md): die Entscheidungen mit Kontext, verworfenen Alternativen, Folgen und dem, der entschieden hat |
| eine autonome Session starten willst | [`playbooks/`](../playbooks/), zuerst den Betriebsvertrag |
| wissen willst, wo die letzte Session aufgehört hat | [`journal.md`](../journal.md), letzter Eintrag |
| wissen willst, welche Fehler hier schon zweimal passiert sind | [`fehlerjournal.md`](../fehlerjournal.md) |

**Wo geändert werden darf.** Frei zum Ändern sind `docs/`, `scripts/`,
`playbooks/`, `data/vermerke.jsonl` und die beiden Journale. **Nicht** geändert
wird `derived/` (erzeugt, jede Änderung ist beim nächsten Lauf weg) und
`../cantus/` (fremdes Repositorium, die Quelle). Nach einer Änderung an
`scripts/` oder `data/` läuft die Kette aus [`AGENTS.md`](../AGENTS.md),
Abschnitt »Reihenfolge nach einer Datenänderung«, vollständig.

## Der Bestand in Zahlen

Steht bewusst nicht hier, sondern in
[`derived/corpus-stats.md`](../derived/corpus-stats.md), weil sich jede Zahl
mit dem nächsten Lauf ändern kann und eine Zahl in Prosa niemand mitzieht.
Wer eine braucht, misst sie dort und nennt die Konvention dazu.

## Die Dokumente

| Dokument | Funktion | Wer liest es |
|---|---|---|
| [INDEX.md](INDEX.md) | Navigation | jede Session zuerst |
| [DATA-MODEL.md](DATA-MODEL.md) | Material: das TEI, seine IDs, seine Eigenheiten | wer Skripte schreibt oder Zahlen nennt |
| [ANFORDERUNGEN.md](ANFORDERUNGEN.md) | Substanz: was gebaut werden soll, als Issues mit Autonomiestufe | wer eine Session plant |
| [DECISIONS.md](DECISIONS.md) | Genese: warum es so ist | wer etwas ändern will |
| [OFFENE-FRAGEN.md](OFFENE-FRAGEN.md) | Genese: was ungeklärt blieb | wer über etwas stolpert |
| [MASCHINELLE-EDITORIK.md](MASCHINELLE-EDITORIK.md) | Prüfung: der Vermerk | jeder Agent, der einen Vorschlag zur Quelle macht |
| [`../AGENTS.md`](../AGENTS.md), [`../CLAUDE.md`](../CLAUDE.md) | Agent-Sozialisierung | jede Session |
| [`../journal.md`](../journal.md), [`../fehlerjournal.md`](../fehlerjournal.md) | die zwei Gedächtnisse | jede Session am Anfang und am Ende |

Das sind acht Dokumente und zwei Journale. Was hier fehlt, fehlt, weil das
Projekt es noch nicht braucht: kein `DESIGN.md`, solange es keine Oberfläche
gibt, kein `PIPELINE.md`, solange die Pipeline zwei Skripte sind.
