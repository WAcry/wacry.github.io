---
title: "Problema da Mochila 01"
date: 2024-12-24
draft: false
description: "O problema da mochila clássico mais básico."
summary: "O problema da mochila clássico mais básico."
tags: [ "Algoritmo", "Programação Dinâmica", "Problema da Mochila" ]
categories: [ "Algoritmos e Estruturas de Dados" ]
---

## Problema

Existem $N$ itens. O volume do $i$-ésimo item é $s_i$ e seu valor é $v_i$.
Cada item só pode ser levado uma vez. Sob a premissa de não exceder o limite máximo de volume total $S$, encontre o valor total máximo $V$ que pode ser obtido.

## Formato de Entrada

A primeira linha contém dois inteiros, $N$ e $S$, separados por um espaço, representando o número de itens e o limite máximo de volume total, respectivamente.
As $N$ linhas seguintes contêm cada uma dois inteiros, $s_i$ e $v_i$, separados por um espaço, representando o volume e o valor do $i$-ésimo item, respectivamente.

## Formato de Saída

Imprima um inteiro representando o valor máximo.

## Intervalo de Dados

$$0 \le N, S \leq 1000$$

$$0 \le s_i, v_i \leq 1000$$

## Exemplo de Entrada

```
4 5
1 2
2 4
3 4
4 5
```

## Exemplo de Saída

```
8
```

## Solução

- Defina o estado: `f[i][j]` representa o valor máximo que pode ser obtido com os primeiros $i$ itens com um limite de volume de $j$.
    - Se o $i$-ésimo item não for levado, então `f[i][j] = f[i - 1][j]`
    - Se o $i$-ésimo item for levado, então `f[i][j] = f[i - 1][j - s[i]] + v[i]`
    - Ao implementar a transição de estado, preste atenção ao intervalo do domínio. Se $j < s_i$, então não considere o caso de levar o $i$-ésimo item. Porque se $j - s_i$ for negativo, o índice do array é inválido.
      Também pode ser explicado desta forma: o volume do $i$-ésimo item é maior que o limite de volume, então é impossível.
- Defina a condição inicial: Para os primeiros $0$ itens, qualquer limite de volume resulta em um valor de $0$, ou seja, `f[0][j] = 0`, `j` $\in [0, S]$.
- Complexidade de tempo: $O(NS)$.

## Código

```cpp
#include<bits/stdc++.h>
using namespace std;
int main() {
    int N, S;
    cin >> N >> S;
    vector<int> s(N + 1), v(N + 1);
    for (int i = 1; i <= N; i++) cin >> s[i] >> v[i];
    vector<vector<int>> f(N + 1, vector<int>(S + 1));
    for (int i = 1; i <= N; i++) {
        for (int j = 0; j <= S; j++) {
            f[i][j] = f[i - 1][j];
            if (j >= s[i]) f[i][j] = max(f[i][j], f[i - 1][j - s[i]] + v[i]);
        }
    }
    cout << f[N][S] << endl;
    return 0;
}
```

## Otimização DP 1D

- Comprimir o array bidimensional em um array unidimensional pode economizar significativamente espaço e melhorar a velocidade de execução até certo ponto (a desvantagem é que ele não pode atender aos requisitos especiais de alguns tipos de problemas).
- Observe que na transição de estado, `f[i][j]` está relacionado apenas a `f[i - 1][j]` e `f[i - 1][j - s[i]]`. Em outras palavras, no array bidimensional `f` no código,
  `f[i][j]` está relacionado apenas aos elementos na linha anterior que estão à sua esquerda ou na mesma coluna. Portanto, o array bidimensional pode ser comprimido em um array unidimensional ou um array rolante.
- Observe que no código abaixo, o segundo loop itera em ordem inversa. Isso ocorre porque queremos garantir que ao calcular `f[i][j]`, `f[i - 1][j - s[i]]` ainda não tenha sido atualizado.

```cpp
#include<bits/stdc++.h>
using namespace std;
int main() {
    int N, S;
    cin >> N >> S;
    vector<int> s(N + 1), v(N + 1);
    for (int i = 1; i <= N; i++) cin >> s[i] >> v[i];
    vector<int> f(S + 1);
    for (int i = 1; i <= N; i++) {
        for (int j = S; j >= s[i]; j--) {
            f[j] = max(f[j], f[j - s[i]] + v[i]);
        }
    }
    cout << f[S] << endl;
    return 0;
}
```

## Se o Número de Esquemas for Necessário

Não apenas o valor total máximo que pode ser obtido deve ser impresso, mas também "quantos métodos de seleção diferentes podem atingir esse valor total máximo". O seguinte descreve **como contar o número de esquemas** no problema da mochila 01.

### DP 2D para Contar Esquemas

O seguinte usa DP 2D como um exemplo para explicar.

