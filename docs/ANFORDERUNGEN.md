# Anforderungen als Issue-Entwürfe

Solange das Repositorium nicht auf GitHub liegt, stehen die Anforderungen
hier; danach werden sie Issues mit genau diesen Labels, und diese Datei
verweist nur noch dorthin. Jede Anforderung ist eine User Story, ein
Akzeptanzkriterium, eine Autonomiestufe mit Begründung und eine Antwort auf die
Frage, **was der Agent entscheiden darf und was nicht**.

Die ersten drei stammen aus Christian Steiners Vortrag »Coding Vibes« (HAB
Wolfenbüttel, 20.03.2026), wo sie als Beispiele für Scholar-Centred Design am
Liber ordinarius standen. Die übrigen sind Befunde aus dem ersten Lauf von
`scripts/ableiten.py` am 22.09.2026.

## A1: Offiziumsstruktur eines Fests über mehrere Libri ordinarii vergleichen

**Als** Liturgiewissenschaftler*in **will ich** für ein Fest (Festcode) die
Abfolge der Horen und ihrer Gesänge in mehreren Handschriften nebeneinander
sehen, **damit** ich regionale Unterschiede der liturgischen Praxis erkenne.

**Akzeptanz.** Ein Skript nimmt einen Festcode und eine Liste von
Handschriften und gibt je Hora die Incipits mit Gattung und Cantus-ID in einer
Tabelle aus, Handschriften als Spalten. Fehlt ein Fest in einer Handschrift,
steht das da, nicht eine leere Spalte ohne Erklärung. Ein Testfall mit einem
Fest, das in allen Traditionen belegt ist, und einem, das nur in einer steht.

**Labels.** `auto:brief`, `area:pipeline`, `effort:medium`.

**Warum `brief`.** Zwei Fragen vorab: Werden die vier Salzburger Zeugen als
eine Spalte oder als vier gezeigt? Zählt ein `supplied`-Incipit als belegt?
Beides entscheidet Christian im Kickoff; danach läuft es durch. **Was der
Agent entscheidet:** Ausgabeformat, Sortierung, Umgang mit Incipits ohne
Cantus-ID (er zeigt den Text). **Was er nicht entscheidet:** ob zwei
Incipits mit verschiedenem Text dasselbe Stück sind.

## A2: Incipits gegen den Cantus Index prüfen

**Als** Liturgiewissenschaftler*in **will ich** die Cantus-IDs der Incipits
gegen den Cantus Index abgleichen (Gattung, Volltext, Konkordanzen), **damit**
ich Identifikationen prüfen kann, ohne im gedruckten Katalog nachzuschlagen.

**Akzeptanz.** Ein Skript fragt für jede `cantus_id` aus `incipits.jsonl` die
Cantus-Index-API ab, mit Cache auf Platte, und schreibt je ID: existiert,
Gattung dort, Gattung hier, stimmt überein. Abweichungen werden als Vermerke
mit Sachverhalt `cantus-index-abweichung` vorgeschlagen, nicht korrigiert. Die
Zahl der Abfragen und der Treffer steht in der Ausgabe.

**Labels.** `auto:brief`, `area:pipeline`, `effort:medium`, `quelle`.

**Warum `brief`.** Ein Aufruf eines externen Dienstes braucht die Freigabe im
Kickoff (Rate, Umfang, ob eine Stichprobe reicht). **Was der Agent
entscheidet:** Cache, Fehlerbehandlung, Format der Vermerke. **Was er nicht
entscheidet:** ob eine Abweichung ein Fehler in der Edition oder im Index ist;
der Vermerk bleibt `vorgeschlagen`.

## A3: Rubriken nach Raumbezügen filtern

**Als** Liturgiewissenschaftler*in **will ich** Rubriken nach Orten im
Kirchenraum filtern (Altäre, Kapellen, Prozessionsstationen), **damit** ich die
rituelle Bewegung in einem bestimmten Kirchengebäude rekonstruieren kann.

**Akzeptanz.** Der Kommentar- und Rubrikentext der Horen wird in die
abgeleitete Schicht aufgenommen (heute nur die Incipits, siehe ADR-2), und
`seg @ana="#place"` wird je Fest und Hora gezählt und gelistet. Ein Skript gibt
für eine Handschrift alle Feste mit Ortsnennung aus, mit dem Ortsnamen, wie er
dasteht.

**Labels.** `auto:checkin`, `area:data`, `effort:large`, `modell:offen`.

**Warum `checkin`.** Erst eine Stichprobe zeigt, ob `#place` die Orte im
Kirchenraum trägt oder nur Ortsnamen (Diözesen, Städte); danach fällt die
Entscheidung, ob ein zweites Vokabular nötig ist. **Warum `modell:offen`.** Ob
zwei Schreibungen wie »ad altare sancti Ruperti« und »altare s. Rudberti«
(ein konstruiertes Beispiel, beide stehen so nicht im Bestand) ein Ort sind, ist eine
Vokabularfrage an der Datenschicht (ADR-5); ein Frontier-Modell darf sie mit
Belegen entscheiden. **Was der Agent nicht entscheidet:** welcher reale Altar
gemeint ist.

## A4: Verschriebene Cantus-ID-Präfixe als Vermerke erfassen

**Als** Bearbeiter*in **will ich** jede Stelle, an der `@n` erkennbar eine
Cantus-ID mit Tippfehler ist, als Vermerk sehen, **damit** ich sie gesammelt
an die Herausgeber der Edition weitergeben kann.

**Akzeptanz.** `pruefen.py` meldet die Fälle heute schon; ein Skript schreibt
sie als Vermerke mit Sachverhalt `n-verschrieben` nach `data/vermerke.jsonl`,
Status `vorgeschlagen`, `von` mit Modell oder Skriptname.

**Labels.** `auto:full`, `area:data`, `effort:small`, `quelle`.

**Warum `full`.** Ziel, Kriterium und Daten liegen vor, es gibt keine offene
Frage: die Verschreibungen sind aufgezählt, der Vorschlag ist mechanisch, und
der Status bleibt `vorgeschlagen`.

## A5: Incipits außerhalb einer Hora, die kein Kommentar sind

**Als** Bearbeiter*in **will ich** wissen, warum Incipits mit einer
Horen-Sigle in der `xml:id` in keinem `div type="time:*"` stehen, **damit**
ich entscheiden kann, ob die Struktur oder die ID falsch ist.

**Akzeptanz.** Eine Liste je Datei mit Umfeld (die drei Elemente davor), eine
Klassifikation der Fälle und ein Vorschlag je Klasse. Kein Eingriff.

**Labels.** `auto:checkin`, `area:data`, `effort:small`, `quelle`.

**Warum `checkin`.** Ob das ein Fehler der ID-Erzeugung von 2020 oder eine
bewusste Struktur (Nota-Abschnitte nach den Horen) ist, zeigt erst die Liste;
dann entscheidet Christian, ob daraus Vermerke werden.

## A6: Das Repositorium öffentlich schalten und mit DOI versehen

**Labels.** `auto:pair`, `area:orga`, `effort:small`.

Braucht Christians Autorität: GitHub-Repo anlegen, Lizenz festlegen
(README), Zenodo-Release. Kein Agent tut das.
