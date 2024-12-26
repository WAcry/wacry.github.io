---
title: "Ordinamento Rapido"
date: 2024-12-26
draft: false
description: "Analisi dei punti chiave per implementare correttamente l'algoritmo di ordinamento rapido."
summary: "Analisi dei punti chiave per implementare correttamente l'algoritmo di ordinamento rapido."
tags: [ "Algoritmi", "Algoritmi di ordinamento", "Ordinamento rapido", "Algoritmi divide et impera" ]
categories: [ "Algoritmi e Strutture Dati" ]
---

# Ordinamento Rapido

L'ordinamento rapido è un algoritmo di ordinamento non stabile basato sul confronto, che utilizza il principio del divide et impera, con una complessità temporale media di $O(n\log n)$ e una complessità temporale nel caso peggiore di $O(n^2)$
, e una complessità spaziale di $O(1)$. Di seguito, prendendo come esempio l'ordinamento di una sequenza di numeri interi in ordine crescente, vengono presentati i dettagli dell'implementazione e gli errori comuni.

---

## Descrizione del Problema

Dato un elenco di $n$ numeri interi, utilizzare l'ordinamento rapido per ordinarli in ordine crescente e visualizzare il risultato.

### Formato di Input

- La prima riga contiene l'intero $n$.
- La seconda riga contiene $n$ numeri interi, tutti nell'intervallo $[1,10^9]$.

### Formato di Output

- Una riga contenente l'elenco ordinato.

### Intervallo di Dati

$1 \leq n \leq 100000$

### Esempio di Input

```
5
3 1 2 4 5
```

### Esempio di Output

```
1 2 3 4 5
```

---

## Idea dell'Ordinamento Rapido

Ogni volta che l'ordinamento rapido divide il problema, seleziona un numero qualsiasi come numero di riferimento `pivot` (di seguito, si seleziona il numero nella posizione centrale).

Utilizza puntatori sinistro e destro che si muovono uno verso l'altro. Il puntatore sinistro `L` cerca da sinistra a destra il primo numero maggiore o uguale a `pivot`, mentre il puntatore destro `R` cerca da destra a sinistra il primo numero minore o uguale a `pivot`, quindi scambia questi due numeri.

Ripeti questo processo continuamente fino a quando i puntatori sinistro e destro si sovrappongono o il puntatore sinistro supera il puntatore destro di una posizione. Questo è chiamato un ciclo.

Dopo ogni spostamento del puntatore e scambio, assicurarsi che la struttura "parte sinistra ≤ pivot, parte destra ≥ pivot" non venga interrotta, cioè che ci sia un invariante `[left, L) <= pivot`, `(R, right] >= pivot`.

Nel seguente esempio di codice, `left` e `right` sono i limiti dell'intervallo chiuso attualmente elaborato, e `pivot` è l'elemento nel punto medio dell'intervallo.

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

## Complessità e Scelta del `pivot`

Poiché l'ordinamento rapido ha una complessità di $O(n^2)$ nel caso peggiore, la scelta del `pivot` è molto importante. Se si sceglie sempre il primo o l'ultimo elemento, è probabile che si verifichi il caso peggiore in array quasi ordinati.

Oltre a prendere l'elemento nella posizione centrale, è anche possibile selezionare casualmente un elemento come `pivot`, oppure prendere la mediana dei tre elementi a sinistra, al centro e a destra come `pivot`.

---

## Esempi di Errori Comuni

Il codice seguente contiene molti errori comuni.

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

**Analisi degli Errori:**

1. `pivot` dovrebbe essere un numero nell'array, non un indice.
2. Usare `<` e `>` rispettivamente invece di `<=` e `>=`, altrimenti il puntatore sinistro potrebbe superare il puntatore destro di più di una posizione, quindi non è possibile dividere l'array in due parti.
3. Dopo aver rilevato `l >= r`, il ciclo dovrebbe essere interrotto immediatamente, senza eseguire scambi. In caso contrario, non è possibile garantire che gli elementi a sinistra non siano maggiori di `pivot` e che gli elementi a destra non siano inferiori a `pivot`.
4. Dopo ogni scambio, è necessario eseguire `l++` e `r--`.
5. In realtà, `pivot` prende il numero centrale a sinistra. Se si utilizzano $l - 1$ e $l$ per dividere l'array, considerando l'array `[1, 2]`, non è difficile scoprire che ciò porterà a un ciclo infinito, dividendo continuamente l'array in due parti di dimensioni
   0 e 2. Al contrario, quando il ciclo termina, $r$ è necessariamente minore di $right$, quindi è possibile utilizzare $r$ e $r+1$ per
   dividere l'array. I lettori possono simulare il processo dell'algoritmo per vedere perché. Un altro modo semplice per evitare cicli infiniti è selezionare casualmente
   `pivot` o gestire in modo speciale i casi con solo due elementi. Analogamente, non è possibile distinguere l'array con $r$ e $l$.
6. Inoltre, anche con $l$, $l+1$ non va bene, perché questa divisione non è conforme alla definizione. Quando $r$ è a sinistra di $l$, usando $l$, $l+1$ non è possibile dividere correttamente l'array in due parti, quella a sinistra minore o uguale a
   `pivot`, e quella a destra maggiore o uguale a `pivot`.
7. Questo problema presuppone che l'array non sia vuoto, quindi non esiste il caso `>`. Tuttavia, si consiglia di utilizzare `>=`, per maggiore sicurezza.

---

## Aggiunta

L'ordinamento rapido può anche evolvere in "selezione rapida", che può trovare il k-esimo numero più piccolo in un array non ordinato nel tempo previsto di $O(n)$. L'idea specifica è simile all'ordinamento rapido, ma ogni volta ricorre solo su un sottointervallo, riducendo così la complessità temporale.