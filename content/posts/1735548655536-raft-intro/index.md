---
title: Detailed explanation of Raft algorithm
date: 2024-12-30
draft: false
description: Detailed discussion of the simplest implementation details of the Raft
  algorithm, code examples, and correctness proofs.
summary: Detailed discussion of the simplest implementation details of the Raft algorithm,
  code examples, and correctness proofs.
tags:
  - Distributed System
  - CAP Theorem
  - Distributed consensus algorithm
  - System Design
  - Raft algorithm
---

## 1. Background: Why is Distributed Consensus Needed?

### 1.1 The Consistency Challenge in Distributed Systems

In distributed systems, data and computation are spread across multiple servers, each server (node) connected via a network. This approach enhances system throughput and availability, but it also introduces a core challenge: **how to maintain a consistent state or data across multiple nodes.**

Consider a simple example: Suppose we have a distributed key-value storage system. To improve reliability, we need to replicate client write operations across multiple nodes. If a node crashes or a network failure occurs, how do we ensure that the node can obtain the latest state upon recovery? How do we prevent "dirty data" or inconsistencies? These are the problems that distributed consensus algorithms need to solve.

### 1.2 Common Consensus Algorithms

When it comes to distributed consensus, many people first think of **Paxos**. Paxos has rigorous mathematical proofs, but its implementation and understanding are relatively obscure. In 2014, **Raft** was proposed as a "more readable version" of Paxos. It breaks down the consensus process into more understandable steps and is easier to implement while ensuring safety. It is widely used in industrial-grade projects such as **etcd**, **Consul**, and **TiKV**.

### 1.3 Raft's Design Goals

- **Easy to understand**: Compared to Paxos, Raft strives for simplicity and clarity in both abstraction and implementation.
- **Strong consistency**: Multiple nodes eventually agree on the order and content of log entries.
- **High availability**: The system can continue to provide services as long as a **majority of nodes** are alive.
- **Scalability**: Supports dynamically adding or removing nodes (configuration changes).

### 1.4 Raft Visualization

{{<raw>}}
<iframe src="https://raft.github.io/raftscope/index.html" title="raft visualization" aria-hidden="true" style="border: 0; width: 800px; height: 580px; margin-bottom: 20px"></iframe>
{{</raw>}}

------

## 2. Raft's Core Ideas

### 2.1 Process Overview

Raft breaks down the consensus problem into three sub-problems:

1. **Leader Election**: How to elect a "Leader" from multiple nodes.
2. **Log Replication**: After the Leader receives a write request, how to safely replicate the log to a majority of nodes.
3. **Safety**: When the Leader crashes or a network partition occurs, how to ensure that the system does not experience log loss or overwriting.

In Raft, nodes have three roles:

- **Leader**: Handles client requests and replicates them to other Followers; monitors failures.
- **Follower**: Passively receives log replication RPCs and heartbeats from the Leader.
- **Candidate**: A role that competes to become the new Leader during the election phase.

The system's timeline is divided into a series of **Terms**. There can be at most one legitimate Leader in the same term. If a Leader cannot be successfully elected in the current term or the Leader crashes, the system enters the next term to re-elect.

### 2.2 Data Structures

When implementing Raft, it is usually necessary to maintain:

1. **Term**: A monotonically increasing number that identifies the current term.
2. **Log**: Stores client requests or commands. Each log entry includes `index`, `term`, and `command`.
3. **commitIndex**: The highest log index that has been committed and is visible to the outside world.
4. **lastApplied**: The highest log index that this node has applied to its local state machine, $\text{lastApplied} \leq \text{commitIndex}$.
5. **nextIndex[]**: Maintained in the Leader, it records the next log index that needs to be sent to each Follower.
6. **matchIndex[]**: Maintained in the Leader, it records the highest log index that each Follower has replicated.

------

## 3. Roles and State Transitions

### 3.1 Follower

- **Initial State**: Nodes are in the Follower state when the system starts; or when a candidate election fails and returns to Follower.
- Behavior:
    - Receives and responds to the Leader's log replication RPCs, heartbeats, and vote requests from candidates.
    - If it does not receive any messages from the Leader or candidates within the election timeout period, it transitions to the Candidate state.

