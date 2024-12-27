---
title: "Pesquisa Binária"
date: 2024-12-24
draft: false
description: "Como implementar o algoritmo de pesquisa binária de forma elegante."
summary: "Como implementar o algoritmo de pesquisa binária de forma elegante."
tags: [ "Algoritmos", "Pesquisa Binária", "Modelos de Algoritmos" ]
categories: [ "Algoritmos e Estruturas de Dados" ]
---

Se um espaço de solução ordenado for dividido em duas partes, onde uma parte satisfaz a condição e a outra não, então a pesquisa binária pode ser usada para encontrar o ponto crítico no espaço de solução ordenado.

A ideia básica da pesquisa binária é dividir continuamente o intervalo de pesquisa ao meio. A cada verificação, o elemento do meio é examinado. Se o elemento do meio não satisfaz a condição, metade do intervalo pode ser descartada; caso contrário, a pesquisa continua na outra metade do intervalo. Como metade do intervalo de pesquisa é descartada a cada vez, a complexidade de tempo da pesquisa pode atingir $O(\log n)$.

## Exemplo

**Descrição do Problema:**  
Dado um array de inteiros de comprimento $n$ em ordem crescente, e $q$ consultas. Cada consulta fornece um inteiro $k$, e precisamos encontrar a "posição inicial" e a "posição final" de $k$ no array (índices começando em 0). Se o número não existir no array, retorne `-1 -1`.

### Formato de Entrada

1. Primeira linha: dois inteiros $n$ e $q$, representando o comprimento do array e o número de consultas, respectivamente.
2. Segunda linha: $n$ inteiros, representando o array completo, já ordenado em ordem crescente.
3. Próximas $q$ linhas: cada linha contém um inteiro $k$, representando um elemento de consulta.

## Intervalo de Dados

$1 \leq n \leq 100000$

$1 \leq q \leq 10000$

$1 \leq k \leq 10000$

### Formato de Saída

Para cada consulta, imprima a posição inicial e final do elemento no array em uma linha. Se o elemento não existir no array, imprima `-1 -1`.

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

- O intervalo em que o elemento $3$ aparece é $[3, 4]$;
- O elemento $4$ aparece apenas uma vez, na posição $5$;
- O elemento $5$ não existe no array, então retorna $-1$ $-1$.

---

## Resposta

- **Encontrar a "posição inicial":**
  Ou seja, encontrar a primeira posição maior ou igual a $k$. O array pode ser dividido em duas partes:
    - Todos os números à esquerda são "menores" que $k$
    - Todos os números à direita são "maiores ou iguais" a $k$
    - A resposta é a primeira posição à direita

- **Encontrar a "posição final":**
  Ou seja, encontrar a última posição menor ou igual a $k$. O array pode ser dividido em duas partes:
    - Todos os números à esquerda são "menores ou iguais" a $k$
    - Todos os números à direita são "maiores" que $k$
    - A resposta é a última posição à esquerda

---

## Modelo Recomendado

A seguir está um modelo de pesquisa binária elegante e menos propenso a erros.

Defina dois ponteiros $l, r$, com o invariante: o intervalo fechado $[0, l]$ pertence à parte esquerda, e o intervalo fechado $[r, n - 1]$ pertence à parte direita. $l$ e $r$ são inicializados como $-1$ e $n$.

Quando o algoritmo termina, $l$ e $r$ são adjacentes, apontando para o último elemento da parte esquerda e o primeiro elemento da parte direita, respectivamente.

Como a solução que queremos pode não existir, se o problema não indicar que uma solução existe, precisamos verificar se `l` ou `r` estão fora dos limites e se apontam para o valor correto.

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
        //    Dividir o array em duas partes, à esquerda todos < k, à direita todos >= k.
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
        //    Dividir o array em duas partes, à esquerda todos <= k, à direita todos > k.
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
2. Ela se aplica tanto para encontrar a "posição inicial" quanto a "posição final", sem a necessidade de tratamento e mudanças adicionais.
3. Algumas abordagens usam `l == r` como condição de término. Quando $l$ e $r$ diferem em $1$, $mid$ será calculado como igual a $l$ ou $r$. Se não for tratado corretamente, atualizar $l$ ou $r$ para $mid$ fará com que o intervalo de pesquisa não diminua, levando a um loop infinito. Em vez disso, esta abordagem termina quando $l$ e $r$ são adjacentes, garantindo que $mid$ seja menor que $l$ e maior que $r$, e que o intervalo de pesquisa diminua ao atualizar $l$ ou $r$.

---

## STL

Se você usar as funções `lower_bound` e `upper_bound` fornecidas pela STL do C++, você também pode realizar a mesma tarefa:

- `lower_bound(first, last, val)` retornará a "primeira posição maior ou igual a val"
- `upper_bound(first, last, val)` retornará a "primeira posição maior que val"

Por exemplo, suponha que `nums = {1,2,3,4,4,4,4,4,5,5,6}`, e queremos saber o intervalo em que 4 aparece:

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

- `it1` aponta para a primeira posição com um valor maior ou igual a $4$.
- `it2` aponta para a primeira posição com um valor maior que $4$.  
  Portanto, `it2 - it1` é o número de vezes que $4$ aparece no array; `it2 - nums.begin() - 1` é a posição do limite direito de $4$.

---

## Adicional

A pesquisa binária também pode ser estendida para a pesquisa em intervalos de números de ponto flutuante (como encontrar raízes de equações) e para a pesquisa ternária para encontrar os valores máximos de funções unimodais.

---

## Prática

LeetCode 33. Search in Rotated Sorted Array

Dica: Primeiro, use a pesquisa binária para encontrar o ponto de rotação e, em seguida, use a pesquisa binária novamente para encontrar o valor alvo.