---
title: "Analisi Approfondita del Teorema CAP: Creare Sistemi Distribuiti ad Alta Concorrenza e Alta Disponibilità"
date: 2024-12-27
draft: false
description: "Discussione dall'aspetto teorico a quello pratico dell'applicazione del teorema CAP nei sistemi distribuiti."
summary: "Discussione dall'aspetto teorico a quello pratico dell'applicazione del teorema CAP nei sistemi distribuiti."
tags: [ "Sistemi distribuiti", "Teorema CAP", "Progettazione di sistemi", "Modelli di coerenza" ]
categories: [ "Progettazione di sistemi" , "Sistemi distribuiti" ]
---

## I. Il Teorema CAP

### 1.1 Cos'è il Teorema CAP

Il **Teorema CAP** è stato proposto da Eric Brewer nel 2000, e il suo concetto fondamentale è:

- **C (Consistency, Coerenza)**: Tutti i nodi del sistema vedono gli stessi dati nello stesso momento. Più precisamente, quando un client legge i dati, indipendentemente dalla replica da cui legge, il risultato dovrebbe essere coerente con i dati più recenti (solitamente si riferisce a coerenza forte/coerenza lineare).
- **A (Availability, Disponibilità)**: Il sistema può ancora fornire servizi normali anche in caso di guasti parziali, e ogni richiesta può ottenere una "risposta valida" in un tempo ragionevole (non necessariamente sempre positiva, ma anche risposte di errore corrette).
- **P (Partition tolerance, Tolleranza alle partizioni)**: Il sistema può tollerare le partizioni di rete (comunicazione non raggiungibile tra i nodi), e anche se la rete si divide, il sistema può fornire un certo grado di disponibilità o coerenza.

In un ambiente distribuito reale, le partizioni di rete sono inevitabili, quindi **P** è fondamentalmente considerata un'opzione "obbligatoria". Quando si verifica una partizione di rete, il sistema non può garantire contemporaneamente la **forte coerenza** e l'**alta disponibilità** dei dati su tutti i nodi, e può solo scegliere tra C e A, da cui derivano i due tipi principali **CP** e **AP**.

### 1.2 Limiti del Teorema CAP

È necessario sottolineare che il Teorema CAP è di per sé una teoria di livello relativamente alto, utilizzata come guida concettuale, e **non può essere semplicemente inteso come "o si sceglie C o si sceglie A"**. Esistono alcuni malintesi comuni:

1. **C non è necessariamente una forte coerenza**
   La C nel Teorema CAP si riferisce spesso alla coerenza nel senso più stretto (cioè la coerenza lineare). Tuttavia, nei sistemi reali, abbiamo molti modelli più granulari tra cui scegliere, come la coerenza debole, la lettura confermata (Read Committed), la coerenza causale (Causal Consistency), ecc.
2. **La disponibilità non è 0 o 1**
   Non significa che se si sceglie CP, la disponibilità sia completamente sacrificata; o se si sceglie AP, la coerenza non sia affatto garantita. Sia la disponibilità che la coerenza hanno diversi gradi di compromesso e strategie di downgrade.
3. **La coerenza finale** non viola il CAP
   È una soluzione di compromesso molto comune, che scambia una minore coerenza di scrittura con una maggiore disponibilità e throughput, e converge i dati in background in modo asincrono.

Pertanto, il Teorema CAP dovrebbe essere combinato con vari **modelli di coerenza** e **modelli di architettura ad alta disponibilità** in scenari specifici, per generare un vero valore di guida pratica.

------

## II. Modelli di Coerenza nei Sistemi Distribuiti

La classificazione dei modelli di coerenza è molto ricca, ma i modelli principali comuni possono essere suddivisi in: **forte coerenza** e **debole coerenza** (che include la coerenza finale, la coerenza causale, ecc.). Questo articolo introduce principalmente la **forte coerenza** e la **coerenza finale**, e spiega le loro applicazioni comuni in modalità CP o AP.

### 2.1 Forte Coerenza

