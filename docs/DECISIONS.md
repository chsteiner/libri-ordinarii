# Entscheidungen

Architecture Decision Records: was entschieden wurde, mit Kontext, verworfenen
Alternativen, Folgen und dem, der entschieden hat. Eine Entscheidung wird nicht
umgeschrieben, sondern durch eine spätere ersetzt, die auf sie verweist.
`OFFENE-FRAGEN.md` ist die Gegenseite: was ungeklärt blieb.

## ADR-1: Die TEIs werden nicht kopiert

**Datum:** 22.09.2026. **Entschieden von:** Christian Steiner, vorgeschlagen
von Claude Fable 5.1.

**Kontext.** Die TEIs des Cantus Network liegen in `chsteiner/cantus` (PUBLIC)
und in GAMS, Lizenz CC BY-NC 4.0 der ÖAW. Dieses Repositorium soll öffentlich
werden und einen DOI bekommen.

**Entscheidung.** Die Skripte lesen aus einem Klon von `chsteiner/cantus`
neben diesem Repositorium (`--tei-dir`, Default `../cantus/TEIs`). Hier liegt
nur die abgeleitete Schicht, unter der Lizenz der Quelle.

**Alternativen.** Submodul (bindet an einen Commit, gut, aber `git submodule`
ist für ein Editionsteam eine Hürde); Kopie unter `data/tei/` (verdoppelt eine
Quelle, die jemand anderem gehört, und lädt zu Änderungen ein).

**Folgen.** `derived/corpus-stats.md` und `derived/incipits-felder.md` werden
mitcommittet, damit ein frischer Klon die Zahlen und die Konventionen ohne die
TEIs hat. `derived/incipits.jsonl` nicht: 145 MB am 22.09.2026, über der
GitHub-Grenze von 100 MB je Datei, und in etwa einer Minute neu erzeugt.
`.gitignore` sperrt beides, `data/tei/` und die JSONL.

## ADR-2: Eine flache Zeile je Incipit

**Datum:** 22.09.2026. **Entschieden von:** Claude Fable 5.1 nach dem Muster
von `corema/derived/recipes.jsonl`, von Christian Steiner übernommen.

**Kontext.** Das TEI ist verschachtelt (Fest > Kommentar | Hora > Incipit) und
bis zu 2,9 MB je Datei; ein Agent kann es nicht in den Kontext nehmen und soll
es nicht bei jeder Frage neu parsen.

**Entscheidung.** `derived/incipits.jsonl`, eine Zeile je `seg[@type='incipit']`
mit Fest, Hora, Gattung, Cantus-ID, Konkordanz, `supplied`, Variantenzahl,
Folio und Text. Die Felder sind in `incipits-felder.md` erklärt, jede Zahl in
`corpus-stats.md` trägt ihre Konvention.

**Alternativen.** CSV (die XSLT `all_incipits_to_csv.xsl` tut das schon, aber
ohne Fest- und Horenzuordnung und ohne Konventionen); SQLite (eine Datenbank
verlangt ein Werkzeug, eine JSONL-Zeile liest jeder Editor).

**Folgen.** Jede Zahl über den Bestand wird aus dieser Datei gemessen, nicht
aus dem TEI gezählt. Was das Skript nicht abbildet (Kommentartext, Personen,
Orte, Traktatzitate), ist damit auch nicht zählbar; wer es braucht, erweitert
das Skript und dokumentiert das Feld.

## ADR-3: `@n` wird nicht normalisiert

**Datum:** 22.09.2026. **Entschieden von:** Claude Fable 5.1, offen zur
Revision durch Christian Steiner.

**Kontext.** `seg/@n` ist Freitext: `CantusID 006583`, `CanutsID 006583`,
`Ps. 22`, `AH 2-18`, `Unklar`. Ein Skript könnte die Verschreibungen still
glattziehen und hätte mehr Cantus-IDs.

**Entscheidung.** `ableiten.py` erkennt nur das Präfix `CantusID ` und legt
alles andere in `n_roh`. Verschreibungen werden in `pruefen.py` gezählt und
gemeldet und sind Kandidaten für Vermerke (`MASCHINELLE-EDITORIK.md`).

**Alternativen.** Tolerantes Muster (`(?i)ca?n[ut]+s?id`): mehr Treffer, aber
die Zahl »mit Cantus-ID« sagt dann nichts mehr über die Quelle aus, und der
Befund verschwindet.

**Folgen.** Die Zahl der Incipits mit Cantus-ID ist eine Untergrenze. Wer sie
nennt, sagt das dazu.

## ADR-4: Freigabe über Kickoff, Autonomie über Labels

**Datum:** 22.09.2026. **Entschieden von:** Christian Steiner, übernommen aus
`mhdbdb-tei-only` (Betriebsvertrag seit 05.08.2026) und `corema` (Labelschema
seit 24.08.2026).

**Kontext.** Ein Repositorium, an dem Agenten arbeiten, braucht eine Antwort
auf die Frage, was ein Agent allein darf. Ein Zeitplan, der Sessions von selbst
startet, wurde in `corema` am 25.08.2026 verworfen.

**Entscheidung.** Kein Label gibt etwas frei. Der Auftrag kommt je Lauf als
Kickoff-Prompt, der den Betriebsvertrag wörtlich enthält. Die `auto:*`-Labels
sagen, wie viel Klärung ein Issue vorher braucht.

**Alternativen.** Autonomie am Issue selbst freigeben (ein Label ist billig zu
setzen und billig zu vergessen); alles `auto:pair` (dann ist das Repositorium
ein Ordner, kein Arbeitsplatz für Agenten).

**Folgen.** `playbooks/KICKOFF-VORLAGE.md` ist Pflichtlektüre vor jedem Lauf,
und ein Playbook autorisiert nichts.

## ADR-5: Editorische Entscheidungen bleiben beim Menschen

**Datum:** 22.09.2026. **Entschieden von:** Christian Steiner.

**Kontext.** `modell:offen` erlaubt in `corema`, dass ein Frontier-Modell eine
Modellfrage entscheidet, wenn der Auftrag Belege und Lesarten mitbringt. Bei
einem Liber ordinarius ist die Grenze zwischen Datenmodell und Interpretation
schmal: ob eine Variante eine Lesart ist, ist keine Modellfrage.

**Entscheidung.** `modell:offen` gilt hier nur für Fragen an der Datenschicht
(Feldzuschnitt, Konvention, Muster). Alles, was die Transkription, die
Identifikation eines Incipits oder die Zuordnung einer Tradition betrifft, ist
`auto:pair` oder ein Vermerk mit Status `vorgeschlagen`.

**Alternativen.** Dieselbe Regel wie in `corema`: dort sind die Modellfragen
Vokabularfragen (Wikidata-QID je Zutat), hier wären es Lesarten.

**Folgen.** Der Sachverhalt `lesart` in `MASCHINELLE-EDITORIK.md` ist immer
`auto:pair`.
