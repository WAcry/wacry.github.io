---
title: Raft 算法详解
date: 2024-12-30
draft: false
description: 详细讨论 Raft 算法的最简实现细节，代码示例，以及正确性证明。
summary: 详细讨论 Raft 算法的最简实现细节，代码示例，以及正确性证明。
tags:
  - 分布式系统
  - CAP 定理
  - 分布式一致性算法
  - 系统设计
  - Raft 算法
---

## 1. 背景：为什么需要分布式共识

### 1.1 分布式系统中的一致性难题

在分布式系统中，数据与计算分散在多台服务器之间，每台服务器（节点）通过网络连接。这样做能够提高系统的吞吐量和可用性，但也带来了核心挑战——
**如何在多个节点之间保持一致的状态或数据**。

举个简单的例子：假设我们有一个分布式键值存储系统，为了提高可靠性，需要将客户端的写操作复制到多个节点。如果某个节点宕机或网络故障，那么如何保证当该节点恢复后能拿到最新状态？如何确保不会产生“脏数据”或不一致？这就是分布式一致性算法需要解决的问题。

### 1.2 常见的一致性算法

提到分布式一致性，很多人首先会想到 **Paxos**。Paxos 拥有严谨的数学证明，但实现和理解都相对晦涩。2014 年，**Raft** 作为对
Paxos 的“可读性改进版本”被提出，它把一致性过程分解成更易理解的几个步骤，且在保证安全性的同时更易实现，被广泛应用于 **etcd
**、**Consul**、**TiKV** 等工业级项目中。

### 1.3 Raft 的设计目标

- **容易理解**：相比于 Paxos，Raft 在抽象和实现上都力图简单清晰。
- **强一致性**：多个节点对日志条目的顺序与内容最终达成一致。
- **高可用**：在**大多数节点**存活的情况下，系统可继续对外服务。
- **可扩展性**：支持动态地添加或移除节点（配置变更）。

### 1.4 Raft 可视化

{{<raw>}}
<iframe src="https://raft.github.io/raftscope/index.html" title="raft visualization" aria-hidden="true" style="border: 0; width: 800px; height: 580px; margin-bottom: 20px"></iframe>
{{</raw>}}

------

## 2. Raft 的核心思路

### 2.1 流程概览

Raft 将共识问题分解为三个子问题：

1. **领导者选举（Leader Election）**：如何从多个节点中选出一个“Leader”。
2. **日志复制（Log Replication）**：Leader 收到写请求后，如何安全地将日志复制到大多数节点。
3. **安全性（Safety）**：在 Leader 崩溃或网络分区时，如何确保系统不会出现日志丢失或被覆盖的情况。

在 Raft 中，节点分为三类角色：

- **Leader**：处理客户端请求并将其复制到其他 Follower；监控故障。
- **Follower**：被动接收 Leader 的日志复制 RPC 和心跳。
- **Candidate（候选者）**：在选举阶段争取成为新 Leader 的角色。

系统的时序被分割成一个又一个的 **Term（任期）**。同一任期里最多只能有一个合法 Leader。如果本任期没能成功选出 Leader 或
Leader 崩溃了，则进入下一个任期重新选举。

### 2.2 数据结构

实现 Raft 时通常需要维护：

1. **Term（任期号）**：单调递增的数值，标识当前的任期。
2. **Log（日志）**：存储客户端请求或命令，每条日志包含 `index`, `term`, `command`。
3. **commitIndex（已提交索引）**：当前已对外生效的最高日志索引。
4. **lastApplied（最后应用索引）**：本节点已经应用到本地状态机的最高日志索引，$\text{lastApplied} \leq \text{commitIndex}$。
5. **nextIndex[]**：在 Leader 中维护，对每个 Follower 记录下一条需要发送的日志索引。
6. **matchIndex[]**：在 Leader 中维护，对每个 Follower 记录该 Follower 已复制的最高日志索引。

------

## 3. 角色与状态变迁

### 3.1 Follower

- **初始状态**：系统启动时节点都处于 Follower；或者候选者选举失败后回到 Follower。
- 行为：
    - 接收并响应 Leader 的日志复制 RPC、心跳消息，以及候选者的投票请求。
    - 超过选举超时没收到任何 Leader 或候选者消息，就会转变为 Candidate。

