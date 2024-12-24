---
title: "Busca Binária"
date: 2024-12-24
draft: false
description: "Como implementar elegantemente o algoritmo de busca binária de inteiros"
summary: "Como implementar elegantemente o algoritmo de busca binária de inteiros"
tags: [ "Algoritmos", "Busca Binária", "Modelos de Algoritmos" ]
categories: [ "Algoritmos e Estruturas de Dados" ]
---
{{< katex >}}

# Busca Binária

Em uma sequência ordenada, a busca binária pode ser usada para encontrar um elemento específico rapidamente. Comparada à complexidade de tempo da busca linear $O(n)$, a busca binária requer apenas tempo de $O(\log n)$, por isso é muito eficiente em casos de grande escala de dados.

## A Ideia Central da Busca Binária

A ideia básica da busca binária é dividir o intervalo de busca pela metade repetidamente. Em cada comparação, o elemento do ponto médio é comparado com o valor-alvo. Se o elemento do ponto médio não atender à condição, metade do intervalo é eliminada; caso contrário, a busca continua na outra metade do intervalo. Como metade do intervalo de busca é descartada a cada vez, a complexidade de tempo da busca pode atingir $O(\log n)$.

A busca binária é muito útil para problemas em que " **a solução viável pode ser dividida em um intervalo ordenado (que atende à condição) e outro intervalo ordenado (que não atende à condição)**". Por exemplo:

- Encontrar se um determinado elemento existe em um array ordenado
- Encontrar a "primeira posição" ou a "última posição" em que um número aparece

## Exemplo: Encontrar as Posições Inicial e Final de um Elemento

**Descrição do problema:**  
Dado um array de inteiros de comprimento $n$ em ordem crescente, e também $q$ consultas. Cada consulta fornece um inteiro $k$, e precisamos encontrar a "posição inicial" e a "posição final" de $k$ no array (índice começando em 0). Se o número não existir no array, retorne $-1$ $-1$.

**Formato de entrada:**

1. Primeira linha: dois inteiros $n$ e $q$, representando o comprimento do array e o número de consultas, respectivamente.
2. Segunda linha: $n$ inteiros (dentro do intervalo de 1 a 10000), representando o array completo, já ordenado em ordem crescente.
3. Próximas $q$ linhas: cada linha contém um inteiro $k$, representando um elemento de consulta.

**Formato de saída:**  
Para cada consulta, imprima a posição inicial e final do elemento no array em uma linha. Se o elemento não existir no array, imprima $-1$ $-1$.

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

Explicação:

- O intervalo em que o elemento 3 aparece é `[3, 4]`;
- O elemento 4 aparece apenas uma vez, na posição 5;
- O elemento 5 não existe no array, então retorne `-1 -1`.

## Aplicação da Busca Binária

Neste problema, para encontrar o "limite esquerdo" e o "limite direito" de um determinado valor, podemos confiar na busca binária. A chave é entender como definir o intervalo de busca e como mover os ponteiros de acordo com o resultado da comparação.

- **Encontrar o "limite esquerdo":**  
  Ou seja, encontrar a primeira posição maior ou igual a $k$. O array pode ser dividido em duas partes:
    - Todos os números à esquerda são "menores" que $k$
    - Todos os números à direita são "maiores ou iguais" a $k$

- **Encontrar o "limite direito":**  
  Ou seja, encontrar a última posição menor ou igual a $k$. O array pode ser dividido em duas partes:
    - Todos os números à esquerda são "menores ou iguais" a $k$
    - Todos os números à direita são "maiores" que $k$

Contanto que você possa manter esses dois intervalos corretamente, você pode obter os resultados rapidamente por meio da busca binária.

## Modelo Recomendado: Busca Binária para Evitar Loops Infinitos

Abaixo está um modelo de busca binária elegante e sem erros. Ele garante que o loop termine quando $l$ e $r$ estiverem adjacentes, movendo $l$ e $r$ gradualmente para perto um do outro:

Defina dois ponteiros $l, r$, com o invariante: o intervalo fechado $[0, l]$ pertence à parte esquerda e o intervalo fechado $[r, n - 1]$ pertence à parte direita. $l$ e $r$ são inicializados para $-1$ e $n$.

Quando o algoritmo termina, $l$ e $r$ estão adjacentes, apontando respectivamente para o valor máximo da parte esquerda e o valor mínimo da parte direita.

Como a solução que desejamos pode não existir, ao retornar $l$ ou $r$, precisamos verificar se o valor correspondente é o valor que queremos e se está fora dos limites.
Por exemplo, $l$ representa o valor máximo $\leq k$, e precisamos verificar `l != -1 && nums[l] == k`

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

        // 1. Encontre a posição inicial de k (limite esquerdo)
        //    Divida o array em duas partes, todos à esquerda < k, todos à direita >= k.
        //    O limite esquerdo é o menor índice da parte direita.
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

        int leftPos = r; // Registre o limite esquerdo de k

        // 2. Encontre a posição final de k (limite direito)
        //    Divida o array em duas partes, todos à esquerda <= k, todos à direita > k.
        //    O limite direito é o maior índice da parte esquerda.
        l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] <= k) l = mid;
            else r = mid;
        }

        // Como já verificamos que k existe, não precisamos verificar novamente aqui
        int rightPos = l; // Limite direito
        cout << leftPos << " " << rightPos << endl;
    }
    return 0;
}
```

### Por que essa escrita não é propensa a erros?

1. Esta escrita tem um invariante estritamente definido.
2. Ela pode encontrar tanto o limite esquerdo quanto o limite direito, o que pode ser aplicado a todos os cenários.
3. Algumas escritas usam $l == r$ como condição de parada. Quando $l$ e $r$ diferem em 1, o $mid$ será calculado como igual a `l` ou `r`. Se não for tratado corretamente, atualizando `l` ou `r` para `mid`, o intervalo de busca não será reduzido, o que levará a um loop infinito. Por outro lado, a escrita aqui termina quando $l$ e $r$ são adjacentes, o que evita esse problema.

## Solução STL: `lower_bound` e `upper_bound`

Se você usar as funções `lower_bound` e `upper_bound` fornecidas pelo C++ STL, poderá concluir facilmente a mesma coisa:

- `lower_bound(first, last, val)` retornará "a primeira posição maior ou igual a val"
- `upper_bound(first, last, val)` retornará "a primeira posição maior que val"

Por exemplo, suponha `nums = {1,2,3,4,4,4,4,4,5,5,6}`, queremos saber o intervalo em que 4 aparece:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    // Significa que 4 não existe no array
    cout << "4 aparece 0 vezes" << endl;
} else {
    cout << "o primeiro 4 está em " << it1 - nums.begin() << endl;
    cout << "o último 4 está em " << it2 - nums.begin() - 1 << endl;
    cout << "4 aparece " << it2 - it1 << " vezes" << endl;
}
```

- `it1` aponta para a primeira posição cujo valor é maior ou igual a 4.
- `it2` aponta para a primeira posição cujo valor é maior que 4.  
  Portanto, `it2 - it1` é o número de vezes que 4 aparece no array; `it2 - nums.begin() - 1` é o limite direito de 4.

Essas duas funções são particularmente convenientes ao procurar intervalos ou contar o número de ocorrências.

## Complemento

A busca binária também pode ser estendida para a pesquisa em um intervalo de números de ponto flutuante (como encontrar raízes de uma equação) e a busca ternária para encontrar o máximo de uma função unimodal. Contanto que você entenda o princípio central de "**em um intervalo ordenado, metade pode ser eliminada a cada vez**", você descobrirá que a busca binária pode ajudá-lo a resolver problemas de forma eficiente em muitas situações.

## Exercícios

LeetCode 33. Search in Rotated Sorted Array

Dica: O primeiro passo é usar a busca binária para encontrar o ponto de rotação, e o segundo passo é usar a busca binária para encontrar o valor de destino.