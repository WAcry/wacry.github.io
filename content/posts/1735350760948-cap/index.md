---
title: 'In-depth explanation of the CAP theorem: Building high-concurrency and high-availability
  distributed systems'
date: 2024-12-20
draft: false
description: Discussing the Application of the CAP Theorem in Distributed Systems
  from Theory to Practice.
summary: Discussing the Application of the CAP Theorem in Distributed Systems from
  Theory to Practice.
tags:
- Distributed System
- CAP Theorem
- System Design
- Consistency Model
weight: 1
---

## I. The CAP Theorem

### 1.1 What is the CAP Theorem?

The **CAP Theorem** was proposed by Eric Brewer in 2000. Its core idea is:

- **C (Consistency)**: All nodes in the system see the same data at the same time. More strictly, when a client reads data, the result should be consistent with the latest committed data, regardless of which replica is read from (usually referring to strong consistency/linearizability).
- **A (Availability)**: The system can still provide normal services when partial failures occur. Each request can receive a "valid response" within a reasonable time (including successful responses and correct failure responses).
- **P (Partition Tolerance)**: The system can tolerate network partitions (unreachable communication between nodes). Even if the network is split, the system can provide a certain degree of availability or consistency.

In a real distributed environment, network partitions are inevitable, so **P** is basically considered a "must-have". When a network partition occurs, the system cannot simultaneously ensure **strong consistency** and **high availability** for all nodes. It can only make a trade-off between C and A, thus giving rise to two main types: **CP** and **AP**.

### 1.2 Limitations of the CAP Theorem

It should be noted that the CAP Theorem itself is a relatively high-level theory used for conceptual guidance and **should not be simply understood as "either choose C or choose A"**. There are some common misunderstandings:

1.  **C is not necessarily strong consistency**
    The C in the CAP Theorem often refers to consistency in the strictest sense (i.e., linearizability). However, in actual systems, we have many fine-grained models to choose from, such as weak consistency, Read Committed, and Causal Consistency.
2.  **Availability is not 0 or 1**
    It is not that choosing CP means availability is completely sacrificed, or choosing AP means consistency is not guaranteed at all. There is room for trade-offs and degradation strategies for both availability and consistency.
3.  **Eventual Consistency** does not violate CAP
    It is a very common compromise, using lower write consistency in exchange for higher availability and throughput, and converging data in the background asynchronously.

Therefore, the CAP Theorem should be combined with various **consistency models** and **high-availability architecture patterns** in specific scenarios to generate real practical guidance.

------

## II. Consistency Models in Distributed Systems

Consistency models are classified in many ways, but the common mainstream models can be roughly divided into: **Strong Consistency** and **Weak Consistency** (which includes eventual consistency, causal consistency, etc.). This article mainly introduces **Strong Consistency** and **Eventual Consistency**, and explains their common applications in CP or AP modes.

### 2.1 Strong Consistency

**Strong Consistency**, also known as **Linearizability**, refers to the fact that once a write operation is completed and returns successfully, any subsequent read operation can read the updated content. That is, the system behaves as if all operations are executed serially.

- **Common Implementation**: Relies on synchronous replication and a quorum (majority) mechanism, using protocols (such as Paxos/Raft) to ensure that there is only one valid leader in the system. All operations are written to the log in order and replicated to the majority of nodes.
- Advantages and Disadvantages:
    - Advantages: Guarantees the strictest data correctness. Data read at any time will not "revert".
    - Disadvantages: In the event of network jitter, partitions, or leader failures, write operations are often blocked to maintain consistency, leading to a decrease in overall availability. Performance and throughput are also relatively lower.

### 2.2 Eventual Consistency

**Eventual Consistency** is a typical form of weak consistency. It only requires that if the system no longer has new update operations, the data of all replicas will gradually converge to the same state over time. During this period, users may see outdated values when reading replica data, but it will eventually become consistent.

- **Common Implementation**: Gossip protocol, asynchronous multi-replica replication, CRDT (Conflict-free Replicated Data Type), etc.
- Advantages and Disadvantages:
    - Advantages: High availability, high throughput, low write operation latency, and high tolerance for network partitions.
    - Disadvantages: Requires tolerance for short-term data inconsistencies. Application logic is more complex and may require conflict detection and merging.

------

## III. Common Consistency Protocols and Algorithms

