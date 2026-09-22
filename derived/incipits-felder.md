# Felder von `incipits.jsonl`

Eine Zeile je `seg type="incipit"` in Dokumentreihenfolge, erzeugt von
`scripts/ableiten.py`. Nicht von Hand aendern.

| Feld | Herkunft im TEI | Bedeutung |
|---|---|---|
| `handschrift` | `teiHeader/@xml:id` | Kennung der Handschrift, z. B. `brixen` |
| `kurztitel` | `titleStmt/title[@type='short']` | Kurzname |
| `datei` | Dateiname | Quelle der Zeile |
| `lfd` | gezaehlt | laufende Nummer des Incipits in der Datei, ab 1 |
| `incipit_id` | `seg/@xml:id` | z. B. `incipit.01011000.V.9` |
| `fest` | `head/@corresp` des naechsten Fest-`div` | Feastcode, z. B. `01011000` |
| `fest_id` | `head/@xml:id` | |
| `hora` | `label/@n` im `ab[@ana='#head']` des `div[@type='time:*']` | Horen-Sigle, z. B. `V` |
| `hora_id`, `hora_text` | `label/@xml:id`, Labeltext | z. B. `Ad vesperam` |
| `hora_typ` | `div/@type` | `time:1` oder `time:2` |
| `gattung` | `seg/@ana` ohne `#` | Gattungssigle, z. B. `RP`, `AN`, `HY` |
| `cantus_id` | `seg/@n`, wenn es mit `CantusID ` beginnt | die Cantus-ID; bei mehreren IDs alle, durch Leerzeichen getrennt |
| `n_roh` | `seg/@n` sonst | andere Sigle, z. B. `AH 2-18` |
| `konkordanz` | `seg/@corresp` | Konkordanzen, roh |
| `supplied` | `seg/@subtype='supplied'` | vom Bearbeiter ergaenzt, nicht im Original |
| `kommentar` | `.comment.` in `seg/@xml:id` | Incipit im Kommentarteil des Fests, nicht in einer Hora |
| `varianten` | Zahl der `metamark[@function='variant']` im `seg` | |
| `neume` | `phr[@type='neume']` im `seg` vorhanden | |
| `seite` | letztes `pb/@n` vor dem `seg` | Folio |
| `text` | Textinhalt des `seg`, Leerraum normalisiert | einschliesslich des Texts in Variantenmarken |

## Zaehlkonventionen

Dieselbe Frage hat je nach Konvention verschiedene Antworten. Wer eine Zahl nennt,
nennt die Konvention dazu.

- **Incipits** zaehlt jedes `seg type="incipit"`, auch `supplied`. Wer nur den
  Originalbestand will, zieht `supplied` ab; beide Zahlen stehen in `corpus-stats.md`.
- **Mit Cantus-ID** zaehlt nur `@n` der Form `CantusID <id>`. Andere Siglen
  (`AH`, `CAO` usw.) sind Belege, aber keine Cantus-ID.
- **Varianten** zaehlt `metamark`-Elemente, nicht Lesarten: eine Marke kann
  mehrere Zeugen buendeln. `varianten` je Zeile zaehlt nur die Marken innerhalb
  des Incipits; die Spalte in `corpus-stats.md` zaehlt die ganze Datei.
- **Feste** zaehlt `head` mit `@corresp`; ein Fest mit zwei `head` zaehlt zweimal.
- **Horen** zaehlt `div` mit `@type`, das mit `time` beginnt.
- **Handschriften** zaehlt Dateien mit der Endung `_current_tei.xml`, nicht
  Ueberlieferungstraeger: `salzburg_sal`, `salzburg_ur`, `salzburg_ra`, `salzburg_vo`
  sind vier Dateien einer Tradition.
