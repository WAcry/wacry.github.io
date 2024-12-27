---
title: "Busca Binária"
date: 2024-12-24
draft: false
description: "Como implementar elegantemente o algoritmo de busca binária."
summary: "Como implementar elegantemente o algoritmo de busca binária."
tags: [ "Algoritmo", "Busca Binária", "Template de Algoritmo" ]
categories: [ "Algoritmos e Estruturas de Dados" ]
---

Se um espaço de solução ordenado é dividido em duas partes, onde uma parte satisfaz uma condição e a outra não, então a busca binária pode ser usada para encontrar o ponto crítico no espaço de solução ordenado.

A ideia básica da busca binária é reduzir repetidamente pela metade o intervalo de busca. A cada vez, o elemento do meio é verificado. Se o elemento do meio não satisfaz a condição, metade do intervalo pode ser eliminada; caso contrário, a busca continua na outra metade. Como metade do intervalo de busca é descartada a cada vez, a complexidade de tempo da busca pode atingir $O(\log n)$.

## Problema de Exemplo

**Descrição do Problema:**
Dado um array de inteiros ordenado de forma crescente de tamanho $n$, e $q$ consultas. Cada consulta fornece um inteiro $k$, e precisamos encontrar a "posição inicial" e a "posição final" de $k$ no array (os índices começam em 0). Se o número não existir no array, retorne `-1 -1`.

### Formato de Entrada

1. Primeira linha: dois inteiros $n$ e $q$, representando o tamanho do array e o número de consultas, respectivamente.
2. Segunda linha: $n$ inteiros, representando o array completo, já ordenado em ordem crescente.
3. Próximas $q$ linhas: cada linha contém um inteiro $k$, representando um elemento de consulta.

## Intervalo de Dados

$1 \leq n \leq 100000$

$1 \leq q \leq 10000$

$1 \leq k \leq 10000$

### Formato de Saída

Para cada consulta, imprima as posições inicial e final do elemento no array em uma única linha. Se o elemento não existir no array, imprima `-1 -1`.

**Exemplo:**

```
Entrada:
6 3
1 2 2 3 3 4
3
4
5

Saída:
3 4
5 5
-1 -1
```

**Explicação:**

- O intervalo onde o elemento $3$ aparece é $[3, 4]$;
- O elemento $4$ aparece apenas uma vez, na posição $5$;
- O elemento $5$ não existe no array, então retorne $-1$ $-1$.

---

## Solução

- **Encontrando a "Posição Inicial":**
  Ou seja, encontrar a primeira posição que é maior ou igual a $k$. O array pode ser dividido em duas partes:
    - Todos os números à esquerda são "menores que" $k$
    - Todos os números à direita são "maiores ou iguais a" $k$
    - A resposta é a primeira posição à direita

- **Encontrando a "Posição Final":**
  Ou seja, encontrar a última posição que é menor ou igual a $k$. O array pode ser dividido em duas partes:
    - Todos os números à esquerda são "menores ou iguais a" $k$
    - Todos os números à direita são "maiores que" $k$
    - A resposta é a última posição à esquerda

---

## Template Recomendado

Abaixo está um template de busca binária elegante e menos propenso a erros.

Defina dois ponteiros $l, r$, com o invariante: o intervalo fechado $[0, l]$ pertence à parte esquerda, e o intervalo fechado $[r, n - 1]$ pertence à parte direita. $l$ e $r$ são inicializados com $-1$ e $n$, respectivamente.

Quando o algoritmo termina, $l$ e $r$ são adjacentes, apontando para o último elemento da parte esquerda e o primeiro elemento da parte direita, respectivamente.

Como a solução que queremos pode não existir, se o problema não afirmar que uma solução definitivamente existe, precisamos verificar se `l` ou `r` está fora dos limites e se aponta para o valor correto.

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, q;
    cin >> n >> q;
    vector<int> nums(n);
    for(int i = 0; i < n; i++) cin >> nums[i];

    while(q--) {
        int k;
        cin >> k;

        // 1. Encontrar a posição inicial de k
        //    Dividir o array em duas partes, a parte esquerda é toda < k, e a parte direita é toda >= k.
        //    A resposta é o menor índice da parte direita.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // Se r estiver fora dos limites ou nums[r] != k, significa que k não existe
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. Encontrar a posição final de k
        //    Dividir o array em duas partes, a parte esquerda é toda <= k, e a parte direita é toda > k.
        //    A resposta é o maior índice da parte esquerda.
        l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] <= k) l = mid;
            else r = mid;
        }

        int rightPos = l;
        cout << leftPos << " " << rightPos << endl;
    }
    return 0;
}
```

### Vantagens

1. Esta abordagem tem invariantes estritamente definidos.
2. Aplica-se tanto para encontrar a "posição inicial" quanto a "posição final" sem tratamento ou alterações extras.
3. Algumas abordagens usam `l == r` como condição de término. Quando $l$ e $r$ diferem em $1$, $mid$ será calculado para ser igual a $l$ ou $r$. Se não for tratado corretamente, atualizar $l$ ou $r$ para $mid$ não reduzirá o intervalo de busca, levando a um loop infinito. Em contraste, esta abordagem termina quando $l$ e $r$ são adjacentes, garantindo que $mid$ seja menor que $l$ e maior que $r$, e atualizar $l$ ou $r$ sempre reduzirá o intervalo de busca.

---

## STL

Se você usar as funções `lower_bound` e `upper_bound` fornecidas pela STL do C++, você pode obter o mesmo resultado:

- `lower_bound(first, last, val)` retornará "a primeira posição que é maior ou igual a val"
- `upper_bound(first, last, val)` retornará "a primeira posição que é maior que val"

Por exemplo, suponha que `nums = {1,2,3,4,4,4,4,4,5,5,6}`, e queremos saber o intervalo onde 4 aparece:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    cout << "4 aparece 0 vezes" << endl;
} else {
    cout << "o primeiro 4 está em " << it1 - nums.begin() << endl;
    cout << "o último 4 está em " << it2 - nums.begin() - 1 << endl;
    cout << "4 aparece " << it2 - it1 << " vezes" << endl;
}
```

- `it1` aponta para a primeira posição onde o valor é maior ou igual a $4$.
- `it2` aponta para a primeira posição onde o valor é maior que $4$.
  Portanto, `it2 - it1` é o número de vezes que $4$ aparece no array; `it2 - nums.begin() - 1` é a posição do limite direito de $4$.

---

## Notas Adicionais

A busca binária também pode ser estendida para pesquisar em intervalos de ponto flutuante (como encontrar as raízes de uma equação) e busca ternária para encontrar os extremos de funções unimodais.

---

## Prática

LeetCode 33. Search in Rotated Sorted Array

Dica: Primeiro, use a busca binária para encontrar o ponto de rotação e, em seguida, use a busca binária para encontrar o valor alvo.