### 3.2 Candidate

- **Trigger Condition**: After a Follower times out, it becomes a Candidate and initiates an election.
- Main Behaviors:
    1. Increments `currentTerm` by 1, and votes for itself (`voteFor = self`).
    2. Sends "Request Vote" RPCs to other nodes in parallel.
    3. If it receives a majority of votes, it becomes the Leader; if a Leader with a newer term appears, it returns to Follower; if a Leader is not elected before the timeout, it starts the next round of elections.

### 3.3 Leader

- **Trigger Condition**: A Candidate receives a majority of votes.
- Main Behaviors:
    1. Periodically sends heartbeats (AppendEntries RPC) to all nodes to prevent them from initiating elections.
    2. Processes client requests, encapsulates them into log entries, writes them to its own log, and then broadcasts them to other Followers. That is, in a strongly consistent scenario, Followers/Candidates are not responsible for handling read/write operations, but only serve as redundancy for the Leader to enhance availability.
    3. When a majority of nodes have replicated a log entry, it updates `commitIndex` and notifies Followers to commit.
    4. Is responsible for updating the cluster configuration (adding/removing nodes) and committing the corresponding log entries in a safe manner.

------

## 4. Leader Election Process

Raft's election process can be summarized as follows:

1. **Follower Timeout**
   If a Follower does not receive a heartbeat or log replication message from the Leader within the election timeout period, it switches to the Candidate state.

2. **Candidate Initiates Election**

    - `currentTerm++`
    - `voteFor = candidateID`
    - Resets the election timer
    - Sends "Request Vote" RPCs to all nodes, including:
      $\langle \text{candidateTerm}, \text{candidateId}, \text{lastLogIndex}, \text{lastLogTerm} \rangle$

3. **Node Responds to Vote**
   If the following conditions are met, the node votes for the requester:

    - Requester's term number >= this node's term number
    - This node has not voted in this term
    - Requester's log is not older than its own (Term is newer or Index is greater)

   Otherwise, it refuses to vote.

4. **Election Completion**

    - If the Candidate receives a majority of votes => becomes the Leader.
    - If it does not receive a majority of votes before the timeout => enters the next round of elections (Term is incremented by 1 again).
    - If it receives a message from a Leader with a higher term during this period => returns to Follower.

5. **Leader Initialization**
   After becoming the Leader:

    - Initializes `nextIndex[] = (Leader's latest log index + 1)`
    - Initializes `matchIndex[] = 0`
    - Immediately broadcasts a heartbeat to announce its leadership.

------

## 5. Log Replication

### 5.1 AppendEntries RPC

This is the core RPC for Raft log replication and heartbeats. The fields of the request and response are as follows:

- **Request**:
  $ \langle \text{term}, \text{leaderId}, \text{prevLogIndex}, \text{prevLogTerm}, \text{entries[]}, \text{leaderCommit} \rangle$
    - When `entries[]` is empty, it acts as a heartbeat.
    - `prevLogIndex` and `prevLogTerm` are used to match the Follower's log. If there is a mismatch, replication fails.
- **Response**:
  $\langle \text{term}, \text{success} \rangle$
    - `term`: The Follower's current term (if it is greater than the requester's, the requester updates its term and returns to Follower).
    - `success`: Whether the log was successfully matched and appended.

### 5.2 Core Log Replication Logic

1. **Leader Writes to Local Log First**: Upon receiving a client write request, the Leader first forms a new log entry `[index, term, command]` and writes it to its own log.
2. **Leader Sends AppendEntries**: The Leader sends this new log entry to all Followers in parallel.
3. **Follower Checks and Matches**: If `prevLogIndex/prevLogTerm` do not match, it returns `success = false`, and the Leader will roll back and retry.
4. **Commit**: When the Leader finds that a majority of nodes have replicated a log entry at index N, it updates `commitIndex` to N and informs the Followers in subsequent heartbeats that they "can commit up to N", thereby applying the log to the state machine.

### 5.3 Important Guarantees: Log Consistency

- **Log Matching Property**: Same index, same term => all preceding logs are consistent; ensures that there will be no different commands at the same position.
- **Leader Completeness Property**: A log entry committed in term $t$ must exist in the log of any Leader elected in any subsequent term; ensures that committed log entries are not discarded or overwritten.

