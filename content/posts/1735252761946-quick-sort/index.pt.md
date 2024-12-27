---
title: "Ordenação Rápida"
date: 2024-12-26
draft: false
description: "Análise dos pontos-chave para implementar corretamente o algoritmo de ordenação rápida."
summary: "Análise dos pontos-chave para implementar corretamente o algoritmo de ordenação rápida."
tags: [ "Algoritmo", "Algoritmos de Ordenação", "Ordenação Rápida", "Algoritmo de Divisão e Conquista" ]
categories: [ "Algoritmos e Estruturas de Dados" ]
---

# Ordenação Rápida

A ordenação rápida é um algoritmo de ordenação não estável baseado em comparação, que utiliza a abordagem de divisão e conquista. Sua complexidade de tempo média é $O(n\log n)$, no pior caso é $O(n^2)$, e a complexidade de espaço é $O(1)$. Abaixo, usando a ordenação de uma sequência de números inteiros em ordem crescente como exemplo, apresentamos os detalhes de implementação e erros comuns.

---

## Descrição do Problema

Dado um sequência de $n$ números inteiros, use a ordenação rápida para ordená-los em ordem crescente e imprima o resultado.

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

Na ordenação rápida, a cada divisão, um número é escolhido como o número de referência `pivot` (abaixo, o número na posição do meio é escolhido).

Usando ponteiros esquerdo e direito que se movem em direções opostas, o ponteiro esquerdo `L` procura da esquerda para a direita o primeiro número maior ou igual a `pivot`, e o ponteiro direito `R` procura da direita para a esquerda o primeiro número menor ou igual a `pivot`, e então esses dois números são trocados.

Este processo é repetido continuamente até que os ponteiros esquerdo e direito se sobreponham ou o ponteiro esquerdo seja uma posição maior que o ponteiro direito. Isso é chamado de uma iteração.

Após cada movimento e troca de ponteiro, a estrutura "parte esquerda ≤ pivot, parte direita ≥ pivot" é garantida, ou seja, há um invariante `[left, L) <= pivot`, `(R, right] >= pivot`.

No exemplo de código abaixo, `left` e `right` são os limites do intervalo fechado atual que está sendo processado, e `pivot` é o elemento no ponto médio do intervalo.

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

Como a ordenação rápida tem uma complexidade de $O(n^2)$ no pior caso, a escolha do `pivot` é crucial. Se o primeiro ou o último elemento for sempre escolhido, o pior caso provavelmente ocorrerá em um array quase ordenado.

Além de escolher o elemento na posição do meio, um elemento pode ser escolhido aleatoriamente como `pivot`, ou a mediana dos três elementos à esquerda, no meio e à direita pode ser escolhida como `pivot`.

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

**Análise de Erros:**

1. `pivot` deve ser um número no array, não um índice.
2. Use `<` e `>` em vez de `<=` e `>=`, caso contrário, o ponteiro esquerdo pode ultrapassar o ponteiro direito em mais de uma posição, o que impede que o array seja dividido em duas partes.
3. Depois de encontrar `l >= r`, o loop deve ser encerrado imediatamente e nenhuma troca deve ser executada. Caso contrário, não é garantido que os elementos à esquerda não sejam maiores que `pivot` e que os elementos à direita não sejam menores que `pivot`.
4. Após cada troca, `l++` e `r--` devem ser executados.
5. `pivot` na verdade pega o número do meio à esquerda. Portanto, se você usar $l - 1$ e $l$ para dividir o array, considere o array `[1, 2]`, não é difícil descobrir que isso levará a um loop infinito, dividindo continuamente o array em duas partes de tamanho 0 e 2. Da mesma forma, usar $r$ e $l$ para distinguir o array também não funciona. Em vez disso, quando um loop termina, $r$ deve ser menor que $right$, então $r$ e $r+1$ podem ser usados para dividir o array. O leitor pode simular o processo do algoritmo para ver por quê. Outra maneira simples de evitar loops infinitos é escolher um `pivot` aleatoriamente ou lidar com o caso especial de apenas dois elementos.
6. Além disso, usar $l$, $l+1$ também não funciona, porque essa divisão não está de acordo com a definição. Quando $r$ está à esquerda de $l$, usar $l$, $l+1$ não pode dividir corretamente o array em duas partes onde a esquerda é menor ou igual a `pivot` e a direita é maior ou igual a `pivot`.
7. Este problema assume que o array não está vazio, então não há caso de `>`. Mas é recomendável usar `>=`, o que é mais seguro.

---

## Adicional

A ordenação rápida também pode evoluir para "seleção rápida", que pode encontrar o $k$-ésimo menor número em um array não ordenado em um tempo esperado de $O(n)$. A ideia específica é semelhante à ordenação rápida, exceto que a recursão continua apenas em um subintervalo de cada vez, reduzindo assim a complexidade de tempo.