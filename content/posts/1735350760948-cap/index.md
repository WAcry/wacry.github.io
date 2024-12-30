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

The **CAP Theorem**, proposed by Eric Brewer in 2000, states that in the design of distributed systems, a maximum of two out of the three properties—**Consistency (C)**, **Availability (A)**, and **Partition Tolerance (P)**—can be satisfied simultaneously.

- **C (Consistency)**: All nodes in the system see the same data at the same time. More strictly, when a client reads data, the result should be consistent with the latest committed data, regardless of which replica it reads from (usually referring to strong/linear consistency).
- **A (Availability)**: The system can still provide normal service when partial failures occur, and each request can receive a valid response within a reasonable time.
- **P (Partition Tolerance)**: The system can tolerate network partitions (unreachable communication between nodes). Even if the network is split, the system can provide a certain degree of availability or consistency.

In real distributed environments, network partitions are inevitable, so **P** is generally regarded as a "must-have". When a network partition occurs, the system cannot simultaneously ensure both **strong consistency** and **high availability** of data across all nodes. It must choose between C and A, resulting in two main types: **CP** and **AP**.

### 1.2 Limitations of the CAP Theorem

It is important to note that the CAP Theorem itself is a relatively high-level theory, used for conceptual guidance, and **should not be simply interpreted as "either choose C or choose A"**. There are some common misconceptions:

1. **C does not necessarily mean strong consistency**
   The C in the CAP Theorem often refers to the strictest sense of consistency (i.e., linearizability). However, in real systems, there are many fine-grained models to choose from, such as weak consistency, Read Committed, and Causal Consistency.
2. **Availability is not binary (0 or 1)**
   It is not the case that choosing CP means availability is completely sacrificed, or that choosing AP means consistency is completely unguaranteed. There is room for trade-offs and degradation strategies for both availability and consistency.
3. **Eventual consistency does not violate CAP**
   It is a very common compromise, trading lower write consistency for higher availability and throughput, and converging data in the background asynchronously.

Therefore, the CAP Theorem should be combined with various **consistency models** and **high-availability architecture patterns** in specific scenarios to provide real practical guidance.

------

## II. Consistency Models in Distributed Systems

There are many classifications of consistency models, but the common mainstream models can be broadly divided into: **Strong Consistency** and **Weak Consistency** (which includes eventual consistency, causal consistency, etc.). This article mainly introduces **Strong Consistency** and **Eventual Consistency**, and explains their common applications in CP or AP modes.

### 2.1 Strong Consistency

**Strong Consistency**, also known as **Linearizability**, means that once a write operation completes and returns successfully, any subsequent read operation will be able to read the updated content. That is, the system behaves as if all operations were executed serially.

- **Common Implementation**: Relies on synchronous replication and a quorum (majority) mechanism, using protocols (such as Paxos/Raft) to ensure that there is only one valid leader in the system. All operations are written to the log in order and replicated to the majority of nodes.
- Advantages and Disadvantages:
    - Advantages: Guarantees the strictest data correctness, and the data read at any time will not "revert".
    - Disadvantages: In the event of network jitter, partitions, or leader failures, write operations are often blocked to maintain consistency, leading to a decrease in overall availability; performance and throughput are also relatively lower.

### 2.2 Eventual Consistency

**Eventual Consistency** is a typical form of weak consistency. It only requires that if there are no new update operations in the system, the data of all replicas will gradually converge to the same state over time. During this period, users may see outdated values when reading replica data, but it will eventually become consistent.

- **Common Implementation**: Gossip protocol, asynchronous multi-replica replication, CRDT (Conflict-free Replicated Data Type), etc.
- Advantages and Disadvantages:
    - Advantages: High availability, high throughput, low write operation latency, and high tolerance for network partitions.
    - Disadvantages: Requires tolerance for short-term data inconsistencies, more complex application logic, and may require conflict detection and merging.

------

## III. Common Consistency Protocols and Algorithms

To maintain consistency between replicas in a distributed system, the industry has proposed many classic algorithms and protocols. Here is a brief introduction to several of them:

### 3.1 Paxos

Paxos is a distributed consensus algorithm proposed by Leslie Lamport in the 1990s, mainly used to achieve strong or linear consistency.