To keep distributed system replicas consistent, the industry has proposed many classic algorithms and protocols. Here is a brief introduction to several:

### 3.1 Paxos

Paxos is a distributed consensus algorithm proposed by Leslie Lamport in the 1990s, mainly used to achieve strong consistency or linearizability.

- **Basic Principle**: Through role division (Proposer, Acceptor, Learner), multiple rounds of voting are conducted to determine whether an operation or value is accepted by the majority of nodes.
- Advantages and Disadvantages:
    - Advantages: Can still reach a consensus under network partitions and node failures, with high security.
    - Disadvantages: Complex to implement, difficult to debug and troubleshoot, and performance is limited due to multiple rounds of voting. Industrial applications often use its variants (Multi-Paxos, etc.).

### 3.2 Raft

Raft was officially proposed in 2013, with the goal of **simplifying implementation and understanding while ensuring the same level of security as Paxos**. It establishes a stable **Leader** role to centrally perform log replication and fault recovery:

- **Key Stages**: Leader Election, Log Replication, Safety, etc.
- **Common Applications**: Etcd, Consul, TiKV, LogCabin, etc., are all based on Raft to achieve strong consistent replication.
- Advantages and Disadvantages:
    - Advantages: Relatively easy to understand, less code to implement; good performance for small and medium-sized clusters.
    - Disadvantages: Relies on the master node (Leader). Leader failures or partitions can cause temporary write blocking. In large-scale clusters or cross-regional deployments, latency and availability can be affected.

### 3.3 Gossip Protocol

The Gossip protocol is not a traditional consensus protocol. It is mainly used in decentralized scenarios to exchange metadata or status information through random interactions between nodes, thereby spreading and converging across the entire network.

- **Features**: Decentralized, low overhead, nodes exchange messages periodically and randomly.
- **Common Applications**: Cassandra, Riak, distributed membership management (such as Serf), etc., are used to achieve eventual consistency, replica state synchronization, etc.
- Advantages and Disadvantages:
    - Advantages: Good scalability, simple to implement, suitable for scenarios with low consistency requirements and high scalability requirements.
    - Disadvantages: Weak consistency guarantee, requires higher-level conflict handling methods (such as CRDT, version number merging, etc.) to eventually resolve conflicts.

### 3.4 2PC / 3PC

In distributed transaction scenarios, common commit protocols are **2PC (Two-phase Commit)** and **3PC (Three-phase Commit)**:

- **2PC**: The coordinator notifies all participants to "prepare". If all succeed, it broadcasts "commit"; otherwise, it broadcasts "abort".
- **3PC**: Adds a stage on top of 2PC to reduce blocking caused by single-point failures, but is more complex to implement and still has unavailability issues in extreme network partition or failure scenarios.
- Advantages and Disadvantages:
    - Advantages: Easy to understand, clear transaction semantics, widely used in distributed databases, message queues, etc.
    - Disadvantages: Strong dependence on the coordinator, risk of blocking; may not be able to continue the transaction when the network has a long partition.

------

## IV. Two Main Choices of CAP: CP and AP

After we determine that **P** is a "must-have" attribute, if a distributed system wants to continue providing services during network partitions, it must make a choice between **C** and **A**. Common system designs are therefore divided into two major camps: **CP** and **AP**.

### 4.1 CP Systems

**CP (Consistency + Partition Tolerance)**: When encountering network partitions, the system will choose to **prioritize consistency** and **sacrifice availability** when necessary.

- Typical Implementation:
    - Majority consensus (Paxos, Raft, etc.), requiring more than half of the nodes to be alive and reach a consensus before allowing writes.
    - If a quorum cannot be reached or the master node fails, the system will block or reject write operations to prevent brain splits that lead to data inconsistencies.
- Common Applications:
    - Zookeeper, Etcd, Consul, distributed lock services, distributed metadata management, etc.
    - Core financial transaction processes, bank accounting systems, and other scenarios with high consistency requirements.
- Features:
    - Strict data guarantees: Rather than having dual masters or data chaos, it would rather shut down.
    - Sacrifice some availability: During network partitions or failovers, there will be a window of service unavailability or rejection of write operations.

### 4.2 AP Systems

**AP (Availability + Partition Tolerance)**: When encountering network partitions, the system will choose to **prioritize availability** while **relaxing consistency**.

