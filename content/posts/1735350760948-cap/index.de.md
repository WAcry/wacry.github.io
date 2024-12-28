---
title: "Tiefe Einblicke in das CAP-Theorem: Entwicklung hochgradig paralleler und hochverfügbarer verteilter Systeme"
date: 2024-12-27
draft: false
description: "Diskussion der Anwendung des CAP-Theorems in verteilten Systemen von der Theorie zur Praxis."
summary: "Diskussion der Anwendung des CAP-Theorems in verteilten Systemen von der Theorie zur Praxis."
tags: [ "Verteilte Systeme", "CAP-Theorem", "Systemdesign", "Konsistenzmodelle" ]
categories: [ "Systemdesign" , "Verteilte Systeme" ]
---

## I. Das CAP-Theorem

### 1.1 Was ist das CAP-Theorem?

Das **CAP-Theorem** wurde im Jahr 2000 von Eric Brewer aufgestellt und besagt im Kern:

- **C (Consistency, Konsistenz)**: Alle Knoten im System sehen zu jedem Zeitpunkt die gleichen Daten. Genauer gesagt, wenn ein Client Daten liest, sollte das Ergebnis, unabhängig davon, von welcher Replik gelesen wird, mit den zuletzt übermittelten Daten übereinstimmen (normalerweise bezieht sich dies auf starke Konsistenz/lineare Konsistenz).
- **A (Availability, Verfügbarkeit)**: Das System kann auch bei Teilausfällen weiterhin normale Dienste anbieten, und jede Anfrage erhält innerhalb einer angemessenen Zeit eine "gültige Antwort" (nicht unbedingt erfolgreich, sondern auch eine korrekte Fehlerantwort).
- **P (Partition tolerance, Partitionstoleranz)**: Das System kann Netzwerkpartitionen tolerieren (Kommunikation zwischen Knoten ist nicht erreichbar), und selbst wenn das Netzwerk aufgeteilt ist, kann das System ein gewisses Maß an Verfügbarkeit oder Konsistenz bieten.

In realen verteilten Umgebungen sind Netzwerkpartitionen unvermeidlich, daher wird **P** im Grunde als "Pflichtoption" angesehen. Wenn eine Netzwerkpartition auftritt, kann das System nicht gleichzeitig die *
*starke Konsistenz** und **hohe Verfügbarkeit** aller Knoten für Daten gewährleisten, sondern muss zwischen C und A abwägen, woraus die beiden Haupttypen **CP** und **AP** hervorgehen.

### 1.2 Einschränkungen des CAP-Theorems

Es ist wichtig zu betonen, dass das CAP-Theorem selbst eine relativ hochrangige Theorie ist, die als konzeptionelle Richtlinie dient und **nicht einfach als "entweder C oder A wählen" verstanden werden sollte**. Es gibt einige häufige Missverständnisse:

1. **C ist nicht unbedingt starke Konsistenz**
   Das C im CAP-Theorem bezieht sich oft auf die strengste Form der Konsistenz (d. h. lineare Konsistenz). In der Praxis gibt es jedoch viele feinere Modelle zur Auswahl, wie z. B. schwache Konsistenz, Read Committed, kausale Konsistenz usw.
2. **Verfügbarkeit ist nicht 0 oder 1**
   Es bedeutet nicht, dass die Verfügbarkeit vollständig geopfert wird, wenn CP gewählt wird, oder dass die Konsistenz nicht gewährleistet ist, wenn AP gewählt wird. Sowohl Verfügbarkeit als auch Konsistenz haben unterschiedliche Spielräume für Kompromisse und Downgrade-Strategien.
3. **Letztendliche Konsistenz** verstößt nicht gegen CAP
   Es ist ein sehr häufiger Kompromiss, bei dem eine geringere Schreibkonsistenz gegen eine höhere Verfügbarkeit und einen höheren Durchsatz eingetauscht wird und die Daten im Hintergrund asynchron konvergieren.

Daher sollte das CAP-Theorem in Kombination mit verschiedenen **Konsistenzmodellen** und **Architekturmustern für hohe Verfügbarkeit** in konkreten Szenarien angewendet werden, um einen echten praktischen Nutzen zu erzielen.