------

## 6. Safety

### 6.1 Why Raft Can Guarantee Consistency

1. **Majority Mechanism**: Decisions (such as committing logs) require agreement from a majority of nodes, tolerating a small number of failures.
2. **Term Mechanism**: Only trust messages from a higher term, avoiding cross-term log conflicts.
3. **Log Matching**: Followers must match the previous log entry before appending a new log entry, preventing forks.

### 6.2 Leader Crashes and Safe Log Inheritance

- After a Leader crashes, Followers time out and enter the Candidate state, initiating a new term election.
- If a new Leader is elected, its log must be the "newest" in the cluster (because the voting rules require a majority of nodes to agree); therefore, committed logs will not be discarded.
- Log entries that have not been replicated to a majority of nodes may be overwritten by the new Leader, but this is the correct "safe behavior" because these logs have not yet reached consensus in the cluster.

------

## 7. Implementation Key Points and Difficulties

### 7.1 Election Timeout

- The election timeout for each node is randomized within the range of [150ms, 300ms] (or a larger range).
- This reduces conflicts caused by "simultaneous elections".

### 7.2 Heartbeat Interval

- The Leader needs to periodically (e.g., every 50~100ms) send heartbeats to Followers to reset their election timeouts.
- Heartbeats are also empty AppendEntries RPCs, just without any log entries.

### 7.3 Log Conflict Handling

- When a Follower's log does not match the Leader's, it needs to roll back to the matching position.
- Raft provides several optimization schemes (such as maintaining richer index information in the log) to reduce repeated retries of RPCs.

### 7.4 Persistence

- Raft nodes need to **persist**: `currentTerm`, `voteFor`, and the written logs.
- Whenever the term or log is updated, it should first be written to the disk log before returning success, so that the node can recover its state after a crash and restart.
- Raft usually uses sequential log writing + on-demand truncation + snapshots to improve disk write performance.

### 7.5 State Machine

- Committed logs are applied to the **state machine**, and the specific logic is defined by the user (e.g., key-value storage, database operations, etc.).
- Raft ensures that the log order is consistent, but the specific execution process takes place in the state machine.

### 7.6 Cluster Configuration Changes

- In actual engineering, it is often necessary to add or remove nodes.
- Raft uses a "two-phase" configuration change mechanism: old configuration -> joint configuration (including old and new nodes) -> new configuration, to prevent majority confusion during configuration transitions.

------

## 8. Core Properties of Raft Correctness Proof

### 8.1 Distributed Environment Assumptions and Safety/Liveness

1. Raft assumes a **partially synchronous network**: that is, the network is synchronous most of the time (with a stable maximum delay), but long delays or partitions may occasionally occur. As long as the network eventually returns to a communicable state, Raft can achieve consensus.
2. **Safety**: No matter how unstable the network is, there will be no conflicts such as committed logs being rolled back or two nodes applying different commands at the same index.
3. **Liveness**: As long as the network is in a synchronous state for a sufficient amount of time, Raft will eventually elect a Leader and continuously commit new logs. If the network is always partitioned or messages are lost, even the best distributed algorithm may be blocked. This is the famous FLP (Fischer–Lynch–Paterson) impossibility theorem.

### 8.2 Main Properties and Overall Approach

Raft relies on the following two core properties to ensure that the system log remains consistent between nodes and does not roll back:

1. **Log Matching Property**
   "If the term numbers at log index $i$ of two nodes are the same, then the entire log segment from the beginning to $i$ is consistent."
2. **Leader Completeness Property**
   "If a log entry has been committed in term $t$, then any Leader's log in subsequent terms must also contain that log entry."

Based on these two points, we can derive **State Machine Safety**:

> Once a node applies command $cmd$ at index $i$, no other node will apply a different command at the same index $i$ that is not $cmd$.

### 8.3 Log Matching Property

> **Property Statement**: If the term numbers at index $i$ of any two nodes are the same, then the log entries from 1 to $i$ of the two nodes are completely the same (both term and command are consistent).

