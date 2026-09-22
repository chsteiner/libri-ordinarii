# libri-ordinarii

Ein Arbeitsrepositorium für die Weiterarbeit an den Libri ordinarii des
[Cantus Network](https://gams.uni-graz.at/context:cantus) mit Coding Agents.
Es ist das Begleitmaterial zu Christian Steiners Beitrag im ZfdG-Sonderband
»Liturgie, digital« und zeigt, wie ein Editionsprojekt aussieht, das nach der
Arbeitsweise aus [`mhdbdb-tei-only`](https://github.com/DigitalHumanitiesCraft/mhdbdb-tei-only)
aufgesetzt ist: eine Wissensbasis in Markdown, eine abgeleitete Schicht mit
Zählkonventionen, Anforderungen als Issues mit Autonomiestufe, Prüfungen, die
nicht dem Modell gehören, und zwei Gedächtnisse.

**Was das nicht ist.** Keine Edition und kein Ersatz für GAMS: die Edition
steht dort, mit PIDs, und wird hier nicht kopiert. Kein Promptotyping-Durchlauf
mit Exploration und Prototyp: das Repositorium ist der Zustand *vor* der ersten
Session, also das, was ein Editionsteam anlegt, bevor ein Agent die erste
Aufgabe bekommt. Die TEI-Dateien liegen nicht hier (CC BY-NC 4.0, ÖAW), sondern
werden aus [`chsteiner/cantus`](https://github.com/chsteiner/cantus) gelesen.

## Anfangen

```
git clone https://github.com/chsteiner/cantus ../cantus
python scripts/ableiten.py          # erzeugt derived/ aus ../cantus/TEIs
python scripts/pruefen.py           # prüft derived/ gegen die Konventionen
```

Python 3.11 oder neuer, dazu `lxml`. Wer wissen will, was danach zu tun ist,
liest [`AGENTS.md`](AGENTS.md) (die Einstiegskarte für jede Session) und
[`docs/INDEX.md`](docs/INDEX.md) (wo was steht).

## Was wo liegt

| Pfad | Inhalt | Wer ändert es |
|---|---|---|
| `AGENTS.md`, `CLAUDE.md` | Einstiegskarte und Fallstricke für Agenten | Christian |
| `docs/` | die Wissensbasis, Einstieg über `docs/INDEX.md` | Christian, Agenten mit Vermerk |
| `derived/` | die abgeleitete Schicht, bei jedem Lauf neu erzeugt; die JSONL (145 MB) liegt nicht im Repositorium, `ableiten.py` erzeugt sie | niemand von Hand |
| `scripts/` | Ableitung und Prüfung, deterministisch, ohne Modell | Agenten, mit Review |
| `playbooks/` | Betriebsvertrag und Kickoff-Vorlage für autonome Sessions | Christian |
| `journal.md` | Arbeitsstand über Sessions hinweg | jede Session |
| `fehlerjournal.md` | rote Zeilen: Fehler, deren Lehre schon dastand | jede Session |
| `.github/labels.json` | das Labelschema für Issues | Christian |

## Zitieren

Christian Steiner: libri-ordinarii. Ein Arbeitsrepositorium für Libri
ordinarii mit Coding Agents. GitHub 2026. `[PRÜFEN: DOI nach dem Release]`

Lizenz der Skripte und Dokumente: [CC BY 4.0](LICENSE.md), Christian Steiner,
Digital Humanities Craft OG, Graz. Die Daten, die `derived/` aus den TEIs
ableitet, stehen unter der Lizenz der Quelle, CC BY-NC 4.0 (Österreichische
Akademie der Wissenschaften, Institut für kunst- und musikhistorische
Forschungen).
