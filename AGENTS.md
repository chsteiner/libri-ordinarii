# AGENTS.md

Werkzeugneutrale Einstiegskarte für LLM-Agenten: was jede Session zuerst
wissen muss. Der inhaltliche Einstieg in den Bestand ist
[docs/INDEX.md](docs/INDEX.md). Fallstricke und Zählfallen stehen in
[CLAUDE.md](CLAUDE.md); die Datei ist trotz des Namens nicht Claude-spezifisch
und bindet diese Karte ein, statt sie zu wiederholen.

**Was als Nächstes ansteht, steht in den Issues**, nicht in einer Datei.
Solange das Repositorium nicht auf GitHub liegt, hält
[docs/ANFORDERUNGEN.md](docs/ANFORDERUNGEN.md) die Issue-Entwürfe. Der
Arbeitsstand über Sessions hinweg steht in [journal.md](journal.md), die roten
Zeilen getrennt davon in [fehlerjournal.md](fehlerjournal.md).

## Was das hier ist

Ein **Arbeitsrepositorium** zu den Libri ordinarii des Cantus Network
(Salzburger Kirchenprovinz, TEI, 2014 bis 2023). Kein Programm, keine Website,
keine Edition. Die Edition steht in GAMS, hat PIDs und ist zitierfähig; hier
entsteht die Schicht darüber, mit der ein Team und seine Agenten daran
weiterarbeiten können, ohne die Edition zu verändern.

Die wichtigste Unterscheidung: **`../cantus/TEIs/` gegen `derived/`.** Das
erste ist die Quelle, ein Klon eines fremden Repositoriums, und wird hier
**nie** geändert. Das zweite ist erzeugt, jede Handänderung ist beim nächsten
Lauf weg. Was an den Daten korrigiert gehört, wird als **Vermerk** festgehalten
(siehe [docs/MASCHINELLE-EDITORIK.md](docs/MASCHINELLE-EDITORIK.md)) und geht
als Vorschlag an die Herausgeber der Edition, nicht als Diff in die Quelle.

## Issue-Labels

Drei Achsen, **genau ein Label je Achse**, dazu zwei Flags. Das Schema ist für
Agenten gebaut, nicht für Menschen: es sagt einer Session, was sie darf. Es
stammt aus `mhdbdb-tei-only` und `corema` und ist dort seit August 2026 in
Betrieb; die Definitionen liegen in [`.github/labels.json`](.github/labels.json).

- **`auto:*`** sagt, **wie viel menschliche Klärung ein Issue braucht**, nicht
  ob es freigegeben ist. Der Auftrag zum Loslegen kommt immer eigens von
  Christian, als Kickoff je Lauf. Das Label sagt nur, was danach noch nötig
  ist.
  `auto:full` (Ziel, Kriterien und Daten liegen vor, keine offene Frage: ein
  Agent bringt es allein zu Ende) | `auto:brief` (ein bis drei Fragen vorab,
  dann durchziehbar) | `auto:checkin` (eine Entscheidung fällt **mitten** im
  Lauf an, etwa nachdem eine Stichprobe zeigt, wie zu verfahren ist) |
  `auto:pair` (braucht Christians Anwesenheit oder Autorität durchgehend:
  Orga, Strategie, Kontakt zu den Herausgebern der Edition) | `auto:blocked`
  (wartet auf Dritte, auf Zugang von außen oder auf ein anderes Issue; wer so
  labelt, schreibt die Nummer des blockierenden Issues in den Grund).

  Der Unterschied zwischen den ersten dreien ist der **Zeitpunkt** der offenen
  Frage, nicht ihre Schwere. Keine Frage heißt `full`, eine vorab
  beantwortbare heißt `brief` und gehört in den Kickoff-Prompt, eine erst
  unterwegs entstehende heißt `checkin`. Wer ein Issue auf `checkin` setzt,
  sollte sagen können, warum sich die Frage **nicht** vorab klären lässt.
- **`area:*`**: `data` | `pipeline` | `docs` | `agents` | `orga`
- **`effort:*`**: `small` (eine Stunde oder weniger) | `medium` (halber Tag) |
  `large` (ein Tag oder mehr)
- **Flags**: `quelle` (betrifft die TEIs in `../cantus`, also die Edition
  selbst: hier nur als Vermerk, nie als Änderung) und `modell:offen` (die
  Entscheidung über eine Lesart oder ein Modell fehlt noch, die Umsetzung ist
  blockiert).

**`modell:offen` heißt nicht »wartet auf Christian«.** Eine Modellfrage darf
ein Frontier-Modell entscheiden, wenn der Auftrag Zählung, Belege und die
vertretbaren Lesarten mitbringt und das Ergebnis im Issue belegt wird. Die
Aufbereitung führt jedes Modell, die Entscheidung geht als abgegrenzter Auftrag
an das stärkste verfügbare, und ihr Ergebnis wird übernommen statt überstimmt.
**Nicht** unter dieses Label fallen editorische Entscheidungen über die Quelle:
ob eine Variante eine Lesart ist, welche Tradition ein Fest hat, ob ein Incipit
richtig identifiziert ist. Das entscheidet ein Mensch mit liturgischer
Kompetenz, und das Repositorium hält nur den Vorschlag und den Vermerk.

Wer ein Issue anfasst, zieht die Labels in derselben Session nach.

## Reihenfolge nach einer Datenänderung

Es gibt hier keine Datenänderung an der Quelle. Was sich ändert, sind
`scripts/`, `docs/` und die Vermerke. Nach jeder Änderung an einem Skript oder
an `data/vermerke.jsonl` läuft die Kette vollständig:

1. `python scripts/ableiten.py` erzeugt `derived/` neu.
2. `python scripts/pruefen.py` prüft `derived/` gegen die Konventionen und
   endet rot, wenn etwas nicht stimmt. Die letzte Zeile der Ausgabe ist das
   Ergebnis und gehört unverändert in den PR.
3. `git diff --stat derived/` zeigt, was sich an den Zahlen geändert hat. Eine
   Zahl, die sich ändert, ohne dass jemand sagen kann warum, ist ein Befund.

## Zahlen

**Nenne mit jeder Zahl die Zählkonvention.** Die Konventionen stehen in
[`derived/incipits-felder.md`](derived/incipits-felder.md); dieselbe Frage hat
je nach Konvention verschiedene Antworten (Incipits mit oder ohne `supplied`,
Handschriften als Dateien oder als Traditionen). Zahlen werden nicht in Prosa
fortgeschrieben, sondern beim Nennen gemessen; die Tabelle dafür ist
[`derived/corpus-stats.md`](derived/corpus-stats.md).

## Befunde

**Ein Befund ist selbst eine Behauptung.** Was ein Reviewer, ein Bot, ein
anderer Agent oder ein früherer Eintrag im Journal sagt, wird an der genannten
Stelle nachgemessen, bevor es in eine Datei wandert. Ein Agent darf Belege
sammeln, vergleichen, Prüfungen laufen lassen und Vorschläge festhalten; er
darf **nicht** den Status »geprüft« oder »übernommen« an einem Vermerk setzen.
Das tut ein Mensch, mit Namen und Datum.

## Was ohne Freigabe tabu bleibt

Kein Push nach `main`, kein Force-Push, kein Schließen von Issues, keine
Kontaktaufnahme mit den Herausgebern der Edition oder anderen Externen. Die
vollständige Fassung steht in
[`playbooks/BETRIEBSVERTRAG.md`](playbooks/BETRIEBSVERTRAG.md) und wird beim
Kickoff wörtlich in den Prompt kopiert.