- **Proof Approach**: Raft's replication rules require a Follower to match `prevLogIndex` & `prevLogTerm` before appending a new log entry; otherwise, it returns failure and causes the Leader to roll back. Therefore, only when their preceding logs are completely consistent can they write the same `(index, term)`. From this, we can inductively conclude that the same position and the same term must have the same preceding logs.

### 8.4 Leader Completeness Property

> **Property Statement**: If a log entry is committed (written to a majority of nodes) in term $t$, then any legitimate Leader in subsequent terms must contain this log entry.

- **Proof Approach**: A log entry being committed means that a majority has written it; a new Leader being elected requires a majority vote; when voting, each node will refuse to vote for a candidate whose log is "behind" it. Therefore, a candidate who can be elected must already contain all committed logs; from this, we can infer that the log committed in term $t$ will not be "forgotten" or overwritten.

### 8.5 Election Safety

> **Proposition**: It is impossible for two different nodes to receive a majority of votes and become Leader in the same term $t$.

- **Core Reason**: In term $t$, each node can only cast 1 vote. If one candidate has already received a majority of votes, it is impossible for another candidate to also receive a majority of votes (because the nodes in the majority have already voted for the former and cannot vote again).

### 8.6 No Commit Overwritten

> **Proposition**: If a log entry has been committed, it will not be overwritten with a different command or be revoked.

- **Proof Approach**: As long as a log has been written to a majority, in order to overwrite it, it is necessary to obtain votes from these majority nodes and successfully write the log. However, if the majority nodes find that a candidate is "missing" this log, they will refuse to vote or refuse the matching of AppendEntries. Therefore, it is impossible to form a new majority to overwrite this log.

### 8.7 State Machine Safety

> **Proposition**: If node A applies command $cmd$ at index $i$, then no node B will apply a different command $cmd' \neq cmd$ at the same index $i$.

- **Proof Approach**: Applying to the state machine means that the log has been committed; committing means that it has been replicated to a majority, and the subsequent new Leader will also carry this log; it is impossible for a parallel, conflicting log to be written to the same index and be accepted by a majority of nodes.

### 8.8 Liveness

- In a normal partially synchronous network, once a Leader is stable, client requests will be continuously committed.
- If the Leader crashes or the network is temporarily partitioned, an election will be initiated after recovery, and a new Leader will eventually be elected.
- In a completely asynchronous or permanently partitioned situation, all distributed consensus protocols cannot guarantee inevitable liveness (FLP theorem), but as long as the network is "occasionally stable", Raft can continue to move forward.

In summary, Raft's design balances the three major goals of **easy to understand**, **easy to implement**, and **strong consistency**. Through terms, elections, log replication, and majority mechanisms, it ensures the linearizable semantics of data in distributed systems. Its core safety can be summarized as:

- There will not be two legitimate Leaders at the same time.
- Committed logs are never rolled back.
- Committed logs are still retained by the new Leader.
- Ensures that the same (index, term) position will not have different commands on different nodes.
- Ensures that logs committed in a certain term will not disappear on subsequent Leaders.

------

## 9. Implementing a Minimal Raft from Scratch: Key Steps

1. **Define Data Structures**
    - `currentTerm`, `voteFor`, `log[]`, `commitIndex`, `lastApplied`, etc.
    - Node roles (Follower/Candidate/Leader)
    - Timers, RPC channels, etc.
2. **Persistence Layer**
    - Write key data such as term, votes, and logs to disk or store in a storage engine such as RocksDB.
    - Load from storage first when restarting.
3. **RPC Communication Layer**
    - Implement two types of RPCs: `RequestVote` and `AppendEntries`.
    - Handle network exceptions and timeout retries.
4. **Event Loop & Timers**
    - Periodically check if a heartbeat has been received from the Leader.
    - Initiate an election if a timeout occurs.
    - If it is a Leader, send heartbeats periodically.
    - Process network RPCs and update local state.
5. **Leader Election**
    - Follower timeout -> Candidate initiates voting -> If a majority is obtained -> Leader
    - If it fails or encounters a Leader with a higher term -> returns to Follower
6. **Log Replication**
    - Leader receives a new command -> writes to local log -> AppendEntries to Followers
    - Majority of nodes replicate -> Leader commits and notifies Followers to commit
