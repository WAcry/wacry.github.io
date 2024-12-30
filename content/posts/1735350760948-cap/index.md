---
title: 'In-depth explanation of the CAP theorem: Building high-concurrency and high-availability
  distributed systems'
date: 2024-12-28
draft: false
description: Discussing the Application of the CAP Theorem in Distributed Systems
  from Theory to Practice.
summary: Discussing the Application of the CAP Theorem in Distributed Systems from
  Theory to Practice.
tags:
  - Distributed System
  - CAP Theorem
  - Distributed consensus algorithm
  - System Design
---

## I. The CAP Theorem

### 1.1 What is the CAP Theorem?

The **CAP theorem**, proposed by Eric Brewer in 2000, states that in the design of distributed systems, at most two of the following three properties can be satisfied simultaneously: **Consistency (C)**, **Availability (A)**, and **Partition Tolerance (P)**.

-   **C (Consistency)**: All nodes in the system see the same data at the same time. More strictly, when a client reads data, the result should be consistent with the latest committed data, regardless of which replica is read from (usually referring to strong consistency/linearizability).
-   **A (Availability)**: The system can still provide normal services when partial failures occur, and each request can receive a valid response within a reasonable time.
-   **P (Partition Tolerance)**: The system can tolerate network partitions (unreachable communication between nodes). Even if the network is split, the system can provide a certain degree of availability or consistency.

In real distributed environments, network partitions are inevitable, so **P** is basically considered a "must-have". When a network partition occurs, the system cannot simultaneously maintain **strong consistency** and **high availability** of data across all nodes. It can only make a trade-off between C and A, which gives rise to two main types: **CP** and **AP**.

### 1.2 Limitations of the CAP Theorem

It should be noted that the CAP theorem itself is a relatively high-level theory used for conceptual guidance and **should not be simply interpreted as "either choose C or choose A"**. There are some common misconceptions:

1.  **C is not necessarily strong consistency**
    The C in the CAP theorem often refers to consistency in the strictest sense (i.e., linearizability). However, in actual systems, we have many fine-grained models to choose from, such as weak consistency, Read Committed, and Causal Consistency.
2.  **Availability is not 0 or 1**
    It is not the case that choosing CP means that availability is completely sacrificed, or that choosing AP means that consistency is not guaranteed at all. Both availability and consistency have different degrees of trade-off space and degradation strategies.
3.  **Eventual consistency does not violate CAP**
    It is a very common compromise solution, trading lower write consistency for higher availability and throughput, and converging data in the background asynchronously.

Therefore, the CAP theorem should be combined with various **consistency models** and **high-availability architectural patterns** in specific scenarios to generate real practical guidance value.

---

## II. Consistency Models in Distributed Systems

Consistency models are classified in many ways, but the common mainstream models can be roughly divided into: **strong consistency** and **weak consistency** (which includes eventual consistency, causal consistency, etc.). This article mainly introduces **strong consistency** and **eventual consistency**, and explains their common applications in CP or AP modes.

### 2.1 Strong Consistency

**Strong Consistency**, also known as **Linearizability**, means that once a write operation is completed and returns success, any subsequent read operation can read the updated content. That is, the system behaves as if all operations are executed serially.

-   **Common implementation**: It relies on synchronous replication and a quorum (majority) mechanism, using protocols (such as Paxos/Raft) to ensure that there is only one valid leader in the system. All operations are written to the log in order and replicated to a majority of nodes.
-   Advantages and disadvantages:
    -   Advantages: Guarantees the strictest data correctness, and the data read at any time will not "roll back".
    -   Disadvantages: In the event of network jitter, partitions, or leader failures, write operations are often blocked to maintain consistency, resulting in a decrease in overall availability; performance and throughput are also relatively lower.

### 2.2 Eventual Consistency

**Eventual Consistency** is a typical form of weak consistency. It only requires that if there are no new update operations in the system, the data of all replicas will gradually converge to the same state over time. During this period, users may see outdated values when reading replica data, but it will eventually become consistent.

-   **Common implementation**: Gossip protocol, asynchronous multi-replica replication, CRDT (Conflict-free Replicated Data Type), etc.
-   Advantages and disadvantages:
    -   Advantages: High availability, high throughput, low write operation latency, and high tolerance for network partitions.
    -   Disadvantages: Need to tolerate short-term data inconsistencies, more complex application logic, and may require conflict detection and merging.

---

## III. Common Consistency Protocols and Algorithms

In order to keep the replicas in a distributed system consistent, the industry has proposed many classic algorithms and protocols. Here is a brief introduction to several:

### 3.1 Paxos

Paxos is a distributed consensus algorithm proposed by Leslie Lamport in the 1990s, mainly used to achieve strong consistency or linearizability.

-   **Basic principle**: Through role division (Proposer, Acceptor, Learner), multiple rounds of voting are conducted to determine whether an operation or value is accepted by a majority of nodes.
-   Advantages and disadvantages:
    -   Advantages: Can still reach consensus under network partitions and node failures, with high security.
    -   Disadvantages: Complex to implement, difficult to debug and troubleshoot, and performance is limited due to multiple rounds of voting. Its variants (Multi-Paxos, etc.) are mostly used in the industry.

### 3.2 Raft

Raft was officially proposed in 2013, with the goal of **simplifying the implementation and understanding while ensuring the same level of security as Paxos**. It establishes a stable **Leader** role to centrally perform log replication and failure recovery:

-   **Key stages**: Leader Election, Log Replication, Safety, etc.
-   **Common applications**: Etcd, Consul, TiKV, LogCabin, etc. are all based on Raft to achieve strong consistent replication.
-   Advantages and disadvantages:
    -   Advantages: Relatively easy to understand, less implementation code; good performance for small and medium-sized clusters.
    -   Disadvantages: Relies on the master node (Leader), and leader failures or partitions can cause temporary write blocking; in large-scale clusters or cross-regional deployments, latency and availability will be affected.

### 3.3 Gossip Protocol

The Gossip protocol is not a traditional consensus protocol. It is mainly used in decentralized scenarios to exchange metadata or status information through random interactions between nodes, thereby spreading and converging across the entire network.

-   **Features**: Decentralized, low overhead, nodes periodically and randomly exchange messages.
-   **Common applications**: Cassandra, Riak, distributed membership management (such as Serf), etc., used to achieve eventual consistency, replica state synchronization, etc.
-   Advantages and disadvantages:
    -   Advantages: Good scalability, simple to implement, suitable for scenarios with low consistency requirements and high scalability requirements.
    -   Disadvantages: Weaker consistency guarantees, requiring more advanced conflict handling methods (such as CRDT, version number merging, etc.) to ultimately resolve conflicts.

### 3.4 2PC / 3PC

In distributed transaction scenarios, common commit protocols are **2PC (Two-phase Commit)** and **3PC (Three-phase Commit)**:

-   **2PC**: The coordinator notifies all participants to "prepare", if all are successful, it broadcasts "commit", otherwise "abort".
-   **3PC**: Adds a stage on top of 2PC to reduce blocking caused by single-point failures, but the implementation is more complex, and there are still unavailability issues in extreme network partition or failure scenarios.
-   Advantages and disadvantages:
    -   Advantages: Easy to understand, clear transaction semantics, widely used in distributed databases, message queues, etc.
    -   Disadvantages: Strong dependence on the coordinator, with the risk of blocking; transactions may not be able to continue when the network is partitioned for a long time.

---

## IV. Two Main Choices of CAP: CP and AP

After we determine that **P** is a "must-have" attribute, if a distributed system wants to continue to provide services during network partitions, it must make a choice between **C** and **A**. Common system designs are therefore divided into two major camps: **CP** and **AP**.

### 4.1 CP Systems

**CP (Consistency + Partition tolerance)**: When encountering network partitions, the system will choose to **prioritize consistency** and **sacrifice availability** when necessary.

-   Typical implementation:
    -   Majority consensus (Paxos, Raft, etc.), requires more than half of the nodes to be alive and reach a consensus before writing is allowed.
    -   If a quorum cannot be reached or the master node fails, the system will block or reject write operations to prevent data inconsistencies caused by split-brain.
-   Common applications:
    -   Zookeeper, Etcd, Consul, distributed lock services, distributed metadata management, etc.
    -   Core financial transaction processes, bank accounting systems, and other scenarios with high consistency requirements.
-   Features:
    -   Has strict data guarantees: rather shut down than have dual masters or data chaos.
    -   Sacrifices a certain degree of availability: There will be a window of service unavailability or rejection of write operations during network partitions or failovers.

### 4.2 AP Systems

**AP (Availability + Partition tolerance)**: When encountering network partitions, the system will choose to **prioritize availability** and **relax consistency** at the same time.

-   Typical implementation:
    -   Eventual consistency, multi-master replication, Gossip protocol, Dynamo-style tunable consistency strategies, etc.
