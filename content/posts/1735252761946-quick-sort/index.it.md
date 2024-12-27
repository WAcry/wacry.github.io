---
title: "Ordinamento Rapido"
date: 2024-12-26
draft: false
description: "Analisi dei punti chiave per implementare correttamente l'algoritmo di ordinamento rapido."
summary: "Analisi dei punti chiave per implementare correttamente l'algoritmo di ordinamento rapido."
tags: [ "algoritmi", "algoritmi di ordinamento", "ordinamento rapido", "algoritmi divide et impera" ]
categories: [ "Algoritmi e Strutture Dati" ]
---

# Ordinamento Rapido

L'ordinamento rapido (Quicksort) è un algoritmo di ordinamento non stabile basato sul confronto, che adotta la strategia divide et impera. La sua complessità temporale media è $O(n\log n)$, nel caso peggiore è $O(n^2)$, mentre la complessità spaziale è $O(1)$. Di seguito, prendendo come esempio l'ordinamento crescente di una sequenza di numeri interi, vengono presentati i dettagli di implementazione e gli errori comuni.

---

## Descrizione del Problema

Data una sequenza di $n$ numeri interi, ordinarla in modo crescente utilizzando l'ordinamento rapido e stampare il risultato.

### Formato di Input

- La prima riga contiene l'intero $n$
- La seconda riga contiene $n$ numeri interi, tutti compresi nell'intervallo $[1,10^9]$

### Formato di Output

- Una riga contenente la sequenza ordinata

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

## Approccio all'Ordinamento Rapido

Ad ogni passo di divide et impera, l'ordinamento rapido seleziona un numero come `pivot` (di seguito, viene scelto il numero nella posizione centrale).

Si utilizzano due puntatori, uno sinistro `L` e uno destro `R`, che si muovono in direzioni opposte. Il puntatore sinistro `L` si sposta da sinistra verso destra cercando il primo numero maggiore o uguale al `pivot`, mentre il puntatore destro `R` si sposta da destra verso sinistra cercando il primo numero minore o uguale al `pivot`. Quindi, questi due numeri vengono scambiati.

Questo processo viene ripetuto finché i puntatori sinistro e destro si sovrappongono o il puntatore sinistro supera di una posizione il puntatore destro. Questo è chiamato un ciclo.

Dopo ogni spostamento e scambio dei puntatori, si garantisce che la struttura "parte sinistra ≤ pivot, parte destra ≥ pivot" non venga violata, ovvero si mantiene l'invariante `[left, L) <= pivot`, `(R, right] >= pivot`.

Nel codice di esempio seguente, `left` e `right` sono i limiti dell'intervallo chiuso attualmente in elaborazione, mentre `pivot` è l'elemento nel punto medio dell'intervallo.

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

Poiché nel caso peggiore l'ordinamento rapido ha una complessità di $O(n^2)$, la scelta del `pivot` è cruciale. Se si sceglie sempre il primo o l'ultimo elemento, è molto probabile che si verifichi il caso peggiore in array quasi ordinati.

Oltre a scegliere l'elemento nella posizione centrale, è possibile selezionare casualmente un elemento come `pivot`, oppure scegliere la mediana tra gli elementi di sinistra, centrale e destra.

---

## Esempio di Errori Comuni

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

**Analisi degli Errori:**

1. `pivot` dovrebbe essere un numero nell'array, non un indice.
2. Si usano `<=` e `>=` invece di `<` e `>`, altrimenti il puntatore sinistro potrebbe superare il puntatore destro di più di una posizione, impedendo la divisione dell'array in due parti.
3. Dopo aver trovato `l >= r`, il ciclo dovrebbe terminare immediatamente, senza eseguire lo scambio. Altrimenti, non si garantisce che gli elementi a sinistra non siano maggiori di `pivot` e che gli elementi a destra non siano minori di `pivot`.
4. Dopo ogni scambio, è necessario eseguire `l++` e `r--`.
5. `pivot` in realtà prende il numero centrale sinistro. Pertanto, se si usa $l - 1$ e $l$ per dividere l'array, considerando l'array `[1, 2]`, è facile vedere che si verificherà un ciclo infinito, dividendo continuamente l'array in due parti di dimensione 0 e 2. Analogamente, non è corretto usare $r$ e $l$ per dividere l'array. Al contrario, alla fine di un ciclo, $r$ è necessariamente minore di $right$, quindi è possibile usare $r$ e $r+1$ per dividere l'array. Il lettore può simulare il processo dell'algoritmo per capire il perché. Un altro modo semplice per evitare il ciclo infinito è scegliere casualmente il `pivot` o gestire in modo speciale il caso in cui ci sono solo due elementi.
6. Inoltre, non è corretto usare $l$, $l+1$ perché questa divisione non è conforme alla definizione. Quando $r$ è a sinistra di $l$, usare $l$, $l+1$ non divide correttamente l'array in due parti, una a sinistra minore o uguale a `pivot` e una a destra maggiore o uguale a `pivot`.
7. Questo problema presuppone che l'array non sia vuoto, quindi non esiste il caso `>`. Tuttavia, si consiglia di usare `>=`, per maggiore sicurezza.

---

## Aggiunte

L'ordinamento rapido può anche essere trasformato in "selezione rapida", che consente di trovare l'elemento $k$-esimo più piccolo in un array non ordinato in un tempo atteso di $O(n)$. L'idea è simile all'ordinamento rapido, ma ad ogni passo si continua la ricorsione solo in un sottointervallo, riducendo così la complessità temporale.