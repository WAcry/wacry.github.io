---
title: "Análise Profunda do Teorema CAP: Construindo Sistemas Distribuídos de Alta Concorrência e Alta Disponibilidade"
date: 2024-12-27
draft: false
description: "Discussão da teoria à prática sobre a aplicação do teorema CAP em sistemas distribuídos."
summary: "Discussão da teoria à prática sobre a aplicação do teorema CAP em sistemas distribuídos."
tags: [ "Sistemas Distribuídos", "Teorema CAP", "Design de Sistemas", "Modelos de Consistência" ]
categories: [ "Design de Sistemas" , "Sistemas Distribuídos" ]
---

## I. Teorema CAP

### 1.1 O que é o Teorema CAP

O **Teorema CAP** foi proposto por Eric Brewer em 2000, e seu ponto central é:

- **C (Consistência)**: Todos os nós do sistema veem os mesmos dados no mesmo instante. Mais estritamente, quando um cliente lê dados, o resultado deve ser consistente com os dados mais recentemente submetidos, independentemente de qual réplica seja lida (geralmente referindo-se à consistência forte/consistência linear).
- **A (Disponibilidade)**: O sistema ainda pode fornecer serviços normais quando ocorrem falhas parciais, e cada solicitação pode obter uma "resposta válida" em um tempo razoável (não necessariamente bem-sucedida, incluindo respostas de falha corretas).
- **P (Tolerância a Partição)**: O sistema pode tolerar partições de rede (comunicação inacessível entre nós), e mesmo que a rede se divida, o sistema pode fornecer um certo grau de disponibilidade ou consistência.

Em ambientes distribuídos reais, as partições de rede são inevitáveis, então **P** é basicamente considerado um "item obrigatório". Quando ocorre uma partição de rede, o sistema não pode levar em consideração simultaneamente a **consistência forte** dos dados em todos os nós e a **alta disponibilidade**, e só pode escolher entre C e A, resultando nos dois principais tipos **CP** e **AP**.

### 1.2 Limitações do Teorema CAP

É importante notar que o Teorema CAP em si é uma teoria de nível relativamente alto, usada para orientação conceitual, e **não deve ser simplesmente entendido como "escolher C ou escolher A"**. Existem alguns equívocos comuns:

1. **C não é necessariamente consistência forte**
   O C no Teorema CAP geralmente se refere à consistência no sentido mais estrito (ou seja, consistência linear). No entanto, em sistemas reais, existem muitos modelos de granularidade fina para escolher, como consistência fraca, leitura confirmada (Read Committed), consistência causal (Causal Consistency), etc.
2. **Disponibilidade não é 0 ou 1**
   Não é que escolher CP signifique que a disponibilidade seja completamente sacrificada; ou escolher AP signifique que a consistência não tenha garantia. Tanto a disponibilidade quanto a consistência têm diferentes graus de espaço de compensação e estratégias de degradação.
3. **Consistência eventual** não viola o CAP
   É uma solução de compromisso muito comum, usando uma consistência de escrita mais baixa em troca de maior disponibilidade e taxa de transferência, e convergindo dados em segundo plano de forma assíncrona.

Portanto, o Teorema CAP deve ser combinado com vários **modelos de consistência** e **padrões de arquitetura de alta disponibilidade** em cenários específicos para gerar um verdadeiro valor de orientação prática.

------

## II. Modelos de Consistência de Sistemas Distribuídos

A classificação dos modelos de consistência é muito rica, mas os modelos principais comuns podem ser divididos em: **consistência forte** e **consistência fraca** (que inclui consistência eventual, consistência causal, etc.). Este artigo apresenta principalmente **consistência forte** e **consistência eventual**, e explica suas aplicações comuns nos modos CP ou AP.

### 2.1 Consistência Forte

**Consistência Forte (Strong Consistency)**, também conhecida como **Consistência Linear (Linearizability)**, refere-se ao fato de que, uma vez que uma operação de escrita é concluída e retorna com sucesso, qualquer operação de leitura subsequente pode ler o conteúdo atualizado. Ou seja, o sistema se comporta como se todas as operações fossem executadas em série.

- **Implementação comum**: Depende da replicação síncrona e de um mecanismo de quórum (maioria), e usa protocolos (como Paxos/Raft) para garantir que haja apenas um líder (Leader) válido no sistema, e todas as operações são gravadas no log em ordem e replicadas para a maioria dos nós.
- Vantagens e desvantagens:
    - Vantagens: Garante a correção de dados mais estrita, e os dados lidos em qualquer momento não "retrocedem".
    - Desvantagens: Em caso de instabilidade de rede, partição ou falha do líder, para manter a consistência, as operações de escrita são frequentemente bloqueadas, levando a uma diminuição da disponibilidade geral; o desempenho e a taxa de transferência também são relativamente mais baixos.

