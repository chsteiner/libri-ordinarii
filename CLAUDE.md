# CLAUDE.md

Betriebsanleitung für Claude Code in diesem Repositorium. Die Einstiegskarte
ist eingebunden und wird hier nicht wiederholt:

@AGENTS.md

## Fallstricke

1. **Vier Salzburger Dateien sind eine Tradition, nicht vier Handschriften.**
   `salzburg_sal`, `salzburg_ur`, `salzburg_ra`, `salzburg_vo` tragen denselben
   Variantenapparat (`metamark`: 5.229, 5.229, 5.229, 5.230, am 22.09.2026
   gemessen); dasselbe gilt für die sechs Passauer (5 × 7.710, 1 × 7.709) und
   die vier Klosterneuburger Dateien (4 × 6.473). Die Abweichungen um eins
   sind `docs/OFFENE-FRAGEN.md`, F6. Wer »Handschriften« zählt, sagt, ob Dateien oder
   Traditionen gemeint sind.
2. **`@n` an einem Incipit ist kein Feld, sondern ein Freitext.** Meist
   `CantusID 006583`, aber auch Bibelstellen (`Ps. 22`, `Mt 5`), AH-Nummern,
   CAO, `Unklar`, `?`, und Schreibvarianten von `CantusID`. `ableiten.py`
   trennt `cantus_id` von `n_roh` und normalisiert nichts; die Varianten
   stehen in `docs/OFFENE-FRAGEN.md`. Wer sie »repariert«, ändert die Quelle.
3. **Ein Incipit ohne Hora ist meist kein Fehler.** Die Kommentarteile der
   Feste (`.comment.` in der `xml:id`) enthalten Incipits, die in keiner Hora
   stehen. `derived/corpus-stats.md` trennt sie von den echten Resten.
4. **Die Quelle wird nicht angefasst.** `../cantus` ist ein Klon eines
   fremden Repositoriums. Ein Diff dort ist ein Fehler, auch ein gut gemeinter.
   Korrekturvorschläge sind Vermerke (`docs/MASCHINELLE-EDITORIK.md`).
5. **Eine Zahl in einem Dokument ist am Tag ihrer Messung richtig.** Sie
   trägt das Datum oder sie steht nicht da; die lebenden Zahlen stehen in
   `derived/`.

## Schreibregeln

- Deutsch in `docs/`, `journal.md`, `fehlerjournal.md`, Issues und Commits;
  Latein und Siglen bleiben, wie sie in der Quelle stehen.
- Keine Gedankenstriche (U+2014) in Prosa, keine doppelten Bindestriche als
  Ersatz. Doppelpunkt, Komma, Klammer oder ein eigener Satz. Der
  Halbgeviertstrich mit Leerzeichen ist erlaubt.
- Echte Umlaute in Prosa. In `scripts/` sind ASCII-Ersatzformen in Kommentaren
  zulässig, weil die Windows-Konsole der Grund ist.
- Keine Emoji.

## Werkzeuge

```
python scripts/ableiten.py [--tei-dir ../cantus/TEIs]   # derived/ neu erzeugen
python scripts/pruefen.py                                # derived/ prüfen, Exit 1 bei Verstoß
```

Beide laufen ohne Modell und ohne Netz. Was ein Modell entscheiden soll, steht
als Issue mit `modell:offen`; was ein Mensch entscheiden muss, als `auto:pair`.

## Git

- Nur benannte Dateien stagen, nie `git add -A` oder `git add .`.
- Jede Session in ihrem eigenen Worktree unter `.claude/worktrees/`, angelegt
  mit `claude --bg --name <name> --worktree <name>`.
- `derived/corpus-stats.md` und `derived/incipits-felder.md` werden
  mitcommittet, damit ein frischer Klon die Zahlen hat, ohne die TEIs zu
  brauchen; `derived/incipits.jsonl` ist gitignoriert (ADR-1). Ein Commit, der
  `scripts/` ändert, ändert die beiden Markdown-Dateien im selben Commit oder
  sagt, warum nicht.
- Review vor dem ersten Push jedes Branches (`reviewer`, wenn verfügbar),
  mit Branch, Basis, Ziel in einem Satz und Rundennummer im Auftrag.
- Kein Push nach `main` ohne Kickoff, siehe `playbooks/BETRIEBSVERTRAG.md`.