### 3.2 Candidate

- **触发条件**：Follower 超时后，成为 Candidate 发起选举。
- 主要行为：
    1. 将 `currentTerm` + 1，给自己投票 (`voteFor = self`)。
    2. 并行向其他节点发送“请求投票”RPC。
    3. 若获得多数票，则成为 Leader；若有更新任期的 Leader 出现，则回到 Follower；若超时还未选出 Leader，则启动下一轮选举。

### 3.3 Leader

- **触发条件**：Candidate 获得多数票。
- 主要行为：
    1. 向所有节点周期性发送心跳 (AppendEntries RPC) 防止它们发起选举。
    2. 处理客户端请求，封装为日志条目写入自身日志后，再广播给其他 Follower。也就是说，强一致场景下，Follower/Candidate
       是不负责处理读写操作的，只是作为 Leader 的冗余来增强可用性。
    3. 当大多数节点都复制某条日志后，更新 `commitIndex` 并通知 Follower 提交。
    4. 负责更新集群配置（增删节点），并以安全方式提交对应日志条目。

------

## 4. Leader 选举流程

Raft 的选举流程概括如下：

1. **Follower 超时**
   如果 Follower 超过选举超时时间没收到 Leader 心跳或日志复制消息，便会切换到 Candidate。

2. **Candidate 发起选举**

    - `currentTerm++`
    - `voteFor = candidateID`
    - 重置选举计时器
    - 向所有节点发送“请求投票”RPC，包含：
      $\langle \text{candidateTerm}, \text{candidateId}, \text{lastLogIndex}, \text{lastLogTerm} \rangle$

3. **节点响应投票**
   若以下条件满足，则投票给请求者：

    - 请求者任期号 >= 本节点任期号
    - 本节点本任期尚未投过票
    - 请求者日志不比自己旧（Term 更新或 Index 更大）

   否则拒绝投票。

4. **完成选举**

    - 若 Candidate 获得多数票 => 成为 Leader。
    - 若超时前没拿到多数票 => 进入下一轮选举（Term 再增 1）。
    - 若在此期间收到了来自更高任期 Leader 的消息 => 退回 Follower。

5. **Leader 初始化**
   成为 Leader 后：

    - 初始化 `nextIndex[] = (Leader 的最新日志索引 + 1)`
    - 初始化 `matchIndex[] = 0`
    - 立刻广播心跳，宣告自己上任。

------

## 5. 日志复制 (Log Replication)

### 5.1 AppendEntries RPC

这是 Raft 日志复制和心跳的核心 RPC。请求与响应的字段示意：

- **请求**：
  $ \langle \text{term}, \text{leaderId}, \text{prevLogIndex}, \text{prevLogTerm}, \text{entries[]}, \text{leaderCommit} \rangle$
    - `entries[]` 为空时，就起到心跳作用。
    - `prevLogIndex` 和 `prevLogTerm` 用来匹配 Follower 日志，若不一致则复制失败。
- **响应**：
  $\langle \text{term}, \text{success} \rangle$
    - `term`：Follower 的当前任期（如比请求者更大，则请求者更新任期，退回 Follower）。
    - `success`：是否成功匹配并追加日志。

### 5.2 日志复制核心逻辑

1. **Leader 先写入本地日志**：接到客户端写请求，先形成新日志条目 `[index, term, command]` 写到自己日志。
2. **Leader 发送 AppendEntries**：并行向所有 Follower 发送该新日志条目。
3. **Follower 检查并匹配**：若 `prevLogIndex/prevLogTerm` 不匹配，则返回 `success = false`，Leader 会回退并重试。
4. **提交 (Commit)**：当 Leader 发现大多数节点都复制了某条日志索引 N，就将 `commitIndex` 更新到 N，并在后续心跳中告知
   Follower “可以提交到 N 了”，从而把日志应用到状态机。

### 5.3 重要保证：日志一致性

- **Log Matching Property**：相同索引、相同任期 => 前面的日志均一致；确保不会出现相同位置却存不同命令的情况。
- **Leader Completeness Property**：在任期 $t$ 被提交的日志，在之后任何任期里当选的 Leader 日志中必然存在这条日志；保证已经提交的日志不被丢弃或覆盖。

------

## 6. 安全性 (Safety)

