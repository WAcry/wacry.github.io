---
title: "Busca Binária"
date: 2024-12-24
draft: false
description: "Como implementar elegantemente o algoritmo de busca binária para inteiros."
summary: "Como implementar elegantemente o algoritmo de busca binária para inteiros."
tags: [ "Algoritmo", "Busca Binária", "Modelo de Algoritmo" ]
categories: [ "Algoritmos e Estruturas de Dados" ]
---

{{< katex >}}

# Busca Binária

Se um espaço de solução ordenado for dividido em duas partes, onde uma parte satisfaz uma condição e a outra não, então é possível usar a busca binária para encontrar o ponto crítico no espaço de solução ordenado.

A ideia básica da busca binária é dividir continuamente o intervalo de busca ao meio. A cada verificação, o elemento do ponto médio é examinado. Se o elemento do ponto médio não satisfaz a condição, então metade do intervalo pode ser descartada; caso contrário, a busca continua na outra metade do intervalo. Como metade do intervalo de busca é descartada a cada vez, a complexidade de tempo da busca pode atingir \\(O(\log n)\\).

## Exemplo de Problema

**Descrição do problema:**  
Dado um array de inteiros de comprimento \\(n\\) classificado em ordem crescente, e também \\(q\\) consultas. Cada consulta fornece um inteiro \\(k\\). Precisamos encontrar a "posição inicial" e a "posição final" de \\(k\\) no array (índices a partir de 0). Se o número não existir no array, retorne \\(-1\\) \\(-1\\).

### Formato de Entrada

1. Primeira linha: Dois inteiros \\(n\\) e \\(q\\), indicando o comprimento do array e o número de consultas, respectivamente.
2. Segunda linha: \\(n\\) inteiros, representando o array completo, classificado em ordem crescente.
3. Próximas \\(q\\) linhas: Cada linha contém um inteiro \\(k\\), representando um elemento de consulta.

## Intervalo de Dados

\\(1 \leq n \leq 100000\\)

\\(1 \leq q \leq 10000\\)

\\(1 \leq k \leq 10000\\)

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

- O intervalo em que o elemento \\(3\\) aparece é \\([3, 4]\\);
- O elemento \\(4\\) aparece apenas uma vez, na posição \\(5\\);
- O elemento \\(5\\) não existe no array, então retorne \\(-1\\) \\(-1\\).

---

## Resolução

- **Encontrar a "posição inicial":**
  Ou seja, encontrar a primeira posição maior ou igual a \\(k\\). O array pode ser dividido em duas partes:
    - Todos os números à esquerda são "menores" que \\(k\\)
    - Todos os números à direita são "maiores ou iguais" a \\(k\\)
    - A resposta é a primeira posição da direita

- **Encontrar a "posição final":**
  Ou seja, encontrar a última posição menor ou igual a \\(k\\). O array pode ser dividido em duas partes:
    - Todos os números à esquerda são "menores ou iguais" a \\(k\\)
    - Todos os números à direita são "maiores" que \\(k\\)
    - A resposta é a última posição da esquerda

---

## Modelo Recomendado

Abaixo está um modelo de busca binária elegante e que não comete erros facilmente. Ele garante que o loop termine quando \\(l\\) e \\(r\\) estiverem adjacentes, fazendo com que eles se aproximem gradualmente:

Defina dois ponteiros \\(l, r\\), com o invariante: o intervalo fechado \\([0, l]\\) pertence à parte esquerda e o intervalo fechado \\([r, n - 1]\\) pertence à parte direita. \\(l\\) e \\(r\\) são inicializados com \\(-1\\) e \\(n\\).

Quando o algoritmo termina, \\(l\\) e \\(r\\) são adjacentes, apontando para o último elemento da parte esquerda e para o primeiro elemento da parte direita, respectivamente.

Como a solução desejada pode não existir, se o problema não especificar que uma solução existe, precisamos verificar se `l` ou `r` estão fora dos limites e se apontam para o valor correto.

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
        //    Dividir o array em duas partes, a esquerda com todos os elementos < k, e a direita com todos os elementos >= k.
        //    A resposta é o menor índice da parte direita.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // Se r estiver fora dos limites ou nums[r] != k, isso significa que k não existe
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. Encontrar a posição final de k
        //    Dividir o array em duas partes, a esquerda com todos os elementos <= k, e a direita com todos os elementos > k.
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

### Por que escrever dessa forma

1. Essa forma de escrita possui invariantes definidos de maneira estrita.
2. Ela é adequada para encontrar tanto a "posição inicial" quanto a "posição final", sem a necessidade de tratamento e mudanças adicionais.
3. Algumas formas de escrita usam `l == r` como condição de término. Quando \\(l\\) e \\(r\\) diferem em \\(1\\), isso calculará \\(mid\\) igual a \\(l\\) ou \\(r\\). Se isso não for tratado corretamente, a atualização de \\(l\\) ou \\(r\\) para \\(mid\\) fará com que o intervalo de busca não seja reduzido, levando a um loop infinito. Em contraste, a forma de escrita aqui termina quando \\(l\\) e \\(r\\) são adjacentes, garantindo que \\(mid\\) seja menor que \\(l\\) e maior que \\(r\\), e que a atualização de \\(l\\) ou \\(r\\) reduza o intervalo de busca.

---

## STL

Se você usar as funções `lower_bound` e `upper_bound` fornecidas pela STL do C++, você também pode fazer a mesma coisa:

- `lower_bound(first, last, val)` retorna "a primeira posição maior ou igual a val"
- `upper_bound(first, last, val)` retorna "a primeira posição maior que val"

Por exemplo, suponha que `nums = {1,2,3,4,4,4,4,4,5,5,6}`, e queiramos saber o intervalo onde 4 aparece:

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

- `it1` aponta para a primeira posição com um valor maior ou igual a \\(4\\).
- `it2` aponta para a primeira posição com um valor maior que \\(4\\).  
  Então `it2 - it1` é o número de vezes que \\(4\\) aparece no array; `it2 - nums.begin() - 1` é o limite direito de \\(4\\).

---

## Adicional

A busca binária também pode ser estendida para busca em intervalos de números de ponto flutuante (como encontrar raízes de equações), bem como busca ternária para encontrar o valor máximo de funções unimodais.
Contanto que você entenda o princípio fundamental de "**em um intervalo ordenado, metade pode ser eliminada a cada vez**", você descobrirá que a busca binária pode ajudá-lo a resolver problemas de forma eficiente em vários cenários.

---

## Prática

LeetCode 33. Search in Rotated Sorted Array

Dica: O primeiro passo é usar busca binária para encontrar o ponto de rotação, e o segundo passo é usar busca binária novamente para encontrar o valor alvo.