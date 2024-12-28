---
title: "Analyse approfondie du théorème CAP : Créer des systèmes distribués à haute concurrence et haute disponibilité"
date: 2024-12-27
draft: false
description: "Discussion de l'application du théorème CAP dans les systèmes distribués, de la théorie à la pratique."
summary: "Discussion de l'application du théorème CAP dans les systèmes distribués, de la théorie à la pratique."
tags: [ "Systèmes distribués", "Théorème CAP", "Conception de systèmes", "Modèles de cohérence" ]
categories: [ "Conception de systèmes" , "Systèmes distribués" ]
---

## I. Le théorème CAP

### 1.1 Qu'est-ce que le théorème CAP ?

Le **théorème CAP** a été proposé par Eric Brewer en 2000. Son idée centrale est la suivante :

- **C (Cohérence)** : Tous les nœuds du système voient les mêmes données au même moment. Plus précisément, lorsqu'un client lit des données, quel que soit le réplica à partir duquel il lit, le résultat doit être cohérent avec les données les plus récemment validées (généralement, cela fait référence à une cohérence forte/linéaire).
- **A (Disponibilité)** : Le système peut toujours fournir des services normaux même en cas de panne partielle. Chaque requête peut obtenir une « réponse valide » dans un délai raisonnable (cela n'implique pas nécessairement une réussite, mais aussi une réponse d'échec correcte).
- **P (Tolérance au partitionnement)** : Le système peut tolérer les partitions réseau (communication inaccessible entre les nœuds). Même si le réseau est divisé, le système peut fournir un certain degré de disponibilité ou de cohérence.

Dans un environnement distribué réel, les partitions réseau sont inévitables, donc **P** est fondamentalement considéré comme une « option obligatoire ». Lorsqu'une partition réseau se produit, le système ne peut pas prendre en charge simultanément la **forte cohérence** et la **haute disponibilité** des données sur tous les nœuds. Il doit faire un compromis entre C et A, ce qui donne naissance aux deux principaux types : **CP** et **AP**.

### 1.2 Les limites du théorème CAP

Il convient de souligner que le théorème CAP lui-même est une théorie de niveau relativement élevé, utilisée pour guider les concepts. Il **ne faut pas simplement le comprendre comme « soit choisir C, soit choisir A »**. Il existe des malentendus courants :