------

## II. Konsistenzmodelle für verteilte Systeme

Die Klassifizierung von Konsistenzmodellen ist sehr vielfältig, aber die gängigen Mainstream-Modelle lassen sich grob in **starke Konsistenz** und **schwache Konsistenz** (einschließlich letztendlicher Konsistenz, kausaler Konsistenz usw.) unterteilen. In diesem Artikel werden hauptsächlich **starke Konsistenz** und **letztendliche Konsistenz** vorgestellt und ihre gängigen Anwendungen im CP- oder AP-Modus erläutert.

### 2.1 Starke Konsistenz

**Starke Konsistenz** (Strong Consistency), auch bekannt als **lineare Konsistenz** (Linearizability), bedeutet, dass, sobald ein Schreibvorgang erfolgreich abgeschlossen wurde, jeder nachfolgende Lesevorgang den aktualisierten Inhalt lesen kann. Das heißt, das System verhält sich nach außen so, als ob alle Operationen seriell ausgeführt würden.

- **Gängige Implementierungen**: Sie beruhen auf synchroner Replikation und einem Quorum-Mechanismus (Mehrheitsprinzip), um sicherzustellen, dass es im System nur einen gültigen Leader gibt, und alle Operationen werden sequenziell in ein Protokoll geschrieben und auf die Mehrheit der Knoten repliziert.
- Vor- und Nachteile:
    - Vorteile: Gewährleistet die strengste Datenkorrektheit, und die gelesenen Daten werden zu keinem Zeitpunkt "zurückgesetzt".
    - Nachteile: Bei Netzwerkstörungen, Partitionen oder Ausfällen des Leaders werden Schreibvorgänge oft blockiert, um die Konsistenz aufrechtzuerhalten, was zu einer geringeren Gesamtverfügbarkeit führt; Leistung und Durchsatz sind ebenfalls relativ geringer.

### 2.2 Letztendliche Konsistenz

**Letztendliche Konsistenz** (Eventual Consistency) ist eine typische Form der schwachen Konsistenz, die nur verlangt, dass, wenn das System keine neuen Aktualisierungen mehr vornimmt, die Daten aller Replikate im Laufe der Zeit allmählich in denselben Zustand konvergieren. Während dieser Zeit können Benutzer beim Lesen von Replikaten veraltete Werte sehen, die aber schließlich konsistent werden.

- **Gängige Implementierungen**: Gossip-Protokoll, asynchrone Replikation mehrerer Replikate, CRDT (Conflict-free Replicated Data Type) usw.
- Vor- und Nachteile:
    - Vorteile: Hohe Verfügbarkeit, hoher Durchsatz, geringe Latenz bei Schreibvorgängen, hohe Toleranz gegenüber Netzwerkpartitionen.
    - Nachteile: Es ist notwendig, kurzzeitige Dateninkonsistenzen zu tolerieren, die Anwendungslogik ist komplexer und es kann erforderlich sein, Konflikte zu erkennen und zusammenzuführen.

------

## III. Gängige Konsistenzprotokolle und -algorithmen

Um die Konsistenz zwischen den Replikaten eines verteilten Systems zu gewährleisten, hat die Branche viele klassische Algorithmen und Protokolle entwickelt. Im Folgenden werden einige davon kurz vorgestellt:

### 3.1 Paxos

Paxos ist ein Algorithmus für verteilte Konsistenz, der in den 1990er Jahren von Leslie Lamport entwickelt wurde und hauptsächlich zur Implementierung starker oder linearer Konsistenz verwendet wird.

- **Grundprinzip**: Durch die Aufteilung in Rollen (Proposer, Acceptor, Learner) werden mehrere Abstimmungsrunden durchgeführt, um zu entscheiden, ob eine Operation oder ein Wert von der Mehrheit der Knoten akzeptiert wird.
- Vor- und Nachteile:
    - Vorteile: Kann auch bei Netzwerkpartitionen und Knotenausfällen eine Einigung erzielen und ist sehr sicher.
    - Nachteile: Komplex in der Implementierung, schwierig zu debuggen und zu beheben, und die Leistung ist durch mehrere Abstimmungsrunden eingeschränkt. In der Industrie werden häufiger Varianten davon verwendet (Multi-Paxos usw.).