La **forte coerenza (Strong Consistency)**, nota anche come **coerenza lineare (Linearizability)**, si riferisce al fatto che una volta che un'operazione di scrittura viene completata e restituisce successo, qualsiasi operazione di lettura successiva può leggere il contenuto aggiornato. In altre parole, il sistema si comporta come se tutte le operazioni fossero state eseguite in serie.

- **Implementazione comune**: Si basa sulla replica sincrona e su un meccanismo di arbitraggio (maggioranza), e utilizza protocolli (come Paxos/Raft) per garantire che ci sia un solo leader (Leader) valido nel sistema, e tutte le operazioni vengono scritte nel log in ordine e replicate sulla maggior parte dei nodi.
- Vantaggi e svantaggi:
    - Vantaggi: Garantisce la correttezza dei dati più rigorosa, e i dati letti in qualsiasi momento non "tornano indietro".
    - Svantaggi: In caso di fluttuazioni di rete, partizioni o guasti del leader, per mantenere la coerenza, le operazioni di scrittura vengono spesso bloccate, con conseguente diminuzione della disponibilità complessiva; anche le prestazioni e il throughput sono relativamente inferiori.

### 2.2 Coerenza Finale

La **coerenza finale (Eventual Consistency)** è una forma tipica di coerenza debole, che richiede solo che se il sistema non ha più nuove operazioni di aggiornamento, con il passare del tempo, i dati di tutte le repliche convergeranno gradualmente allo stesso stato. Durante questo periodo, gli utenti che leggono i dati della replica potrebbero vedere valori obsoleti, ma alla fine diventeranno coerenti.

- **Implementazione comune**: Protocollo Gossip, replica asincrona multi-replica, CRDT (Conflict-free Replicated Data Type), ecc.
- Vantaggi e svantaggi:
    - Vantaggi: Alta disponibilità, alto throughput, bassa latenza di scrittura, alta tolleranza alle partizioni di rete.
    - Svantaggi: È necessario tollerare l'incoerenza dei dati per un breve periodo, la logica dell'applicazione è più complessa e potrebbe essere necessario eseguire il rilevamento e l'unione dei conflitti.

------

## III. Protocolli e Algoritmi di Coerenza Comuni

Per mantenere la coerenza tra le repliche dei sistemi distribuiti, l'industria ha proposto molti algoritmi e protocolli classici. Di seguito è riportata una breve introduzione ad alcuni di essi:

### 3.1 Paxos

Paxos è un algoritmo di coerenza distribuita proposto da Leslie Lamport negli anni '90, utilizzato principalmente per implementare una forte coerenza o coerenza lineare.

- **Principio di base**: Attraverso la divisione dei ruoli (Proponente Proposer, Accettatore Acceptor, Apprendista Learner), vengono eseguite più tornate di votazione per decidere se un'operazione o un valore viene accettato dalla maggior parte dei nodi.
- Vantaggi e svantaggi:
    - Vantaggi: Può raggiungere un consenso anche in caso di partizioni di rete e guasti dei nodi, con un'elevata sicurezza.
    - Svantaggi: L'implementazione è complessa, la difficoltà di debug e risoluzione dei problemi è elevata e le molteplici tornate di votazione portano a prestazioni limitate. L'industria utilizza spesso le sue varianti (Multi-Paxos, ecc.).

### 3.2 Raft

Raft è stato formalmente proposto nel 2013, con l'obiettivo di **semplificare la difficoltà di implementazione e comprensione, garantendo al contempo la stessa sicurezza di Paxos**. Stabilisce un ruolo di **leader (Leader)** stabile, per eseguire centralmente la replica dei log e il ripristino dei guasti:

- **Fasi chiave**: Elezione del leader (Leader Election), replica dei log (Log Replication), sicurezza (Safety), ecc.
- **Applicazioni comuni**: Etcd, Consul, TiKV, LogCabin, ecc. si basano su Raft per implementare la replica a forte coerenza.
- Vantaggi e svantaggi:
    - Vantaggi: Relativamente facile da capire, la quantità di codice di implementazione è inferiore; le prestazioni sono migliori per i cluster di piccole e medie dimensioni.
    - Svantaggi: Dipende dal nodo principale (Leader), i guasti o le partizioni del nodo principale causano un blocco temporaneo della scrittura; in cluster di grandi dimensioni o distribuzioni transregionali, la latenza e la disponibilità ne risentono.

