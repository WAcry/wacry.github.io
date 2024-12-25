---
title: "Problema da Mochila 0-1"
date: 2024-12-24
draft: false
description: "O problema clássico mais básico de mochila."
summary: "O problema clássico mais básico de mochila."
tags: [ "Algoritmo", "Programação Dinâmica", "Problema da Mochila" ]
categories: [ "Algoritmos e Estruturas de Dados" ]
series: [ "Nove Palestras sobre Mochila" ]
series_order: 1
---

## Problema

Existem $N$ itens. O volume do $i$-ésimo item é $s_i$, e o valor é $v_i$.
Cada item só pode ser pego uma vez. Sob a premissa de não exceder a restrição de volume máximo total $S$, encontre o valor total máximo $V$ que pode ser obtido.

## Formato de Entrada

A primeira linha contém dois inteiros, $N$ e $S$, separados por espaços, indicando o número de itens e a restrição de volume máximo total, respectivamente.
As próximas $N$ linhas contêm cada uma dois inteiros, $s_i$ e $v_i$, separados por espaços, indicando o volume e o valor do $i$-ésimo item, respectivamente.

## Formato de Saída

Imprima um inteiro, indicando o valor máximo.

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

- Definir estado: `f[i][j]` representa o valor máximo que pode ser obtido com os primeiros $i$ itens, sob uma restrição de volume de $j$.
    - Se não pegarmos o $i$-ésimo item, então `f[i][j] = f[i - 1][j]`
    - Se pegarmos o $i$-ésimo item, então `f[i][j] = f[i - 1][j - s[i]] + v[i]`
    - Ao implementar a transição de estado, preste atenção ao intervalo do domínio. Se $j < s_i$, não considere o caso de pegar o $i$-ésimo item. Porque se $j - s_i$ for negativo, o índice do array será inválido.
      Também pode ser explicado assim: o volume do $i$-ésimo item é maior que a restrição de volume, então é impossível.
- Definir condição inicial: os primeiros $0$ itens, qualquer restrição de volume resulta em um valor $0$, ou seja, `f[0][j] = 0`, `j` $\in [0, S]$.
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

## Otimização com DP Unidimensional

- Comprimir o array bidimensional em um array unidimensional pode economizar significativamente espaço e melhorar a velocidade de execução até certo ponto (a desvantagem é que ele não pode atender aos requisitos especiais de certos tipos de problemas).
- Observe que na transição de estado, `f[i][j]` está relacionado apenas a `f[i - 1][j]` e `f[i - 1][j - s[i]]`. Em outras palavras, no array bidimensional `f` no código, `f[i][j]` está relacionado apenas aos elementos em sua linha anterior que estão mais à esquerda ou na mesma coluna, portanto, o array bidimensional pode ser comprimido em um array unidimensional ou array de rolagem.
- Observe que no código abaixo, o segundo loop itera na ordem inversa, porque queremos garantir que ao calcular `f[i][j]`, `f[i - 1][j - s[i]]` ainda não tenha sido atualizado.

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

## Se o Número de Soluções For Necessário

Não apenas o valor total máximo que pode ser obtido, mas também o número de diferentes métodos de seleção que podem atingir esse valor total máximo precisa ser impresso. Abaixo está uma introdução sobre **como calcular o número de soluções** no problema da mochila 0-1.

### Contando o Número de Soluções com DP Bidimensional

A seguir, a contagem do número de soluções será explicada usando DP bidimensional como exemplo.

- Definir estado:
  - `dp[i][j]` representa "o valor máximo que pode ser obtido com os primeiros i itens, quando a capacidade (restrição de volume) é j".
  - `ways[i][j]` representa "o **número de soluções** correspondente quando o valor máximo é obtido com os primeiros i itens, com capacidade j".