7. **Fault Recovery**
    - After a node restarts, it first restores its state from storage.
    - After a Leader or network failure, a new Leader will continue to be elected through the election timeout mechanism.
8. **Testing and Verification**
    - Simulate network delays, partitions, node failures, etc., to check whether Raft can correctly maintain consistency and external availability.

### Code Example: Minimal Raft in C#

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

// This code example focuses on the core election logic of the Raft algorithm, omitting details such as network communication and persistence.
namespace RaftDemo
{
    #region Data Structures

    public enum NodeRole
    {
        Follower,
        Candidate,
        Leader
    }

    public class LogEntry
    {
        public int Index { get; set; }
        public int Term { get; set; }
        public string Command { get; set; }
    }

    public class RequestVoteRequest
    {
        public int Term { get; set; }
        public string CandidateId { get; set; }
        public int LastLogIndex { get; set; }
        public int LastLogTerm { get; set; }
    }

    public class RequestVoteResponse
    {
        public int Term { get; set; }
        public bool VoteGranted { get; set; }
    }

    public class AppendEntriesRequest
    {
        public int Term { get; set; }
        public string LeaderId { get; set; }
        public int PrevLogIndex { get; set; }
        public int PrevLogTerm { get; set; }
        public List<LogEntry> Entries { get; set; } = new List<LogEntry>();
        public int LeaderCommit { get; set; }
    }

    public class AppendEntriesResponse
    {
        public int Term { get; set; }
        public bool Success { get; set; }
        // To simplify, no additional rollback information is carried here; if more information is included, nextIndex can be rolled back more quickly to find the matching position, reducing the number of network interactions.
    }

    public interface IRaftRpc
    {
        RequestVoteResponse RequestVote(RequestVoteRequest request);
        AppendEntriesResponse AppendEntries(AppendEntriesRequest request);
    }

    #endregion

    #region RaftNode Core Class

    public class RaftNode : IRaftRpc
    {
        private readonly string _nodeId;
        private readonly InMemoryDispatcher _dispatcher;
        private readonly Random _rand = new Random();

        private NodeRole _role = NodeRole.Follower;
        private int _currentTerm = 0;
        private string _votedFor = null;

        private List<LogEntry> _log = new List<LogEntry>();
        private int _commitIndex = 0;
        private int _lastApplied = 0;

        // Only Leaders need to maintain these
        private Dictionary<string, int> _nextIndex = new Dictionary<string, int>();
        private Dictionary<string, int> _matchIndex = new Dictionary<string, int>();

        private CancellationTokenSource _cts;
        private Task _timerTask;

        // The state machine in the demo uses a simple list to record commands
        private List<string> _stateMachine = new List<string>();

        public RaftNode(string nodeId, InMemoryDispatcher dispatcher)
        {
            _nodeId = nodeId;
            _dispatcher = dispatcher;
        }

        public void Start()
        {
            _dispatcher.RegisterNode(_nodeId, this);
            ResetTimer();
        }

        public void Stop()
        {
            _cts?.Cancel();
        }

        // For testing, input commands from external sources
        public void SendClientCommand(string command)
        {
            if (_role != NodeRole.Leader)
            {
                Console.WriteLine($"[{_nodeId}] I'm not the leader, ignoring client command.");
                return;
            }

            // 1. Append the command to the local log
            var newLogIndex = LastLogIndex() + 1;
            _log.Add(new LogEntry
            {
                Index = newLogIndex,
                Term = _currentTerm,
                Command = command
            });

            Console.WriteLine($"[{_nodeId}] Leader received client command '{command}', logIndex={newLogIndex}.");

            // 2. Asynchronously send AppendEntries to other nodes
            BroadcastAppendEntries();
        }

        #region Core RPC Implementation