- Typical Implementation:
    - Eventual consistency, multi-master replication, Gossip protocol, Dynamo-style tunable consistency policies, etc.
- Common Applications:
    - NoSQL databases (Cassandra, Riak, DynamoDB, etc.), distributed caching systems (Redis Cluster), etc.
    - Social networks, log collection, recommendation systems, and other businesses that require high availability and high throughput, with relatively relaxed requirements for data consistency.
- Features:
    - Even during partitions, all nodes still accept read and write requests, ensuring the system is "as available as possible".
    - Data may have short-term inconsistencies, but it will gradually converge in the background through asynchronous synchronization, conflict merging, etc.

------

## V. How to Choose Between CP and AP?

In real large-scale distributed systems, it is often **rare to rely on a single model**. Instead, different data or business scenarios are processed in layers to achieve the optimal balance between **consistency** and **availability**.

1.  **Choose CP for Core Data**
    - Such as user account balances, order payments, financial transaction flows, etc., which have extremely high consistency requirements.
    - Tolerate short-term unavailability due to network jitter, but cannot tolerate errors in balances or transaction amounts.
2.  **Choose AP for Edge or Cached Data**
    - Such as cached product detail pages, user behavior logs, recommendation candidate lists, etc., which have lower consistency requirements.
    - More emphasis is placed on high concurrency and high availability, and it is acceptable to tolerate some delay in updates or dirty reads.

Many internet companies use a **hybrid architecture**: core transaction processes use CP-style storage (such as distributed relational databases or distributed storage with strong consistency); peripheral businesses or "read-heavy" scenarios use AP-style storage or caching solutions.

------

## VI. How CP and AP Achieve High Concurrency and Eventual Consistency

### 6.1 How CP Systems Cope with High Concurrency

Although consensus protocols face higher latency and lower throughput when the single cluster node scale and write request volume are large, concurrency and scalability can still be improved through the following methods:

1.  Batch Reads and Writes
    - Package multiple write operations on the client or middleware layer and write them to the leader node at once, reducing network round trips and protocol rounds.
2.  Database Sharding & Multiple Clusters
    - Split data logically or by hash into multiple clusters (sharding). Each cluster still runs the CP protocol internally. Requests are distributed to different shards through routing or proxy layers.
    - Improve overall concurrency and limit the impact of failures to a single shard.

> The single-shard cluster throughput of CP systems is often 2 to 10 times lower than that of AP systems.

### 6.2 How AP Systems Ensure Eventual Consistency

AP systems can usually provide high write throughput and read availability, but they relax consistency. Therefore, it is necessary to implement consistency convergence guarantees in the background or business logic layer:

1.  Version Numbers (Vector Clock) or Logical Timestamps
    - Assign a version number to each update operation (or based on Lamport Clock / Hybrid Clock) and merge in conflict scenarios or use a timestamp-based win strategy (Last Write Wins).
2.  Gossip Protocol / Anti-entropy Mechanism
    - Nodes periodically exchange the latest data or metadata and merge if conflicts are found.
3.  Tunable Consistency Policies
    - Represented by the Dynamo model, clients can configure parameters such as `R` and `W` (such as writing to a majority, replica confirmation), thereby flexibly adjusting between consistency and availability.
4.  Custom Conflict Resolution Strategies
    - Merge based on business semantics, such as using "union" for shopping carts, and using CRDT (G-counter, PN-counter, etc.) for counters to ensure the monotonicity of data.

------

## VII. Cross-Shard Strong Consistency Implementation in CP

As mentioned in Chapter VII, **database sharding** can "split" the pressure of a single CP cluster into multiple sub-clusters to support higher concurrency. However, when a business needs to perform transactions across shards (i.e., involving updates to multiple databases or tables), it still faces the challenge of **multi-shard consistency**. There are usually the following approaches:

1.  **Distributed Transactions: 2PC / 3PC**
    - If an application needs to perform atomic updates across multiple shards, distributed transaction protocols (such as 2PC, 3PC) are usually used to coordinate the commit or rollback of each shard.
    - Problems and Countermeasures:
        - 2PC/3PC both rely on a coordinator node, which can become a single point of bottleneck.
        - In extreme cases of severe network partitions or coordinator failures, blocking may occur.
        - Generally, master-slave switching, heartbeat detection and timeout mechanisms, idempotent retries, MVCC, etc., are used to reduce the impact of blocking and the risk of data inconsistencies.
