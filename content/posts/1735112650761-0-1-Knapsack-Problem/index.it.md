---
title: "Problema dello Zaino 0/1"
date: 2024-12-24
draft: false
description: "Il problema dello zaino classico più basilare."
summary: "Il problema dello zaino classico più basilare."
tags: [ "algoritmi", "programmazione dinamica", "problema dello zaino" ]
categories: [ "Algoritmi e Strutture Dati" ]
series: [ "Le Nove Lezioni sullo Zaino" ]
series_order: 1
---

## Problema

C'è un numero $N$ di oggetti. L'oggetto $i$-esimo ha volume $s_i$ e valore $v_i$.
Ogni oggetto può essere preso solo una volta. Trovare il valore totale massimo $V$ che si può ottenere senza superare il limite di volume totale massimo $S$.

## Formato di Input

La prima riga contiene due interi, $N$ e $S$, separati da uno spazio, che rappresentano rispettivamente il numero di oggetti e il limite di volume totale massimo.
Le successive $N$ righe contengono due interi, $s_i$ e $v_i$, separati da uno spazio, che rappresentano rispettivamente il volume e il valore dell'oggetto $i$-esimo.

## Formato di Output

Restituisci un intero, che rappresenta il valore massimo.

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

- Definizione dello stato: `f[i][j]` rappresenta il valore massimo che si può ottenere considerando i primi $i$ oggetti, con un limite di volume di $j$.
    - Se non prendiamo l'oggetto $i$-esimo, allora `f[i][j] = f[i - 1][j]`
    - Se prendiamo l'oggetto $i$-esimo, allora `f[i][j] = f[i - 1][j - s[i]] + v[i]`
    - Quando si implementa la transizione di stato, bisogna prestare attenzione all'intervallo del dominio. Se $j < s_i$, allora non si considera il caso in cui si prende l'oggetto $i$-esimo. Questo perché se $j-s_i$ fosse un numero negativo, l'indice dell'array non sarebbe valido.
      Si può anche spiegare così: il volume dell'oggetto $i$-esimo è maggiore del limite di volume, quindi è impossibile prenderlo.
- Definizione delle condizioni iniziali: considerando i primi $0$ oggetti, si ottiene un valore di $0$ per qualsiasi limite di volume, cioè `f[0][j] = 0`, `j` $\in [0, S]$.
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

## Ottimizzazione DP a una Dimensione

- Comprimendo l'array bidimensionale in un array unidimensionale, si può risparmiare significativamente spazio e aumentare in una certa misura la velocità di esecuzione (lo svantaggio è che non si possono soddisfare i requisiti speciali di alcuni tipi di problemi)
- Si noti che nella transizione di stato, `f[i][j]` è correlato solo a `f[i - 1][j]` e `f[i - 1][j - s[i]]`. In altre parole, nell'array bidimensionale `f` nel codice,
  `f[i][j]` è correlato solo agli elementi della riga precedente che si trovano più a sinistra o nella stessa colonna, quindi l'array bidimensionale può essere compresso in un array unidimensionale o in un array scorrevole.
- Si noti che nel codice seguente, il secondo ciclo itera in ordine inverso, questo perché dobbiamo assicurarci che quando calcoliamo `f[i][j]`, `f[i - 1][j - s[i]]` non sia ancora stato aggiornato.

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

## Se si Richiede il Numero di Soluzioni

Non solo si deve restituire il valore totale massimo che si può ottenere, ma anche "quanti modi diversi ci sono per selezionare gli oggetti per raggiungere questo valore totale massimo". Di seguito viene introdotto **come contare il numero di soluzioni** nel problema dello zaino 0/1.

### Conteggio delle Soluzioni con DP Bidimensionale

Di seguito viene spiegato l'esempio con DP bidimensionale.

- Definizione dello stato:
  - `dp[i][j]` rappresenta "il valore massimo che si può ottenere considerando i primi i oggetti, con una capacità (limite di volume) di j".
  - `ways[i][j]` rappresenta "il **numero di soluzioni** corrispondenti al valore massimo ottenuto considerando i primi i oggetti, con una capacità di j".