        public RequestVoteResponse RequestVote(RequestVoteRequest request)
        {
            lock (this)
            {
                // If the term in the request is higher than the local term, update the local term and become a Follower
                if (request.Term > _currentTerm)
                {
                    _currentTerm = request.Term;
                    _role = NodeRole.Follower;
                    _votedFor = null;
                }

                var response = new RequestVoteResponse
                {
                    Term = _currentTerm,
                    VoteGranted = false
                };

                // If the term in the request is less than the local term, reject the vote
                if (request.Term < _currentTerm)
                {
                    return response;
                }

                // Check if already voted for another candidate or if the log is up-to-date
                var myLastLogIndex = LastLogIndex();
                var myLastLogTerm = LastLogTerm();

                bool logIsAtLeastUpToDate =
                    (request.LastLogTerm > myLastLogTerm) ||
                    (request.LastLogTerm == myLastLogTerm && request.LastLogIndex >= myLastLogIndex);

                if ((_votedFor == null || _votedFor == request.CandidateId) && logIsAtLeastUpToDate)
                {
                    _votedFor = request.CandidateId;
                    response.VoteGranted = true;
                    // Reset the election timeout
                    ResetTimer();
                }

                return response;
            }
        }

        public AppendEntriesResponse AppendEntries(AppendEntriesRequest request)
        {
            lock (this)
            {
                var response = new AppendEntriesResponse
                {
                    Term = _currentTerm,
                    Success = false
                };

                // If the term is less than the local term, reject the request
                if (request.Term < _currentTerm)
                {
                    return response;
                }

                // If the term is higher than the local term, update the term and become a Follower
                if (request.Term > _currentTerm)
                {
                    _currentTerm = request.Term;
                    _role = NodeRole.Follower;
                    _votedFor = null;
                }

                // Received a heartbeat/log replication from the Leader, reset the election timeout
                ResetTimer();

                // Simplified basic checks:
                // Check if the local log at prevLogIndex has the same term
                if (request.PrevLogIndex > 0)
                {
                    if (request.PrevLogIndex > _log.Count)
                    {
                        // Does not match (local log is shorter than the Leader's)
                        return response;
                    }
                    else
                    {
                        var localTerm = _log[request.PrevLogIndex - 1].Term;
                        if (localTerm != request.PrevLogTerm)
                        {
                            // Does not match (term conflict)
                            return response;
                        }
                    }
                }

                // If it matches, continue: first overwrite any conflicting logs
                foreach (var entry in request.Entries)
                {
                    if (entry.Index <= _log.Count)
                    {
                        // Existing log at the same index, check for conflict
                        if (_log[entry.Index - 1].Term != entry.Term)
                        {
                            _log[entry.Index - 1] = entry;
                            Console.WriteLine($"[{_nodeId}] Overwritten log at index {entry.Index} with term {entry.Term}.");
                        }
                    }
                    else
                    {
                        _log.Add(entry);
                        Console.WriteLine($"[{_nodeId}] Appended log at index {entry.Index} with term {entry.Term}.");
                    }
                }

                // Update commitIndex
                if (request.LeaderCommit > _commitIndex)
                {
                    _commitIndex = Math.Min(request.LeaderCommit, _log.Count);
                    ApplyStateMachine();
                }

                response.Success = true;
                response.Term = _currentTerm;
                return response;
            }
        }

        #endregion

        #region Election and Heartbeat Timers

        private void ResetTimer()
        {
            _cts?.Cancel();
            _cts = new CancellationTokenSource();
            _timerTask = RunTimer(_cts.Token);
        }

        private async Task RunTimer(CancellationToken token)
        {
            // In a production environment, the election timeout is typically set to around 150~300ms,
            // here it's extended to 1.5~3 seconds for demonstration purposes, making it easier to observe log outputs in the Console.
            var electionTimeout = _rand.Next(1500, 3000); // Random between 1.5~3s
            var heartbeatInterval = 500; // Leader heartbeat interval 0.5s

            var start = DateTime.UtcNow;
            while (!token.IsCancellationRequested)
            {
                await Task.Delay(100, token);
                var elapsed = (DateTime.UtcNow - start).TotalMilliseconds;

                if (_role == NodeRole.Leader)
                {
                    // Leader periodically sends heartbeats
                    if (elapsed >= heartbeatInterval)
                    {
                        BroadcastAppendEntries();
                        start = DateTime.UtcNow;
                    }
                }
                else
                {
                    // Follower or Candidate, need to check if election should be triggered
                    if (elapsed >= electionTimeout)
                    {
                        BecomeCandidate();
                        start = DateTime.UtcNow;
                    }
                }
            }
        }

