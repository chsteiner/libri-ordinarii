# Kickoff-Vorlage für autonome Sessions

Eine autonome Session startet nur mit einem Kickoff-Prompt von Christian. Kein
Playbook autorisiert sich selbst. Diese Vorlage sagt, was in den Prompt gehört,
damit die Session nicht auf halbem Weg nachfragen muss; das Nachfragen ist ihr
ja gerade untersagt. Übertragen aus `mhdbdb-tei-only`
(`docs/playbooks/KICKOFF-VORLAGE.md`), die acht Bausteine sind dieselben.

**Die wichtigste Regel dieser Vorlage:** der Betriebsvertrag wird **in den
Prompt kopiert**, nicht verlinkt. `BETRIEBSVERTRAG.md` ist die eine Quelle,
aus der kopiert wird. Redundanz zur Laufzeit ist ein Sicherheitsmerkmal;
Redundanz im Repositorium war die Driftquelle, die diese Trennung überhaupt
nötig gemacht hat.

## Bausteine

### 1. Autorisierung (immer, wörtlich)

Was diese Session darf, und was auch sie nicht darf. Die Freigabe übersteuert
die Regel »kein Push ohne Freigabe« aus `CLAUDE.md` für den genannten Umfang
und nur für ihn: Commits und Pushes auf `claude/*`-Branches, PRs erstellen.
`main` bleibt tabu.

### 2. Der Betriebsvertrag (immer, kopiert)

Der vollständige Inhalt von `BETRIEBSVERTRAG.md`. Wenn er zu lang erscheint:
die Abschnitte 1, 2 und 4 sind der harte Kern und dürfen nie fehlen.

### 3. Der Umfang (immer, konkret)

Welche Issues, in welcher Reihenfolge, je ein Arbeitspaket. Die Auswahl kommt
aus den `auto:*`-Labels, aber sie ist damit noch nicht freigegeben. Was in den
Prompt gehört, ist die geprüfte Auswahl, nicht die Labelabfrage. In eine
autonome Session gehören nur Issues der Stufen `auto:full` und `auto:brief`,
letztere erst, wenn ihre Vorabfragen beantwortet sind und die Antworten unter
den Weichen (4) stehen. `auto:checkin` und `auto:pair` brauchen Christian am
Terminal und passen nicht zu einem Vertrag, der Fragen und Warten untersagt.

### 4. Die Weichen (session-spezifisch)

Fragen, die die Session sonst stellen müsste, was ihr untersagt ist. In
diesem Repositorium typisch:

- **Externe Dienste:** darf die Session den Cantus Index abfragen, mit
  welcher Rate, für welche Stichprobe? Ohne diesen Satz gilt: nein.
- **Handschriften als Dateien oder als Traditionen:** die Antwort für diesen
  Lauf, mit Verweis auf `derived/incipits-felder.md`.
- **`supplied`:** zählt es in diesem Lauf als belegt oder nicht?

### 5. Nicht anfassen (immer)

Die Issues und Bereiche, die diese Session nicht berührt, mit Grund. Dazu
ausdrücklich **die Fallen**: was nach leichtem Einstieg aussieht, sich aber im
eigenen Ticket-Text auf etwas anderes sperrt. In diesem Repositorium immer:
`../cantus/`.

### 6. Vorab getroffene Entscheidungen (wenn es welche gibt)

Richtungsentscheidungen bei mehreren vertretbaren Umsetzungen, je mit einem
Satz Begründung, damit die Session sie nicht neu verhandelt. Die ADRs in
`docs/DECISIONS.md` gelten ohnehin; hier stehen die, die nur für diesen Lauf
gelten.

### 7. Notationsfallen (wenn welche im Spiel sind)

Etwa Vermerk-Nummern, die wie Issue-Nummern aussehen, oder Festcodes, die wie
Cantus-IDs aussehen (beide sind Ziffernfolgen; der Festcode hat acht Stellen,
die Cantus-ID sechs).

### 8. Der Abschluss (immer, wörtlich)

»Unbeschaffbarer Input führt zum dokumentierten Überspringen, nicht zum Warten
und nicht zum Nachfragen.«

## Was diese Vorlage nicht ist

Kein Generator. Der Prompt wird von Hand aus diesen Bausteinen zusammengesetzt.
Abgeschickte Kickoffs werden unter `playbooks/kickoffs/JJJJ-MM-TT-<name>.md`
im Wortlaut abgelegt: Protokolle, keine Vorlagen, weil der darin kopierte
Vertrag ab dem Tag des Abschickens altert.