### 3.2 Raft

Raft wurde 2013 offiziell vorgestellt und zielt darauf ab, **die Implementierung und das Verständnis zu vereinfachen, während gleichzeitig die gleiche Sicherheit wie Paxos gewährleistet wird**. Es verwendet eine stabile *
*Leader-Rolle**, um die Protokollreplikation und die Fehlerbehebung zentralisiert durchzuführen:

- **Schlüsselphasen**: Leader-Wahl (Leader Election), Protokollreplikation (Log Replication), Sicherheit (Safety) usw.
- **Gängige Anwendungen**: Etcd, Consul, TiKV, LogCabin usw. basieren alle auf Raft, um eine stark konsistente Replikation zu implementieren.
- Vor- und Nachteile:
    - Vorteile: Relativ einfach zu verstehen, weniger Code für die Implementierung; gute Leistung für kleine und mittlere Cluster.
    - Nachteile: Abhängig vom Hauptknoten (Leader), Ausfälle oder Partitionen des Hauptknotens verursachen eine kurzzeitige Blockierung des Schreibens; bei großen Clustern oder standortübergreifenden Bereitstellungen werden Latenz und Verfügbarkeit beeinträchtigt.

### 3.3 Gossip-Protokoll

Das Gossip-Protokoll (Klatschprotokoll) ist kein traditionelles Konsensprotokoll, sondern wird hauptsächlich in dezentralen Szenarien verwendet, um Metadaten oder Statusinformationen durch zufällige Interaktion zwischen Knoten auszutauschen und so im gesamten Netzwerk zu verbreiten und zu konvergieren.

- **Merkmale**: Dezentralisiert, geringer Aufwand, periodischer und zufälliger Nachrichtenaustausch zwischen Knoten.
- **Gängige Anwendungen**: Cassandra, Riak, verteiltes Mitgliedschaftsmanagement (z. B. Serf) usw., die zur Implementierung von letztendlicher Konsistenz, Replikatsynchronisation usw. verwendet werden.
- Vor- und Nachteile:
    - Vorteile: Gute Skalierbarkeit, einfach zu implementieren, geeignet für Szenarien, in denen die Konsistenzanforderungen nicht hoch und die Skalierbarkeitsanforderungen hoch sind.
    - Nachteile: Schwache Konsistenzgarantie, erfordert fortgeschrittenere Methoden zur Konfliktbehandlung (z. B. CRDT, Versionsnummernzusammenführung usw.), um Konflikte letztendlich zu lösen.

### 3.4 2PC / 3PC

In verteilten Transaktionsszenarien sind die gängigen Commit-Protokolle **2PC (Two-phase Commit)** und **3PC (Three-phase Commit)**:

- **2PC**: Der Koordinator benachrichtigt alle Teilnehmer über "Prepare", und wenn alle erfolgreich sind, wird "Commit" gesendet, andernfalls "Abort".
- **3PC**: Fügt dem 2PC eine weitere Phase hinzu, um die Blockierung durch Single-Point-of-Failure zu reduzieren, ist aber komplexer zu implementieren und weist immer noch Probleme mit der Nichtverfügbarkeit in extremen Netzwerkpartitionen oder Ausfallszenarien auf.
- Vor- und Nachteile:
    - Vorteile: Leicht zu verstehen, klare Transaktionssemantik, weit verbreitet in verteilten Datenbanken, Message Queues usw.
    - Nachteile: Starke Abhängigkeit vom Koordinator, Blockierungsrisiko; Transaktionen können bei längeren Netzwerkpartitionen möglicherweise nicht fortgesetzt werden.

------

## IV. Die beiden wichtigsten CAP-Optionen: CP und AP