### 3.3 Protocollo Gossip

Il protocollo Gossip (pettegolezzo) non è un protocollo di consenso tradizionale, ma viene utilizzato principalmente in scenari decentralizzati per scambiare metadati o informazioni sullo stato attraverso interazioni casuali tra i nodi, in modo da diffondere e convergere in tutta la rete.

- **Caratteristiche**: Decentralizzato, a basso costo, i nodi scambiano messaggi periodicamente e casualmente.
- **Applicazioni comuni**: Cassandra, Riak, gestione distribuita dei membri (come Serf), ecc., utilizzati per implementare la coerenza finale, la sincronizzazione dello stato della replica, ecc.
- Vantaggi e svantaggi:
    - Vantaggi: Buona scalabilità, semplice da implementare, adatto a scenari con bassi requisiti di coerenza e alti requisiti di scalabilità.
    - Svantaggi: La garanzia di coerenza è debole, sono necessari mezzi di gestione dei conflitti di livello superiore (come CRDT, unione di numeri di versione, ecc.) per risolvere i conflitti in modo definitivo.

### 3.4 2PC / 3PC

Negli scenari di transazioni distribuite, i protocolli di commit comuni sono **2PC (Two-phase Commit)** e **3PC (Three-phase Commit)**:

- **2PC**: Il coordinatore notifica a tutti i partecipanti "prepara (prepare)", se tutti hanno successo, trasmette "commit (commit)", altrimenti "rollback (abort)".
- **3PC**: Aggiunge una fase sulla base di 2PC, riducendo il blocco causato da guasti single-point, ma l'implementazione è più complessa e ci sono ancora problemi di indisponibilità in scenari estremi di partizioni di rete o guasti.
- Vantaggi e svantaggi:
    - Vantaggi: Facile da capire, semantica delle transazioni chiara, ampiamente utilizzata in database distribuiti, code di messaggi, ecc.
    - Svantaggi: Forte dipendenza dal coordinatore, rischio di blocco; quando la rete è partizionata per un periodo di tempo più lungo, potrebbe non essere possibile continuare a far avanzare la transazione.

------

## IV. Le Due Principali Scelte del CAP: CP e AP

Dopo aver stabilito che **P** è un attributo "obbligatorio", se un sistema distribuito vuole continuare a fornire servizi durante una partizione di rete, deve scegliere tra **C** e **A**. La progettazione comune del sistema è quindi divisa in due campi principali: **CP** e **AP**.

### 4.1 Sistemi CP

**CP (Consistency + Partition tolerance)**: Quando si verifica una partizione di rete, il sistema sceglie di **dare la priorità alla garanzia della coerenza**, e **sacrifica la disponibilità** quando necessario.

- Implementazione tipica:
    - Consenso della maggioranza (Paxos, Raft, ecc.), richiede che più della metà dei nodi siano attivi e raggiungano un consenso prima di consentire la scrittura.
    - Se non è possibile raggiungere il quorum (numero legale) o si verifica un guasto del nodo principale, il sistema blocca o rifiuta le operazioni di scrittura, per evitare che la divisione del cervello causi incoerenza dei dati.
- Applicazioni comuni:
    - Zookeeper, Etcd, Consul, servizi di blocco distribuiti, gestione di metadati distribuiti, ecc.
    - Processi core di transazioni finanziarie, sistemi di contabilità bancaria e altri scenari con elevati requisiti di coerenza.
- Caratteristiche:
    - Ha una rigorosa garanzia dei dati: preferisce l'arresto piuttosto che la comparsa di doppi master o confusione dei dati.
    - Sacrifica una certa disponibilità: quando si verifica una partizione di rete o un failover, ci sarà una finestra di servizio non disponibile o di rifiuto delle operazioni di scrittura.

### 4.2 Sistemi AP