- Transição de estado:
  1. Se o item `i` não for selecionado:
     $$
       \text{dp}[i][j] = \text{dp}[i-1][j],
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
     $$
  2. Se o item `i` for selecionado (com a condição de que $j \ge s_i$):
     $$
       \text{dp}[i][j]
         = \text{dp}[i-1][j - s_i] + v_i,
       \quad
       \text{ways}[i][j]
         = \text{ways}[i-1][j - s_i]
     $$
  3. Selecionar ou não, o valor maior entre os dois deve ser tomado para o `dp[i][j]`:
     - Se
       $$
         \text{dp}[i-1][j - s_i] + v_i
           > \text{dp}[i-1][j],
       $$
       então isso significa que o valor de "selecionar o item i" é maior:
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
       isso significa que o valor máximo obtido por duas maneiras é o mesmo, então o número de soluções deve ser sobreposto:
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
       então isso significa que o valor de "não selecionar o item i" é maior, e o número de soluções herda o número de soluções quando não seleciona:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Condição inicial:
  - `dp[0][j] = 0` significa que com 0 itens, o valor máximo obtido com qualquer capacidade é 0.
  - `ways[0][0] = 1` significa que "0 itens anteriores, capacidade de 0" é uma solução viável (ou seja, não selecionar nada), o **número de soluções** é definido como 1.
  - Para `j > 0`, quando não há itens para selecionar, mas a capacidade é maior que 0, é impossível obter qualquer valor positivo, e o número de soluções correspondente é 0, ou seja, `ways[0][j] = 0`.

- Resposta final:
  - `dp[N][S]` é o valor máximo.
  - `ways[N][S]` é o número de soluções para atingir esse valor máximo.
  - Complexidade de tempo: $O(NS)$.
  - Este problema também pode ser otimizado usando DP unidimensional.

## Se a Condição Exigir o Volume Exatamente

- Definir estado: `f[i][j]` representa o valor máximo dos primeiros `i` itens com exatamente o volume $j$.
- Se o `i`-ésimo item não for selecionado, então `f[i][j] = f[i - 1][j]`
- Se o `i`-ésimo item for selecionado, então `f[i][j] = f[i - 1][j - s[i]] + v[i]`
- Pode-se notar que não há diferença na transição de estado do problema original.
- Mas as condições iniciais são diferentes. Além de `f[0][0] = 0`, o restante `f[0][j]` = $-\infty$, `j` $\in [1, S]$. $-\infty$ representa um estado impossível.

## Se a Restrição de Volume $S$ For Especialmente Grande (1e9), Enquanto o Número de Itens $N$ e o Valor Total Máximo $V$ São Relativamente Pequenos

- Para um problema como este, existe uma solução com complexidade $O(NV)$.
- Definir estado: `f[i][j]` representa o volume mínimo de selecionar alguns itens dos primeiros `i` itens, cujo valor total é exatamente `j`.
    - Se o `i`-ésimo item não for selecionado, então `f[i][j] = f[i - 1][j]`
    - Se o `i`-ésimo item for selecionado, então `f[i][j] = f[i - 1][j - v[i]] + s[i]`
    - Pegue o menor dos dois.
- Condição inicial: `f[0][0] = 0`, o restante `f[0][j]` = $\infty$, `j` $\in [1, V]$. $\infty$ representa um estado impossível. Observe que não é $-\infty$.
- A resposta final é o maior `j` em `f[N][j]` tal que `f[N][j] <= S`.

## Se a Restrição de Volume $S$ e o Valor do Item Individual $v_i$ São Muito Grandes (da Ordem de 1e9), Enquanto o Número de Itens $N$ For Muito Pequeno (No Máximo 40)

- Quando $N \leq 20$, todos os subconjuntos podem ser enumerados diretamente por força bruta (complexidade de tempo $O(2^N)$).
- Quando $N \leq 40$, como $2^{40}$ está na ordem de $10^{12}$, a força bruta direta também será relativamente grande, então a **pesquisa de divisão ao meio** pode ser usada para reduzir a complexidade para aproximadamente $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$
  , que pode ser concluída em um tempo aceitável.