Nachdem wir **P** als "Pflichtattribut" festgelegt haben, muss ein verteiltes System, wenn es bei Netzwerkpartitionen weiterhin Dienste anbieten möchte, zwischen **C** und **A** wählen. Das gängige Systemdesign ist daher in zwei Lager unterteilt: **CP** und **AP**.

### 4.1 CP-System

**CP (Consistency + Partition tolerance)**: Wenn eine Netzwerkpartition auftritt, wählt das System **die Priorität der Konsistenz** und **opfert bei Bedarf die Verfügbarkeit**.

- Typische Implementierungen:
    - Mehrheitskonsens (Paxos, Raft usw.), bei dem mehr als die Hälfte der Knoten aktiv sein und sich einigen müssen, um das Schreiben zu erlauben.
    - Wenn kein Quorum erreicht werden kann oder der Hauptknoten ausfällt, blockiert oder verweigert das System Schreibvorgänge, um zu verhindern, dass ein Split-Brain zu Dateninkonsistenzen führt.
- Gängige Anwendungen:
    - Zookeeper, Etcd, Consul, verteilte Lock-Dienste, verteiltes Metadatenmanagement usw.
    - Kernprozesse für Finanztransaktionen, Bankbuchhaltungssysteme und andere Szenarien mit hohen Konsistenzanforderungen.
- Merkmale:
    - Strenge Datensicherung: Lieber herunterfahren, als Dual-Master oder Datenchaos zu verursachen.
    - Opfert ein gewisses Maß an Verfügbarkeit: Bei Netzwerkpartitionen oder Failover gibt es ein Zeitfenster, in dem der Dienst nicht verfügbar ist oder Schreibvorgänge abgelehnt werden.

### 4.2 AP-System

**AP (Availability + Partition tolerance)**: Wenn eine Netzwerkpartition auftritt, wählt das System **die Priorität der Verfügbarkeit** und **lockert gleichzeitig die Konsistenz**.

- Typische Implementierungen:
    - Letztendliche Konsistenz, Multi-Master-Replikation, Gossip-Protokoll, Dynamo-ähnliche Strategien für einstellbare Konsistenz usw.
- Gängige Anwendungen:
    - NoSQL-Datenbanken (Cassandra, Riak, DynamoDB usw.), verteilte Caching-Systeme (Redis Cluster) usw.
    - Soziale Netzwerke, Protokollerfassung, Empfehlungssysteme und andere Dienste, die eine hohe Verfügbarkeit und einen hohen Durchsatz erfordern und bei denen die Datenkonsistenz relativ gering ist.
- Merkmale:
    - Auch bei Partitionen akzeptieren alle Knoten weiterhin Lese- und Schreibanfragen, um sicherzustellen, dass das System "so weit wie möglich verfügbar" ist.
    - Daten können kurzzeitig inkonsistent sein, werden aber durch asynchrone Synchronisation, Konfliktzusammenführung usw. im Hintergrund schrittweise konvergiert.

------

## V. Wie wählt man zwischen CP und AP?

In realen, groß angelegten verteilten Systemen wird **selten nur ein einziges Modell verwendet**, sondern verschiedene Daten oder Geschäftsszenarien werden in Schichten verarbeitet, um ein optimales Gleichgewicht zwischen **Konsistenz** und **Verfügbarkeit** zu erreichen.

1. **Kern-Daten wählen CP**
    - Wie z. B. Kontostände von Benutzern, Auftragszahlungen, Finanztransaktionsflüsse usw., die sehr hohe Konsistenzanforderungen haben.
    - Toleriert kurzzeitige Schreibsperren aufgrund von Netzwerkstörungen, aber keine Fehler bei Salden oder Transaktionsbeträgen.
2. **Rand- oder Cache-Daten wählen AP**
    - Wie z. B. der Cache von Produktdetailseiten, Benutzerverhaltensprotokolle, Empfehlungskandidatenlisten usw., die geringere Konsistenzanforderungen haben.
    - Legt mehr Wert auf hohe Parallelität und hohe Verfügbarkeit und kann eine gewisse Zeitverzögerung bei Aktualisierungen oder Dirty Reads tolerieren.