### 6.1 为什么 Raft 能够保证一致性

1. **多数派机制**：决策（如提交日志）需得到大多数节点同意，容忍少量故障。
2. **任期机制**：只相信来自更大任期的消息，避免跨任期日志冲突。
3. **日志匹配**：Follower 必须先匹配前一条日志，再能追加新日志，防止分叉。

### 6.2 Leader 崩溃与日志安全继承

- Leader 崩溃后，Follower 超时进入 Candidate，发起新任期选举。
- 若新的 Leader 当选，它的日志一定是集群中最“新”的（因投票规则需多数节点认同）；因此已提交的日志不会被丢弃。
- 那些未复制到大多数节点的日志可能会被新 Leader 覆盖，但这是正确的“安全行为”，因为这些日志尚未在集群中达成共识。

------

## 7. 实现要点与难点

### 7.1 选举超时 (Election Timeout)

- 每个节点的选举超时在 [150ms, 300ms]（或更大范围）随机化。
- 这样能减少“同时发起选举”导致的冲突。

### 7.2 心跳间隔 (Heartbeat Interval)

- Leader 需要定期（如 50~100ms）给 Follower 发心跳，重置它们的选举超时。
- 心跳也是空的 AppendEntries RPC，只是不附带任何日志条目。

### 7.3 日志冲突处理

- 遇到 Follower 日志与 Leader 不匹配时，需要回退到匹配位置。
- Raft 提供了几种优化方案（如在日志中维护更丰富的索引信息），以减少反复重试的 RPC。

### 7.4 持久化

- Raft 节点需要**持久化**：`currentTerm`、`voteFor`、以及写入的日志。
- 每当任期或日志更新，都应先写入硬盘日志再返回成功，以便节点宕机重启后能恢复状态。
- Raft 通常使用顺序写入日志 + 按需截断 + 快照等方式来提高硬盘写入性能。

### 7.5 状态机

- 已提交的日志会被应用到**状态机**中，由用户定义具体逻辑（例如键值存储、数据库操作等）。
- Raft 保证日志顺序一致，但具体执行过程在状态机中进行。

### 7.6 集群配置变更

- 实际工程中常需要添加或移除节点。
- Raft 使用“两阶段”配置变更机制：旧配置 -> 联合配置（包含新旧节点）-> 新配置，防止在配置过渡中出现多数派混乱。

------

## 8. Raft 正确性证明核心性质

### 8.1 分布式环境假设与安全性/活性

1. Raft 假设了**部分同步网络**：即大多数时候网络是同步的（有稳定的最大延迟），但偶尔可能发生长延迟或分区。只要网络最终恢复到可通信状态，Raft
   就能完成共识。
2. **安全性 (Safety)**：无论网络如何不稳定，都不会出现已提交的日志遭回退或两个节点在同一索引应用不同命令等冲突。
3. **活性 (Liveness)**：只要网络处于同步状态足够长时间，Raft 最终能选出一个 Leader
   并持续提交新日志。若网络一直分区或消息丢失，再好的分布式算法也可能阻塞，这是著名的 FLP (Fischer–Lynch–Paterson) 不可解定理。

### 8.2 主要性质与整体思路

Raft 依赖以下两大核心性质，来保证系统日志在节点之间保持一致且不会回退：

1. **Log Matching Property（日志匹配性质）**
   “若在两个节点的某日志索引 $i$ 处，任期相同，则从开头到 $i$ 的整段日志都一致。”
2. **Leader Completeness Property（领导者完备性质）**
   “若某条日志在任期 $t$ 已经被提交，则在之后任期的任何 Leader 的日志中，也必定包含该条日志。”

基于这两点，可以推导出**状态机安全性 (State Machine Safety)**：

> 一旦某节点在索引 $i$ 处应用到命令 $cmd$，就不会再有节点在同一索引 $i$ 处应用到与 $cmd$ 不同的命令。

### 8.3 日志匹配性质 (Log Matching Property)

> **性质表述**：如果在任意两个节点的某索引 $i$ 处的任期号相同，则两节点从 1 到 $i$ 的日志条目都完全相同（任期与命令都一致）。