**AP (Availability + Partition tolerance)**: Quando si verifica una partizione di rete, il sistema sceglie di **dare la priorità alla garanzia della disponibilità**, e allo stesso tempo **allenta la coerenza**.

- Implementazione tipica:
    - Coerenza finale, replica multi-master, protocollo Gossip, strategia di coerenza regolabile in stile Dynamo, ecc.
- Applicazioni comuni:
    - Database NoSQL (Cassandra, Riak, DynamoDB, ecc.), sistemi di cache distribuiti (Redis Cluster), ecc.
    - Social network, acquisizione di log, sistemi di raccomandazione e altri servizi che richiedono alta disponibilità, alto throughput e requisiti di coerenza dei dati relativamente flessibili.
- Caratteristiche:
    - Anche in caso di partizione, tutti i nodi continuano a ricevere richieste di lettura e scrittura, garantendo che il sistema sia "il più disponibile possibile".
    - I dati potrebbero essere temporaneamente incoerenti, ma convergeranno gradualmente in background attraverso la sincronizzazione asincrona, l'unione dei conflitti, ecc.

------

## V. Come Scegliere tra CP e AP?

In un sistema distribuito su larga scala reale, è **raro fare affidamento su un singolo modello**, ma piuttosto elaborare diversi dati o scenari di servizio a livelli, al fine di ottenere il miglior equilibrio tra **coerenza** e **disponibilità**.

1. **I dati core scelgono CP**
    - Come il saldo del conto utente, il pagamento degli ordini, il flusso di transazioni finanziarie, ecc., che hanno requisiti di coerenza estremamente elevati.
    - Tollerano la temporanea non scrivibilità causata da fluttuazioni di rete, ma non possono tollerare errori nel saldo o nell'importo della transazione.
2. **I dati periferici o della cache scelgono AP**
    - Come la cache della pagina dei dettagli del prodotto, i log del comportamento dell'utente, gli elenchi di candidati per le raccomandazioni, ecc., che hanno requisiti di coerenza inferiori.
    - Danno più importanza all'alta concorrenza e all'alta disponibilità, e possono tollerare aggiornamenti ritardati o letture sporche per un certo periodo di tempo.

Molte aziende Internet adottano un'**architettura ibrida**: i processi di transazione core utilizzano l'archiviazione in stile CP (come database relazionali distribuiti o archiviazione distribuita con forte coerenza); i servizi periferici o gli scenari "lettura più scrittura meno" utilizzano l'archiviazione in stile AP o soluzioni di cache.

------

## VI. Come CP e AP Realizzano Alta Concorrenza e Coerenza Finale

### 6.1 Come i Sistemi CP Gestiscono l'Alta Concorrenza

Sebbene i protocolli di consenso possano affrontare latenze più elevate e throughput inferiori quando la scala dei nodi di un singolo cluster e la quantità di richieste di scrittura sono elevate, è comunque possibile migliorare la concorrenza e la scalabilità attraverso i seguenti mezzi:

1. Lettura e scrittura in batch
    - Impacchetta più operazioni di scrittura sul client o nel livello intermedio e le scrive sul nodo leader in una sola volta, riducendo i round trip di rete e i round di protocollo.
2. Suddivisione di database e tabelle e multi-cluster
    - Suddivide i dati in più cluster (sharding) in base alla logica o all'hash, e ogni cluster esegue ancora il protocollo CP; le richieste vengono distribuite a diverse partizioni attraverso il routing o il livello proxy.
    - Migliora la capacità di concorrenza complessiva e limita l'impatto dei guasti all'interno di una singola partizione.

> Il throughput di un singolo cluster di partizioni di un sistema CP è spesso da 2 a 10 volte inferiore rispetto a un sistema AP.

### 6.2 Come i Sistemi AP Garantiscono la Coerenza Finale

I sistemi AP sono in genere in grado di fornire un elevato throughput di scrittura e disponibilità di lettura, ma allentano la coerenza, quindi è necessario implementare garanzie di convergenza della coerenza in background o nel livello della logica di business:

1. Numero di versione (Vector Clock) o timestamp logico
    - Assegna un numero di versione a ogni operazione di aggiornamento (o basato su Lamport Clock / Hybrid Clock), ed esegue l'unione in scenari di conflitto o una strategia di vittoria basata sul timestamp (Last Write Wins).
