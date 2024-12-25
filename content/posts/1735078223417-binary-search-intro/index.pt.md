---
title: "Busca Binária"
date: 2024-12-24
draft: false
description: "Como implementar elegantemente o algoritmo de busca binária."
summary: "Como implementar elegantemente o algoritmo de busca binária."
tags: [ "algoritmo", "busca binária", "modelo de algoritmo" ]
categories: [ "Algoritmos e Estruturas de Dados" ]
---

Se um espaço de solução ordenado for dividido em duas partes, onde uma parte satisfaz uma condição e a outra não, então podemos usar a busca binária para encontrar o ponto crítico no espaço de solução ordenado.

A ideia básica da busca binária é dividir repetidamente o intervalo de busca pela metade. A cada vez, verificamos o elemento do meio. Se o elemento do meio não satisfaz a condição, podemos descartar metade do intervalo; caso contrário, continuamos a busca na outra metade. Como descartamos metade do intervalo de busca a cada vez, a complexidade de tempo da busca pode atingir $O(\log n)$.

## Exemplo

**Descrição do Problema:**
Dado um array de inteiros de comprimento $n$ classificado em ordem crescente e $q$ consultas. Cada consulta fornece um inteiro $k$, e precisamos encontrar a "posição inicial" e a "posição final" de $k$ no array (índices começando de 0). Se o número não existir no array, retornaremos `-1 -1`.

### Formato de Entrada

1. Primeira linha: dois inteiros $n$ e $q$, que representam o comprimento do array e o número de consultas, respectivamente.
2. Segunda linha: $n$ inteiros, representando o array completo, já ordenado em ordem crescente.
3. Próximas $q$ linhas: cada linha contém um inteiro $k$, que representa um elemento de consulta.

## Intervalo de Dados

$1 \leq n \leq 100000$

$1 \leq q \leq 10000$

$1 \leq k \leq 10000$

### Formato de Saída

Para cada consulta, imprima em uma linha a posição inicial e final do elemento no array. Se o elemento não existir no array, imprima `-1 -1`.

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
- O elemento $5$ não existe no array, então retornamos $-1$ $-1$.

---

## Resposta

- **Encontrar a "posição inicial":**
  Ou seja, encontrar a primeira posição que é maior ou igual a $k$. Podemos dividir o array em duas partes:
    - Todos os números à esquerda são "menores" que $k$
    - Todos os números à direita são "maiores ou iguais" a $k$
    - A resposta é a primeira posição na direita

- **Encontrar a "posição final":**
  Ou seja, encontrar a última posição que é menor ou igual a $k$. Podemos dividir o array em duas partes:
    - Todos os números à esquerda são "menores ou iguais" a $k$
    - Todos os números à direita são "maiores" que $k$
    - A resposta é a última posição na esquerda

---

## Modelo Recomendado

A seguir, um modelo de busca binária elegante e difícil de errar. Ele garante que o loop termine quando $l$ e $r$ se tornarem adjacentes, fazendo com que $l$ e $r$ se aproximem gradualmente:

Definimos dois ponteiros $l, r$, com o invariante: o intervalo fechado $[0, l]$ pertence à parte esquerda, e o intervalo fechado $[r, n - 1]$ pertence à parte direita. $l$ e $r$ são inicializados com $-1$ e $n$, respectivamente.

Quando o algoritmo termina, $l$ e $r$ são adjacentes, apontando para o último elemento da parte esquerda e o primeiro elemento da parte direita, respectivamente.

Como a solução que queremos pode não existir, precisamos verificar se `l` ou `r` estão fora dos limites, e se apontam para o valor correto, a menos que o problema garanta que uma solução sempre existe.

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
        //    Dividimos o array em duas partes, à esquerda todos < k, à direita todos >= k.
        //    A resposta é o menor índice na metade direita.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid;
            else l = mid;
        }

        // Se r estiver fora dos limites ou nums[r] != k, k não existe
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. Encontrar a posição final de k
        //    Dividimos o array em duas partes, à esquerda todos <= k, à direita todos > k.
        //    A resposta é o maior índice na metade esquerda.
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

### Por que escrever assim

1. Esta escrita tem um invariante estritamente definido.
2. Ela se aplica tanto para encontrar a "posição inicial" quanto a "posição final", sem a necessidade de processamento ou mudanças adicionais.
3. Algumas implementações usam `l == r` como condição de parada. Quando $l$ e $r$ são separados por $1$, calcular $mid$ resultará em $mid$ igual a $l$ ou $r$. Se não for tratada corretamente, atualizar $l$ ou $r$ com $mid$ fará com que o intervalo de busca não diminua, levando a um loop infinito. Em contraste, esta implementação termina quando $l$ e $r$ são adjacentes, garantindo que $mid$ seja menor que $l$ e maior que $r$, e que o intervalo de busca diminua quando $l$ ou $r$ forem atualizados.

---

## STL

Se você usar as funções `lower_bound` e `upper_bound` fornecidas pela C++ STL, poderá alcançar o mesmo resultado:

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
    cout << "primeiro 4 está em " << it1 - nums.begin() << endl;
    cout << "último 4 está em " << it2 - nums.begin() - 1 << endl;
    cout << "4 aparece " << it2 - it1 << " vezes" << endl;
}
```

- `it1` aponta para a primeira posição com um valor maior ou igual a $4$.
- `it2` aponta para a primeira posição com um valor maior que $4$.
Portanto, `it2 - it1` é o número de vezes que $4$ aparece no array; `it2 - nums.begin() - 1` é o limite direito de $4$.

---

## Adicional

A busca binária pode ser estendida para pesquisar em intervalos de ponto flutuante (como encontrar raízes de equações) e também para busca ternária para encontrar os valores máximos e mínimos de funções unimodais.
Contanto que você entenda o princípio central de "**em um intervalo ordenado, podemos descartar metade dele a cada vez**", você descobrirá que a busca binária pode ajudá-lo a resolver problemas com eficiência em muitos cenários.

---

## Prática

LeetCode 33. Search in Rotated Sorted Array

Dica: Use a busca binária para encontrar o ponto de rotação como o primeiro passo, e use a busca binária novamente para encontrar o valor de destino como o segundo passo.