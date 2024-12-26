---
title: "Ordenação Rápida"
date: 2024-12-26
draft: false
description: "Análise dos pontos-chave para implementar corretamente o algoritmo de ordenação rápida."
summary: "Análise dos pontos-chave para implementar corretamente o algoritmo de ordenação rápida."
tags: [ "Algoritmo", "Algoritmos de Ordenação", "Ordenação Rápida", "Algoritmo Dividir para Conquistar" ]
categories: [ "Algoritmos e Estruturas de Dados" ]
---

# Ordenação Rápida

A ordenação rápida é um algoritmo de ordenação não estável baseado em comparação, que utiliza o paradigma de dividir para conquistar. Possui uma complexidade de tempo média de $O(n\log n)$ e, no pior caso, de $O(n^2)$, com complexidade de espaço de $O(1)$. Abaixo, usando como exemplo a ordenação de uma sequência de números inteiros em ordem crescente, são apresentados detalhes de implementação e erros comuns.

---

## Descrição do Problema

Dada uma sequência de $n$ números inteiros, ordene-a em ordem crescente utilizando a ordenação rápida e exiba o resultado.

### Formato de Entrada

- A primeira linha contém o inteiro $n$
- A segunda linha contém $n$ inteiros, todos no intervalo $[1,10^9]$

### Formato de Saída

- Uma linha contendo a sequência ordenada

### Intervalo de Dados

$1 \leq n \leq 100000$

### Exemplo de Entrada

```
5
3 1 2 4 5
```

### Exemplo de Saída

```
1 2 3 4 5
```

---

## Ideia da Ordenação Rápida

Na ordenação rápida, a cada etapa da divisão para conquistar, um número é escolhido como `pivot` (abaixo, o número na posição do meio é escolhido).

Dois ponteiros são usados: um ponteiro `L` que se move da esquerda para a direita procurando o primeiro número maior ou igual a `pivot`, e um ponteiro `R` que se move da direita para a esquerda procurando o primeiro número menor ou igual a `pivot`. Em seguida, esses dois números são trocados.

Esse processo é repetido até que os ponteiros se sobreponham ou o ponteiro esquerdo ultrapasse o ponteiro direito. Isso é chamado de uma iteração.

Após cada movimentação e troca de ponteiros, garante-se que a estrutura "parte esquerda ≤ pivot, parte direita ≥ pivot" seja mantida, ou seja, o invariante `[left, L) <= pivot`, `(R, right] >= pivot`.

No exemplo de código abaixo, `left` e `right` são os limites do intervalo fechado que está sendo processado atualmente, e `pivot` é o elemento no ponto médio do intervalo.

```cpp
#include <bits/stdc++.h>
using namespace std;

void quickSort(vector<int> &a, int left, int right) {
    if (left >= right) return;
    
    int pivot = a[(left + right) / 2];
    int l = left, r = right;
    
    while (true) {
        while (a[l] < pivot) l++;
        while (a[r] > pivot) r--;
        if (l >= r) break;
        swap(a[l], a[r]);
        l++; r--;
    }
    
    quickSort(a, left, r);
    quickSort(a, r + 1, right);
}

int main() {
    int n; cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    
    quickSort(a, 0, n - 1);
    
    for (int i = 0; i < n; i++) cout << a[i] << " ";
    return 0;
}
```

---

## Complexidade e Escolha do `pivot`

Como no pior caso a ordenação rápida tem uma complexidade de $O(n^2)$, a escolha do `pivot` é crucial. Se o primeiro ou o último elemento for sempre escolhido como `pivot`, é muito provável que ocorra o pior caso em arrays quase ordenados.

Além de escolher o elemento da posição central, um elemento pode ser escolhido aleatoriamente como `pivot`, ou a mediana de três elementos (o da esquerda, do meio e da direita) pode ser escolhida como `pivot`.

---

## Exemplos de Erros Comuns

O código abaixo contém vários erros comuns.

```cpp
#include <bits/stdc++.h>
using namespace std;

void quickSort(vector<int> &a, int left, int right) {
    if (left == right) return; // 7

    int pivot = (left + right) >> 1; // 1
    int l = left, r = right;

    while (true) {
        while (a[l] <= pivot) l++; // 2
        while (a[r] >= pivot) r--; // 2
        swap(a[l], a[r]);
        if (l >= r) break; // 3
        // 4
    }

    quickSort(a, left, l - 1); // 5, 6
    quickSort(a, l, right);    // 5, 6
}

int main() {
    int n; cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    
    quickSort(a, 0, n - 1);
    
    for (int i = 0; i < n; i++) cout << a[i] << " ";
    return 0;
}
```

**Análise dos Erros:**

1.  `pivot` deve ser um número do array, não um índice.
2.  Use `<` e `>` em vez de `<=` e `>=`, caso contrário, o ponteiro esquerdo pode ultrapassar o ponteiro direito em mais de uma posição, o que impede a divisão do array em duas partes.
3.  Após encontrar `l >= r`, o loop deve ser interrompido imediatamente, sem realizar mais trocas. Caso contrário, não há garantia de que os elementos à esquerda sejam menores ou iguais a `pivot` e os elementos à direita sejam maiores ou iguais a `pivot`.
4.  Após cada troca, `l++` e `r--` devem ser executados.
5.  `pivot` na verdade pega o número do meio tendendo para a esquerda. Se $l-1$ e $l$ forem usados para dividir o array, considerando o array `[1, 2]`, não é difícil perceber que isso levará a um loop infinito, dividindo o array em duas partes de tamanho 0 e 2 continuamente. Por outro lado, quando o loop termina, $r$ é necessariamente menor que $right$, portanto, $r$ e $r+1$ podem ser usados para dividir o array. O leitor pode simular o processo do algoritmo para entender o porquê. Uma maneira alternativa e simples de evitar o loop infinito é escolher o `pivot` aleatoriamente ou tratar especialmente o caso de apenas dois elementos. De modo semelhante, usar $r$ e $l$ para dividir o array também não funciona.
6. Além disso, usar $l$ e $l+1$ também não funciona, pois essa divisão não está de acordo com a definição, e quando $r$ está à esquerda de $l$, usar $l$ e $l+1$ não dividirá corretamente o array em duas partes, onde os elementos à esquerda são menores ou iguais a `pivot` e os elementos à direita são maiores ou iguais a `pivot`.
7. Este problema assume que o array não está vazio, portanto não há caso de  `>` mas é aconselhável usar `>=` para maior segurança.

---

## Complemento

A ordenação rápida também pode ser desenvolvida para a "seleção rápida", que encontra o k-ésimo menor número em um array não ordenado em um tempo esperado de $O(n)$. A ideia é semelhante à da ordenação rápida, mas a recursão continua apenas em uma sub-intervalo a cada vez, reduzindo assim a complexidade de tempo.