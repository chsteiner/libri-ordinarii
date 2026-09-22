# Das TEI der Libri ordinarii

Was in `../cantus/TEIs/` liegt und wie es gebaut ist. Gemessen am 22.09.2026
an `brixen_current_tei.xml` und `salzburg_sal_current_tei.xml` mit einem
Elementinventar, dann gegen alle Dateien durch `scripts/ableiten.py` geprüft.
Die Zahlen stehen in [`../derived/corpus-stats.md`](../derived/corpus-stats.md);
hier steht die Struktur.

## Herkunft

Das Cantus Network (ÖAW, Institut für kunst- und musikhistorische Forschungen,
mit dem Zentrum für Informationsmodellierung Graz; Projektleitung Franz Karl
Praßl und Robert Klugseder, Transkription Gionata Brusa, Modellierung Christian
Steiner) hat die Libri ordinarii der Salzburger Kirchenprovinz in Word
erfasst und nach TEI überführt. Der Word-Workflow ist in
`../cantus/Cantus-Dokumentation.pdf` beschrieben: Formatvorlagen für
Festbezeichnung, Zeiteinheit, Incipit, Neume, Person, Ort, Funktion, dazu eine
Zeichen-Notation für alles, was Word nicht kennt (`|R|` Rasur, `|R::Text|`
Rasur mit Ergänzung, `%D::Text%` Streichung, `$E::Text$` Einfügung,
`|M::Text|` Marginalie, `|I::Kommentar|` Bearbeiterkommentar, `@` fixes
Leerzeichen, `€` Pre-Phrase vor einer Zeiteinheit). Ein Makro hat daraus TEI
erzeugt; `../cantus/xslt/` hält die Nachbearbeitung (IDs, Querverweise,
Incipit-CSV, RDF), `../cantus/print/` die Ausgabe nach LaTeX.

Die Edition steht in GAMS unter `o:cantus.<handschrift>` mit PIDs, Lizenz
CC BY-NC 4.0. Was hier liegt, ist der Stand des GitHub-Repositoriums
`chsteiner/cantus` vom 17.01.2023.

## Eine Datei je Handschrift oder Tradition

Jede Datei `<name>_current_tei.xml` ist ein Liber ordinarius. Die Dateinamen
folgen keiner einheitlichen Regel: `brixen`, `freising`, `moosburg` sind je
eine Handschrift; `salzburg_sal`, `salzburg_ur`, `salzburg_ra`, `salzburg_vo`
sind vier Zeugen einer Tradition mit gemeinsamem Variantenapparat, ebenso die
fünf `passau_*`, die vier `klosterneuburg_knb*`, die drei `emmeram_emm*` und
`seckau1_pac` / `seckau1_se1`. Wer Handschriften zählt, sagt, ob Dateien oder
Traditionen gemeint sind. `emmeram_emm1_NOVARIANTS.xml` ist eine Ableitung
ohne Apparat und wird übersprungen; `AuthorsTract.xml` ist die gemeinsame
Bibliografie der Traktate, auf die `list type="traktate"` per `xml:base`
zeigt.

## Der Header

`teiHeader/@xml:id` ist die Kennung der Handschrift (`brixen`, `salzburg`).
`titleStmt` trägt den Originaltitel mit `pb`, `title type="short"` und
`title type="citation"`, dazu `respStmt` je Rolle. `sourceDesc/msDesc` hält
Signatur und Datierung, `list type="traktate"` die zitierten Traktate
(Durandus, Beleth, Bernold usw.), auf die `quote/@source` im Text verweist.
`facsimile` listet `surface`/`graphic` je Seite mit `@url`.

## Der Text

