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

Noch keine. Die nächste ist 1.