### 2.2 Consistência Eventual

**Consistência Eventual (Eventual Consistency)** é uma forma típica de consistência fraca, que exige apenas que, se o sistema não tiver novas operações de atualização, com o tempo, os dados de todas as réplicas convergirão gradualmente para o mesmo estado. Durante este período, os usuários que leem dados de réplicas podem ver valores desatualizados, mas eventualmente se tornarão consistentes.

- **Implementação comum**: Protocolo Gossip, replicação assíncrona de várias réplicas, CRDT (Conflict-free Replicated Data Type), etc.
- Vantagens e desvantagens:
    - Vantagens: Alta disponibilidade, alta taxa de transferência, baixa latência de operações de escrita e alta tolerância a partições de rede.
    - Desvantagens: É necessário tolerar inconsistências de dados de curto prazo, a lógica da aplicação é mais complexa e pode ser necessário realizar detecção e fusão de conflitos.

------

## III. Protocolos e Algoritmos de Consistência Comuns

Para manter a consistência entre as réplicas do sistema distribuído, a indústria propôs muitos algoritmos e protocolos clássicos. A seguir, apresentamos brevemente alguns deles:

### 3.1 Paxos

Paxos é um algoritmo de consistência distribuída proposto por Leslie Lamport na década de 1990, usado principalmente para implementar consistência forte ou consistência linear.

- **Princípio básico**: Através da divisão de funções (Proponente, Aceitador, Aprendiz), várias rodadas de votação são realizadas para determinar se uma operação ou valor é aceito pela maioria dos nós.
- Vantagens e desvantagens:
    - Vantagens: Pode chegar a um consenso sob partições de rede e falhas de nós, e tem alta segurança.
    - Desvantagens: A implementação é complexa, a depuração e a solução de problemas são difíceis e várias rodadas de votação levam a um desempenho limitado. A indústria usa principalmente suas variantes (Multi-Paxos, etc.).

### 3.2 Raft

Raft foi formalmente proposto em 2013, com o objetivo de **simplificar a implementação e a dificuldade de compreensão, garantindo a mesma segurança que o Paxos**. Ele estabelece um **líder (Leader)** estável para realizar centralizadamente a replicação de logs e a recuperação de falhas:

- **Etapas principais**: Eleição de líder (Leader Election), replicação de logs (Log Replication), segurança (Safety), etc.
- **Aplicações comuns**: Etcd, Consul, TiKV, LogCabin, etc. são todos baseados em Raft para implementar replicação de consistência forte.
- Vantagens e desvantagens:
    - Vantagens: Relativamente fácil de entender, menos código de implementação; bom desempenho para clusters de pequena e média escala.
    - Desvantagens: Depende do nó principal (Líder), e falhas ou partições do nó principal causarão um bloqueio de escrita temporário; em clusters de grande escala ou implantações entre regiões, a latência e a disponibilidade serão afetadas.

### 3.3 Protocolo Gossip

O protocolo Gossip (fofoca) não é um protocolo de consenso tradicional, usado principalmente em cenários descentralizados para trocar metadados ou informações de estado por meio de interações aleatórias de nós, de modo a se espalhar e convergir em toda a rede.

- **Características**: Descentralizado, baixo custo, troca periódica e aleatória de mensagens entre nós.
- **Aplicações comuns**: Cassandra, Riak, gerenciamento de membros distribuídos (como Serf), etc., usados para implementar consistência eventual, sincronização de estado de réplica, etc.
- Vantagens e desvantagens:
    - Vantagens: Boa escalabilidade, simples de implementar, adequado para cenários que não exigem alta consistência e alta escalabilidade.
    - Desvantagens: A garantia de consistência é fraca e são necessários meios de tratamento de conflitos de nível superior (como CRDT, fusão de número de versão, etc.) para resolver conflitos.

### 3.4 2PC / 3PC

Em cenários de transações distribuídas, os protocolos de commit comuns são **2PC (Two-phase Commit)** e **3PC (Three-phase Commit)**:

- **2PC**: O coordenador notifica todos os participantes para "preparar (prepare)", se todos forem bem-sucedidos, ele transmite "commit (commit)", caso contrário, "abort (abort)".
- **3PC**: Adiciona uma etapa com base em 2PC para reduzir o bloqueio causado por falhas de ponto único, mas a implementação é mais complexa e ainda existem problemas de indisponibilidade em cenários extremos de partição de rede ou falha.
- Vantagens e desvantagens:
    - Vantagens: Fácil de entender, semântica de transação clara, amplamente utilizada em bancos de dados distribuídos, filas de mensagens, etc.
    - Desvantagens: Forte dependência do coordenador, risco de bloqueio; pode não ser possível continuar a transação quando a rede é particionada por um longo tempo.

------

## IV. As Duas Principais Escolhas do CAP: CP e AP

Depois que determinamos que **P** é um atributo "obrigatório", se um sistema distribuído quiser continuar a fornecer serviços durante uma partição de rede, ele deve escolher entre **C** e **A**. O design comum do sistema é, portanto, dividido em dois campos principais: **CP** e **AP**.

### 4.1 Sistemas CP

**CP (Consistência + Tolerância a Partição)**: Ao encontrar uma partição de rede, o sistema escolherá **priorizar a garantia de consistência** e **sacrificar a disponibilidade** quando necessário.

- Implementação típica:
    - Consenso da maioria (Paxos, Raft, etc.), mais da metade dos nós precisam estar ativos e chegar a um consenso para permitir a escrita.
    - Se um quórum (número legal) não puder ser alcançado no momento ou se o nó principal falhar, o sistema bloqueará ou rejeitará operações de escrita para evitar inconsistências de dados causadas por divisão cerebral.
- Aplicações comuns:
    - Zookeeper, Etcd, Consul, serviços de bloqueio distribuído, gerenciamento de metadados distribuídos, etc.
    - Processos principais de transações financeiras, sistemas de contabilidade bancária e outros cenários que exigem alta consistência.
- Características:
    - Possui garantia de dados estrita: prefere desligar a ter um mestre duplo ou confusão de dados.
    - Sacrifica uma certa disponibilidade: quando ocorre uma partição de rede ou failover, haverá uma janela de serviço indisponível ou rejeição de operações de escrita.

### 4.2 Sistemas AP

**AP (Disponibilidade + Tolerância a Partição)**: Ao encontrar uma partição de rede, o sistema escolherá **priorizar a garantia de disponibilidade** e, ao mesmo tempo, **relaxar a consistência**.

- Implementação típica:
    - Consistência eventual, replicação multi-mestre, protocolo Gossip, estratégia de consistência ajustável no estilo Dynamo, etc.
- Aplicações comuns:
    - Bancos de dados NoSQL (Cassandra, Riak, DynamoDB, etc.), sistemas de cache distribuído (Redis Cluster), etc.
    - Redes sociais, coleta de logs, sistemas de recomendação e outros negócios que exigem alta disponibilidade, alta taxa de transferência e requisitos relativamente flexíveis de consistência de dados.
- Características:
    - Mesmo que haja uma partição, todos os nós ainda aceitam solicitações de leitura e escrita, garantindo que o sistema esteja "o mais disponível possível".
    - Pode haver inconsistências de dados de curto prazo, mas eles convergirão gradualmente em segundo plano por meio de sincronização assíncrona, fusão de conflitos, etc.

------

## V. Como Escolher entre CP e AP?

Em sistemas distribuídos de grande escala reais, é **raro depender de um único modelo**, mas sim processar diferentes dados ou cenários de negócios em camadas, a fim de buscar o melhor equilíbrio entre **consistência** e **disponibilidade**.

1. **Escolha CP para dados principais**
    - Como saldos de contas de usuários, pagamentos de pedidos, fluxos de transações financeiras, etc., que têm requisitos extremamente altos de consistência.
    - Tolere a indisponibilidade temporária de escrita causada por instabilidade de rede, mas não tolere erros no saldo ou no valor da transação.
2. **Escolha AP para dados de borda ou em cache**
    - Como o cache da página de detalhes do produto, logs de comportamento do usuário, listas de candidatos de recomendação, etc., que têm requisitos mais baixos de consistência.
    - Mais foco em alta concorrência e alta disponibilidade, capaz de tolerar atualizações atrasadas ou leituras sujas por um certo tempo.

Muitas empresas de internet adotarão uma **arquitetura híbrida**: os processos de transação principais usam armazenamento no estilo CP (como bancos de dados relacionais distribuídos ou armazenamento distribuído com consistência forte); os negócios periféricos ou cenários de "muitas leituras e poucas escritas" usam armazenamento no estilo AP ou soluções de cache.

------

## VI. Como CP e AP Alcançam Alta Concorrência e Consistência Eventual

### 6.1 Como os Sistemas CP Lidam com Alta Concorrência