- **Basic Principle**: Through role division (Proposer, Acceptor, Learner), multiple rounds of voting are conducted to determine whether an operation or value is accepted by the majority of nodes.
- Advantages and Disadvantages:
    - Advantages: Can still reach a consensus under network partitions and node failures, with high security.
    - Disadvantages: Complex implementation, difficult to debug and troubleshoot, and performance is limited due to multiple rounds of voting. Its variants (Multi-Paxos, etc.) are more commonly used in the industry.

### 3.2 Raft

Raft was officially proposed in 2013, with the goal of **simplifying the implementation and understanding while ensuring the same level of security as Paxos**. It establishes a stable **Leader** role, centrally performing log replication and fault recovery:

- **Key Stages**: Leader Election, Log Replication, Safety, etc.
- **Common Applications**: Etcd, Consul, TiKV, LogCabin, etc., are all based on Raft to implement strong consistency replication.
- Advantages and Disadvantages:
    - Advantages: Relatively easy to understand, less implementation code; better performance for small and medium-sized clusters.
    - Disadvantages: Relies on the master node (Leader), and leader failures or partitions can cause short-term write blocking; in large-scale clusters or cross-regional deployments, latency and availability can be affected.

### 3.3 Gossip Protocol

The Gossip protocol is not a traditional consensus protocol. It is mainly used in decentralized scenarios to exchange metadata or status information through random node interactions, thereby achieving diffusion and convergence across the entire network.

- **Features**: Decentralized, low overhead, nodes exchange messages periodically and randomly.
- **Common Applications**: Cassandra, Riak, distributed membership management (such as Serf), etc., are used to achieve eventual consistency, replica state synchronization, etc.
- Advantages and Disadvantages:
    - Advantages: Good scalability, simple to implement, suitable for scenarios with low consistency requirements and high scalability requirements.
    - Disadvantages: Weak consistency guarantee, requiring higher-level conflict handling methods (such as CRDT, version number merging, etc.) to ultimately resolve conflicts.

### 3.4 2PC / 3PC

In distributed transaction scenarios, common commit protocols are **2PC (Two-phase Commit)** and **3PC (Three-phase Commit)**:

- **2PC**: The coordinator notifies all participants to "prepare," and if all are successful, it broadcasts "commit," otherwise "abort."
- **3PC**: Adds a phase on top of 2PC to reduce blocking caused by single points of failure, but is more complex to implement and still has unavailability issues in extreme network partitions or failure scenarios.
- Advantages and Disadvantages:
    - Advantages: Easy to understand, clear transaction semantics, widely used in distributed databases, message queues, etc.
    - Disadvantages: Strong dependency on the coordinator, risk of blocking; transactions may not be able to proceed when the network has a long partition.

------

## IV. Two Main Choices of CAP: CP and AP

When we consider **P** as a "must-have" property, if a distributed system wants to continue providing services during network partitions, it must choose between **C** and **A**. Common system designs are therefore divided into two major camps: **CP** and **AP**.

### 4.1 CP Systems

**CP (Consistency + Partition tolerance)**: When encountering a network partition, the system will choose to **prioritize consistency** and **sacrifice availability** when necessary.

- Typical Implementation:
    - Majority consensus (Paxos, Raft, etc.), requiring more than half of the nodes to be alive and reach a consensus before allowing writes.
    - If a quorum cannot be reached or the master node fails, the system will block or reject write operations to prevent data inconsistencies caused by split-brain scenarios.
- Common Applications:
    - Zookeeper, Etcd, Consul, distributed lock services, distributed metadata management, etc.
    - Core financial transaction processes, bank accounting systems, and other scenarios with high consistency requirements.
- Features:
    - Strict data guarantees: Preferring downtime rather than dual-master or data confusion.
    - Sacrificing some availability: During network partitions or failovers, there will be a window of service unavailability or rejection of write operations.

### 4.2 AP Systems

**AP (Availability + Partition tolerance)**: When encountering a network partition, the system will choose to **prioritize availability** while **relaxing consistency**.

- Typical Implementation:
    - Eventual consistency, multi-master replication, Gossip protocol, Dynamo-style tunable consistency policies, etc.
- Common Applications:
    - NoSQL databases (Cassandra, Riak, DynamoDB, etc.), distributed caching systems (Redis Cluster), etc.
    - Social networks, log collection, recommendation systems, and other businesses that require high availability and high throughput, and have relatively relaxed requirements for data consistency.
