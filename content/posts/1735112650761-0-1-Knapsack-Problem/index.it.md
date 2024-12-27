---
title: "Problema dello Zaino 0/1"
date: 2024-12-24
draft: false
description: "Il problema dello zaino classico più basilare."
summary: "Il problema dello zaino classico più basilare."
tags: [ "Algoritmo", "Programmazione Dinamica", "Problema dello Zaino" ]
categories: [ "Algoritmi e Strutture Dati" ]
---

## Problema

Ci sono $N$ oggetti. Il volume dell'oggetto $i$-esimo è $s_i$ e il suo valore è $v_i$.
Ogni oggetto può essere preso solo una volta. Con la premessa di non superare il limite massimo di volume totale $S$, trova il valore totale massimo $V$ che può essere ottenuto.

## Formato di Input

La prima riga contiene due interi, $N$ e $S$, separati da uno spazio, che rappresentano rispettivamente il numero di oggetti e il limite massimo di volume totale.
Le seguenti $N$ righe contengono ciascuna due interi, $s_i$ e $v_i$, separati da uno spazio, che rappresentano rispettivamente il volume e il valore dell'oggetto $i$-esimo.

## Formato di Output

Restituisci un intero che rappresenta il valore massimo.

## Intervallo di Dati

$$0 \le N, S \leq 1000$$

$$0 \le s_i, v_i \leq 1000$$

## Esempio di Input

```
4 5
1 2
2 4
3 4
4 5
```

## Esempio di Output

```
8
```

## Soluzione

- Definisci lo stato: `f[i][j]` rappresenta il valore massimo che può essere ottenuto dai primi $i$ oggetti con un limite di volume di $j$.
    - Se l'oggetto $i$-esimo non viene preso, allora `f[i][j] = f[i - 1][j]`
    - Se l'oggetto $i$-esimo viene preso, allora `f[i][j] = f[i - 1][j - s[i]] + v[i]`
    - Quando si implementa la transizione di stato, prestare attenzione all'intervallo del dominio. Se $j < s_i$, allora non considerare il caso di prendere l'oggetto $i$-esimo. Perché se $j - s_i$ è negativo, l'indice dell'array non è valido.
      Può anche essere spiegato in questo modo: il volume dell'oggetto $i$-esimo è maggiore del limite di volume, quindi è impossibile.
- Definisci la condizione iniziale: per i primi $0$ oggetti, qualsiasi limite di volume produce un valore di $0$, cioè `f[0][j] = 0`, `j` $\in [0, S]$.
- Complessità temporale: $O(NS)$.

## Codice

```cpp
#include<bits/stdc++.h>
using namespace std;
int main() {
    int N, S;
    cin >> N >> S;
    vector<int> s(N + 1), v(N + 1);
    for (int i = 1; i <= N; i++) cin >> s[i] >> v[i];
    vector<vector<int>> f(N + 1, vector<int>(S + 1));
    for (int i = 1; i <= N; i++) {
        for (int j = 0; j <= S; j++) {
            f[i][j] = f[i - 1][j];
            if (j >= s[i]) f[i][j] = max(f[i][j], f[i - 1][j - s[i]] + v[i]);
        }
    }
    cout << f[N][S] << endl;
    return 0;
}
```

## Ottimizzazione DP 1D

- La compressione dell'array bidimensionale in un array unidimensionale può far risparmiare significativamente spazio e migliorare in una certa misura la velocità di esecuzione (lo svantaggio è che non può soddisfare i requisiti speciali di alcuni tipi di problemi).
- Si noti che nella transizione di stato, `f[i][j]` è correlato solo a `f[i - 1][j]` e `f[i - 1][j - s[i]]`. In altre parole, nell'array bidimensionale `f` nel codice,
  `f[i][j]` è correlato solo agli elementi nella riga precedente che si trovano alla sua sinistra o nella stessa colonna. Pertanto, l'array bidimensionale può essere compresso in un array unidimensionale o in un array scorrevole.
- Si noti che nel codice seguente, il secondo ciclo itera in ordine inverso. Questo perché vogliamo assicurarci che quando si calcola `f[i][j]`, `f[i - 1][j - s[i]]` non sia ancora stato aggiornato.

```cpp
#include<bits/stdc++.h>
using namespace std;
int main() {
    int N, S;
    cin >> N >> S;
    vector<int> s(N + 1), v(N + 1);
    for (int i = 1; i <= N; i++) cin >> s[i] >> v[i];
    vector<int> f(S + 1);
    for (int i = 1; i <= N; i++) {
        for (int j = S; j >= s[i]; j--) {
            f[j] = max(f[j], f[j - s[i]] + v[i]);
        }
    }
    cout << f[S] << endl;
    return 0;
}
```

## Se è Richiesto il Numero di Schemi

Non solo dovrebbe essere restituito il valore totale massimo che può essere ottenuto, ma anche "quanti metodi di selezione diversi possono raggiungere questo valore totale massimo". Di seguito viene descritto **come contare il numero di schemi** nel problema dello zaino 0/1.

### DP 2D per Contare gli Schemi

Di seguito viene utilizzato il DP 2D come esempio per spiegare.

