---
title: "Problema dello Zaino 0-1"
date: 2024-12-24
draft: false
description: "Il problema dello zaino classico più elementare."
summary: "Il problema dello zaino classico più elementare."
tags: [ "algoritmi", "programmazione dinamica", "problema dello zaino" ]
categories: [ "algoritmi e strutture dati" ]
series: [ "Lezioni sul problema dello zaino" ]
series_order: 1
---

## Problema

Ci sono $N$ oggetti. Il volume dell'oggetto $i$-esimo è $s_i$ e il suo valore è $v_i$.
Ogni oggetto può essere preso solo una volta. Con il vincolo che il volume totale non superi il limite massimo $S$, si trovi il massimo valore totale $V$ che si può ottenere.

## Formato di Input

La prima riga contiene due interi, $N$ e $S$, separati da uno spazio, che rappresentano rispettivamente il numero di oggetti e il limite massimo del volume totale.
Le successive $N$ righe contengono ciascuna due interi $s_i$ e $v_i$, separati da uno spazio, che rappresentano rispettivamente il volume e il valore dell'oggetto $i$-esimo.

## Formato di Output

Si stampi un intero, che rappresenta il valore massimo.

## Intervallo dei Dati

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

- Definizione dello stato: `f[i][j]` rappresenta il massimo valore ottenibile considerando i primi $i$ oggetti e con un limite di volume pari a $j$.
    - Se non si prende l'oggetto $i$-esimo, allora `f[i][j] = f[i - 1][j]`
    - Se si prende l'oggetto $i$-esimo, allora `f[i][j] = f[i - 1][j - s[i]] + v[i]`
    - Quando si implementa la transizione di stato, bisogna fare attenzione al dominio. Se $j < s_i$, allora non si considera il caso in cui si prende l'oggetto $i$-esimo, perché se $j - s_i$ fosse negativo, l'indice dell'array non sarebbe valido.
      Si può anche spiegare così: il volume dell'oggetto $i$-esimo è maggiore del limite di volume, quindi è impossibile prenderlo.
- Condizioni iniziali: Con 0 oggetti, qualsiasi limite di volume porta a un valore 0, cioè `f[0][j] = 0`, `j` $\in [0, S]$.
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

- Comprimere l'array bidimensionale in un array unidimensionale può far risparmiare significativamente spazio e migliorare la velocità di esecuzione (lo svantaggio è che non soddisfa i requisiti speciali di alcuni tipi di problemi)
- Si noti che nella transizione di stato `f[i][j]` dipende solo da `f[i - 1][j]` e `f[i - 1][j - s[i]]`. In altre parole, nell'array bidimensionale `f` nel codice,
  `f[i][j]` dipende solo dagli elementi della riga precedente che si trovano alla sua sinistra o sulla stessa colonna, quindi è possibile comprimere l'array bidimensionale in un array unidimensionale o in un array "rolling".
- Si noti che nel codice seguente, il secondo ciclo esegue l'iterazione in ordine inverso, questo perché dobbiamo assicurarci che quando calcoliamo `f[i][j]`, `f[i - 1][j - s[i]]` non sia ancora stato aggiornato.

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

Non solo è necessario restituire il massimo valore totale ottenibile, ma anche "quante sono le diverse modalità di selezione per raggiungere questo massimo valore totale". Di seguito si spiega **come contare il numero di soluzioni** nel problema dello zaino 0-1.

### Conteggio delle soluzioni con DP bidimensionale

Di seguito si fornisce una spiegazione utilizzando un DP bidimensionale come esempio.