Embora os protocolos de consenso enfrentem alta latência e baixa taxa de transferência quando o tamanho do nó de um único cluster e o número de solicitações de escrita são grandes, a concorrência e a escalabilidade ainda podem ser melhoradas pelos seguintes meios:

1. Leitura e escrita em lote
    - Empacote várias operações de escrita no cliente ou na camada intermediária e grave-as no nó líder de uma só vez, reduzindo as viagens de ida e volta da rede e as rodadas de protocolo.
2. Divisão de banco de dados e tabelas e vários clusters
    - Divida os dados em vários clusters (sharding) por lógica ou hash, e cada cluster ainda executa o protocolo CP; as solicitações são dispersas para diferentes shards por meio de roteamento ou camada de proxy.
    - Melhore a capacidade geral de concorrência e limite o impacto da falha ao escopo de um único shard.

> A taxa de transferência de um único cluster de shard de um sistema CP é geralmente 2 a 10 vezes menor do que a de um sistema AP.

### 6.2 Como os Sistemas AP Garantem a Consistência Eventual

Os sistemas AP geralmente podem fornecer alta taxa de transferência de escrita e disponibilidade de leitura, mas relaxam a consistência, portanto, é necessário implementar garantias de convergência de consistência em segundo plano ou na camada de lógica de negócios:

1. Número de versão (Vector Clock) ou carimbo de data/hora lógico
    - Atribua um número de versão (ou baseado em Lamport Clock / Hybrid Clock) a cada operação de atualização e realize a fusão ou a estratégia de vitória baseada em carimbo de data/hora (Last Write Wins) em cenários de conflito.
2. Protocolo Gossip / mecanismo anti-entropia
    - Os nós trocam periodicamente os dados ou metadados mais recentes e, se encontrarem conflitos, eles são mesclados.
3. Estratégia de consistência ajustável
    - Representado pelo modelo Dynamo, o cliente pode configurar parâmetros como `R` e `W` (como gravar a maioria, confirmação de réplica), de modo a ajustar a consistência e a disponibilidade de forma flexível.
4. Estratégia de resolução de conflitos personalizada
    - Combine a semântica de negócios para mesclar, como usar "união" para mesclar carrinhos de compras e usar CRDT (G-counter, PN-counter, etc.) para garantir a monotonicidade dos dados para contadores.

------

## VII. Implementação de Consistência Forte entre Shards de CP

No Capítulo VII, foi mencionado que **a divisão de bancos de dados e tabelas (Sharding)** pode "dividir" a pressão de um único cluster CP em vários subclusters para suportar maior concorrência. No entanto, quando os negócios precisam executar transações entre shards (ou seja, envolvendo atualizações de vários bancos de dados ou tabelas), eles ainda enfrentam o desafio da **consistência de vários shards**. Geralmente, existem as seguintes ideias:

1. **Transações distribuídas: 2PC / 3PC**
    - Se o aplicativo precisar realizar atualizações atômicas em vários shards, os protocolos de transação distribuída (como 2PC, 3PC) são geralmente usados para coordenar o commit ou rollback de cada shard.
    - Problemas e contramedidas:
        - 2PC/3PC dependem de um nó coordenador, que pode se tornar um gargalo de ponto único.
        - Em casos extremos de partição de rede grave ou falha do coordenador, pode ocorrer bloqueio.
        - Geralmente, a troca mestre-escravo, detecção de batimentos cardíacos e mecanismos de tempo limite, repetição idempotente, MVCC, etc. são usados para reduzir o impacto do bloqueio e o risco de inconsistência de dados.
2. **Arquitetura baseada em células (Cell-based)**
    - Divida os negócios em várias unidades autônomas, e os dados em cada unidade estão no mesmo conjunto de shards, garantindo que a maioria das transações seja concluída em uma única unidade, reduzindo as operações entre shards.
    - Use mecanismos assíncronos ou de consistência eventual nos limites da unidade para troca de dados, levando em consideração a alta disponibilidade e consistência geral.
3. **Banco de dados distribuído global + protocolo de consenso global**
    - Por exemplo, o Google Spanner implementa replicação de consistência forte em cada shard por meio de Paxos e usa a API TrueTime para fornecer carimbos de data/hora globais para garantir a consistência entre shards.
    - Esta solução tem uma complexidade de implementação extremamente alta, mas pode fornecer recursos de transação distribuída quase consistentes em um escopo global.