2. Protocollo Gossip / meccanismo anti-entropia
    - I nodi scambiano periodicamente i dati o i metadati più recenti e, se vengono rilevati conflitti, vengono uniti.
3. Strategia di coerenza regolabile
    - Rappresentata dal modello Dynamo, il client può configurare parametri come `R`, `W` (come la scrittura della maggioranza, la conferma della replica), in modo da regolare in modo flessibile tra coerenza e disponibilità.
4. Strategia di risoluzione dei conflitti personalizzata
    - Unisce in base alla semantica del servizio, come l'unione del carrello della spesa con "unione", e il contatore utilizza CRDT (G-counter, PN-counter, ecc.) per garantire la monotonicità dei dati.

------

## VII. Implementazione della Forte Coerenza Cross-Shard di CP

Nel capitolo VII, è stato menzionato che **la suddivisione di database e tabelle (Sharding)** può "dividere" la pressione di un singolo cluster CP in più sottocluster, per supportare una maggiore concorrenza. Tuttavia, quando un servizio deve eseguire transazioni cross-shard (ovvero, coinvolge aggiornamenti di più database o tabelle), si trova ancora di fronte alla sfida della **coerenza multi-shard**. Di solito ci sono le seguenti idee:

1. **Transazioni distribuite: 2PC / 3PC**
    - Se un'applicazione deve eseguire aggiornamenti atomici su più partizioni, di solito utilizza protocolli di transazioni distribuite (come 2PC, 3PC) per coordinare il commit o il rollback di ciascuna partizione.
    - Problemi e contromisure:
        - Sia 2PC/3PC si basano su un nodo coordinatore, che può diventare un collo di bottiglia single-point.
        - In casi estremi di gravi partizioni di rete o guasti del coordinatore, potrebbe verificarsi un blocco.
        - In genere, il failover master-slave, il rilevamento heartbeat e il meccanismo di timeout, il retry idempotente, MVCC, ecc. vengono utilizzati per ridurre l'impatto del blocco e il rischio di incoerenza dei dati.
2. **Architettura basata su celle (Cell-based)**
    - Divide il servizio in più unità autonome, i dati all'interno di ciascuna unità si trovano nello stesso set di partizioni, garantendo che la maggior parte delle transazioni venga completata in una singola unità, riducendo le operazioni cross-shard.
    - Utilizza meccanismi asincroni o di coerenza finale al confine dell'unità per lo scambio di dati, tenendo conto dell'alta disponibilità e della coerenza complessive.
3. **Database distribuiti globali + protocollo di consenso globale**
    - Ad esempio, Google Spanner implementa la replica a forte coerenza su ciascuna partizione (Shard) tramite Paxos, e quindi utilizza l'API TrueTime per fornire timestamp globali per garantire la coerenza cross-shard.
    - Questa soluzione ha un'elevata complessità di implementazione, ma può fornire capacità di transazioni distribuite quasi a forte coerenza a livello globale.

> **Riepilogo**: Per le transazioni cross-shard che richiedono rigorosamente una forte coerenza, **2PC/3PC + coordinatore** è ancora una soluzione comune, e la possibilità di guasti viene ridotta il più possibile migliorando l'alta disponibilità del coordinatore. Tuttavia, nella pratica ingegneristica, è necessario ridurre al minimo le operazioni di scrittura cross-shard o limitare la maggior parte delle transazioni all'interno di una singola partizione attraverso l'idea di unità, riducendo la complessità del sistema.

------

## VIII. Discussione di Casi Famosi

Di seguito, vengono brevemente discussi alcuni sistemi distribuiti che vengono spesso menzionati nel settore, per vedere i loro compromessi e metodi di implementazione sul CAP:

1. **Google Spanner**
    - Un tipico sistema **CP** (può persino raggiungere l'illusione "CA" che il mondo esterno dice spesso, ma in sostanza deve comunque sacrificare parte della disponibilità).
    - Utilizza timestamp esterni precisi forniti da TrueTime + replica Paxos all'interno di ciascuna partizione per garantire una forte coerenza tra i data center.
    - Adatto per transazioni finanziarie globali o scenari con elevati requisiti di coerenza, ma i costi infrastrutturali sono estremamente elevati.
2. **BigTable / HBase**
    - In superficie, è più orientato a **CP**, e la coerenza dei metadati è garantita attraverso il coordinamento distribuito tra RegionServer e Master.
    - Tuttavia, nel percorso di lettura e scrittura effettivo, può anche fornire alcuni mezzi di alta disponibilità attraverso la replica asincrona multi-replica, e la coerenza di lettura può essere regolata in base alle esigenze dell'applicazione.
3. **AWS DynamoDB**
    - Tende a **AP**, il design iniziale è stato ispirato dal documento Dynamo, e il livello di coerenza può essere regolato tramite parametri come `R`, `W`.
    - Nella modalità predefinita, fornisce un'altissima disponibilità e coerenza finale, e può anche attivare la "lettura a forte coerenza" (ma garantisce solo la forte coerenza di una singola partizione, non necessariamente cross-partition).
4. **Cassandra**
    - Allo stesso modo, è orientato a **AP**, e il protocollo Gossip viene utilizzato a livello inferiore per mantenere lo stato della topologia dei nodi.
    - La coerenza di lettura e scrittura può configurare il numero di repliche di lettura e scrittura `R` / `W`, per ottenere una transizione graduale dalla coerenza finale a una coerenza più forte.

> **Confronto visibile**: In termini ingegneristici, non esiste un "AP o CP" assoluto, ma piuttosto una combinazione di più strategie di coerenza; la maggior parte dei sistemi fornisce un certo grado di coerenza regolabile per adattarsi a diversi scenari applicativi.

------

## IX. Riepilogo

1. **Il Teorema CAP non è una soluzione unica**
    - I sistemi distribuiti reali non possono semplicemente dire "scelgo C, rinuncio ad A" o "scelgo A, rinuncio a C".
    - È più comune nel settore scegliere in modo flessibile la modalità **CP** o **AP** per diverse dimensioni di dati e diversi tipi di operazioni, e persino all'interno dello stesso sistema, adottare diverse strategie di tolleranza ai guasti e coerenza per diverse tabelle/diverse funzioni.
2. **AP non è assolutamente disponibile al 100%**
    - Ad esempio, Cassandra, DynamoDB, ecc. possono anche non essere in grado di soddisfare le richieste in caso di partizioni di rete estreme o guasti su larga scala dei nodi.
    - I sistemi AP sono progettati per preferire "scrivere prima finché la replica è scrivibile", sacrificando parte della garanzia di coerenza in cambio di una disponibilità e un throughput relativamente più elevati.
3. **Anche CP può cercare di ottenere un'elevata disponibilità**
    - Paxos/Raft possono anche fornire una disponibilità del 99,99% o superiore in condizioni normali, ma è necessario investire più costi di rete, hardware e ingegneristici, e in caso di partizioni di rete estreme, si verificheranno comunque blocchi di scrittura e sacrifici di disponibilità per mantenere la coerenza.
4. **L'architettura ibrida è la corrente principale**
    - Gli scenari di transazioni core insistono sulla forte coerenza (CP), mentre gli scenari ausiliari periferici o i canali di cache adottano la coerenza debole (AP), e i due si coordinano tra loro.
    - È necessario combinare la tolleranza del servizio, l'ambiente di rete, l'investimento dei costi e le riserve tecniche del team per fare compromessi completi.

Il Teorema CAP fornisce un quadro di pensiero di alto livello per la progettazione di sistemi distribuiti, aiutandoci a prendere decisioni razionali di fronte alla realtà inevitabile delle partizioni di rete. Nei sistemi reali, è necessario utilizzare modelli di **coerenza**, **protocolli di consenso**, **meccanismi di replica multi-replica** più ricchi e pratiche ingegneristiche (tolleranza ai disastri, downgrade, idempotenza, unione dei conflitti, ecc.) per bilanciare coerenza e disponibilità.