- Defina o estado:
  - `dp[i][j]` representa "o valor máximo que pode ser obtido ao considerar os primeiros i itens com uma capacidade (limite de volume) de j".
  - `ways[i][j]` representa "o **número de esquemas** correspondentes ao valor máximo obtido ao considerar os primeiros i itens com uma capacidade de j".

- Transição de estado:
  1. Se o `i`-ésimo item não for selecionado:
     $$
       \text{dp}[i][j] = \text{dp}[i-1][j], 
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
     $$
  2. Se o `i`-ésimo item for selecionado (desde que $ j \ge s_i $):
     $$
       \text{dp}[i][j] 
         = \text{dp}[i-1][j - s_i] + v_i,
       \quad
       \text{ways}[i][j]
         = \text{ways}[i-1][j - s_i]
     $$
  3. Se deve selecionar ou não, o `dp[i][j]` final deve pegar o maior dos dois:
     - Se
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           > \text{dp}[i-1][j],
       $$
       então significa que "selecionar o i-ésimo item" tem um valor maior:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j - s_i] + v_i,
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j - s_i].
       $$
     - Se
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           = \text{dp}[i-1][j],
       $$
       significa que o valor máximo obtido pelos dois métodos é o mesmo, então o número de esquemas deve ser adicionado:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j], 
         \quad
         \text{ways}[i][j] 
           = \text{ways}[i-1][j] 
             + \text{ways}[i-1][j - s_i].
       $$
     - Se
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           < \text{dp}[i-1][j],
       $$
       então significa que "não selecionar o i-ésimo item" tem um valor maior, e o número de esquemas herda o número de esquemas ao não selecionar:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Condições iniciais:
  - `dp[0][j] = 0` significa que quando há 0 itens, o valor máximo obtido para qualquer capacidade é 0.
  - `ways[0][0] = 1` significa que o caso de "0 itens, capacidade 0" é um esquema viável (ou seja, não selecionar nada), e o **número de esquemas** é definido como 1.
  - Para `j > 0`, quando não há itens para escolher e a capacidade é maior que 0, é impossível obter qualquer valor positivo, e o número correspondente de esquemas é 0, ou seja, `ways[0][j] = 0`.

- Resposta final:
  - `dp[N][S]` é o valor máximo.
  - `ways[N][S]` é o número de esquemas para atingir esse valor máximo.
  - Complexidade de tempo: $O(NS)$.
  - Este problema também pode ser otimizado usando DP 1D.

## Se o Requisito for Atingir Exatamente o Limite de Volume

- Defina o estado: `f[i][j]` representa o valor máximo quando os primeiros `i` itens têm exatamente um volume de $j$.
- Se o `i`-ésimo item não for levado, então `f[i][j] = f[i - 1][j]`
- Se o `i`-ésimo item for levado, então `f[i][j] = f[i - 1][j - s[i]] + v[i]`
- Pode-se notar que não há diferença na transição de estado do problema original.
- No entanto, as condições iniciais são diferentes. Exceto por `f[0][0] = 0`, o resto `f[0][j]` = $-\infty$, `j` $\in [1, S]$. $-\infty$ representa um estado impossível.

## Se o Limite de Volume $S$ for Muito Grande (1e9), Enquanto o Número de Itens $N$ e o Valor Total Máximo $V$ forem Relativamente Pequenos

- Para tais problemas, existe uma solução com uma complexidade de $O(NV)$.
- Defina o estado: `f[i][j]` representa o volume mínimo ao selecionar vários itens dos primeiros `i` itens, e o valor total é exatamente `j`.
    - Se o `i`-ésimo item não for levado, então `f[i][j] = f[i - 1][j]`
    - Se o `i`-ésimo item for levado, então `f[i][j] = f[i - 1][j - v[i]] + s[i]`
    - Pegue o menor dos dois.
- Condições iniciais: `f[0][0] = 0`, o resto `f[0][j]` = $\infty$, `j` $\in [1, V]$. $\infty$ representa um estado impossível. Observe que não é $-\infty$.
- A resposta final é o maior `j` em `f[N][j]` tal que `f[N][j] <= S`.

## Se o Limite de Volume $S$ e o Valor de um Único Item $v_i$ forem Ambos Muito Grandes (na ordem de 1e9), Enquanto o Número de Itens $N$ for Muito Pequeno (não mais que 40)

- Quando $N \leq 20$, todos os subconjuntos podem ser diretamente enumerados por força bruta (complexidade de tempo $O(2^N)$).
- Quando $N \leq 40$, como $2^{40}$ está na ordem de $10^{12}$, a força bruta direta também será relativamente grande, então a **busca meet-in-the-middle** pode ser usada para reduzir a complexidade para aproximadamente $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$, que pode ser concluída em um tempo aceitável.