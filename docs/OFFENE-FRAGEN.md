# Offene Fragen

Was beim Lesen der Daten aufgefallen ist und niemand hier entscheiden kann
oder darf. Jede Frage nennt, wer sie gemessen hat und wann; die Zahlen gelten
für diesen Tag, die lebenden stehen in `derived/corpus-stats.md` und in der
Ausgabe von `scripts/pruefen.py`. Eine Frage wird nicht gelöscht, sondern mit
der Antwort und ihrer Herkunft abgeschlossen.

Alle Einträge: gemessen am 22.09.2026 mit `scripts/ableiten.py` und
`scripts/pruefen.py` an `chsteiner/cantus`, Stand 17.01.2023, durch Claude
Fable 5.1; kein Eintrag ist von einem Menschen geprüft.

## F1: Cantus-IDs mit Schrägstrich, Komma oder Suffix

2.811 von 166.209 `cantus_id` liegen außerhalb des Musters »sechs Ziffern,
optional Buchstabe«: `003540/003541/003542` (197 Incipits, drei IDs für ein
Incipit), `001358-001360,a00408` (50), `007840Pzc` (50), `g02486.1` (48),
`008193/008193.1` (46). Ist der Schrägstrich eine Alternative (»eine von
dreien«) oder eine Folge (»alle drei nacheinander«)? Ist `.1` eine
Cantus-Index-Notation oder eine Projektkonvention? **Wer antworten kann:** die
Herausgeber der Edition. Bis dahin zählt `pruefen.py` sie als Befund und
`ableiten.py` lässt sie stehen.

## F2: Verschriebene Präfixe

Vier Incipits tragen ein verschriebenes Präfix: `CanutsID a02107`,
`CaantusID 001886`, `CantusiD 004349`, `ChantID g01102`. Sie stehen in `n_roh`,
nicht in `cantus_id` (ADR-3). Kandidaten für Vermerke mit Sachverhalt
`n-verschrieben` (A4). Dazu 312 Incipits mit mehr als einer Cantus-ID in einem
`@n`, durch Leerzeichen getrennt; ob das dasselbe meint wie der Schrägstrich in
F1, ist offen.

## F3: Was `@n` sonst noch trägt

70.215 Incipits haben in `@n` etwas anderes als eine Cantus-ID: Psalmen
(`Ps.` 24.122), AH-Nummern (`AH` 13.282), Bibelstellen (`Mt` 3.395, `Lc` 3.514,
`Io` 2.339, `Sir` 2.080 usw.), Nummern nach dem Muster `II-1518` (vermutlich
ein Repertorium, welches, ist nicht dokumentiert), `CorpOr`/`CorpOrat` (603),
`HCM` (427), `Unklar` (185), `?` (22), `kein` (5), `Ende` und `CL-Ende` (117).
Das Attribut ist damit kein Feld, sondern ein Beleg im Freitext. Frage: welche
Repertorien stehen hinter `II-1518`, `HCM`, `CorpOr`, `CP`, `PD`, `TT`? Ein
Glossar der Siglen gehört in `DATA-MODEL.md`, sobald jemand es kennt.

## F4: 210 Incipits mit Horen-Sigle in der ID, aber außerhalb jeder Hora

193 in `freising`, 17 in `enns`. In Freising stehen sie in einem `div` ohne
`@type` nach den Horen-`div`s eines Fests (`Nota ab adventu Christi ...`),
tragen aber `C` oder eine andere Sigle in der `xml:id`
(`incipit.01011000.C.58`). Vermutung, nicht geprüft: die ID-Erzeugung
(`xslt/create__inc_head_ids.xsl`, 2020) hat die Sigle der vorangehenden Hora
fortgeschrieben. In Enns haben die 17 Incipits gar keine `xml:id` und kein
Fest: die Datei ist ein Fragment (ein `pb`, sieben Horen, null Feste). A5.

## F5: Hartkirchen und Enns

`hartkirchen_current_tei.xml`: 107 Feste, 0 Horen, 11 Incipits, 25 Seiten.
`enns_current_tei.xml`: 0 Feste, 7 Horen, 17 Incipits, 1 Seite. Beide sind
keine Libri ordinarii im Sinn der übrigen 29 Dateien, sondern Fragmente oder
Kalendare. Ob sie in Zählungen über »den Bestand« mitzählen, entscheidet die
Konvention; `corpus-stats.md` zählt sie mit, weil sie auf `_current_tei.xml`
enden.

## F6: Der Apparat einer Tradition ist nicht überall gleich

Die Dateien einer Tradition tragen fast, aber nicht genau dieselbe Zahl
`metamark`: Salzburg 5.229, 5.229, 5.229, 5.230; Passau 7.710, 7.710, 7.710,
7.710, 7.709; Emmeram 2.664, 2.664, 2.662; Klosterneuburg 4 × 6.473; Seckau 1
2 × 968. Ist der Apparat je Tradition einmal erzeugt und in jede Datei
kopiert worden, und sind die Abweichungen spätere Handkorrekturen? Dann wäre
die Frage, welche Datei den aktuellen Apparat hat. **Wer antworten kann:**
Christian Steiner (Modellierung) und die Git-Historie von `chsteiner/cantus`.

## F7: `passau_sal` hat drei Seitenumbrüche

`passau_sal_current_tei.xml` zählt 3 `pb`, die vier anderen Passauer Dateien
zwischen 200 und 300. Fehlt die Seitenzählung, oder ist die Datei aus einer
Quelle ohne Foliierung? Folgen für jede Angabe »Folio« in `incipits.jsonl` für
diese Datei.

## F8: `seg/@function`

Nur in den Salzburger Dateien belegt (2.597 in `salzburg_sal`), in
`brixen` nicht. Die Bedeutung ist weder in `Cantus-Dokumentation.pdf` noch im
Schema dokumentiert. `ableiten.py` bildet es nicht ab.

## F9: Die seltene Horen-Sigle `ASP`

Einmal im Bestand. Ein Tippfehler, eine Sonderhora (Asperges?) oder eine
Konvention? Die 14 häufigen Siglen: `C`, `D`, `L`, `M`, `MI`, `N`, `NOHO`,
`P`, `PRO`, `S`, `T`, `V`, `V2`, `X`. Auch diese Liste braucht ein Glossar in
`DATA-MODEL.md`; `NOHO`, `PRO`, `X` und `D` sind nicht selbsterklärend.
