---
title: "Ricerca Binaria"
date: 2024-12-24
draft: false
description: "Come implementare elegantemente l'algoritmo di ricerca binaria."
summary: "Come implementare elegantemente l'algoritmo di ricerca binaria."
tags: [ "algoritmi", "ricerca binaria", "modelli di algoritmi" ]
categories: [ "algoritmi e strutture dati" ]
---

Se uno spazio di soluzione ordinato viene diviso in due parti, dove una parte soddisfa una condizione e l'altra no, allora è possibile utilizzare la ricerca binaria per trovare il punto critico nello spazio di soluzione ordinato.

L'idea di base della ricerca binaria è quella di dividere ripetutamente l'intervallo di ricerca a metà. Ad ogni passo, viene esaminato l'elemento centrale. Se l'elemento centrale non soddisfa la condizione, è possibile escludere metà dell'intervallo; altrimenti, la ricerca continua nell'altra metà. Poiché ogni volta viene scartata metà dell'intervallo di ricerca, la complessità temporale della ricerca può raggiungere $O(\log n)$.

## Esempio di problema

**Descrizione del problema:**
Dato un array di interi di lunghezza $n$ ordinato in modo crescente, e $q$ query. Ogni query fornisce un intero $k$, e dobbiamo trovare la "posizione iniziale" e la "posizione finale" (gli indici partono da 0) di $k$ nell'array. Se il numero non è presente nell'array, restituisci `-1 -1`.

### Formato di input

1. Prima riga: due interi $n$ e $q$, che rappresentano rispettivamente la lunghezza dell'array e il numero di query.
2. Seconda riga: $n$ interi, che rappresentano l'array completo, già ordinato in modo crescente.
3. Le successive $q$ righe: ogni riga contiene un intero $k$, che rappresenta un elemento di query.

## Intervallo dei dati

$1 \leq n \leq 100000$

$1 \leq q \leq 10000$

$1 \leq k \leq 10000$

### Formato di output

Per ogni query, stampa in una riga la posizione iniziale e finale dell'elemento nell'array. Se l'elemento non è presente nell'array, stampa `-1 -1`.

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

- L'intervallo in cui compare l'elemento $3$ è $[3, 4]$;
- L'elemento $4$ compare una sola volta, nella posizione $5$;
- L'elemento $5$ non esiste nell'array, quindi viene restituito $-1$ $-1$.

---

## Soluzione

- **Trovare la "posizione iniziale":**
  Ovvero, trovare la prima posizione maggiore o uguale a $k$. L'array può essere diviso in due parti:
    - Tutti i numeri a sinistra sono "minori" di $k$.
    - Tutti i numeri a destra sono "maggiori o uguali" di $k$.
    - La risposta è la prima posizione a destra.

- **Trovare la "posizione finale":**
  Ovvero, trovare l'ultima posizione minore o uguale a $k$. L'array può essere diviso in due parti:
    - Tutti i numeri a sinistra sono "minori o uguali" di $k$.
    - Tutti i numeri a destra sono "maggiori" di $k$.
    - La risposta è l'ultima posizione a sinistra.

---

## Modello raccomandato

Di seguito è presentato un modello di ricerca binaria elegante e non soggetto a errori. Facendo in modo che $l$ e $r$ si avvicinino gradualmente, si garantisce che il ciclo termini quando i due sono adiacenti:

Definisci due puntatori $l, r$, con le seguenti invarianti: l'intervallo chiuso $[0, l]$ appartiene alla metà sinistra, l'intervallo chiuso $[r, n - 1]$ appartiene alla metà destra. $l$ e $r$ sono inizializzati rispettivamente a $-1$ e $n$.

Quando l'algoritmo termina, $l$ e $r$ sono adiacenti, puntando rispettivamente all'ultimo elemento della metà sinistra e al primo elemento della metà destra.

Poiché la soluzione desiderata potrebbe non esistere, se il problema non specifica che la soluzione esiste sempre, dobbiamo controllare se `l` o `r` sono fuori dai limiti e se puntano al valore corretto.

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
        //    La risposta è l'indice minimo nella parte destra.
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
        //    La risposta è l'indice massimo nella parte sinistra.
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

1. Questa scrittura ha invarianti definiti rigorosamente.
2. Si adatta sia alla ricerca della "posizione iniziale" che della "posizione finale", senza bisogno di elaborazioni e modifiche aggiuntive.
3. Alcune scritture usano `l == r` come condizione di terminazione. Quando $l$ e $r$ differiscono di $1$, verrà calcolato un valore $mid$ uguale a $l$ o $r$. Se non vengono gestiti correttamente, aggiornando $l$ o $r$ con $mid$, l'intervallo di ricerca non si riduce, portando a un ciclo infinito. Al contrario, questa scrittura termina quando $l$ e $r$ sono adiacenti, garantendo che $mid$ sia minore di $l$ e maggiore di $r$, e che aggiornando $l$ o $r$ l'intervallo di ricerca si riduca sempre.

---

## STL

Se si utilizzano le funzioni `lower_bound` e `upper_bound` fornite dalla libreria C++ STL, è possibile ottenere lo stesso risultato:

- `lower_bound(first, last, val)` restituisce "la prima posizione maggiore o uguale a val"
- `upper_bound(first, last, val)` restituisce "la prima posizione maggiore di val"

Ad esempio, supponiamo `nums = {1,2,3,4,4,4,4,4,5,5,6}`, e vogliamo sapere l'intervallo in cui compare 4:

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

- `it1` punta alla prima posizione con un valore maggiore o uguale a $4$.
- `it2` punta alla prima posizione con un valore maggiore di $4$.
  Pertanto, `it2 - it1` è il numero di volte in cui $4$ compare nell'array; `it2 - nums.begin() - 1` è il confine destro di $4$.

---

## Aggiunte

La ricerca binaria può essere estesa anche alla ricerca in intervalli di numeri in virgola mobile (come trovare la radice di un'equazione), e alla ricerca ternaria per trovare il massimo di una funzione unimodale.
Non appena si comprende il principio fondamentale " **in un intervallo ordinato, è possibile escludere sempre la metà**", si scoprirà che la ricerca binaria può aiutare a risolvere i problemi in modo efficiente in molti scenari.

---

## Esercizi

LeetCode 33. Search in Rotated Sorted Array

Suggerimento: al primo passaggio, utilizzare la ricerca binaria per trovare il punto di rotazione, al secondo passaggio utilizzare nuovamente la ricerca binaria per trovare il valore target.