- Features:
    - Even during partitions, all nodes still accept read and write requests, ensuring the system is "as available as possible."
    - Data may have short-term inconsistencies, but will gradually converge in the background through asynchronous synchronization and conflict merging.

------

## V. How to Choose Between CP and AP?

In real large-scale distributed systems, it is often **rare to rely on a single model**. Instead, different data or business scenarios are layered to achieve the optimal balance between **consistency** and **availability**.

1. **Choose CP for Core Data**
    - Such as user account balances, order payments, financial transaction records, etc., which have extremely high consistency requirements.
    - Tolerating short-term write unavailability caused by network jitter, but not tolerating errors in balances or transaction amounts.
2. **Choose AP for Edge or Cached Data**
    - Such as caches of product detail pages, user behavior logs, recommendation candidate lists, etc., which have lower consistency requirements.
    - Prioritizing high concurrency and high availability, and tolerating a certain amount of delayed updates or dirty reads.

Many internet companies adopt a **hybrid architecture**: Core transaction processes use CP-style storage (such as distributed relational databases or distributed storage with strong consistency); peripheral businesses or "read-heavy" scenarios use AP-style storage or caching solutions.

------

## VI. How CP and AP Achieve High Concurrency and Eventual Consistency

### 6.1 How CP Systems Cope with High Concurrency

Although consensus protocols face higher latency and lower throughput when the scale of a single cluster node and the volume of write requests are large, concurrency and scalability can still be improved through the following methods:

1. Batch Reads and Writes
    - Pack multiple write operations at the client or middleware layer and write them to the leader node at once, reducing network round trips and protocol rounds.
2. Database Sharding & Multi-Cluster
    - Split data logically or by hash into multiple clusters (sharding), with each cluster still running the CP protocol internally; requests are distributed to different shards through routing or proxy layers.
    - Improve overall concurrency and limit the impact of failures to a single shard.

> The throughput of a single-shard cluster in a CP system is often 2 to 10 times lower than that of an AP system.

### 6.2 How AP Systems Ensure Eventual Consistency

AP systems can usually provide high write throughput and read availability, but they relax consistency. Therefore, consistency convergence needs to be ensured in the background or at the business logic layer:

1. Version Numbers (Vector Clock) or Logical Timestamps
    - Assign a version number (or based on Lamport Clock / Hybrid Clock) to each update operation, and merge or use a timestamp-based winner strategy (Last Write Wins) in conflict scenarios.
2. Gossip Protocol / Anti-entropy Mechanism
    - Nodes periodically exchange the latest data or metadata and merge when conflicts are found.
3. Tunable Consistency Policies
    - Represented by the Dynamo model, clients can configure parameters such as `R` and `W` (such as writing to a majority, replica confirmation), thereby flexibly adjusting between consistency and availability.
4. Custom Conflict Resolution Strategies
    - Merge based on business semantics, such as using "union" for shopping carts, and using CRDT (G-counter, PN-counter, etc.) for counters to ensure data monotonicity.

------

## VII. Cross-Shard Strong Consistency Implementation in CP Systems

As mentioned in Chapter VII, **database sharding** can "split" the pressure of a single CP cluster into multiple sub-clusters to support higher concurrency. However, when a business needs to perform transactions across shards (i.e., involving updates to multiple databases or tables), it still faces the challenge of **multi-shard consistency**. The following are common approaches:

1. **Distributed Transactions: 2PC / 3PC**
    - If an application needs to perform atomic updates across multiple shards, distributed transaction protocols (such as 2PC, 3PC) are usually used to coordinate the commit or rollback of each shard.
    - Problems and Countermeasures:
        - 2PC/3PC both rely on a coordinator node, which can become a single point of failure.
        - Blocking may occur in extreme cases of severe network partitions or coordinator failures.
        - Generally, master-slave switching, heartbeat detection and timeout mechanisms, idempotent retries, and MVCC are used to reduce the impact of blocking and the risk of data inconsistency.
2. **Cell-based Architecture**
    - Divide the business into multiple autonomous units, with data in each unit within the same shard set, ensuring that most transactions are completed within a single unit, reducing cross-shard operations.
    - Use asynchronous or eventual consistency mechanisms for data exchange at unit boundaries, taking into account overall high availability and consistency.