- **证明思路**：Raft 的复制规则要求 Follower 先匹配 `prevLogIndex` & `prevLogTerm` 后才能追加新日志，否则返回失败并令
  Leader 回退。所以只有当它们前面的日志完全一致时，才能写入同一个 `(index, term)`。由此归纳可知，相同位置、相同任期必然拥有相同的前序日志。

### 8.4 Leader 完备性质 (Leader Completeness Property)

> **性质表述**：若某条日志在任期 $t$ 上被提交（写到了大多数节点），则后续任何任期的合法 Leader 都一定包含这条日志。

- **证明思路**：日志被提交意味着一个多数派都写了它；新的 Leader
  当选需要获得多数派投票；投票时每个节点会拒绝给日志“落后”它的候选者投票，因此能当选的候选者必然已包含所有已提交日志；由此推论，那条在任期 $t$
  提交的日志不会被“忘记”或覆盖。

### 8.5 选举安全 (Election Safety)

> **命题**：同一任期 $t$ 内不可能有两个不同节点都获得多数派投票从而成为 Leader。

- **核心原因**：在任期 $t$ 内，每个节点只能投 1 票，若一个候选者已得到多数票，就不可能再有另一个候选者也拿到多数票（因为多数派的节点已经投票给前者，不可能重复投票）。

### 8.6 已提交日志不可回退 (No Commit Overwritten)

> **命题**：若某条日志已被提交，则不会被覆盖为不同命令或被撤销。

- **证明思路**：只要日志已写在多数派，后续想要覆盖它，必须取得这些多数派节点投票并成功将日志写入。但多数派节点若发现候选者“缺失”这条日志，会拒绝投票或拒绝
  AppendEntries 的匹配，故无法形成新的多数派来覆盖这条日志。

### 8.7 状态机安全性 (State Machine Safety)

> **命题**：如果节点 A 在索引 $i$ 处应用了命令 $cmd$，则不会有节点 B 在同一索引 $i$ 处应用不同的命令 $cmd' \neq cmd$。

- **证明思路**：应用到状态机说明该日志已提交；提交意味着它已复制到多数派，后续新 Leader
  也必然携带该日志；不可能再有并行的、冲突的日志写入同一个索引被大多数节点接受。

### 8.8 活性 (Liveness)

- 在正常的部分同步网络中，一旦 Leader 稳定，客户端的请求会被源源不断提交。
- 若 Leader 崩溃或网络暂时分区，也会在恢复后启动选举，最终选出新 Leader。
- 在完全异步或永远分区的情况下，所有分布式一致性协议都无法保证必然的活性（FLP 定理），但只要网络“偶尔稳定”，Raft 就能继续前行。

综上所述，Raft 在设计上兼顾了**易理解**、**易实现**与**强一致性**
三大目标，通过任期、选举、日志复制、以及多数派机制，确保了分布式系统中对数据的线性一致(Linearizable) 语义。其核心安全性可归结为：

- 不会同时出现两个合法的 Leader。
- 已提交的日志永不回退。
- 已提交的日志在新的 Leader 身上依旧保留。
- 保证同一个 (index, term) 位置不会在不同节点上出现不同命令。
- 保证已经在某任期提交的日志不会在后续 Leader 上消失。

------

## 9. 从零实现一个最简 Raft：关键步骤

1. **定义数据结构**
    - `currentTerm`、`voteFor`、`log[]`、`commitIndex`、`lastApplied` 等
    - 节点角色 (Follower/Candidate/Leader)
    - 定时器、RPC 通道等
2. **持久化层**
    - 将任期、投票、日志等关键数据写盘或存于 RocksDB 等存储引擎
    - 重启时先从存储中加载
3. **RPC 通信层**
    - 实现 `RequestVote` 和 `AppendEntries` 两类 RPC
    - 处理网络异常、超时重试
4. **事件循环 & 定时器**
    - 定期检查是否收到 Leader 心跳
    - 若超时则发起选举
    - 若是 Leader，则定期发心跳
    - 处理网络 RPC 并更新本地状态
5. **Leader 选举**
    - Follower 超时 -> Candidate 发起投票 -> 若获得多数 -> Leader
    - 若失败或遇到更高任期 Leader -> 回到 Follower
6. **日志复制**
    - Leader 收到新命令 -> 写本地日志 -> AppendEntries 给 Follower
    - 大多数节点复制 -> Leader 提交并通知 Follower 提交