2.  **Cell-based Architecture**
    - Divide the business into multiple autonomous units. The data in each unit is in the same shard set, ensuring that most transactions are completed in a single unit, reducing cross-shard operations.
    - Use asynchronous or eventual consistency mechanisms at unit boundaries for data exchange, taking into account the overall high availability and consistency.
3.  **Globally Distributed Database + Global Consensus Protocol**
    - For example, Google Spanner uses Paxos to achieve strong consistent replication of replicas on each shard, and then uses the TrueTime API to provide global timestamps to ensure cross-shard consistency.
    - This solution is extremely complex to implement, but it can provide near-strong consistent distributed transaction capabilities on a global scale.

> **Summary**: For cross-shard transactions that strictly require strong consistency, **2PC/3PC + coordinator** is still a common solution. The possibility of failures is reduced by maximizing the high availability of the coordinator. However, in engineering practice, cross-shard write operations should be minimized, or the complexity of the system should be reduced by limiting most transactions to a single shard using a cell-based approach.

------

## VIII. Discussion of Famous Cases

Here is a brief discussion of several distributed systems that are often mentioned in the industry, looking at their trade-offs and implementation methods in CAP:

1.  **Google Spanner**
    - A typical **CP** system (it can even achieve the "CA" illusion often talked about, but in essence, it still needs to sacrifice some availability).
    - Uses external precise timestamps provided by TrueTime + Paxos replication within each shard to ensure strong consistency across data centers.
    - Suitable for global financial transactions or scenarios with high consistency requirements, but the infrastructure cost is extremely high.
2.  **BigTable / HBase**
    - Superficially more inclined towards **CP**, using distributed coordination between RegionServer and Master to ensure the consistency of metadata.
    - However, in the actual read and write paths, it can also provide a certain degree of high availability through asynchronous multi-replica replication. Read consistency can be adjusted according to application needs.
3.  **AWS DynamoDB**
    - Inclined towards **AP**. Early design inspiration came from the Dynamo paper. Consistency levels can be adjusted through parameters such as `R` and `W`.
    - Provides extremely high availability and eventual consistency in the default mode. "Strong consistent reads" can also be enabled (but only guarantees strong consistency within a single partition, not necessarily across partitions).
4.  **Cassandra**
    - Also **AP** inclined, using the Gossip protocol at the bottom layer to maintain the node topology status.
    - Read and write consistency can be configured with the number of read and write replicas `R` / `W` to achieve a smooth transition from eventual consistency to stronger consistency.

> **Comparison shows**: In engineering, there is no absolute "AP or CP". It is more of a mix of multiple consistency strategies. Most systems provide a certain degree of tunable consistency to adapt to different application scenarios.

------

## IX. Summary

1.  **The CAP Theorem is not a one-size-fits-all solution**
    - Real distributed systems cannot simply say "I choose C and give up A" or "I choose A and give up C".
    - It is more common in the industry to flexibly choose **CP** or **AP** modes for different data dimensions and different operation types. Even within the same system, different fault tolerance and consistency strategies are used for different tables/different functions.
2.  **AP is not absolutely 100% available**
    - For example, Cassandra, DynamoDB, etc., may also fail to meet requests in extreme network partitions or large-scale node failures.
    - AP systems are designed to prefer "write as long as the replica is writable", sacrificing some consistency guarantees in exchange for relatively higher availability and throughput.
3.  **CP can also try to achieve high availability**
    - Paxos/Raft can also provide 99.99% or even higher availability under normal circumstances, but it requires more investment in network, hardware, and engineering costs. In extreme network partitions, it will still block writes and sacrifice availability to maintain consistency.
4.  **Hybrid architecture is mainstream**
    - Core transaction scenarios adhere to strong consistency (CP), while peripheral auxiliary scenarios or caching channels use weak consistency (AP), and the two cooperate with each other.
    - It is necessary to make a comprehensive trade-off based on business tolerance, network environment, cost investment, and team technical reserves.

The CAP Theorem provides a high-level thinking framework for the design of distributed systems, helping us make rational decisions in the face of the inevitable reality of network partitions. In actual systems, it is necessary to use richer **consistency models**, **consensus protocols**, **multi-replica replication mechanisms**, and engineering practices (disaster recovery, degradation, idempotency, conflict merging, etc.) to balance consistency and availability.