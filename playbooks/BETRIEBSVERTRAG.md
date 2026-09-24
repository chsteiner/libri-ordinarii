# Betriebsvertrag der autonomen Sessions

Der Teil des Vertrags, der für **alle** autonomen Sessions in diesem
Repositorium gleich lautet. Übertragen aus `mhdbdb-tei-only`
(`docs/playbooks/BETRIEBSVERTRAG.md`, dort seit dem 05.08.2026 in Betrieb)
und an ein Repositorium angepasst, das keine Website, keine Tests in einem
Browser und keine eigene Quelle hat. Was hier anders lautet als dort, sagt es
dazu.

**Dieser Vertrag autorisiert nichts.** Er beschreibt, was gilt, *nachdem* ein
Kickoff-Prompt eine Session eröffnet hat. Ohne Kickoff läuft keine Session;
die Vorlage dafür steht in `KICKOFF-VORLAGE.md`. Weil der Kickoff die Regeln
wörtlich mitbringt, sind sie zur Laufzeit im Kontext, ohne dass jemand eine
zweite Datei öffnen muss. Ein Verweis wäre ein Ladevorgang, der ausfallen
kann, ohne dass es jemand merkt.

## 1. Was ohne ausdrückliche Freigabe tabu bleibt

1. **Kein Push nach `main`.** Ergebnisse sind PRs, die Christian reviewt. Die
   Ausnahme ist eine Merge-Session, deren Kickoff die Merge-Autorisierung
   ausdrücklich enthält; auch sie merged nur, sie pusht nicht direkt.
2. **Kein Force-Push nach `main`,** in keiner Session, unter keinen Umständen.
   Auf `claude/*`-Branches ist `--force-with-lease` nach einem Rebase Standard.
3. **Issues werden nie von der Session geschlossen,** nur per `Closes #N` im
   PR-Body beim Merge, und nur bei Issues, die keine fachliche Abnahme
   brauchen (Regel 22).
4. **Keine Kontaktaufnahme mit Externen:** nicht mit den Herausgebern der
   Edition (ÖAW, Cantus Network), nicht mit dem Cantus Index, nicht mit den
   Herausgebenden des Sonderbands. Entwürfe für sie landen als Text im Issue.
5. **Keine Änderung in `../cantus/`.** Das ist die Quelle und ein fremdes
   Repositorium. Ein Korrekturvorschlag ist ein Vermerk
   (`docs/MASCHINELLE-EDITORIK.md`), und sein Status bleibt `vorgeschlagen`.
   *Neu gegenüber `mhdbdb-tei-only`, wo die Session den Korpus ändern darf,
   weil das Repositorium ihn besitzt.*

## 2. Wie committet und gestaged wird

6. **Nur benannte Dateien stagen, nie `git add -A` oder `git add .`.**
   Parallele Sessions teilen den Arbeitsbaum und damit den Index; ein
   pauschales Staging sammelt fremde Arbeit ein.
7. **Jede Session in ihrem eigenen Worktree**, angelegt beim Start mit
   `claude --bg --name <name> --worktree <name>` und damit unter
   `.claude/worktrees/`. Der Hauptordner bleibt Referenz und wird nicht als
   Arbeitsplatz benutzt.
8. **Die Branch-Basis wird gemessen, nicht am Namen abgelesen**, vor dem
   ersten eigenen Commit: `git rev-list --count "origin/main...HEAD"` und
   `git rev-list --count "origin/main..main"` müssen beide 0 sein.
9. **`derived/` wandert im selben Commit wie das Skript, das es erzeugt**,
   und zwar die beiden Markdown-Dateien; die JSONL ist gitignoriert (ADR-1).
   Ein Commit, der `scripts/` ändert und `derived/` nicht, sagt im Body,
   warum.

## 3. Wie kommuniziert wird

10. **Höchstens ein sachlicher Statuskommentar pro Issue.**
11. **Nicht fragen, nicht warten.** Alles Nötige liegt im Repositorium und in
    den Issue-Threads (`gh issue view N --json title,body,comments`). Nur
    nachweislich Unbeschaffbares wird im Abschlussreport dokumentiert
    übersprungen. **Zu jedem angefassten Issue werden die Kommentare gelesen,
    nicht nur der Body.** Der Body ist der älteste Text im Ticket, und in
    einem laufenden Projekt ist der älteste Text der unwahrscheinlichste.