Viele Internetunternehmen verwenden eine **Hybridarchitektur**: Kern-Transaktionsprozesse verwenden CP-Speicher (z. B. verteilte relationale Datenbanken oder verteilter Speicher mit starker Konsistenz); Peripheriegeschäfte oder "Read-Heavy"-Szenarien verwenden AP-Speicher oder Caching-Lösungen.

------

## VI. Wie erreichen CP und AP hohe Parallelität und letztendliche Konsistenz?

### 6.1 Wie bewältigen CP-Systeme hohe Parallelität?

Obwohl Konsensprotokolle bei einer großen Anzahl von Knoten in einem einzelnen Cluster und einer großen Anzahl von Schreibanfragen mit hoher Latenz und geringem Durchsatz konfrontiert sind, können Parallelität und Skalierbarkeit dennoch durch die folgenden Mittel verbessert werden:

1. Batch-Lese- und -Schreibvorgänge
    - Mehrere Schreibvorgänge werden auf der Client- oder Zwischenschicht gebündelt und einmalig auf den Leader-Knoten geschrieben, wodurch Netzwerk-Roundtrips und Protokollrunden reduziert werden.
2. Datenbank- und Tabellenpartitionierung & Multi-Cluster
    - Daten werden logisch oder per Hash in mehrere Cluster (Sharding) aufgeteilt, wobei jedes Cluster intern weiterhin das CP-Protokoll ausführt; Anfragen werden über die Routing- oder Proxy-Schicht auf verschiedene Shards verteilt.
    - Verbessert die gesamte Parallelität und begrenzt die Auswirkungen von Fehlern auf einen einzelnen Shard.

> Der Durchsatz eines einzelnen Shard-Clusters in einem CP-System ist oft 2 bis 10 Mal geringer als der eines AP-Systems.

### 6.2 Wie stellen AP-Systeme die letztendliche Konsistenz sicher?

AP-Systeme können in der Regel einen sehr hohen Schreibdurchsatz und eine hohe Leseverfügbarkeit bieten, aber die Konsistenz wird gelockert, so dass im Hintergrund oder in der Geschäftslogikschicht eine Konsistenzkonvergenz gewährleistet werden muss:

1. Versionsnummer (Vektor-Uhr) oder logischer Zeitstempel
    - Weist jedem Aktualisierungsvorgang eine Versionsnummer zu (oder basierend auf Lamport Clock / Hybrid Clock), um Konflikte zusammenzuführen oder eine auf Zeitstempeln basierende Gewinnstrategie (Last Write Wins) zu verwenden.
2. Gossip-Protokoll / Anti-Entropie-Mechanismus
    - Knoten tauschen regelmäßig die neuesten Daten oder Metadaten aus und führen bei Konflikten eine Zusammenführung durch.
3. Einstellbare Konsistenzstrategie
    - Repräsentiert durch das Dynamo-Modell können Clients Parameter wie `R` und `W` konfigurieren (z. B. Schreiben in die Mehrheit, Replikatsbestätigung), um die Konsistenz und Verfügbarkeit flexibel anzupassen.
4. Benutzerdefinierte Strategie zur Konfliktlösung
    - Kombiniert die Geschäftssemantik zur Zusammenführung, z. B. Warenkörbe werden mit "Vereinigung" zusammengeführt, Zähler verwenden CRDT (G-Zähler, PN-Zähler usw.), um die Monotonie der Daten zu gewährleisten.

------

## VII. Implementierung starker Konsistenz über Shards in CP

Wie in Kapitel VII erwähnt, kann **durch Datenbank- und Tabellenpartitionierung (Sharding)** der Druck eines einzelnen CP-Clusters auf mehrere Subcluster "aufgeteilt" werden, um eine höhere Parallelität zu unterstützen. Wenn jedoch Transaktionen über Shards hinweg ausgeführt werden müssen (d. h. Aktualisierungen, die mehrere Datenbanken oder Tabellen betreffen), steht man immer noch vor der Herausforderung der **Multi-Shard-Konsistenz**. Es gibt in der Regel die folgenden Ansätze:

1. **Verteilte Transaktionen: 2PC / 3PC**
    - Wenn eine Anwendung atomare Aktualisierungen über mehrere Shards hinweg benötigt, werden in der Regel verteilte Transaktionsprotokolle (z. B. 2PC, 3PC) verwendet, um die Commits oder Rollbacks der einzelnen Shards zu koordinieren.
    - Probleme und Gegenmaßnahmen:
        - 2PC/3PC sind beide von einem Koordinator-Knoten abhängig, der zu einem Single-Point-of-Failure werden kann.
        - In extremen Fällen von schweren Netzwerkpartitionen oder Ausfällen des Koordinators kann es zu Blockierungen kommen.
        - Im Allgemeinen werden Master-Slave-Umschaltung, Heartbeat-Erkennung und Timeout-Mechanismen, idempotente Wiederholungen, MVCC usw. verwendet, um die Auswirkungen von Blockierungen und Dateninkonsistenzrisiken zu reduzieren.
2. **Zellbasierte Architektur**
    - Unterteilt die Dienste in mehrere autonome Einheiten, wobei die Daten in jeder Einheit in derselben Shard-Menge liegen, um sicherzustellen, dass die meisten Transaktionen nur in einer einzigen Einheit abgeschlossen werden und die Anzahl der Shard-übergreifenden Operationen reduziert wird.
    - An den Einheitsgrenzen werden asynchrone oder letztendliche Konsistenzmechanismen für den Datenaustausch verwendet, um sowohl eine hohe Gesamtverfügbarkeit als auch Konsistenz zu gewährleisten.
3. **Globale verteilte Datenbank + globales Konsensprotokoll**
    - Beispielsweise implementiert Google Spanner eine stark konsistente Replikation über Paxos auf jedem Shard und verwendet die TrueTime-API, um globale Zeitstempel bereitzustellen, die die Konsistenz über Shards hinweg gewährleisten.
    - Diese Lösung ist extrem komplex zu implementieren, kann aber im globalen Maßstab nahezu stark konsistente verteilte Transaktionsfunktionen bereitstellen.

> **Zusammenfassung**: Für Shard-übergreifende Transaktionen, die eine strenge starke Konsistenz erfordern, ist **2PC/3PC + Koordinator**
> immer noch eine gängige Lösung, und die Wahrscheinlichkeit von Ausfällen wird durch eine möglichst hohe Verfügbarkeit des Koordinators reduziert. In der Praxis sollte man jedoch versuchen, Shard-übergreifende Schreibvorgänge zu minimieren oder die meisten Transaktionen durch eine zellbasierte Denkweise auf einen einzigen Shard-Bereich zu beschränken, um die Systemkomplexität zu reduzieren.

------

## VIII. Diskussion berühmter Fälle

Im Folgenden werden einige in der Branche häufig erwähnte verteilte Systeme kurz diskutiert, um zu sehen, welche Kompromisse sie bei CAP eingehen und wie sie implementiert werden:

1. **Google Spanner**
    - Ein typisches **CP**-System (das sogar die Illusion von "CA" erzeugen kann, die oft von Außenstehenden wahrgenommen wird, aber im Wesentlichen immer noch einen Teil der Verfügbarkeit opfern muss).
    - Verwendet die von TrueTime bereitgestellten externen präzisen Zeitstempel + Paxos-Replikation innerhalb jedes Shards, um eine starke Konsistenz über Rechenzentren hinweg zu gewährleisten.
    - Geeignet für globale Finanztransaktionen oder Szenarien mit hohen Konsistenzanforderungen, aber die Infrastrukturkosten sind extrem hoch.
2. **BigTable / HBase**
    - Oberflächlich betrachtet eher **CP**, wobei die Konsistenz der Metadaten zwischen RegionServer und Master durch verteilte Koordination gewährleistet wird.
    - Tatsächlich kann der Lese- und Schreibpfad jedoch auch durch asynchrone Replikation mehrerer Replikate ein gewisses Maß an hoher Verfügbarkeit bieten, und die Lesekonsistenz kann je nach Anwendungsanforderungen angepasst werden.