        private void BecomeCandidate()
        {
            lock (this)
            {
                _role = NodeRole.Candidate;
                _currentTerm++;
                _votedFor = _nodeId;

                Console.WriteLine($"[{_nodeId}] Timeout -> Candidate. term={_currentTerm}");

                // Reset the election timeout
                ResetTimer();
            }

            // Initiate voting
            var request = new RequestVoteRequest
            {
                Term = _currentTerm,
                CandidateId = _nodeId,
                LastLogIndex = LastLogIndex(),
                LastLogTerm = LastLogTerm()
            };

            var votesGranted = 1; // Vote for self
            var totalNodes = _dispatcher.GetAllNodes().Count;
            var majority = totalNodes / 2 + 1;

            foreach (var otherId in _dispatcher.GetAllNodes().Where(id => id != _nodeId))
            {
                Task.Run(() =>
                {
                    var resp = _dispatcher.SendRequestVote(otherId, request);
                    if (resp != null)
                    {
                        lock (this)
                        {
                            // If the other node's term is higher, become a Follower
                            if (resp.Term > _currentTerm)
                            {
                                _currentTerm = resp.Term;
                                _role = NodeRole.Follower;
                                _votedFor = null;
                                return;
                            }

                            if (resp.VoteGranted && _role == NodeRole.Candidate && resp.Term == _currentTerm)
                            {
                                votesGranted++;
                                if (votesGranted >= majority)
                                {
                                    BecomeLeader();
                                }
                            }
                        }
                    }
                });
            }
        }

        private void BecomeLeader()
        {
            if (_role != NodeRole.Candidate) return;

            _role = NodeRole.Leader;
            Console.WriteLine($"[{_nodeId}] Became Leader at term {_currentTerm}!");

            // Initialize nextIndex and matchIndex
            foreach (var node in _dispatcher.GetAllNodes())
            {
                if (node == _nodeId) continue;
                _nextIndex[node] = LastLogIndex() + 1;
                _matchIndex[node] = 0;
            }

            // Immediately send a heartbeat
            BroadcastAppendEntries();
        }

        private void BroadcastAppendEntries()
        {
            lock (this)
            {
                if (_role != NodeRole.Leader) return;

                foreach (var otherId in _dispatcher.GetAllNodes().Where(id => id != _nodeId))
                {
                    var prevLogIndex = _nextIndex[otherId] - 1;
                    var prevLogTerm = (prevLogIndex > 0 && prevLogIndex <= _log.Count)
                        ? _log[prevLogIndex - 1].Term : 0;

                    // Simplified: send only a limited set of logs each time
                    // Can send more as needed
                    var entriesToSend = new List<LogEntry>();
                    if (prevLogIndex < _log.Count)
                    {
                        entriesToSend = _log.Skip(prevLogIndex).ToList();
                    }

                    var request = new AppendEntriesRequest
                    {
                        Term = _currentTerm,
                        LeaderId = _nodeId,
                        PrevLogIndex = prevLogIndex,
                        PrevLogTerm = prevLogTerm,
                        Entries = entriesToSend,
                        LeaderCommit = _commitIndex
                    };

                    Task.Run(() =>
                    {
                        var resp = _dispatcher.SendAppendEntries(otherId, request);
                        if (resp != null)
                        {
                            lock (this)
                            {
                                if (resp.Term > _currentTerm)
                                {
                                    _currentTerm = resp.Term;
                                    _role = NodeRole.Follower;
                                    _votedFor = null;
                                    return;
                                }

                                if (resp.Success)
                                {
                                    // Indicates the other node has matched prevLogIndex
                                    // Update nextIndex & matchIndex
                                    var lastEntry = entriesToSend.LastOrDefault();
                                    if (lastEntry != null)
                                    {
                                        _matchIndex[otherId] = lastEntry.Index;
                                        _nextIndex[otherId] = lastEntry.Index + 1;
                                    }

                                    // Update commitIndex
                                    UpdateCommitIndex();
                                }
                                else
                                {
                                    // Decrement nextIndex and retry (simple backoff strategy)
                                    _nextIndex[otherId] = Math.Max(1, _nextIndex[otherId] - 1);
                                }
                            }
                        }
                    });
                }
            }
        }

