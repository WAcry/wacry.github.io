---
title: "Ordinamento rapido"
date: 2024-12-26
draft: false
description: "Analisi dei punti chiave per implementare correttamente l'algoritmo di ordinamento rapido."
summary: "Analisi dei punti chiave per implementare correttamente l'algoritmo di ordinamento rapido."
tags: [ "Algoritmi", "Algoritmi di ordinamento", "Ordinamento rapido", "Algoritmi divide et impera" ]
categories: [ "Algoritmi e strutture dati" ]
---

# Ordinamento rapido

L'ordinamento rapido è un algoritmo di ordinamento non stabile basato sul confronto, che adotta l'approccio divide et impera. La sua complessità temporale media è $O(n\log n)$, nel caso peggiore è $O(n^2)$, e la complessità spaziale è $O(1)$. Di seguito, prendendo come esempio l'ordinamento crescente di una sequenza di numeri interi, vengono presentati i dettagli della sua implementazione e gli errori comuni.

---

## Descrizione del problema

Dato un elenco di numeri interi di lunghezza $n$, utilizzare l'ordinamento rapido per ordinarlo in ordine crescente e visualizzare il risultato.

### Formato di input

- La prima riga inserisce l'intero $n$
- La seconda riga inserisce $n$ numeri interi, tutti compresi nell'intervallo $[1,10^9]$

### Formato di output

- Una riga che visualizza la sequenza ordinata

### Intervallo di dati

$1 \leq n \leq 100000$

### Esempio di input

```
5
3 1 2 4 5
```

### Esempio di output

```
1 2 3 4 5
```

---

## Idea dell'ordinamento rapido

Ogni volta che l'ordinamento rapido divide il problema, seleziona un numero qualsiasi come numero di riferimento `pivot` (di seguito viene scelto il numero nella posizione centrale).

Utilizzare puntatori sinistro e destro che si muovono l'uno verso l'altro. Il puntatore sinistro `L` cerca da sinistra a destra il primo numero maggiore o uguale a `pivot`, mentre il puntatore destro `R` cerca da destra a sinistra il primo numero minore o uguale a `pivot`, quindi scambia questi due numeri.

Ripetere continuamente questo processo finché il puntatore sinistro e il puntatore destro non si sovrappongono o il puntatore sinistro non è maggiore di una posizione rispetto al puntatore destro. Questo è chiamato un ciclo.

Dopo ogni spostamento e scambio dei puntatori, si garantisce che la struttura "parte sinistra ≤ pivot, parte destra ≥ pivot" non venga danneggiata, ovvero si ha l'invariante `[left, L) <= pivot`, `(R, right] >= pivot`.

Nel seguente codice di esempio, `left` e `right` sono i limiti dell'intervallo chiuso attualmente in elaborazione, mentre `pivot` prende l'elemento nel punto medio dell'intervallo.

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

## Complessità e scelta del `pivot`

Poiché nel caso peggiore l'ordinamento rapido ha una complessità di $O(n^2)$, la scelta del `pivot` è fondamentale. Se si sceglie sempre il primo o l'ultimo elemento, in un array quasi ordinato è molto probabile che si verifichi il caso peggiore.

Oltre a prendere l'elemento nella posizione centrale, è anche possibile selezionare casualmente un elemento come `pivot`, oppure prendere la mediana dei tre elementi a sinistra, al centro e a destra come `pivot`.

---

## Esempi di errori comuni

Il seguente codice contiene diversi errori comuni.

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

**Analisi degli errori:**

1. `pivot` dovrebbe essere un numero nell'array, non un indice.
2. Utilizzare rispettivamente `<` e `>` invece di `<=` e `>=`, altrimenti il puntatore sinistro potrebbe superare il puntatore destro di più di una posizione, e quindi non è possibile dividere l'array in due parti.
3. Dopo aver rilevato `l >= r`, è necessario uscire immediatamente dal ciclo e non eseguire più lo scambio. Altrimenti, non è possibile garantire che gli elementi a sinistra non siano maggiori di `pivot` e che gli elementi a destra non siano minori di `pivot`.
4. Dopo ogni scambio, è necessario eseguire `l++` e `r--`.
5. `pivot` in realtà prende il numero centrale a sinistra. Pertanto, se si utilizza $l - 1$ e $l$ per dividere l'array, considerando l'array `[1, 2]`, non è difficile scoprire che si verificherà un ciclo infinito, dividendo continuamente l'array in due parti di dimensione 0 e 2. Allo stesso modo, non è possibile utilizzare $r$ e $l$ per distinguere l'array. Al contrario, quando un ciclo termina, $r$ è necessariamente minore di $right$, quindi è possibile utilizzare $r$ e $r+1$ per dividere l'array. Il lettore può simulare il processo dell'algoritmo per vedere perché. Un altro modo semplice per evitare cicli infiniti è selezionare casualmente `pivot` o gestire in modo speciale il caso in cui ci sono solo due elementi.
6. Inoltre, non è possibile utilizzare $l$, $l+1$, perché questa divisione non è conforme alla definizione. Quando $r$ si trova a sinistra di $l$, l'utilizzo di $l$, $l+1$ non può dividere correttamente l'array in due parti, una a sinistra minore o uguale a `pivot` e una a destra maggiore o uguale a `pivot`.
7. Questo problema presuppone che l'array non sia vuoto, quindi non esiste il caso `>`. Tuttavia, si consiglia di utilizzare `>=`, che è più sicuro.

---

## Aggiunte

L'ordinamento rapido può anche evolvere in "selezione rapida", che consente di trovare l'elemento $k$-esimo più piccolo in un array non ordinato in un tempo previsto di $O(n)$. L'idea specifica è simile all'ordinamento rapido, ma ogni volta si continua la ricorsione solo in un sottointervallo, riducendo così la complessità temporale.