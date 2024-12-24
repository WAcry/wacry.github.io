---
title: "Ricerca Binaria"
date: 2024-12-24
draft: false
description: "Come implementare elegantemente l'algoritmo di ricerca binaria sugli interi"
tags: [ "Algoritmo", "Ricerca Binaria", "Template Algoritmo" ]
categories: [ "Algoritmi e Strutture Dati" ]
---
{{< katex >}}

# Ricerca Binaria

La ricerca binaria può essere utilizzata per trovare rapidamente un elemento specifico in una sequenza ordinata. Rispetto alla ricerca lineare con una complessità temporale di $O(n)$, la ricerca binaria richiede solo $O(\log n)$ tempo, il che la rende molto efficiente quando si ha a che fare con grandi insiemi di dati.

## L'Idea Centrale della Ricerca Binaria

L'idea di base della ricerca binaria è quella di dimezzare ripetutamente l'intervallo di ricerca. Ogni volta, l'elemento centrale viene confrontato con il valore di destinazione. Se l'elemento centrale non soddisfa la condizione, metà dell'intervallo può essere eliminata; altrimenti, la ricerca continua nell'altra metà dell'intervallo. Poiché metà dell'intervallo di ricerca viene scartata ogni volta, la complessità temporale della ricerca può raggiungere $O(\log n)$.

La ricerca binaria è molto utile per i problemi in cui "**le soluzioni possibili possono essere suddivise in un intervallo ordinato (che soddisfa la condizione) e un altro intervallo ordinato (che non soddisfa la condizione)**". Per esempio:

- Trovare se un elemento esiste in un array ordinato
- Trovare la "prima posizione" o "l'ultima posizione" in cui appare un numero

## Esempio: Trovare le Posizioni Iniziale e Finale di un Elemento

**Descrizione del Problema:**
Dato un array di interi ordinato in modo crescente di lunghezza $n$, e $q$ query. Ogni query fornisce un intero $k$, e dobbiamo trovare la "posizione iniziale" e "la posizione finale" di $k$ nell'array (indici che partono da 0). Se il numero non esiste nell'array, restituisci $-1$ $-1$.

**Formato di Input:**

1. La prima riga: due interi $n$ e $q$, che rappresentano la lunghezza dell'array e il numero di query, rispettivamente.
2. La seconda riga: $n$ interi (compresi tra 1 e 10000), che rappresentano l'intero array, già ordinato in ordine crescente.
3. Le seguenti $q$ righe: ogni riga contiene un intero $k$, che rappresenta un elemento di query.

**Formato di Output:**
Per ogni query, stampa le posizioni iniziale e finale dell'elemento nell'array su una singola riga. Se l'elemento non esiste nell'array, stampa $-1$ $-1$.

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

Spiegazione:

- L'intervallo in cui appare l'elemento 3 è `[3, 4]`;
- L'elemento 4 appare solo una volta, alla posizione 5;
- L'elemento 5 non esiste nell'array, quindi restituisci `-1 -1`.

## L'Approccio di Applicazione della Ricerca Binaria

In questo problema, possiamo fare affidamento sulla ricerca binaria per trovare il "limite sinistro" e il "limite destro" di un certo valore. La chiave è capire come definire l'intervallo di ricerca e come spostare i puntatori in base al risultato del confronto.

- **Trovare il "limite sinistro":**
  Cioè, trovare la prima posizione che è maggiore o uguale a $k$. L'array può essere diviso in due parti:
    - Tutti i numeri a sinistra sono "minori di" $k$
    - Tutti i numeri a destra sono "maggiori o uguali a" $k$

- **Trovare il "limite destro":**
  Cioè, trovare l'ultima posizione che è minore o uguale a $k$. L'array può essere diviso in due parti:
    - Tutti i numeri a sinistra sono "minori o uguali a" $k$
    - Tutti i numeri a destra sono "maggiori di" $k$

Finché questi due intervalli possono essere mantenuti correttamente, il risultato può essere ottenuto rapidamente attraverso la ricerca binaria.

## Template Raccomandato: Codice di Ricerca Binaria per Evitare Cicli Infiniti

Ecco un template di ricerca binaria elegante e resistente agli errori. Assicura che il ciclo termini quando $l$ e $r$ sono adiacenti avvicinando gradualmente $l$ e $r$:

Definisci due puntatori $l, r$, con gli invarianti: l'intervallo chiuso $[0, l]$ appartiene tutto alla parte sinistra, l'intervallo chiuso $[r, n - 1]$ appartiene tutto alla parte destra. $l$ e $r$ sono inizializzati rispettivamente a $-1$ e $n$.

Quando l'algoritmo termina, $l$ e $r$ sono adiacenti, puntando rispettivamente al valore massimo nella parte sinistra e al valore minimo nella parte destra.

Poiché la soluzione desiderata potrebbe non esistere, quando si restituisce $l$ o $r$, è necessario verificare se il valore corrispondente è il valore che vogliamo e se è fuori dai limiti.
Ad esempio, $l$ rappresenta il valore massimo $\leq k$, e dobbiamo controllare `l != -1 && nums[l] == k`

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

        // 1. Trova la posizione iniziale di k (limite sinistro)
        //    Dividi l'array in due parti, la parte sinistra tutta < k, e la parte destra tutta >= k.
        //    Il limite sinistro è l'indice più piccolo della parte destra.
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

        int leftPos = r; // Registra il limite sinistro di k

        // 2. Trova la posizione finale di k (limite destro)
        //    Dividi l'array in due parti, la parte sinistra tutta <= k, e la parte destra tutta > k.
        //    Il limite destro è l'indice più grande della parte sinistra.
        l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] <= k) l = mid;
            else r = mid;
        }

        // Dato che abbiamo già verificato che k esiste, non è necessario verificare di nuovo qui
        int rightPos = l; // Limite destro
        cout << leftPos << " " << rightPos << endl;
    }
    return 0;
}
```

### Perché questo metodo è meno soggetto a errori?

1. Questo metodo ha invarianti strettamente definiti.
2. Può trovare sia il limite sinistro che quello destro, rendendolo applicabile a tutti gli scenari.
3. Alcuni metodi usano $l == r$ come condizione di terminazione. Quando $l$ e $r$ differiscono di 1, il $mid$ calcolato sarà uguale a `l` o `r`. Se non gestito correttamente, l'aggiornamento
   di `l` o `r` a `mid` non restringerà l'intervallo di ricerca, portando a un ciclo infinito. Al contrario, questo metodo termina quando $l$ e $r$ sono adiacenti, evitando questo problema.

## Soluzione STL: `lower_bound` e `upper_bound`

Se usi le funzioni `lower_bound` e `upper_bound` fornite dalla STL di C++, puoi facilmente ottenere lo stesso risultato:

- `lower_bound(first, last, val)` restituisce "la prima posizione maggiore o uguale a val"
- `upper_bound(first, last, val)` restituisce "la prima posizione maggiore di val"

Ad esempio, supponiamo che `nums = {1,2,3,4,4,4,4,4,5,5,6}`, e vogliamo conoscere l'intervallo in cui appare 4:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    // Indica che 4 non esiste nell'array
    cout << "4 appare 0 volte" << endl;
} else {
    cout << "il primo 4 è in posizione " << it1 - nums.begin() << endl;
    cout << "l'ultimo 4 è in posizione " << it2 - nums.begin() - 1 << endl;
    cout << "4 appare " << it2 - it1 << " volte" << endl;
}
```

- `it1` punta alla prima posizione in cui il valore è maggiore o uguale a 4.
- `it2` punta alla prima posizione in cui il valore è maggiore di 4.
  Pertanto, `it2 - it1` è il numero di volte in cui 4 appare nell'array; `it2 - nums.begin() - 1` è il limite destro di 4.

Queste due funzioni sono particolarmente utili quando si cercano intervalli o si contano le occorrenze.

## Supplemento

La ricerca binaria può anche essere estesa per la ricerca all'interno di numeri in virgola mobile (ad es. trovare le radici di un'equazione), così come la ricerca ternaria per trovare i valori estremi di funzioni unimodali. Finché capisci il principio fondamentale di "**eliminare metà in un intervallo ordinato ogni volta**", scoprirai che la ricerca binaria può aiutarti a risolvere i problemi in modo efficiente in molti scenari.

## Esercizio

LeetCode 33. Search in Rotated Sorted Array

Suggerimento: usa la ricerca binaria per trovare prima il punto di rotazione, e poi usa la ricerca binaria per trovare il valore di destinazione.