```
body
└── div                                  ein Fest
    ├── head @xml:id="feast.<Festcode>.<n>" @corresp="#<Festcode>"
    ├── div                              Kommentar zum Fest, ohne @type
    │   └── ab
    │       ├── seg @ana="#person" | "#place"
    │       ├── seg @type="incipit" @xml:id="incipit.<Festcode>.comment.<n>"
    │       └── quote @source="#Bernold" @n="XXX;1003A-B"
    └── div @type="time:1"               eine Hora
        ├── ab @ana="#head"
        │   ├── seg                      Festbezeichnung im Original
        │   └── label @xml:id="office.<Festcode>.<Hora>.<n>" @n="<Hora>"
        └── ab
            └── seg @type="incipit" @xml:id="incipit.<Festcode>.<Hora>.<n>"
                    @ana="#<Gattung>" @n="CantusID <id>" @corresp="<Konkordanzen>"
                    @subtype="supplied"
                └── phr @type="neume"
```

Quer dazu, in Dokumentreihenfolge: `pb @n="25r" @xml:id="<SIGLE>.025r"`,
`milestone @unit="page" @n="25rb"` für Spalten, `metamark @function="variant"
@xml:id="V.<n>"` für den Apparat (umschließt das Wort, auf das sich die
Variante bezieht, oder steht leer an der Stelle), `choice/sic/corr`, `del`,
`add`, `note @type`, `hi @rend`, `gap`, `unclear`.

### Was die Attribute tragen

| Stelle | Attribut | Inhalt | Eigenheit |
|---|---|---|---|
| `head` | `@corresp` | Festcode, acht Ziffern, z. B. `01011000` | `nocdb`, wenn das Fest keinen Code hat |
| `label` | `@n` | Horen-Sigle: `V`, `M`, `L`, `P`, `T`, `S`, `N`, `C` und Sonderformen | die Menge steht in `corpus-stats.md` |
| `seg[@type='incipit']` | `@ana` | Gattung als Sigle mit `#`: `RP`, `RV`, `AN`, `HY`, `PS`, `VS`, `CIT` ... | 85 verschiedene Werte im Bestand (22.09.2026) |
| | `@n` | **Freitext.** Meist `CantusID 006583`, auch mehrere IDs, auch Bibelstellen (`Ps. 22`, `Lc 1`), AH-Nummern (`AH 2-18`), CAO, `Unklar`, `?`, `kein` | `ableiten.py` trennt `cantus_id` von `n_roh`, siehe `OFFENE-FRAGEN.md` |
| | `@corresp` | Konkordanzen als Siglenfolge, z. B. `GBE VHRDFSL` | roh übernommen |
| | `@subtype` | `supplied`: vom Bearbeiter ergänzt, nicht im Original | |
| | `@function` | nur in Salzburg belegt, Bedeutung nicht dokumentiert | `OFFENE-FRAGEN.md` |
| `metamark` | `@function` | immer `variant` | der Apparat liegt in den Dateien einer Tradition identisch vor |

## Die abgeleitete Schicht

`scripts/ableiten.py` liest alle `*_current_tei.xml` und schreibt eine Zeile
je `seg[@type='incipit']` nach `derived/incipits.jsonl`, mit Fest, Hora,
Gattung, Cantus-ID, Konkordanz, Variantenzahl und Folio. Was jedes Feld
bedeutet und welche Zählkonvention gilt, steht in
[`../derived/incipits-felder.md`](../derived/incipits-felder.md). Das Skript
normalisiert nichts: ein verschriebenes `CanutsID` bleibt in `n_roh` und wird
gezählt, denn die Verschreibung ist ein Befund über die Daten und ihre Reparatur
wäre eine Änderung an der Quelle, die hier niemandem zusteht.

## Was das Modell nicht hat

Kein kritischer Apparat nach dem TEI-Modul `textcrit` (`app`/`rdg`), sondern
`metamark`; keine `@ref` auf Normdaten an Personen und Orten; keine Verknüpfung
der Cantus-IDs mit dem Cantus Index außer der Sigle im Attribut; kein Schema,
das die Werteräume von `@ana`, `@n` und `@corresp` prüft (`cantus_schema.xsd`
prüft die Struktur). Jedes dieser vier ist ein Kandidat für ein Issue, keines
für eine stille Korrektur.