3. **Globally Distributed Database + Global Consensus Protocol**
    - For example, Google Spanner implements strong consistency replication of replicas through Paxos on each shard, and then uses the TrueTime API to provide global timestamps to ensure cross-shard consistency.
    - This solution is extremely complex to implement, but can provide near-strong consistent distributed transaction capabilities on a global scale.

> **Summary**: For cross-shard transactions that strictly require strong consistency, **2PC/3PC + coordinator** is still a common solution, and the probability of failure is reduced by maximizing the high availability of the coordinator. However, in engineering practice, cross-shard write operations should be minimized, or the complexity of the system should be reduced by using a cell-based approach to limit most transactions within a single shard.

------

## VIII. Discussion of Famous Cases

Here is a brief discussion of several distributed systems that are often mentioned in the industry, and their trade-offs and implementations in terms of CAP:

1. **Google BigTable**
    - A NoSQL database that leans towards **CP**, using distributed coordination between RegionServers and Master to ensure metadata consistency, and providing strong consistency guarantees for single-row transactions by default.
    - Read consistency can be adjusted according to application requirements.
2. **Google Spanner**
    - A very powerful **CP** system (even achieving the "CA" illusion often spoken of, but still requiring some sacrifice in availability).
    - A step further than BigTable, providing globally distributed SQL transactions and external consistency guarantees, supporting ACID transactions and read/write operations across global data centers.
    - Uses TrueTime to provide high-precision external timestamps to ensure the order of transactions and external time consistency across data centers.
    - Uses the Paxos protocol for data replication within each shard to ensure strong data consistency and high availability.
    - Uses a highly available two-phase commit (2PC) protocol to implement reliable commit of global transactions, ensuring the consistency of cross-shard operations.
    - Suitable for global financial transactions or other application scenarios with extremely high consistency requirements, but the infrastructure costs are higher.
3. **AWS DynamoDB**
    - A NoSQL database that leans towards **AP**, providing extremely high availability and eventual consistency.
    - Provides weak consistent reads by default, but can obtain strong consistent reads through the `ConsistentRead` parameter.
    - Provides **DynamoDB Transaction**, which supports ACID transactions, but performance will be reduced, and it only supports transactions within the same region data center.
4. **Cassandra**
    - Also **AP** leaning, using the Gossip protocol to maintain node topology status at the bottom layer.
    - Consistency levels can be adjusted by parameters such as `R` and `W`. When `R + W > N`, strong consistency for single-row read/write is guaranteed.
    - Supports Lightweight Transactions (LWT), providing single-row ACID transaction guarantees.

> **Comparison shows**: In engineering, there is no absolute "AP or CP", but rather a mix of multiple consistency strategies; most systems provide a certain degree of tunable consistency to adapt to different application scenarios.

------

## IX. Conclusion

1. **The CAP Theorem is not a one-size-fits-all solution**
    - Real distributed systems cannot simply say "I choose C, give up A" or "I choose A, give up C."
    - It is more common in the industry to flexibly choose the **CP** or **AP** mode for different data dimensions and different operation types. Even within the same system, different fault tolerance and consistency strategies are adopted for different tables/functions.
2. **AP is not absolutely 100% available**
    - For example, Cassandra, DynamoDB, etc., may also encounter situations where requests cannot be fulfilled during extreme network partitions or large-scale node failures.
    - AP systems are designed to prefer "write as long as the replica is writable," sacrificing some consistency guarantees in exchange for relatively higher availability and throughput.
3. **CP can also try to achieve high availability**
    - Paxos/Raft can also provide 99.99% or even higher availability under normal circumstances, but it requires more investment in network, hardware, and engineering costs. And in extreme network partitions, it will still block writes and sacrifice availability to maintain consistency.
4. **Hybrid architectures are mainstream**
    - Core transaction scenarios adhere to strong consistency (CP), while peripheral auxiliary scenarios or caching channels adopt weak consistency (AP), with the two working together.
    - A comprehensive trade-off should be made based on business tolerance, network environment, cost investment, and team technical reserves.

The CAP Theorem provides a high-level framework for thinking about the design of distributed systems, helping us make rational decisions in the face of the inevitable reality of network partitions. In real systems, richer **consistency models**, **consensus protocols**, **multi-replica replication mechanisms**, and engineering practices (disaster recovery, degradation, idempotency, conflict merging, etc.) are needed to balance consistency and availability.