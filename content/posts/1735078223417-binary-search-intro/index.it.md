---
title: "Ricerca Binaria"
date: 2024-12-24
draft: false
description: "Come implementare in modo elegante l'algoritmo di ricerca binaria per interi."
summary: "Come implementare in modo elegante l'algoritmo di ricerca binaria per interi."
tags: [ "Algoritmi", "Ricerca Binaria", "Template Algoritmi" ]
categories: [ "Algoritmi e Strutture Dati" ]
---

{{< katex >}}

# Ricerca Binaria

Se uno spazio di soluzioni ordinato può essere diviso in due parti, dove una parte soddisfa una condizione e l'altra no, allora è possibile utilizzare la ricerca binaria per trovare il punto critico nello spazio di soluzioni ordinato.

L'idea fondamentale della ricerca binaria è quella di dividere ripetutamente a metà l'intervallo di ricerca. Ad ogni passo, viene controllato l'elemento centrale. Se l'elemento centrale non soddisfa la condizione, si può escludere metà dell'intervallo; altrimenti, si continua la ricerca nell'altra metà. Poiché ad ogni passo viene scartata metà dello spazio di ricerca, la complessità temporale della ricerca può raggiungere \\(O(\log n)\\).

## Esempio di Problema

**Descrizione del problema:**  
Dato un array di interi di lunghezza \\(n\\) ordinato in ordine crescente e \\(q\\) query. Ogni query fornisce un intero \\(k\\) e dobbiamo trovare la "posizione iniziale" e la "posizione finale" di \\(k\\) nell'array (gli indici iniziano da 0). Se il numero non è presente nell'array, restituire \\(-1\\) \\(-1\\).

### Formato di Input

1. Prima riga: due interi \\(n\\) e \\(q\\), che rappresentano rispettivamente la lunghezza dell'array e il numero di query.
2. Seconda riga: \\(n\\) interi, che rappresentano l'intero array, già ordinato in ordine crescente.
3. Le successive \\(q\\) righe: ogni riga contiene un intero \\(k\\), che rappresenta un elemento di query.

## Intervallo di Dati

\\(1 \leq n \leq 100000\\)

\\(1 \leq q \leq 10000\\)

\\(1 \leq k \leq 10000\\)

### Formato di Output

Per ogni query, stampare in una riga la posizione iniziale e finale dell'elemento nell'array. Se l'elemento non è presente nell'array, stampare `-1 -1`.

**Esempio:**

```
Input:
6 3
1 2 2 3 3 4
3
4
5

Output:
3 4
5 5
-1 -1
```

**Spiegazione:**

- L'intervallo in cui compare l'elemento \\(3\\) è \\([3, 4]\\);
- L'elemento \\(4\\) compare una sola volta, nella posizione \\(5\\);
- L'elemento \\(5\\) non è presente nell'array, quindi viene restituito \\(-1\\) \\(-1\\).

---

## Soluzione

- **Trova la "posizione iniziale":**
  Ovvero, trova la prima posizione con un valore maggiore o uguale a \\(k\\). Possiamo dividere l'array in due parti:
    - Tutti i numeri a sinistra sono "minori" di \\(k\\)
    - Tutti i numeri a destra sono "maggiori o uguali" a \\(k\\)
    - La risposta è la prima posizione a destra

- **Trova la "posizione finale":**
  Ovvero, trova l'ultima posizione con un valore minore o uguale a \\(k\\). Possiamo dividere l'array in due parti:
    - Tutti i numeri a sinistra sono "minori o uguali" a \\(k\\)
    - Tutti i numeri a destra sono "maggiori" di \\(k\\)
    - La risposta è l'ultima posizione a sinistra

---

## Template Raccomandato

Di seguito è riportato un template di ricerca binaria elegante e poco incline agli errori. Avvicinando gradualmente \\(l\\) e \\(r\\), si garantisce che il ciclo termini quando sono adiacenti:

Definiamo due puntatori \\(l, r\\), con le seguenti invarianti: l'intervallo chiuso \\([0, l]\\) appartiene alla parte sinistra, l'intervallo chiuso \\([r, n - 1]\\) appartiene alla parte destra. \\(l\\) e \\(r\\) sono inizializzati rispettivamente a \\(-1\\) e \\(n\\).

Quando l'algoritmo termina, \\(l\\) e \\(r\\) sono adiacenti, e puntano rispettivamente all'ultimo elemento della parte sinistra e al primo elemento della parte destra.

Poiché la soluzione desiderata potrebbe non esistere, se il problema non indica che la soluzione esiste sicuramente, dobbiamo verificare se `l` o `r` sono fuori dai limiti, e se puntano al valore corretto.

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

        // 1. Trova la posizione iniziale di k
        //    Dividi l'array in due parti, a sinistra tutti < k, a destra tutti >= k.
        //    La risposta è il minimo indice della parte destra.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // Se r è fuori dai limiti o nums[r] != k, significa che k non esiste
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. Trova la posizione finale di k
        //    Dividi l'array in due parti, a sinistra tutti <= k, a destra tutti > k.
        //    La risposta è il massimo indice della parte sinistra.
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

### Perché scrivere in questo modo

1. Questa scrittura ha invarianti rigorosamente definite.
2. Si adatta sia al caso di trovare la "posizione iniziale" sia a quello di trovare la "posizione finale", senza la necessità di ulteriori elaborazioni o modifiche.
3. Alcune scritture utilizzano `l == r` come condizione di terminazione. Quando \\(l\\) e \\(r\\) differiscono di \\(1\\), calcolando \\(mid\\) si otterrà un valore uguale a \\(l\\) o \\(r\\). Se non viene gestito correttamente, l'aggiornamento di \\(l\\) o \\(r\\) a \\(mid\\), non riduce l'intervallo di ricerca, causando un ciclo infinito. Invece, la scrittura qui riportata termina quando \\(l\\) e \\(r\\) sono adiacenti, garantendo che \\(mid\\) sia minore di \\(l\\) e maggiore di \\(r\\), riducendo sempre l'intervallo di ricerca quando si aggiorna \\(l\\) o \\(r\\).

---

## STL

Se si utilizzano le funzioni `lower_bound` e `upper_bound` fornite dalla STL del C++, è possibile ottenere lo stesso risultato:

- `lower_bound(first, last, val)` restituisce "la prima posizione con un valore maggiore o uguale a val"
- `upper_bound(first, last, val)` restituisce "la prima posizione con un valore maggiore di val"

Per fare un esempio, supponiamo che `nums = {1,2,3,4,4,4,4,4,5,5,6}`, e vogliamo sapere l'intervallo in cui compare 4:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    cout << "4 compare 0 volte" << endl;
} else {
    cout << "il primo 4 è in " << it1 - nums.begin() << endl;
    cout << "l'ultimo 4 è in " << it2 - nums.begin() - 1 << endl;
    cout << "4 compare " << it2 - it1 << " volte" << endl;
}
```

- `it1` punta alla prima posizione con un valore maggiore o uguale a \\(4\\).
- `it2` punta alla prima posizione con un valore maggiore di \\(4\\).  
  Quindi `it2 - it1` è il numero di volte in cui \\(4\\) compare nell'array; `it2 - nums.begin() - 1` è il limite destro di \\(4\\).

---

## Aggiunte

La ricerca binaria può essere estesa anche alla ricerca in intervalli di numeri in virgola mobile (come la ricerca delle radici di un'equazione) e alla ricerca ternaria per trovare il valore massimo o minimo di una funzione unimodale.
Finché si comprende il principio fondamentale di "**eliminare ogni volta la metà di un intervallo ordinato**", si scoprirà che la ricerca binaria può aiutare a risolvere efficacemente i problemi in molti scenari.

---

## Esercizio

LeetCode 33. Search in Rotated Sorted Array

Suggerimento: nel primo passo, utilizzare la ricerca binaria per trovare il punto di rotazione, nel secondo passo, utilizzare di nuovo la ricerca binaria per trovare il valore di destinazione.