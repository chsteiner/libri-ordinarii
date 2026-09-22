# Fehlerjournal

Die roten Zeilen dieses Repositoriums, chronologisch, neue Einträge unten. Was
hierher gehört: ein eigener Fehler, dessen Fehlermodus schon eine dokumentierte
Lehre hat, mit Datum, was passiert ist, und welche Lehre nicht gegriffen hat,
samt Fundstelle. Die Lehren stehen in `AGENTS.md`, `CLAUDE.md`, den ADRs und
dem Betriebsvertrag; was dort noch nicht steht, ist beim ersten Mal kein
roter Fall, sondern ein Grund, es dort einzutragen.

**Diese Datei ist vom Prozessjournal getrennt.** `journal.md` ist der
Arbeitsstand: Entscheidungen, Sackgassen, Handoffs, am Stück gelesen.
Der Zähler hier wird über seine Nummern angesprungen und soll in keinem Lauf im
Kontext liegen, der am Artefakt arbeitet.

**Gezählt wird der eigene Fehler, nicht der fremde**, und nicht der Schaden,
sondern ob dieselbe Lehre ein zweites Mal wirkungslos war. Ein abgewendeter
Fehler ist keiner: wer ihn zählt, gibt dem richtigen Verhalten dieselbe Farbe
wie dem falschen. Abgewendet heißt: etwas hat ihn abgewendet, bevor er etwas
trug (ein Gate, eine Probe, oder die Lehre selbst, wenn ihretwegen nachgesehen
wurde). Was schon getragen hat und danach nur zufällig nicht weiterwirkte,
zählt.

**Bei der dritten Zeile zu derselben Lehre wird nicht mehr gezählt, sondern
der Mechanismus gewechselt**: ein Gate in `pruefen.py`, ein Hook, ein anderer
Ablauf. Eine vierte Zeile ist dann kein Befund mehr, sondern der Beleg, dass
niemand die Konsequenz gezogen hat.

## Die Zeile

```
### Fehler N (rot): <was passiert ist, in einem Halbsatz>

**Nicht gegriffen hat** <Datei, Abschnitt oder Regelnummer>: »<Wortlaut>«.
<Zwei bis fünf Sätze: was getan wurde, was daraus folgte, wer es gefunden hat.>
Letzte Zeile zu derselben Lehre: <Nummer> oder »keine«.
```

Die Nummer vergibt bei mehreren gleichzeitigen Spuren die Koordination, nicht
die Spur selbst: der Zähler ist global, und ein Merge meldet nichts, wenn zwei
Spuren dieselbe Nummer in verschiedenen Abschnitten vergeben.

## Rote Zeilen

### Fehler 1 (rot): »fünf Passauer« in drei Dokumenten, gemessen waren sechs

**Nicht gegriffen hat** `journal.md`, Kopf: »Zahlen werden hier nicht
fortgeschrieben, sondern beim Nennen gemessen und datiert«, und
`playbooks/BETRIEBSVERTRAG.md`, Regel 17: »Jede Zahl im PR-Body nennt ihre
Zählkonvention«. Am 22.09.2026 vormittags stand die Zahl der Passauer Dateien
in `CLAUDE.md` (Fallstrick 1), `docs/OFFENE-FRAGEN.md` (F6) und `journal.md`
als fünf, obwohl `derived/corpus-stats.md` im selben Commit sechs Zeilen für
Passau führt; geschrieben aus dem Gedächtnis der Erkundung, nicht aus der
Tabelle. Getragen hat es: der ZfdG-Beitrag hat die Fünf aus `CLAUDE.md`
übernommen und in einem freigegebenen Absatz stehen gehabt. Gefunden von
einem Opus-Belegprüfer am Nachmittag, nachgesehen von Christian Steiner und
Claude Fable 5.1 an der Tabelle. Letzte Zeile zu derselben Lehre: keine.