-   Common applications:
    -   NoSQL databases (Cassandra, Riak, DynamoDB, etc.), distributed caching systems (Redis Cluster), etc.
    -   Social networks, log collection, recommendation systems, and other businesses that require high availability and high throughput, with relatively relaxed requirements for data consistency.
-   Features:
    -   Even with partitions, all nodes still accept read and write requests, ensuring that the system is "as available as possible".
    -   Data may have temporary inconsistencies, but will gradually converge in the background through asynchronous synchronization, conflict merging, etc.

---

## V. How to Choose Between CP and AP?

In real large-scale distributed systems, it is often **rare to rely solely on a single model**. Instead, different data or business scenarios are processed in layers to achieve the optimal balance between **consistency** and **availability**.

1.  **Choose CP for core data**
    -   Such as user account balances, order payments, financial transaction flows, etc., which have extremely high requirements for consistency.
    -   Tolerate temporary unwriteable states caused by network jitter, but cannot tolerate errors in balances or transaction amounts.
2.  **Choose AP for edge or cached data**
    -   Such as cached product details pages, user behavior logs, recommendation candidate lists, etc., which have lower consistency requirements.
    -   More emphasis is placed on high concurrency and high availability, and the ability to tolerate a certain amount of delayed updates or dirty reads.

Many internet companies use a **hybrid architecture**: the core transaction process uses CP-style storage (such as distributed relational databases or distributed storage with strong consistency); peripheral businesses or "read-heavy" scenarios use AP-style storage or caching solutions.

---

## VI. How CP and AP Achieve High Concurrency and Eventual Consistency

### 6.1 How CP Systems Cope with High Concurrency

Although consensus protocols face higher latency and lower throughput when the single cluster node scale and write request volume are large, concurrency and scalability can still be improved through the following methods:

1.  Batch read and write
    -   Package multiple write operations on the client or middleware layer, write them to the leader node at once, reducing network round trips and protocol rounds.
2.  Database and table sharding & multi-cluster
    -   Split data logically or by hash into multiple clusters (sharding), each cluster still runs the CP protocol internally; requests are distributed to different shards through routing or proxy layers.
    -   Improve overall concurrency capabilities and limit the impact of failures to a single shard.

> The single-shard cluster throughput of CP systems is often 2 to 10 times lower than that of AP systems.

### 6.2 How AP Systems Ensure Eventual Consistency

AP systems can usually provide high write throughput and read availability, but they relax consistency. Therefore, it is necessary to implement consistency convergence guarantees in the background or business logic layer:

1.  Version number (Vector Clock) or logical timestamp
    -   Assign a version number to each update operation (or based on Lamport Clock / Hybrid Clock), and perform merging in conflict scenarios or a timestamp-based win strategy (Last Write Wins).
2.  Gossip protocol / Anti-entropy mechanism
    -   Nodes periodically exchange the latest data or metadata, and merge if conflicts are found.
3.  Tunable consistency strategy
    -   Represented by the Dynamo model, the client can configure parameters such as `R` and `W` (such as writing to a majority, replica confirmation), thereby flexibly adjusting between consistency and availability.
4.  Custom conflict resolution strategy
    -   Merge based on business semantics, such as using "union" to merge shopping carts, and using CRDTs (G-counter, PN-counter, etc.) to ensure the monotonicity of data for counters.

---

## VII. Implementation of Cross-Shard Strong Consistency for CP

As mentioned in Chapter VII, **database and table sharding** can "split" the pressure of a single CP cluster into multiple sub-clusters to support higher concurrency. However, when a business needs to perform transactions across shards (i.e., involving updates to multiple databases or tables), it still faces the challenge of **multi-shard consistency**. There are usually the following approaches:

1.  **Distributed transactions: 2PC / 3PC**
    -   If the application needs to perform atomic updates across multiple shards, distributed transaction protocols (such as 2PC, 3PC) are usually used to coordinate the commit or rollback of each shard.
    -   Problems and countermeasures:
        -   Both 2PC/3PC rely on a coordinator node, which may become a single point bottleneck.
        -   In extreme cases of severe network partitions or coordinator failures, blocking may occur.
        -   Generally, master-slave switching, heartbeat detection and timeout mechanisms, idempotent retries, MVCC, etc. are used to reduce the impact of blocking and the risk of data inconsistency.
2.  **Cell-based architecture**
    -   Divide the business into multiple autonomous units, and the data in each unit is in the same shard set, ensuring that most transactions are completed in a single unit, reducing cross-shard operations.
    -   Asynchronous or eventual consistency mechanisms are used at unit boundaries for data exchange, taking into account the overall high availability and consistency.