1. **C n'est pas nécessairement une forte cohérence**
   Le C du théorème CAP fait souvent référence à la cohérence au sens le plus strict (c'est-à-dire la cohérence linéaire). Cependant, dans les systèmes réels, nous avons de nombreux modèles plus précis à choisir, tels que la cohérence faible, la lecture validée (Read Committed), la cohérence causale (Causal Consistency), etc.
2. **La disponibilité n'est pas 0 ou 1**
   Ce n'est pas parce que vous choisissez CP que la disponibilité est complètement sacrifiée ; ou que vous choisissez AP que la cohérence n'est pas du tout garantie. La disponibilité et la cohérence ont toutes deux différentes marges de compromis et de stratégies de dégradation.
3. **La cohérence éventuelle** ne viole pas le CAP
   Il s'agit d'un compromis très courant, qui échange une cohérence d'écriture plus faible contre une disponibilité et un débit plus élevés, et qui converge les données en arrière-plan de manière asynchrone.

Par conséquent, le théorème CAP doit être combiné avec divers **modèles de cohérence** et **modèles d'architecture à haute disponibilité** dans des scénarios spécifiques pour générer une véritable valeur de guidage pratique.

------

## II. Modèles de cohérence des systèmes distribués

La classification des modèles de cohérence est très riche, mais les modèles courants peuvent être divisés en : **forte cohérence** et **faible cohérence** (qui comprend la cohérence éventuelle, la cohérence causale, etc.). Cet article présente principalement la **forte cohérence** et la **cohérence éventuelle**, et explique leurs applications courantes dans les modes CP ou AP.

### 2.1 Forte cohérence

La **forte cohérence (Strong Consistency)**, également appelée **linéarisabilité (Linearizability)**, fait référence au fait qu'une fois qu'une opération d'écriture est terminée et renvoie un succès, toute opération de lecture ultérieure peut lire le contenu mis à jour. En d'autres termes, le système se comporte comme s'il avait exécuté toutes les opérations en série.

- **Implémentation courante** : Elle repose sur la réplication synchrone et un mécanisme de quorum (majorité), et utilise des protocoles (tels que Paxos/Raft) pour garantir qu'il n'y a qu'un seul leader (Leader) valide dans le système. Toutes les opérations sont écrites dans le journal dans l'ordre et répliquées sur la plupart des nœuds.
- Avantages et inconvénients :
    - Avantages : Garantit la correction des données la plus stricte, et les données lues à tout moment ne « reviennent » pas en arrière.
    - Inconvénients : En cas de gigue du réseau, de partitionnement ou de panne du leader, afin de maintenir la cohérence, les opérations d'écriture sont souvent bloquées, ce qui entraîne une baisse de la disponibilité globale ; les performances et le débit sont également relativement faibles.

### 2.2 Cohérence éventuelle

La **cohérence éventuelle (Eventual Consistency)** est une forme typique de faible cohérence. Elle exige seulement que si le système n'a plus de nouvelles opérations de mise à jour, les données de tous les réplicas convergent progressivement vers le même état au fil du temps. Pendant cette période, les utilisateurs qui lisent les données du réplica peuvent voir des valeurs obsolètes, mais elles finiront par devenir cohérentes.

- **Implémentation courante** : Protocole Gossip, réplication asynchrone multi-réplicas, CRDT (Conflict-free Replicated Data Type), etc.
- Avantages et inconvénients :
    - Avantages : Haute disponibilité, haut débit, faible latence d'écriture et haute tolérance aux partitions réseau.
    - Inconvénients : Nécessite de tolérer une incohérence des données à court terme, une logique d'application plus complexe et peut nécessiter une détection et une fusion des conflits.

------

## III. Protocoles et algorithmes de cohérence courants

Afin de maintenir la cohérence entre les réplicas du système distribué, l'industrie a proposé de nombreux algorithmes et protocoles classiques. Voici une brève introduction à plusieurs d'entre eux :

### 3.1 Paxos

Paxos est un algorithme de cohérence distribuée proposé par Leslie Lamport dans les années 1990, principalement utilisé pour mettre en œuvre une forte cohérence ou une cohérence linéaire.

- **Principe de base** : Il utilise la division des rôles (Proposeur, Accepteur, Apprenant) pour effectuer plusieurs tours de vote afin de déterminer si une opération ou une valeur est acceptée par la majorité des nœuds.
- Avantages et inconvénients :
    - Avantages : Il peut toujours parvenir à un consensus en cas de partitionnement du réseau ou de panne de nœud, et présente une grande sécurité.
    - Inconvénients : La mise en œuvre est complexe, le débogage et le dépannage sont difficiles, et plusieurs tours de vote entraînent des performances limitées. L'industrie utilise principalement ses variantes (Multi-Paxos, etc.).

### 3.2 Raft

Raft a été officiellement proposé en 2013. Son objectif est de **simplifier la mise en œuvre et la difficulté de compréhension tout en garantissant la même sécurité que Paxos**. Il établit un rôle de **leader (Leader)** stable pour effectuer de manière centralisée la réplication des journaux et la récupération des pannes :

- **Étapes clés** : Élection du leader (Leader Election), réplication des journaux (Log Replication), sécurité (Safety), etc.
- **Applications courantes** : Etcd, Consul, TiKV, LogCabin, etc. sont tous basés sur Raft pour mettre en œuvre une forte réplication cohérente.
- Avantages et inconvénients :
    - Avantages : Relativement facile à comprendre, moins de code à mettre en œuvre ; bonnes performances pour les clusters de petite et moyenne taille.
    - Inconvénients : Dépend du nœud principal (Leader), et une panne ou un partitionnement du nœud principal entraînera un blocage temporaire de l'écriture ; dans les clusters à grande échelle ou les déploiements interrégionaux, la latence et la disponibilité seront affectées.

### 3.3 Protocole Gossip

Le protocole Gossip (commérage) n'est pas un protocole de consensus traditionnel. Il est principalement utilisé dans des scénarios décentralisés pour échanger des métadonnées ou des informations d'état par le biais d'interactions aléatoires entre les nœuds, afin de se propager et de converger sur l'ensemble du réseau.

- **Caractéristiques** : Décentralisé, faible coût, échange périodique et aléatoire de messages entre les nœuds.
- **Applications courantes** : Cassandra, Riak, gestion des membres distribués (tels que Serf), etc., utilisés pour mettre en œuvre la cohérence éventuelle, la synchronisation de l'état des réplicas, etc.
- Avantages et inconvénients :
    - Avantages : Bonne évolutivité, simple à mettre en œuvre, adapté aux scénarios qui n'ont pas d'exigences élevées en matière de cohérence et qui ont des exigences élevées en matière d'évolutivité.
    - Inconvénients : La garantie de cohérence est faible et des moyens de traitement des conflits de niveau supérieur (tels que CRDT, fusion de numéros de version, etc.) sont nécessaires pour résoudre les conflits.

### 3.4 2PC / 3PC

Dans les scénarios de transactions distribuées, les protocoles de validation courants sont **2PC (Two-phase Commit)** et **3PC (Three-phase Commit)** :

- **2PC** : Le coordinateur informe tous les participants de la « préparation (prepare) ». S'ils réussissent tous, il diffuse la « validation (commit) », sinon il diffuse l'« annulation (abort) ».
- **3PC** : Une étape est ajoutée sur la base de 2PC pour réduire le blocage causé par une panne unique, mais la mise en œuvre est plus complexe et il existe toujours des problèmes d'indisponibilité dans des scénarios extrêmes de partitionnement ou de panne du réseau.
- Avantages et inconvénients :
    - Avantages : Facile à comprendre, sémantique de transaction claire, largement utilisé dans les bases de données distribuées, les files d'attente de messages, etc.
    - Inconvénients : Forte dépendance au coordinateur, risque de blocage ; il peut être impossible de faire avancer la transaction lorsque le réseau est partitionné pendant une longue période.

------

## IV. Les deux principaux choix du CAP : CP et AP

Une fois que nous avons déterminé que **P** est un attribut « obligatoire », si un système distribué veut continuer à fournir des services lors d'un partitionnement du réseau, il doit faire un choix entre **C** et **A**. La conception courante du système est donc divisée en deux camps principaux : **CP** et **AP**.

### 4.1 Système CP

**CP (Cohérence + Tolérance au partitionnement)** : En cas de partitionnement du réseau, le système choisira de **donner la priorité à la garantie de la cohérence** et de **sacrifier la disponibilité** si nécessaire.

- Implémentation typique :
    - Consensus majoritaire (Paxos, Raft, etc.), qui nécessite que plus de la moitié des nœuds soient actifs et parviennent à un consensus pour autoriser l'écriture.
    - Si le quorum (quorum légal) ne peut pas être atteint ou si le nœud principal tombe en panne, le système bloquera ou rejettera les opérations d'écriture afin d'éviter une incohérence des données due à une division cérébrale.
- Applications courantes :
    - Zookeeper, Etcd, Consul, services de verrouillage distribués, gestion des métadonnées distribuées, etc.
    - Processus centraux de transactions financières, systèmes de comptabilité bancaire et autres scénarios qui nécessitent une forte cohérence.
- Caractéristiques :
    - Possède une garantie de données stricte : il préfère s'arrêter plutôt que d'avoir un double maître ou une confusion de données.
    - Sacrifie une certaine disponibilité : En cas de partitionnement du réseau ou de basculement, il y aura une fenêtre pendant laquelle le service sera indisponible ou les opérations d'écriture seront rejetées.

### 4.2 Système AP

**AP (Disponibilité + Tolérance au partitionnement)** : En cas de partitionnement du réseau, le système choisira de **donner la priorité à la garantie de la disponibilité** et d'**assouplir la cohérence** en même temps.

- Implémentation typique :
    - Cohérence éventuelle, réplication multi-maîtres, protocole Gossip, stratégie de cohérence réglable de style Dynamo, etc.
- Applications courantes :
    - Bases de données NoSQL (Cassandra, Riak, DynamoDB, etc.), systèmes de mise en cache distribués (Redis Cluster), etc.
    - Réseaux sociaux, collecte de journaux, systèmes de recommandation et autres entreprises qui nécessitent une haute disponibilité, un haut débit et des exigences relativement souples en matière de cohérence des données.
- Caractéristiques :
    - Même en cas de partitionnement, tous les nœuds continuent de recevoir les requêtes de lecture et d'écriture, ce qui garantit que le système est « aussi disponible que possible ».
    - Les données peuvent être temporairement incohérentes, mais elles convergeront progressivement en arrière-plan par le biais d'une synchronisation asynchrone et d'une fusion des conflits.

------

## V. Comment choisir entre CP et AP ?

Dans les systèmes distribués à grande échelle réels, il est **rare de ne dépendre que d'un seul modèle**. Au lieu de cela, différents niveaux de traitement sont effectués pour différentes données ou scénarios commerciaux afin d'obtenir l'équilibre optimal entre **cohérence** et **disponibilité**.

1. **Choisir CP pour les données essentielles**
    - Tels que le solde du compte utilisateur, le paiement des commandes, le flux des transactions financières, etc., qui ont des exigences très élevées en matière de cohérence.
    - Tolérer une indisponibilité temporaire de l'écriture causée par une gigue du réseau, mais ne pas tolérer les erreurs de solde ou de montant de transaction.
2. **Choisir AP pour les données périphériques ou mises en cache**
    - Tels que le cache de la page de détails du produit, les journaux de comportement de l'utilisateur, les listes de candidats recommandés, etc., qui ont des exigences de cohérence plus faibles.
    - Accorder plus d'importance à la haute concurrence et à la haute disponibilité, et être en mesure de tolérer un certain temps de mise à jour différée ou de lecture erronée.

De nombreuses entreprises Internet adopteront une **architecture hybride** : les processus de transaction centraux utilisent un stockage de type CP (tel qu'une base de données relationnelle distribuée ou un stockage distribué avec une forte cohérence) ; les entreprises périphériques ou les scénarios « lecture intensive et écriture rare » utilisent un stockage de type AP ou des solutions de mise en cache.

------

## VI. Comment CP et AP atteignent-ils une haute concurrence et une cohérence éventuelle ?

### 6.1 Comment les systèmes CP gèrent-ils la haute concurrence ?

Bien que les protocoles de consensus soient confrontés à une latence élevée et à un faible débit lorsque la taille d'un seul nœud de cluster et le volume de requêtes d'écriture sont importants, la concurrence et l'évolutivité peuvent toujours être améliorées par les moyens suivants :

1. Lecture et écriture par lots
    - Regrouper plusieurs opérations d'écriture côté client ou dans la couche intermédiaire, et les écrire sur le nœud leader en une seule fois, ce qui réduit les allers-retours sur le réseau et les tours de protocole.
2. Division de la base de données et des tables et multi-clusters
    - Diviser les données en plusieurs clusters (sharding) par logique ou par hachage. Chaque cluster exécute toujours le protocole CP ; les requêtes sont dispersées vers différentes partitions par le biais d'une couche de routage ou de proxy.
    - Améliorer la capacité de concurrence globale et limiter l'impact des pannes à une seule partition.

> Le débit d'un seul cluster de partition d'un système CP est souvent 2 à 10 fois inférieur à celui d'un système AP.

### 6.2 Comment les systèmes AP garantissent-ils la cohérence éventuelle ?

Les systèmes AP peuvent généralement fournir un débit d'écriture et une disponibilité de lecture élevés, mais ils relâchent la cohérence. Par conséquent, il est nécessaire de mettre en œuvre une garantie de convergence de la cohérence en arrière-plan ou dans la couche de logique métier :

1. Numéro de version (Vector Clock) ou horodatage logique
    - Attribuer un numéro de version (ou basé sur Lamport Clock / Hybrid Clock) à chaque opération de mise à jour, et effectuer une fusion ou une stratégie de victoire basée sur l'horodatage (Last Write Wins) dans les scénarios de conflit.
2. Protocole Gossip / mécanisme d'anti-entropie
    - Les nœuds échangent périodiquement les dernières données ou métadonnées, et fusionnent les conflits lorsqu'ils sont détectés.
3. Stratégie de cohérence réglable
    - Représentée par le modèle Dynamo, le client peut configurer des paramètres tels que `R` et `W` (tels que l'écriture de la majorité, la confirmation du réplica), afin d'ajuster de manière flexible la cohérence et la disponibilité.
4. Stratégie personnalisée de résolution des conflits
    - Combiner la sémantique métier pour la fusion, par exemple, le panier d'achat est fusionné par « union », et le compteur utilise CRDT (G-counter, PN-counter, etc.) pour garantir la monotonie des données.

------

## VII. Mise en œuvre d'une forte cohérence inter-partitions de CP

Comme mentionné au chapitre VII, la **division de la base de données et des tables (Sharding)** peut « diviser » la pression d'un seul cluster CP en plusieurs sous-clusters afin de prendre en charge une concurrence plus élevée. Cependant, lorsque l'entreprise doit effectuer des transactions inter-partitions (c'est-à-dire impliquant des mises à jour de plusieurs bases de données ou tables), elle est toujours confrontée au défi de la **cohérence multi-partitions**. Il existe généralement les idées suivantes :

1. **Transactions distribuées : 2PC / 3PC**
    - Si l'application doit effectuer des mises à jour atomiques sur plusieurs partitions, les protocoles de transactions distribuées (tels que 2PC, 3PC) sont généralement utilisés pour coordonner la validation ou l'annulation de chaque partition.
    - Problèmes et contre-mesures :
        - 2PC/3PC dépendent tous d'un nœud coordinateur, qui peut devenir un goulot d'étranglement unique.
        - Dans des situations extrêmes de partitionnement grave du réseau ou de panne du coordinateur, un blocage peut se produire.
        - Généralement, le basculement maître-esclave, la détection de battement de cœur et le mécanisme de délai d'attente, la nouvelle tentative idempotente, MVCC, etc. sont utilisés pour réduire l'impact du blocage et le risque d'incohérence des données.
2. **Architecture basée sur les cellules**
    - Diviser l'entreprise en plusieurs unités autonomes. Les données de chaque unité se trouvent dans le même ensemble de partitions, ce qui garantit que la plupart des transactions ne sont effectuées que dans une seule unité, ce qui réduit les opérations inter-partitions.
    - Utiliser des mécanismes asynchrones ou de cohérence éventuelle à la limite de l'unité pour l'échange de données, en tenant compte de la haute disponibilité et de la cohérence globales.
3. **Base de données distribuée mondiale + protocole de consensus global**
    - Par exemple, Google Spanner utilise Paxos sur chaque partition (Shard) pour mettre en œuvre une forte réplication cohérente, puis utilise l'API TrueTime pour fournir un horodatage global afin de garantir la cohérence inter-partitions.
    - Cette solution est extrêmement complexe à mettre en œuvre, mais elle peut fournir des capacités de transactions distribuées quasi fortement cohérentes à l'échelle mondiale.

> **Résumé** : Pour les transactions inter-partitions qui nécessitent strictement une forte cohérence, **2PC/3PC + coordinateur** est toujours une solution courante, et la haute disponibilité du coordinateur est améliorée autant que possible pour réduire la possibilité de pannes. Cependant, dans la pratique de l'ingénierie, il est nécessaire de réduire autant que possible les opérations d'écriture inter-partitions, ou d'utiliser l'idée de l'unité pour limiter la plupart des transactions à une seule partition, ce qui réduit la complexité du système.

------

## VIII. Discussion sur des cas célèbres

Voici une brève discussion sur plusieurs systèmes distribués qui sont souvent mentionnés dans l'industrie, afin de voir leurs compromis et leurs méthodes de mise en œuvre sur CAP :

1. **Google Spanner**
    - Un système **CP** typique (il peut même réaliser l'illusion « CA » que le monde extérieur mentionne souvent, mais en substance, il doit toujours sacrifier une partie de la disponibilité).
    - Utiliser l'horodatage externe précis fourni par TrueTime + la réplication Paxos à l'intérieur de chaque partition pour garantir une forte cohérence entre les centres de données.
    - Convient aux transactions financières mondiales ou aux scénarios qui nécessitent une forte cohérence, mais le coût de l'infrastructure est extrêmement élevé.
2. **BigTable / HBase**
    - En apparence, il est plus orienté **CP**. La cohérence des métadonnées est garantie par la coordination distribuée entre RegionServer et Master.
    - Cependant, dans le chemin de lecture et d'écriture réel, une certaine haute disponibilité peut également être fournie par la réplication asynchrone multi-réplicas, et la cohérence de lecture peut être ajustée en fonction des besoins de l'application.
3. **AWS DynamoDB**
    - Tendance **AP**. La conception initiale s'inspire de l'article Dynamo. Le niveau de cohérence peut être ajusté par des paramètres tels que `R` et `W`.
    - Le mode par défaut offre une très haute disponibilité et une cohérence éventuelle. La « lecture fortement cohérente » peut également être activée (mais seule la forte cohérence d'une seule partition est garantie, pas nécessairement entre les partitions).
4. **Cassandra**
    - Également une tendance **AP**. Le protocole Gossip sous-jacent est utilisé pour maintenir l'état de la topologie des nœuds.
    - La cohérence de lecture et d'écriture peut être configurée avec le nombre de réplicas de lecture et d'écriture `R` / `W` pour réaliser une transition en douceur de la cohérence éventuelle à une cohérence plus forte.

> **Comparaison visible** : Il n'existe pas de « AP ou CP » absolu en ingénierie. Il s'agit plutôt d'un mélange de plusieurs stratégies de cohérence ; la plupart des systèmes offrent un certain degré de cohérence réglable pour s'adapter à différents scénarios d'application.

------

## IX. Résumé

1. **Le théorème CAP n'est pas une solution unique**
    - Les systèmes distribués réels ne peuvent pas simplement dire « Je choisis C et j'abandonne A » ou « Je choisis A et j'abandonne C ».
    - Il est plus courant dans l'industrie de choisir de manière flexible les modes **CP** ou **AP** pour différentes dimensions de données et différents types d'opérations. Même au sein d'un même système, différentes stratégies de tolérance aux pannes et de cohérence sont utilisées pour différentes tables/fonctions.
2. **AP n'est pas absolument disponible à 100 %**
    - Par exemple, Cassandra, DynamoDB, etc. peuvent également ne pas être en mesure de répondre aux requêtes en cas de partitionnement extrême du réseau ou de défaillance à grande échelle des nœuds.
    - Les systèmes AP sont simplement conçus pour avoir tendance à « écrire d'abord tant que le réplica est accessible en écriture », sacrifiant une partie de la garantie de cohérence en échange d'une disponibilité et d'un débit relativement plus élevés.
3. **CP peut également essayer d'atteindre une haute disponibilité**
    - Paxos/Raft peut également fournir une disponibilité de 99,99 % ou même plus dans des circonstances normales, mais il faut investir davantage dans le réseau, le matériel et les coûts d'ingénierie, et un blocage de l'écriture se produira toujours en cas de partitionnement extrême du réseau, sacrifiant la disponibilité pour maintenir la cohérence.
4. **L'architecture hybride est le courant dominant**
    - Les scénarios de transactions centrales insistent sur une forte cohérence (CP), et les scénarios auxiliaires périphériques ou les canaux de mise en cache utilisent une faible cohérence (AP), et les deux coopèrent.
    - Il est nécessaire de combiner la tolérance de l'entreprise, l'environnement réseau, l'investissement en coûts et les réserves techniques de l'équipe pour faire des compromis globaux.

Le théorème CAP fournit un cadre de réflexion de haut niveau pour la conception de systèmes distribués, ce qui nous aide à prendre des décisions rationnelles face à la réalité inévitable du partitionnement du réseau. Dans les systèmes réels, il est nécessaire d'utiliser des **modèles de cohérence**, des **protocoles de consensus**, des **mécanismes de réplication multi-réplicas** plus riches, ainsi que des pratiques d'ingénierie (récupération après sinistre, dégradation, idempotence, fusion des conflits, etc.) pour équilibrer la cohérence et la disponibilité.