- Definizione dello stato:
  - `dp[i][j]` rappresenta "il valore massimo ottenibile considerando i primi i oggetti, con una capacità (limite di volume) pari a j".
  - `ways[i][j]` rappresenta "il **numero di soluzioni** per ottenere il valore massimo quando si considerano i primi i oggetti, con una capacità pari a j".

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
  3. Selezionando o non selezionando, alla fine `dp[i][j]` deve prendere il valore più grande tra i due:
     - Se
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           > \text{dp}[i-1][j],
       $$
       allora significa che il valore di "selezionare l'oggetto i-esimo" è più grande:
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
       allora significa che il valore massimo ottenuto in entrambi i modi è uguale, quindi il numero di soluzioni dovrebbe essere cumulato:
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
       allora significa che il valore di "non selezionare l'oggetto i-esimo" è più grande, e il numero di soluzioni eredita quello di non selezionare:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Condizioni iniziali:
  - `dp[0][j] = 0` significa che quando ci sono 0 oggetti, il massimo valore ottenuto per qualsiasi capacità è 0.
  - `ways[0][0] = 1` significa che la situazione in cui "ci sono 0 oggetti, capacità 0" è una soluzione fattibile (cioè, non si seleziona niente) e il **numero di soluzioni** è impostato a 1.
  - Per `j > 0`, quando non ci sono oggetti selezionabili ma la capacità è maggiore di 0, è impossibile ottenere qualsiasi valore positivo, quindi il numero di soluzioni corrispondente è 0, cioè `ways[0][j] = 0`.

- Risposta finale:
  - `dp[N][S]` è il massimo valore.
  - `ways[N][S]` è il numero di soluzioni per raggiungere questo massimo valore.
  - Complessità temporale: $O(NS)$.
  - Questo problema può anche essere ottimizzato usando DP unidimensionale.

## Se si Richiede di Raggiungere Esattamente il Limite di Volume

- Definizione dello stato: `f[i][j]` rappresenta il valore massimo quando i primi `i` oggetti hanno esattamente un volume $j$.
- Se non si seleziona l'oggetto `i`-esimo, allora `f[i][j] = f[i - 1][j]`
- Se si seleziona l'oggetto `i`-esimo, allora `f[i][j] = f[i - 1][j - s[i]] + v[i]`
- Si può notare che la transizione di stato non è diversa dal problema originale.
- Ma le condizioni iniziali sono diverse. Oltre a `f[0][0] = 0`, tutti gli altri `f[0][j]` = $-\infty$, `j` $\in [1, S]$. $-\infty$ indica uno stato impossibile.

## Se il Limite di Volume $S$ è Particolarmente Grande (1e9), mentre il Numero di Oggetti $N$ e il Valore Totale Massimo $V$ sono Relativamente Piccoli

- Per questo tipo di problema, esiste una soluzione con complessità $O(NV)$.
- Definizione dello stato: `f[i][j]` rappresenta il volume minimo per selezionare un certo numero di oggetti tra i primi `i` con una somma di valori pari esattamente a `j`.
    - Se non si prende l'oggetto `i`-esimo, allora `f[i][j] = f[i - 1][j]`
    - Se si prende l'oggetto `i`-esimo, allora `f[i][j] = f[i - 1][j - v[i]] + s[i]`
    - Si prende il valore più piccolo tra i due.
- Condizioni iniziali: `f[0][0] = 0`, tutti gli altri `f[0][j]` = $\infty$, `j` $\in [1, V]$. $\infty$ indica uno stato impossibile. Si noti che non è $-\infty$.
- La risposta finale è il `j` più grande tra `f[N][j]` tale che `f[N][j] <= S`.

## Se il Limite di Volume $S$ e il Valore del Singolo Oggetto $v_i$ Sono Entrambi Molto Grandi (nell'ordine di 1e9), mentre il Numero di Oggetti $N$ è Molto Piccolo (al Massimo 40)

- Quando $N \leq 20$, è possibile enumerare direttamente tutti i sottoinsiemi (complessità temporale $O(2^N)$).
- Quando $N \leq 40$, dato che $2^{40}$ è nell'ordine di $10^{12}$, la forza bruta diretta sarà ancora piuttosto grande, quindi è possibile utilizzare la **ricerca a metà**
  , riducendo approssimativamente la complessità a $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$
  , che può essere completata in un tempo accettabile.