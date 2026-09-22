# Maschinelle Editorik: der Vermerk

Was ein Sprachmodell an den Daten vorgeschlagen hat, und wer es geprüft hat.

## Die Regel

**Ein Modell ändert die Quelle nicht.** Es liest, zählt, vergleicht, schlägt
vor. Jeder Vorschlag, der eine Stelle in den TEIs betrifft, wird als
**Vermerk** in `data/vermerke.jsonl` festgehalten, eine Zeile je Vorschlag,
und `scripts/pruefen.py` rendert daraus `derived/vermerke.md`, den Prüfstand.
Ein Vermerk hat einen Status, und den Übergang von `vorgeschlagen` nach
`geprueft` oder `verworfen` setzt ein Mensch mit Namen und Datum. Das ist
eine Arbeitsregel, kein Mechanismus: `pruefen.py` erzwingt nur die Form (ein
`geprueft` ohne `geprueft_von` und `geprueft_am` ist ein harter Verstoß); ob
den Namen ein Mensch geschrieben hat, kann kein Skript prüfen. Ein Agent, der
`geprueft` setzt, verstößt gegen diese Regel und gegen den Betriebsvertrag,
nicht gegen das Skript. (Präzisiert am 22.09.2026 nach einem Review des
Beitrags, der das Skript als Durchsetzung beschrieben hatte.)

Das ist die Übertragung der Korrekturregel aus `corema`
(`scripts/korrektur.py --eintragen <pfad> --sachverhalt <kennung>`, jede
Änderung mit zwei Prüfsummen) auf ein Repositorium, das seine Quelle nicht
besitzt: dort wird korrigiert und der Nachweis geführt, hier wird
vorgeschlagen und der Nachweis geführt, und die Korrektur geht als Vorschlag an
die Herausgeber der Edition.

## Das Format

```json
{"id": 1, "datum": "2026-09-22", "datei": "salzburg_sal_current_tei.xml",
 "stelle": "incipit.01011000.V.9", "sachverhalt": "n-verschrieben",
 "beobachtung": "@n lautet 'CanutsID 006583'",
 "vorschlag": "@n zu 'CantusID 006583'",
 "von": "Claude Fable 5.1 via Claude Code", "begruendung": "...",
 "status": "vorgeschlagen", "geprueft_von": null, "geprueft_am": null}
```

| Feld | Inhalt |
|---|---|
| `id` | laufende Nummer, wird nicht wiederverwendet |
| `datum` | Tag des Vorschlags |
| `datei`, `stelle` | Datei und `xml:id` in der Quelle; ohne `xml:id` ein XPath |
| `sachverhalt` | eine Kennung aus der Liste unten |
| `beobachtung` | was dasteht, wörtlich |
| `vorschlag` | was stattdessen stehen soll, oder `keiner` bei einer reinen Meldung |
| `von` | Modell mit Version und Werkzeug, oder ein Mensch mit Namen |
| `begruendung` | warum, mit Beleg (Cantus Index, Parallelstelle, Faksimile) |
| `status` | `vorgeschlagen` \| `geprueft` \| `verworfen` \| `weitergegeben` |
| `geprueft_von`, `geprueft_am` | Mensch und Datum; Pflicht ab `geprueft` |

## Sachverhalte

Die Kennungen sind offen; eine neue wird hier eingetragen, bevor sie benutzt
wird.

| Kennung | Bedeutet |
|---|---|
| `n-verschrieben` | `@n` ist erkennbar eine Cantus-ID mit Tippfehler im Präfix |
| `n-mehrdeutig` | `@n` trägt mehrere IDs oder eine ID und eine Bibelstelle |
| `id-fehlt` | ein Incipit ohne `xml:id` |
| `hora-fehlt` | ein Incipit außerhalb des Kommentars ohne `div type="time:*"` |
| `fest-fehlt` | ein `head` ohne `@corresp` |
| `cantus-index-abweichung` | die ID existiert im Cantus Index nicht oder trägt dort eine andere Gattung |
| `lesart` | ein Vorschlag zur Transkription selbst; **immer** `auto:pair`, nie vom Modell entschieden |

## Was ein Modell nicht darf

- den Status `geprueft` setzen
- eine Datei in `../cantus/` ändern
- einen Vermerk löschen; ein falscher Vermerk bekommt `verworfen` und eine
  Begründung
- eine `lesart` vorschlagen, ohne das Faksimile oder die Parallelstelle zu
  nennen, auf die sich der Vorschlag stützt