3.  **Global distributed database + global consensus protocol**
    -   For example, Google Spanner uses Paxos to achieve strong consistent replication of replicas on each shard, and then uses the TrueTime API to provide global timestamps to ensure cross-shard consistency.
    -   This solution is extremely complex to implement, but it can provide near-strong consistent distributed transaction capabilities on a global scale.

> **Summary**: For cross-shard transactions that strictly require strong consistency, **2PC/3PC + coordinator** is still a common solution, and the possibility of failure is reduced by improving the high availability of the coordinator as much as possible. However, in engineering practice, try to reduce cross-shard write operations as much as possible, or use a cell-based approach to limit most transactions to a single shard range to reduce system complexity.

---

## VIII. Discussion of Famous Cases

The following briefly discusses several distributed systems that are often mentioned in the industry to see their trade-offs and implementations on CAP:

1.  **Google BigTable**
    -   A NoSQL database that tends to **CP**. It uses distributed coordination between RegionServers and Master to ensure the consistency of metadata, and provides strong consistency guarantees for single-row transactions by default.
    -   Read consistency can be adjusted according to application needs.
2.  **Google Spanner**
    -   A very powerful **CP** system (it can even achieve the "CA" illusion often talked about, but it still needs to sacrifice some availability in essence).
    -   Going further than BigTable, it provides global distributed SQL transactions and external consistency guarantees, supporting ACID transactions and read and write operations across global data centers.
    -   It uses TrueTime to provide high-precision external timestamps to ensure the order of transactions and external time consistency across data centers.
    -   It uses the Paxos protocol within each shard to replicate data, ensuring strong data consistency and high availability.
    -   It uses a highly available two-phase commit (2PC) protocol to reliably commit global transactions, ensuring the consistency of cross-shard operations.
    -   Suitable for global financial transactions or other application scenarios with extremely high consistency requirements, but the infrastructure cost is high.
3.  **AWS DynamoDB**
    -   A NoSQL database that tends to **AP**, providing extremely high availability and eventual consistency.
    -   Provides weak consistency reads by default, but strong consistency reads can be obtained through the `ConsistentRead` parameter.
    -   Provides **DynamoDB Transaction**, which supports ACID transactions, but performance will be reduced, and only transactions within the same region data center are supported.
4.  **Cassandra**
    -   Also tends to **AP**, and uses the Gossip protocol at the bottom to maintain the node topology state.
    -   The consistency level can be adjusted through parameters such as `R` and `W`. When `R + W > N`, strong consistency of single-row reads and writes is guaranteed.
    -   Supports Lightweight Transactions (LWT), providing single-row ACID transaction guarantees.

> **Comparison shows**: There is no absolute "AP or CP" in engineering. It is more of a mixture of multiple consistency strategies; most systems provide a certain degree of tunable consistency to adapt to different application scenarios.

---

## IX. Summary

1.  **The CAP theorem is not a one-size-fits-all solution**
    -   Real distributed systems cannot simply say "I choose C and give up A" or "I choose A and give up C".
    -   What is more common in the industry is to flexibly choose the **CP** or **AP** mode for different data dimensions and different operation types. Even within the same system, different fault tolerance and consistency strategies are adopted for different tables/different functions.
2.  **AP is not absolutely 100% available**
    -   For example, Cassandra, DynamoDB, etc. will also fail to meet requests in extreme network partitions or large-scale node failures.
    -   AP systems are designed to prefer "write as long as the replica is writable", sacrificing some consistency guarantees in exchange for relatively higher availability and throughput.
3.  **CP can also try to achieve high availability**
    -   Paxos/Raft can also provide 99.99% or even higher availability under normal circumstances, but it requires more investment in network, hardware, and engineering costs, and will still experience blocked writes and sacrifice availability to maintain consistency in extreme network partitions.
4.  **Hybrid architecture is the mainstream**
    -   Core transaction scenarios adhere to strong consistency (CP), while peripheral auxiliary scenarios or caching channels use weak consistency (AP), and the two cooperate with each other.
    -   It is necessary to make a comprehensive trade-off based on business tolerance, network environment, cost investment, and team technical reserves.

The CAP theorem provides a high-level framework for the design of distributed systems, helping us make rational decisions in the face of the inevitable reality of network partitions. In actual systems, it is necessary to use richer **consistency models**, **consensus protocols**, **multi-replica replication mechanisms**, and engineering practices (disaster recovery, degradation, idempotency, conflict merging, etc.) to balance consistency and availability.