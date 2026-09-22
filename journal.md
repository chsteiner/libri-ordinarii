# Prozessjournal

Arbeitsstand über Sessions hinweg: chronologisch, neue Einträge unten, der
jüngste Handoff-Eintrag ist der Einstieg für die nächste Session.
Bestandsdokumentation gehört nicht hierher, sondern nach `docs/`; Zahlen
werden hier nicht fortgeschrieben, sondern beim Nennen gemessen und datiert.
Rote Zeilen stehen nicht hier, sondern in `fehlerjournal.md`.

Die übrigen Promptotyping-Dokumente führt dieses Repositorium unter eigenen
Namen; keines davon wird ein zweites Mal angelegt:

| Zweck | Ort |
|---|---|
| Domain Knowledge | `docs/` mit `docs/INDEX.md` als Einstieg, dazu `derived/incipits-felder.md` |
| Requirements | die Issues, bis dahin `docs/ANFORDERUNGEN.md`, mit dem Labelschema aus `AGENTS.md` |
| Entscheidungen | `docs/DECISIONS.md` im ADR-Format; `docs/OFFENE-FRAGEN.md` als Gegenseite |
| Technical | `AGENTS.md` und `docs/DATA-MODEL.md` |
| Journal | diese Datei |

## 2026-09-22 – Anlage, handoff

**Stand.** Repositorium angelegt als Begleitmaterial zu Christian Steiners
Beitrag für den ZfdG-Sonderband »Liturgie, digital« (Abgabe 30.09.2026). Es
überträgt die Arbeitsweise aus `mhdbdb-tei-only` und `corema` auf die Libri
ordinarii des Cantus Network: Einstiegskarte (`AGENTS.md`), Fallstricke
(`CLAUDE.md`), Wissensbasis (`docs/`, acht Dokumente), abgeleitete Schicht
(`scripts/ableiten.py` → `derived/`), Prüfung (`scripts/pruefen.py`),
Betriebsvertrag und Kickoff-Vorlage (`playbooks/`), Labelschema
(`.github/labels.json`), zwei Journale. Geschrieben von Claude Fable 5.1 in
Claude Code, Auftrag und Entscheidungen von Christian Steiner; die Entscheidungen
stehen als ADR-1 bis ADR-5 in `docs/DECISIONS.md`.

**Gemessen** (erster Lauf von `ableiten.py`, 22.09.2026, Quelle
`chsteiner/cantus` Stand 17.01.2023): 31 Dateien `*_current_tei.xml`, eine
übersprungen (`emmeram_emm1_NOVARIANTS.xml`), 287.844 Incipits, davon 58.292
`supplied`; 166.209 mit Cantus-ID (Präfix `CantusID `, ADR-3), 70.215 mit
anderer Sigle in `@n`, 51.420 ohne `@n`; 12.382 Incipits ohne Hora, davon
11.754 im Kommentarteil (`.comment.` in der `xml:id`); 4.389 ohne Fest.
Der Variantenapparat liegt in den Dateien einer Tradition fast identisch vor
(Salzburg 3 × 5.229 und 1 × 5.230, Passau 4 × 7.710 und 1 × 7.709,
Klosterneuburg 4 × 6.473; F6 in `docs/OFFENE-FRAGEN.md`). `pruefen.py`:
GRUEN, 0 harte Verstöße, 4 Befundklassen, dokumentiert als F1 bis F9. Die Zahlen
von heute stehen hier mit Datum; die lebenden in `derived/corpus-stats.md`.

**Entschieden.** ADR-1 bis ADR-5. Dazu: kein Promptotyping-Durchlauf mit
Exploration und Prototyp an diesem Material; das Repositorium ist der Zustand
vor der ersten Session (Christian, 22.09.2026, weil er den Durchlauf an
anderen TEIs oft genug gemacht hat und er hier dasselbe Ergebnis liefern
würde).

**Offen.** A1 bis A6 in `docs/ANFORDERUNGEN.md`; die Befunde in
`docs/OFFENE-FRAGEN.md`; Lizenz und DOI (A6, `auto:pair`); ob die
`pruefen.py`-Befunde (verschriebene Cantus-ID-Präfixe, seltene Horen-Siglen,
Reste ohne Hora) als Vermerke erfasst werden (A4, A5).

**Verworfen.** `derived/incipits.jsonl` committen: 145 MB, über der
GitHub-Grenze; gitignoriert, ADR-1 ergänzt. TEIs kopieren oder als Submodul (ADR-1); `@n` tolerant parsen
(ADR-3); CSV oder SQLite statt JSONL (ADR-2).

**Nicht getan.** Kein Aufruf des Cantus Index (externer Dienst, braucht einen
Kickoff mit Freigabe, A2). Kein Vermerk geschrieben: `data/vermerke.jsonl`
existiert noch nicht, `pruefen.py` meldet das.