> **Resumo**: Para transações entre shards que exigem estritamente consistência forte, **2PC/3PC + coordenador** ainda são soluções comuns e, tanto quanto possível, a alta disponibilidade do coordenador é melhorada para reduzir a possibilidade de falha. No entanto, na prática de engenharia, as operações de escrita entre shards devem ser reduzidas o máximo possível, ou a complexidade do sistema deve ser reduzida limitando a maioria das transações ao escopo de um único shard por meio de ideias de unitização.

------

## VIII. Discussão de Casos Famosos

A seguir, discutiremos brevemente vários sistemas distribuídos que são frequentemente mencionados na indústria e veremos suas escolhas e métodos de implementação no CAP:

1. **Google Spanner**
    - Um sistema **CP** típico (pode até atingir a ilusão "CA" que o mundo exterior costuma dizer, mas na verdade ainda precisa sacrificar parte da disponibilidade).
    - Use carimbos de data/hora externos precisos fornecidos pelo TrueTime + replicação Paxos dentro de cada shard para garantir consistência forte entre data centers.
    - Adequado para transações financeiras globais ou cenários que exigem alta consistência, mas o custo da infraestrutura é extremamente alto.
2. **BigTable / HBase**
    - Superficialmente mais inclinado a **CP**, a consistência dos metadados é garantida por meio de coordenação distribuída entre RegionServer e Master.
    - No entanto, no caminho real de leitura e escrita, ele também pode fornecer certos meios de alta disponibilidade por meio de replicação assíncrona de várias réplicas, e a consistência de leitura pode ser ajustada de acordo com as necessidades do aplicativo.
3. **AWS DynamoDB**
    - Inclinado a **AP**, o design inicial foi inspirado no artigo Dynamo, e o nível de consistência pode ser ajustado por meio de parâmetros como `R` e `W`.
    - No modo padrão, ele fornece alta disponibilidade e consistência eventual, e também pode ativar a "leitura de consistência forte" (mas apenas garante a consistência forte de uma única partição, não necessariamente entre partições).
4. **Cassandra**
    - Também é uma tendência **AP**, o protocolo Gossip subjacente é usado para manter o estado da topologia do nó.
    - A consistência de leitura e escrita pode ser configurada para ler e escrever o número de réplicas `R` / `W`, de modo a realizar uma transição suave da consistência eventual para uma consistência mais forte.

> **Comparação visível**: Não existe um "AP ou CP" absoluto na engenharia, mas sim uma mistura de várias estratégias de consistência; a maioria dos sistemas fornece um certo grau de consistência ajustável para se adaptar a diferentes cenários de aplicação.

------

## IX. Resumo

1. **O Teorema CAP não é uma solução única**
    - Sistemas distribuídos reais não podem simplesmente dizer "Eu escolho C e desisto de A" ou "Eu escolho A e desisto de C".
    - O que é mais comum na indústria é escolher de forma flexível os modos **CP** ou **AP** para diferentes dimensões de dados e diferentes tipos de operação, e até mesmo dentro do mesmo sistema, diferentes tabelas/diferentes funções adotam diferentes estratégias de tolerância a falhas e consistência.
2. **AP não é absolutamente 100% disponível**
    - Por exemplo, Cassandra, DynamoDB, etc. também terão situações em que as solicitações não podem ser atendidas em casos extremos de partição de rede ou falha de grande área de nós.
    - Os sistemas AP são projetados para preferir "escrever primeiro, desde que a réplica possa ser escrita", sacrificando parte da garantia de consistência em troca de disponibilidade e taxa de transferência relativamente mais altas.
3. **CP também pode tentar alcançar alta disponibilidade**
    - Paxos/Raft também podem fornecer 99,99% ou até mais alta disponibilidade em circunstâncias normais, mas exigem mais investimento em rede, hardware e custos de engenharia, e ainda haverá bloqueio de escrita e sacrifício de disponibilidade para manter a consistência em partições de rede extremas.
4. **Arquitetura híbrida é a corrente principal**
    - Os cenários de transação principais insistem em consistência forte (CP), e os cenários auxiliares periféricos ou canais de cache adotam consistência fraca (AP), e os dois cooperam entre si.
    - É necessário combinar a tolerância de negócios, o ambiente de rede, o investimento de custo e as reservas técnicas da equipe para fazer uma escolha abrangente.

O Teorema CAP fornece uma estrutura de pensamento de alto nível para o design de sistemas distribuídos, ajudando-nos a tomar decisões racionais diante da realidade inevitável das partições de rede. Em sistemas reais, é necessário usar **modelos de consistência** mais ricos, **protocolos de consenso**, **mecanismos de replicação de várias réplicas** e práticas de engenharia (recuperação de desastres, degradação, idempotência, fusão de conflitos, etc.) para equilibrar consistência e disponibilidade.