        private void UpdateCommitIndex()
        {
            // Leader updates commitIndex based on matchIndex
            // Find an N such that N > current commitIndex, a majority of matchIndex >= N, and _log[N].Term == currentTerm
            for (int i = _log.Count; i > _commitIndex; i--)
            {
                var count = _matchIndex.Values.Count(m => m >= i) + 1; // +1 includes self
                if (count >= (_dispatcher.GetAllNodes().Count / 2 + 1) && _log[i - 1].Term == _currentTerm)
                {
                    _commitIndex = i;
                    ApplyStateMachine();
                    break;
                }
            }
        }

        private void ApplyStateMachine()
        {
            // Apply logs from [lastApplied+1 ... commitIndex] to the state machine
            while (_lastApplied < _commitIndex)
            {
                _lastApplied++;
                var cmd = _log[_lastApplied - 1].Command;
                _stateMachine.Add(cmd);
                Console.WriteLine($"[{_nodeId}] Apply LogIndex={_lastApplied}, Cmd={cmd}");
            }
        }

        #endregion

        #region Helper Methods

        private int LastLogIndex()
        {
            return _log.Count;
        }

        private int LastLogTerm()
        {
            if (_log.Count == 0) return 0;
            return _log[_log.Count - 1].Term;
        }

        public NodeRole Role => _role;
        public int CurrentTerm => _currentTerm;
        public List<string> StateMachine => _stateMachine;

        #endregion
    }

    #endregion

    #region Simple "RPC Dispatcher" to Simulate Network

    public class InMemoryDispatcher
    {
        private Dictionary<string, IRaftRpc> _nodes = new Dictionary<string, IRaftRpc>();

        public void RegisterNode(string nodeId, IRaftRpc node)
        {
            _nodes[nodeId] = node;
        }

        public List<string> GetAllNodes() => _nodes.Keys.ToList();

        public RequestVoteResponse SendRequestVote(string targetNodeId, RequestVoteRequest request)
        {
            if (!_nodes.ContainsKey(targetNodeId)) return null;
            return _nodes[targetNodeId].RequestVote(request);
        }

        public AppendEntriesResponse SendAppendEntries(string targetNodeId, AppendEntriesRequest request)
        {
            if (!_nodes.ContainsKey(targetNodeId)) return null;
            return _nodes[targetNodeId].AppendEntries(request);
        }
    }

    #endregion

    #region Program Demo

    class Program
    {
        static void Main(string[] args)
        {
            var dispatcher = new InMemoryDispatcher();

            var node1 = new RaftNode("Node1", dispatcher);
            var node2 = new RaftNode("Node2", dispatcher);
            var node3 = new RaftNode("Node3", dispatcher);

            node1.Start();
            node2.Start();
            node3.Start();

            Console.WriteLine("Raft cluster started with 3 nodes (Node1, Node2, Node3).");
            Console.WriteLine("Wait a few seconds to see leader election...");

            // Wait a few seconds to allow election to complete
            Task.Delay(5000).Wait();

            // Attempt to send a command to node1; if it's the Leader, it will execute, otherwise it will indicate it's not the Leader
            node1.SendClientCommand("SET X=100");

            Task.Delay(3000).Wait();

            // Stop node2 to simulate a crash
            Console.WriteLine("\n** Stopping Node2 to simulate crash **\n");
            node2.Stop();

            // Wait for a while before sending another command
            Task.Delay(5000).Wait();
            node1.SendClientCommand("SET Y=200");

            // Wait again to allow log replication to complete
            Task.Delay(5000).Wait();

            // Print the data applied to the state machine of each node
            Console.WriteLine($"\nNode1 state: {string.Join(", ", node1.StateMachine)}");
            Console.WriteLine($"\nNode2 state: {string.Join(", ", node2.StateMachine)} (Should not receive new logs after crash)");
            Console.WriteLine($"\nNode3 state: {string.Join(", ", node3.StateMachine)}");

            // Shutdown
            node1.Stop();
            node2.Stop();
            node3.Stop();

            Console.WriteLine("\nDemo finished. Press any key to exit.");
            Console.ReadKey();
        }
    }

    #endregion
}
```