12. **Stil:** keine Emoji, keine Gedankenstriche in Prosa, echte Umlaute.
    Deutsch in Docs, Issues und Commits; Latein und Siglen wie in der Quelle.

## 4. Was vor jedem Push passiert

13. **Review vor dem ersten Push jedes PRs**, mit dem `fable-reviewer`, wenn
    verfügbar (nicht dem `fable-advisor`, der ist der Berater für offene
    Entwurfsfragen). Mitgeben: Branch, Basis, Ziel in einem Satz, Nummer der
    Review-Runde, ab Runde 2 die Vorrunden-Befunde. Bei einem Diff, der etwas
    repariert, zusätzlich die Frage: **was hat diese Änderung wahr gemacht,
    das vorher falsch sein konnte?** Stellt ein Fix eine Invariante her,
    verliert jede Prüfung ihren Gegenstand, die auf deren Gegenteil beruhte.
14. **Jeder Befund wird nachgemessen, bevor er übernommen wird**, auch der
    eines Reviewers und auch der eines Bots. Er ist selbst eine Behauptung,
    und eine ungeprüfte Korrektur einer ungeprüften Zahl ist schlimmer als die
    ursprüngliche, weil sie glaubwürdiger aussieht.
15. **Ab Review-Runde 3 wird nur noch auf Verhaltensbefunde reagiert.**
    Formulierungsfragen werden durch Kürzen erledigt, nicht durch Diskussion.
16. **Verifikation:** `python scripts/ableiten.py` und dann
    `python scripts/pruefen.py`, in dieser Reihenfolge, aus der
    Repositoriumswurzel. Die `ERGEBNIS`-Zeile ist das Ergebnis und gehört
    unverändert in den PR. *An die Stelle von `npm test` und der
    Chrome-Verifikation aus `mhdbdb-tei-only`; hier gibt es nichts zu
    rendern.*
17. **Jede Zahl im PR-Body nennt ihre Zählkonvention**
    (`derived/incipits-felder.md`).

## 5. Was in Tickets wandert und was nicht

18. **Fixes direkt umsetzen.** Ein Issue entsteht nur, wenn eine
    **Entscheidung** nötig ist, die die Session nicht treffen darf, wenn ein
    **Mensch** gebraucht wird, oder wenn es ein **eigenes Arbeitspaket** ist
    (mehr als ein halber Tag). Alles andere wird sofort behoben oder
    verworfen.
19. **Ein Vermerk ist kein Fix.** Was die Quelle betrifft, wird nie »direkt
    umgesetzt«, sondern als Vermerk mit Status `vorgeschlagen` abgelegt, auch
    wenn es offensichtlich ist. *Neu, aus Regel 5.*

## 6. Am Ende jeder Session

20. **Ein Handoff-Eintrag in `journal.md`**: Stand, Entschieden, Offen,
    Verworfen, Geprüft. Der jüngste Eintrag ist der Einstieg der nächsten
    Session.
21. **Jeder eigene Fehler, dessen Lehre schon dokumentiert war, bekommt eine
    Zeile in `fehlerjournal.md`**, mit Datum, was passiert ist, welche Lehre
    nicht gegriffen hat und wo sie steht. Bei der dritten Zeile zu derselben
    Lehre wird nicht mehr gezählt, sondern ein Mechanismus vorgeschlagen.

## 7. Wer abnimmt

22. **Fachliche Abnahme ist eine eigene Rolle, und sie ist unbesetzt.** Ein
    Issue, dessen Ergebnis eine Aussage über das liturgische Material trägt,
    gilt erst als erledigt, wenn eine Fachperson es abgenommen hat. Ein
    gemergter PR ist keine Abnahme und `Closes #N` auch nicht; solche Issues
    bleiben nach dem Merge offen. Christians Review nach Regel 1 prüft die
    technische Seite und ersetzt die Abnahme nicht. Wer abnimmt, begründet im
    Issue, was übernommen und was verworfen wird: die Begründung ist das
    Signal, an dem sich die nächste Session ausrichtet, nicht die Zahl der
    Runden. Solange niemand benannt ist, sagt der Abschlussreport, welche
    Issues auf eine Abnahme warten. *Übernommen aus `mhdbdb-tei-only`
    (Regel 17, Abnahme durch die Fachexpertin), bei der ersten Übertragung am
    22.09.2026 entfallen und am 24.09.2026 zurückgeholt.*