- Transizione di stato:
  1. Se non si seleziona l'oggetto `i`-esimo:
     $$
       \text{dp}[i][j] = \text{dp}[i-1][j], 
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
     $$
  2. Se si seleziona l'oggetto `i`-esimo (a condizione che $ j \ge s_i $):
     $$
       \text{dp}[i][j] 
         = \text{dp}[i-1][j - s_i] + v_i,
       \quad
       \text{ways}[i][j]
         = \text{ways}[i-1][j - s_i]
     $$
  3. Selezionando o non selezionando, alla fine `dp[i][j]` dovrebbe prendere il valore maggiore tra i due:
     - Se
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           > \text{dp}[i-1][j],
       $$
       allora significa che il valore di "selezionare l'oggetto i-esimo" è maggiore:
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
       significa che il valore massimo ottenuto in entrambi i modi è lo stesso, quindi il numero di soluzioni dovrebbe essere sommato:
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
       allora significa che il valore di "non selezionare l'oggetto i-esimo" è maggiore, e il numero di soluzioni eredita il numero di soluzioni quando non si seleziona:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Condizioni iniziali:
  - `dp[0][j] = 0` significa che quando ci sono 0 oggetti, il valore massimo ottenuto per qualsiasi capacità è 0.
  - `ways[0][0] = 1` significa che "0 oggetti, capacità 0" è una soluzione fattibile (cioè non selezionare nulla), e il **numero di soluzioni** è impostato a 1.
  - Per `j > 0`, quando non ci sono oggetti tra cui scegliere e la capacità è maggiore di 0, è impossibile ottenere qualsiasi valore positivo, e il numero di soluzioni corrispondente è 0, cioè `ways[0][j] = 0`.

- Risposta finale:
  - `dp[N][S]` è il valore massimo.
  - `ways[N][S]` è il numero di soluzioni per raggiungere questo valore massimo.
  - Complessità temporale: $O(NS)$.
  - Questo problema può anche essere ottimizzato utilizzando DP unidimensionale.

## Se si Richiede di Raggiungere Esattamente il Limite di Volume

- Definizione dello stato: `f[i][j]` rappresenta il valore massimo quando i primi `i` oggetti hanno esattamente un volume di $j$.
- Se non si prende l'oggetto `i`-esimo, allora `f[i][j] = f[i - 1][j]`
- Se si prende l'oggetto `i`-esimo, allora `f[i][j] = f[i - 1][j - s[i]] + v[i]`
- Si può notare che non c'è differenza nella transizione di stato rispetto al problema originale.
- Tuttavia, le condizioni iniziali sono diverse. Oltre a `f[0][0] = 0`, il resto di `f[0][j]` = $-\infty$, `j` $\in [1, S]$. $-\infty$ rappresenta uno stato impossibile.

## Se il Limite di Volume $S$ è Molto Grande (1e9), mentre il Numero di Oggetti $N$ e il Valore Totale Massimo $V$ sono Relativamente Piccoli

- Per questo tipo di problema, esiste una soluzione con una complessità di $O(NV)$.
- Definizione dello stato: `f[i][j]` rappresenta il volume minimo quando si selezionano alcuni dei primi `i` oggetti, e la somma dei valori è esattamente `j`.
    - Se non si prende l'oggetto `i`-esimo, allora `f[i][j] = f[i - 1][j]`
    - Se si prende l'oggetto `i`-esimo, allora `f[i][j] = f[i - 1][j - v[i]] + s[i]`
    - Si prende il valore minore tra i due.
- Condizioni iniziali: `f[0][0] = 0`, il resto di `f[0][j]` = $\infty$, `j` $\in [1, V]$. $\infty$ rappresenta uno stato impossibile. Si noti che non è $-\infty$.
- La risposta finale è il massimo `j` in `f[N][j]` tale che `f[N][j] <= S`.

## Se il Limite di Volume $S$ e il Valore del Singolo Oggetto $v_i$ sono Entrambi Molto Grandi (nell'ordine di 1e9), mentre il Numero di Oggetti $N$ è Molto Piccolo (non più di 40)

- Quando $N \leq 20$, si possono enumerare direttamente tutti i sottoinsiemi (complessità temporale $O(2^N)$).
- Quando $N \leq 40$, poiché $2^{40}$ è nell'ordine di $10^{12}$, l'enumerazione diretta sarebbe ancora troppo grande, quindi si può usare la **ricerca a metà**
  , che riduce approssimativamente la complessità a $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$
  , che può essere completata in un tempo accettabile.