- Definisci lo stato:
  - `dp[i][j]` rappresenta "il valore massimo che può essere ottenuto quando si considerano i primi i oggetti con una capacità (limite di volume) di j".
  - `ways[i][j]` rappresenta "il **numero di schemi** corrispondenti al valore massimo ottenuto quando si considerano i primi i oggetti con una capacità di j".

- Transizione di stato:
  1. Se l'oggetto `i`-esimo non è selezionato:
     $$
       \text{dp}[i][j] = \text{dp}[i-1][j], 
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
     $$
  2. Se l'oggetto `i`-esimo è selezionato (a condizione che $ j \ge s_i $):
     $$
       \text{dp}[i][j] 
         = \text{dp}[i-1][j - s_i] + v_i,
       \quad
       \text{ways}[i][j]
         = \text{ways}[i-1][j - s_i]
     $$
  3. Che si selezioni o meno, il `dp[i][j]` finale dovrebbe prendere il maggiore dei due:
     - Se
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           > \text{dp}[i-1][j],
       $$
       allora significa che "selezionare l'oggetto i-esimo" ha un valore maggiore:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j - s_i] + v_i,
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j - s_i].
       $$
     - Se
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           = \text{dp}[i-1][j],
       $$
       significa che il valore massimo ottenuto dai due metodi è lo stesso, quindi il numero di schemi dovrebbe essere aggiunto:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j], 
         \quad
         \text{ways}[i][j] 
           = \text{ways}[i-1][j] 
             + \text{ways}[i-1][j - s_i].
       $$
     - Se
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           < \text{dp}[i-1][j],
       $$
       allora significa che "non selezionare l'oggetto i-esimo" ha un valore maggiore e il numero di schemi eredita il numero di schemi quando non si seleziona:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Condizioni iniziali:
  - `dp[0][j] = 0` significa che quando ci sono 0 oggetti, il valore massimo ottenuto per qualsiasi capacità è 0.
  - `ways[0][0] = 1` significa che il caso di "0 oggetti, capacità 0" è uno schema fattibile (cioè, non selezionare nulla) e il **numero di schemi** è impostato a 1.
  - Per `j > 0`, quando non ci sono oggetti tra cui scegliere e la capacità è maggiore di 0, è impossibile ottenere qualsiasi valore positivo e il numero di schemi corrispondente è 0, cioè `ways[0][j] = 0`.

- Risposta finale:
  - `dp[N][S]` è il valore massimo.
  - `ways[N][S]` è il numero di schemi per raggiungere questo valore massimo.
  - Complessità temporale: $O(NS)$.
  - Questo problema può anche essere ottimizzato usando il DP 1D.

## Se il Requisito è di Raggiungere Esattamente il Limite di Volume

- Definisci lo stato: `f[i][j]` rappresenta il valore massimo quando i primi `i` oggetti hanno esattamente un volume di $j$.
- Se l'oggetto `i`-esimo non viene preso, allora `f[i][j] = f[i - 1][j]`
- Se l'oggetto `i`-esimo viene preso, allora `f[i][j] = f[i - 1][j - s[i]] + v[i]`
- Si può notare che non c'è differenza nella transizione di stato rispetto al problema originale.
- Tuttavia, le condizioni iniziali sono diverse. Ad eccezione di `f[0][0] = 0`, il resto `f[0][j]` = $-\infty$, `j` $\in [1, S]$. $-\infty$ rappresenta uno stato impossibile.

## Se il Limite di Volume $S$ è Molto Grande (1e9), Mentre il Numero di Oggetti $N$ e il Valore Totale Massimo $V$ sono Relativamente Piccoli

- Per tali problemi, esiste una soluzione con una complessità di $O(NV)$.
- Definisci lo stato: `f[i][j]` rappresenta il volume minimo quando si selezionano diversi oggetti dai primi `i` oggetti e il valore totale è esattamente `j`.
    - Se l'oggetto `i`-esimo non viene preso, allora `f[i][j] = f[i - 1][j]`
    - Se l'oggetto `i`-esimo viene preso, allora `f[i][j] = f[i - 1][j - v[i]] + s[i]`
    - Prendi il minore dei due.
- Condizioni iniziali: `f[0][0] = 0`, il resto `f[0][j]` = $\infty$, `j` $\in [1, V]$. $\infty$ rappresenta uno stato impossibile. Si noti che non è $-\infty$.
- La risposta finale è il più grande `j` in `f[N][j]` tale che `f[N][j] <= S`.

## Se il Limite di Volume $S$ e il Valore di un Singolo Oggetto $v_i$ sono Entrambi Molto Grandi (dell'ordine di 1e9), Mentre il Numero di Oggetti $N$ è Molto Piccolo (non più di 40)

- Quando $N \leq 20$, tutti i sottoinsiemi possono essere enumerati direttamente con la forza bruta (complessità temporale $O(2^N)$).
- Quando $N \leq 40$, poiché $2^{40}$ è dell'ordine di $10^{12}$, anche la forza bruta diretta sarà relativamente grande, quindi la **ricerca meet-in-the-middle** può essere utilizzata per ridurre la complessità a circa $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$, che può essere completata in un tempo accettabile.