7. **故障恢复**
    - 节点重启后先从存储中恢复状态
    - Leader 或网络故障后，会通过选举超时机制继续选举新的 Leader
8. **测试与验证**
    - 模拟网络延迟、分区、节点故障等，检查 Raft 是否能正确保持一致性和对外可用性

### 代码样例

```c#
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

// 这个代码示例关注 Raft 算法的核心选举逻辑，省略了网络通信和持久化等细节。
namespace RaftDemo
{
    #region 数据结构
    
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
        // 为简化，不在这里携带更多回退信息；如果携带更多信息，可以更快回退 nextIndex 来寻找匹配位置，减少网络交互次数。
    }

    public interface IRaftRpc
    {
        RequestVoteResponse RequestVote(RequestVoteRequest request);
        AppendEntriesResponse AppendEntries(AppendEntriesRequest request);
    }

    #endregion

    #region RaftNode 核心类

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

        // 仅 Leader 需要维护
        private Dictionary<string, int> _nextIndex = new Dictionary<string, int>();
        private Dictionary<string, int> _matchIndex = new Dictionary<string, int>();

        private CancellationTokenSource _cts;
        private Task _timerTask;

        // Demo 中的状态机用一个简单的列表记录命令
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

        // 用于测试，从外部输入命令
        public void SendClientCommand(string command)
        {
            if (_role != NodeRole.Leader)
            {
                Console.WriteLine($"[{_nodeId}] I'm not leader, ignoring client command.");
                return;
            }

            // 1. 将命令追加到本地日志
            var newLogIndex = LastLogIndex() + 1;
            _log.Add(new LogEntry
            {
                Index = newLogIndex,
                Term = _currentTerm,
                Command = command
            });

            Console.WriteLine($"[{_nodeId}] Leader received client command '{command}', logIndex={newLogIndex}.");

            // 2. 异步向其他节点发送 AppendEntries
            BroadcastAppendEntries();
        }

        #region 核心RPC实现

        public RequestVoteResponse RequestVote(RequestVoteRequest request)
        {
            lock (this)
            {
                // 如果请求中的Term比本地大，更新本地Term并变成Follower
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

                // 如果请求的任期 < 本地任期，则拒绝
                if (request.Term < _currentTerm)
                {
                    return response;
                }

                // 检查是否已经投票给其它候选人，或者日志是否足够新
                var myLastLogIndex = LastLogIndex();
                var myLastLogTerm = LastLogTerm();

                bool logIsAtLeastUpToDate = 
                    (request.LastLogTerm > myLastLogTerm) ||
                    (request.LastLogTerm == myLastLogTerm && request.LastLogIndex >= myLastLogIndex);

                if ((_votedFor == null || _votedFor == request.CandidateId) && logIsAtLeastUpToDate)
                {
                    _votedFor = request.CandidateId;
                    response.VoteGranted = true;
                    // 重置选举超时
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

                // 如果Term < 本地Term, 直接拒绝
                if (request.Term < _currentTerm)
                {
                    return response;
                }

                // 如果Term比本地大，更新Term并转为Follower
                if (request.Term > _currentTerm)
                {
                    _currentTerm = request.Term;
                    _role = NodeRole.Follower;
                    _votedFor = null;
                }

                // 收到来自 Leader 的心跳/日志复制, 重置选举超时
                ResetTimer();

                // 由于简化，这里只做基本检查：
                // 检查本地日志在 prevLogIndex 的Term 是否匹配
                if (request.PrevLogIndex > 0)
                {
                    if (request.PrevLogIndex > _log.Count)
                    {
                        // 不匹配 (本地日志比Leader提供的还短)
                        return response;
                    }
                    else
                    {
                        var localTerm = _log[request.PrevLogIndex - 1].Term;
                        if (localTerm != request.PrevLogTerm)
                        {
                            // 不匹配 (任期冲突)
                            return response;
                        }
                    }
                }

                // 如果匹配则继续：先覆盖本地冲突日志
                foreach (var entry in request.Entries)
                {
                    if (entry.Index <= _log.Count)
                    {
                        // 存在冲突或相同Index日志，覆盖掉
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

                // 更新commitIndex
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

        #region 选举与心跳定时器

        private void ResetTimer()
        {
            _cts?.Cancel();
            _cts = new CancellationTokenSource();
            _timerTask = RunTimer(_cts.Token);
        }

        private async Task RunTimer(CancellationToken token)
        {
            // 在实际生产环境中，选举超时一般设置为150~300ms左右，
            // 这里为了演示效果加长到了1.5~3秒，方便我们在Console中观察到日志输出。
            var electionTimeout = _rand.Next(1500, 3000); // 1.5~3s 之间随机
            var heartbeatInterval = 500; // Leader 心跳间隔 0.5s

            var start = DateTime.UtcNow;
            while (!token.IsCancellationRequested)
            {
                await Task.Delay(100, token);
                var elapsed = (DateTime.UtcNow - start).TotalMilliseconds;

                if (_role == NodeRole.Leader)
                {
                    // Leader 周期性发送心跳
                    if (elapsed >= heartbeatInterval)
                    {
                        BroadcastAppendEntries();
                        start = DateTime.UtcNow;
                    }
                }
                else
                {
                    // Follower or Candidate，需要判断是否触发选举
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

                // 重置选举超时
                ResetTimer();
            }

            // 发起投票
            var request = new RequestVoteRequest
            {
                Term = _currentTerm,
                CandidateId = _nodeId,
                LastLogIndex = LastLogIndex(),
                LastLogTerm = LastLogTerm()
            };

            var votesGranted = 1; // 自己投自己
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
                            // 如果对方term更大，转为Follower
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

            // 初始化 nextIndex, matchIndex
            foreach (var node in _dispatcher.GetAllNodes())
            {
                if (node == _nodeId) continue;
                _nextIndex[node] = LastLogIndex() + 1;
                _matchIndex[node] = 0;
            }

            // 立即发送一次心跳
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

                    // 这里简化，每次只发送一段有限的日志
                    // 可以根据实际需求发送更多
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
                                    // 说明对方已经匹配了 prevLogIndex
                                    // 更新 nextIndex & matchIndex
                                    var lastEntry = entriesToSend.LastOrDefault();
                                    if (lastEntry != null)
                                    {
                                        _matchIndex[otherId] = lastEntry.Index;
                                        _nextIndex[otherId] = lastEntry.Index + 1;
                                    }

                                    // 更新 commitIndex
                                    UpdateCommitIndex();
                                }
                                else
                                {
                                    // 回退 nextIndex 重试 (这里是最简单的回退策略)
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
            // Leader 根据 matchIndex 更新 commitIndex
            // 找到一个N，使得N大于当前commitIndex，并且有半数以上的matchIndex >= N, 并且_raftLog[N].Term == currentTerm
            for (int i = _log.Count; i > _commitIndex; i--)
            {
                var count = _matchIndex.Values.Count(m => m >= i) + 1; // +1 包含自己
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
            // 将 [lastApplied+1 ... commitIndex] 的日志应用到状态机
            while (_lastApplied < _commitIndex)
            {
                _lastApplied++;
                var cmd = _log[_lastApplied - 1].Command;
                _stateMachine.Add(cmd);
                Console.WriteLine($"[{_nodeId}] Apply LogIndex={_lastApplied}, Cmd={cmd}");
            }
        }

        #endregion

        #region 帮助方法

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

    #region 简易“RPC调度器”模拟网络

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

            // 等待几秒，让选举完成
            Task.Delay(5000).Wait();

            // 尝试发送命令给节点1, 如果它是Leader则执行，否则会提示自己不是Leader
            node1.SendClientCommand("SET X=100");

            Task.Delay(3000).Wait();

            // 停止节点2, 模拟节点宕机
            Console.WriteLine("\n** Stopping Node2 to simulate crash **\n");
            node2.Stop();

            // 等待一段时间后，再发命令
            Task.Delay(5000).Wait();
            node1.SendClientCommand("SET Y=200");

            // 再等等，让日志复制结束
            Task.Delay(5000).Wait();

            // 打印一下每个节点已应用到状态机的数据
            Console.WriteLine($"\nNode1 state: {string.Join(", ", node1.StateMachine)}");
            Console.WriteLine($"\nNode2 state: {string.Join(", ", node2.StateMachine)} (Should not receive new logs after crash)");
            Console.WriteLine($"\nNode3 state: {string.Join(", ", node3.StateMachine)}");

            // 结束
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
