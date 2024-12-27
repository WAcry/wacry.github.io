---
title: "Ricerca Binaria"
date: 2024-12-24
draft: false
description: "Come implementare elegantemente l'algoritmo di ricerca binaria."
summary: "Come implementare elegantemente l'algoritmo di ricerca binaria."
tags: [ "algoritmi", "ricerca binaria", "modelli di algoritmi" ]
categories: [ "Algoritmi e Strutture Dati" ]
---

Se uno spazio di soluzioni ordinato viene diviso in due parti, dove una parte soddisfa una condizione e l'altra no, allora è possibile utilizzare la ricerca binaria per trovare il punto critico nello spazio di soluzioni ordinato.

L'idea di base della ricerca binaria è quella di dividere ripetutamente a metà l'intervallo di ricerca. Ad ogni controllo, si verifica l'elemento centrale; se l'elemento centrale non soddisfa la condizione, si può escludere metà dell'intervallo; altrimenti, si continua la ricerca nell'altra metà dell'intervallo. Poiché ad ogni passo si scarta metà dell'intervallo di ricerca, la complessità temporale della ricerca può raggiungere $O(\log n)$.

## Esempio

**Descrizione del problema:**  
Dato un array di interi di lunghezza $n$ ordinato in modo crescente, e $q$ query. Ogni query fornisce un intero $k$, e dobbiamo trovare la "posizione iniziale" e la "posizione finale" di $k$ nell'array (gli indici partono da 0). Se il numero non esiste nell'array, restituisci `-1 -1`.

### Formato di input

1. Prima riga: due interi $n$ e $q$, che rappresentano rispettivamente la lunghezza dell'array e il numero di query.
2. Seconda riga: $n$ interi, che rappresentano l'array completo, già ordinato in modo crescente.
3. Le successive $q$ righe: ogni riga contiene un intero $k$, che rappresenta un elemento di query.

## Intervallo di dati

$1 \leq n \leq 100000$

$1 \leq q \leq 10000$

$1 \leq k \leq 10000$

### Formato di output

Per ogni query, stampa in una riga la posizione iniziale e finale dell'elemento nell'array. Se l'elemento non esiste nell'array, stampa `-1 -1`.

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

- L'intervallo in cui appare l'elemento $3$ è $[3, 4]$;
- L'elemento $4$ appare solo una volta, nella posizione $5$;
- L'elemento $5$ non esiste nell'array, quindi restituisce $-1$ $-1$.

---

## Soluzione

- **Trovare la "posizione iniziale":**
  Cioè, trovare la prima posizione maggiore o uguale a $k$. Possiamo dividere l'array in due parti:
    - Tutti i numeri a sinistra sono "minori" di $k$
    - Tutti i numeri a destra sono "maggiori o uguali" a $k$
    - La risposta è la prima posizione a destra

- **Trovare la "posizione finale":**
  Cioè, trovare l'ultima posizione minore o uguale a $k$. Possiamo dividere l'array in due parti:
    - Tutti i numeri a sinistra sono "minori o uguali" a $k$
    - Tutti i numeri a destra sono "maggiori" di $k$
    - La risposta è l'ultima posizione a sinistra

---

## Modello consigliato

Di seguito è riportato un modello di ricerca binaria elegante e poco incline a errori.

Definisci due puntatori $l, r$, con l'invariante: l'intervallo chiuso $[0, l]$ appartiene alla parte sinistra, l'intervallo chiuso $[r, n - 1]$ appartiene alla parte destra. $l$ e $r$ sono inizializzati rispettivamente a $-1$ e $n$.

Quando l'algoritmo termina, $l$ e $r$ sono adiacenti, puntando rispettivamente all'ultimo elemento della parte sinistra e al primo elemento della parte destra.

Poiché la soluzione che cerchiamo potrebbe non esistere, se il problema non specifica che una soluzione esiste sicuramente, dobbiamo verificare se `l` o `r` sono fuori dai limiti, e se puntano al valore corretto.

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
        //    La risposta è l'indice minimo della parte destra.
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
        //    La risposta è l'indice massimo della parte sinistra.
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

### Vantaggi

1. Questa scrittura ha invarianti rigorosamente definiti.
2. Si applica sia alla ricerca della "posizione iniziale" che della "posizione finale", senza bisogno di elaborazioni o modifiche aggiuntive.
3. Alcune scritture usano `l == r` come condizione di terminazione. Quando $l$ e $r$ differiscono di $1$, si calcola che $mid$ è uguale a $l$ o $r$. Se non viene gestito correttamente, aggiornando $l$ o $r$ a $mid$, l'intervallo di ricerca non si riduce, portando a un ciclo infinito. Al contrario, questa scrittura termina quando $l$ e $r$ sono adiacenti, garantendo che $mid$ sia minore di $l$ e maggiore di $r$, e che l'intervallo di ricerca si riduca quando si aggiorna $l$ o $r$.

---

## STL

Se si utilizzano le funzioni `lower_bound` e `upper_bound` fornite dalla STL di C++, si può ottenere lo stesso risultato:

- `lower_bound(first, last, val)` restituisce "la prima posizione maggiore o uguale a val"
- `upper_bound(first, last, val)` restituisce "la prima posizione maggiore di val"

Ad esempio, supponiamo che `nums = {1,2,3,4,4,4,4,4,5,5,6}`, e vogliamo sapere l'intervallo in cui appare 4:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    cout << "4 appare 0 volte" << endl;
} else {
    cout << "il primo 4 è in " << it1 - nums.begin() << endl;
    cout << "l'ultimo 4 è in " << it2 - nums.begin() - 1 << endl;
    cout << "4 appare " << it2 - it1 << " volte" << endl;
}
```

- `it1` punta alla prima posizione con un valore maggiore o uguale a $4$.
- `it2` punta alla prima posizione con un valore maggiore di $4$.  
  Quindi `it2 - it1` è il numero di volte in cui $4$ appare nell'array; `it2 - nums.begin() - 1` è la posizione del limite destro di $4$.

---

## Aggiunte

La ricerca binaria può essere estesa anche alla ricerca in intervalli di numeri in virgola mobile (come trovare le radici di un'equazione) e alla ricerca ternaria per trovare il valore massimo di una funzione unimodale.

---

## Esercizi

LeetCode 33. Search in Rotated Sorted Array

Suggerimento: il primo passo è usare la ricerca binaria per trovare il punto di rotazione, il secondo passo è usare di nuovo la ricerca binaria per trovare il valore target.