3. **AWS DynamoDB**
    - Tendenziell **AP**, das frühe Design wurde von der Dynamo-Veröffentlichung inspiriert und die Konsistenzstufe kann durch Parameter wie `R` und `W` angepasst werden.
    - Bietet standardmäßig eine extrem hohe Verfügbarkeit und letztendliche Konsistenz, kann aber auch "starkes Lesen" aktivieren (garantiert aber nur eine starke Konsistenz für eine einzelne Partition, nicht unbedingt über Partitionen hinweg).
4. **Cassandra**
    - Ebenfalls **AP**-orientiert, verwendet das zugrunde liegende Gossip-Protokoll, um den Topologiezustand der Knoten zu verwalten.
    - Die Lese- und Schreibkonsistenz kann durch die Anzahl der Lese- und Schreibreplikate `R` / `W` konfiguriert werden, um einen reibungslosen Übergang von der letztendlichen Konsistenz zu einer stärkeren Konsistenz zu erreichen.

> **Vergleich zeigt**: In der Praxis gibt es kein absolutes "AP oder CP", sondern eher eine Mischung aus verschiedenen Konsistenzstrategien; die meisten Systeme bieten ein gewisses Maß an einstellbarer Konsistenz, um sich an verschiedene Anwendungsszenarien anzupassen.

------

## IX. Zusammenfassung

1. **Das CAP-Theorem ist keine Einheitslösung**
    - In realen verteilten Systemen kann man nicht einfach sagen: "Ich wähle C und verzichte auf A" oder "Ich wähle A und verzichte auf C".
    - In der Branche ist es üblicher, für verschiedene Datendimensionen und verschiedene Operationstypen flexibel den **CP**- oder **AP**-Modus zu wählen, und sogar innerhalb desselben Systems werden für verschiedene Tabellen/Funktionen unterschiedliche Fehlertoleranz- und Konsistenzstrategien verwendet.
2. **AP ist nicht absolut 100 % verfügbar**
    - Beispielsweise können Cassandra, DynamoDB usw. bei extremen Netzwerkpartitionen oder dem Ausfall einer großen Anzahl von Knoten ebenfalls Anfragen nicht erfüllen.
    - AP-Systeme sind so konzipiert, dass sie "schreiben, solange ein Replikat schreibbar ist", und opfern einen Teil der Konsistenzgarantie, um eine relativ höhere Verfügbarkeit und einen höheren Durchsatz zu erreichen.
3. **CP kann auch versuchen, eine hohe Verfügbarkeit zu erreichen**
    - Paxos/Raft können unter normalen Bedingungen auch eine Verfügbarkeit von 99,99 % oder sogar mehr bieten, erfordern aber mehr Netzwerk-, Hardware- und Engineering-Kosten, und bei extremen Netzwerkpartitionen kann es immer noch zu Blockierungen beim Schreiben und zum Verlust der Verfügbarkeit kommen, um die Konsistenz aufrechtzuerhalten.
4. **Hybridarchitektur ist der Mainstream**
    - Kern-Transaktionsszenarien bestehen auf starker Konsistenz (CP), während periphere Hilfsszenarien oder Caching-Kanäle schwache Konsistenz (AP) verwenden, wobei beide zusammenarbeiten.
    - Es ist notwendig, die Geschäftstoleranz, die Netzwerkumgebung, die Kosteninvestitionen und die technischen Ressourcen des Teams zu berücksichtigen, um eine umfassende Entscheidung zu treffen.

Das CAP-Theorem bietet einen hochrangigen Denkrahmen für das Design verteilter Systeme und hilft uns, angesichts der unvermeidlichen Realität von Netzwerkpartitionen rationale Entscheidungen zu treffen. In der Praxis ist es notwendig, sich auf umfassendere **Konsistenzmodelle**, **Konsensprotokolle**, **Replikationsmechanismen mit mehreren Replikaten** und die technische Praxis (Notfallwiederherstellung, Downgrade, Idempotenz, Konfliktzusammenführung usw.) zu stützen, um Konsistenz und Verfügbarkeit in Einklang zu bringen.