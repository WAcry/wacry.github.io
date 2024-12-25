---
title: "01-Rucksackproblem"
date: 2024-12-24
draft: false
description: "Das grundlegendste klassische Rucksackproblem."
summary: "Das grundlegendste klassische Rucksackproblem."
tags: [ "Algorithmus", "Dynamische Programmierung", "Rucksackproblem" ]
categories: [ "Algorithmen und Datenstrukturen" ]
series: [ "Neun Vorlesungen zum Rucksackproblem" ]
---

## Aufgabe

Es gibt $N$ Gegenstände. Der Platzbedarf des $i$-ten Gegenstands ist $s_i$, sein Wert ist $v_i$.
Jeder Gegenstand kann nur einmal mitgenommen werden. Ermittle den maximalen Gesamtwert $V$, der erzielt werden kann, ohne die maximale Gesamtvolumenbeschränkung $S$ zu überschreiten.

## Eingabeformat

Die erste Zeile enthält zwei durch Leerzeichen getrennte ganze Zahlen $N$ und $S$, die die Anzahl der Gegenstände und die maximale Gesamtvolumenbeschränkung darstellen.
Die nächsten $N$ Zeilen enthalten jeweils zwei durch Leerzeichen getrennte ganze Zahlen $s_i$ und $v_i$, die den Platzbedarf und den Wert des $i$-ten Gegenstands darstellen.

## Ausgabeformat

Gib eine ganze Zahl aus, die den maximalen Wert darstellt.

## Datenbereich

$$0 \le N, S \leq 1000$$

$$0 \le s_i, v_i \leq 1000$$

## Eingabebeispiel

```
4 5
1 2
2 4
3 4
4 5
```

## Ausgabebeispiel

```
8
```

## Lösungsansatz

- Definiere den Zustand: `f[i][j]` stellt den maximalen Wert dar, der mit den ersten $i$ Gegenständen bei einer Volumenbeschränkung von $j$ erzielt werden kann.
    - Wenn der $i$-te Gegenstand nicht genommen wird, dann ist `f[i][j] = f[i - 1][j]`.
    - Wenn der $i$-te Gegenstand genommen wird, dann ist `f[i][j] = f[i - 1][j - s[i]] + v[i]`.
    - Bei der Implementierung des Zustandsübergangs ist auf den Definitionsbereich zu achten. Wenn $j < s_i$, dann kommt die Mitnahme des $i$-ten Gegenstands nicht in Frage, da der Array-Index ungültig wird, wenn $j-s_i$ negativ ist.
      Man kann es auch so erklären: Das Volumen des $i$-ten Gegenstands ist größer als die Volumenbeschränkung, daher ist es nicht möglich.
- Definiere die Anfangsbedingungen: Mit den ersten 0 Gegenständen ist der erzielte Wert bei jeder Volumenbeschränkung 0, d.h. `f[0][j] = 0`, `j` $\in [0, S]$.
- Zeitkomplexität: $O(NS)$.

## Code

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

## Optimierung mit 1D-DP

- Durch Komprimierung des zweidimensionalen Arrays zu einem eindimensionalen Array kann der Speicherverbrauch erheblich reduziert und die Laufzeit leicht erhöht werden (Nachteil ist, dass spezielle Anforderungen bestimmter Aufgabentypen nicht erfüllt werden können)
- Es ist zu beachten, dass im Zustandsübergang `f[i][j]` nur mit `f[i - 1][j]` und `f[i - 1][j - s[i]]` zusammenhängt. Mit anderen Worten, im zweidimensionalen Array `f` im Code hängt `f[i][j]` nur mit Elementen in seiner vorherigen Zeile zusammen, die weiter links oder in derselben Spalte liegen, daher kann das zweidimensionale Array zu einem eindimensionalen Array oder einem Rolling Array komprimiert werden.
- Beachte, dass in dem folgenden Code die zweite Schleife in umgekehrter Reihenfolge iteriert, da wir sicherstellen müssen, dass beim Berechnen von `f[i][j]` `f[i - 1][j - s[i]]` noch nicht aktualisiert wurde.

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

## Wenn die Anzahl der Lösungen erforderlich ist

Neben der Ausgabe des maximalen Gesamtwerts, der erzielt werden kann, muss auch ausgegeben werden, "wie viele verschiedene Auswahlmöglichkeiten es gibt, um diesen maximalen Gesamtwert zu erreichen". Im Folgenden wird erläutert, wie die Anzahl der Lösungen im 01-Rucksackproblem **statistisch erfasst wird**.

### Statistische Erfassung von Lösungen mit 2D-DP

Im Folgenden wird dies anhand von 2D-DP erläutert.

- Definiere den Zustand:
  - `dp[i][j]` stellt den „maximalen Wert dar, der erzielt werden kann, wenn die ersten i Elemente verwendet werden und die Kapazität (Volumenbegrenzung) j beträgt“.
  - `ways[i][j]` stellt die „Anzahl der **Lösungen** dar, die den maximalen Wert ergeben, wenn die ersten i Elemente verwendet werden und die Kapazität j beträgt“.

- Zustandsübergang:
  1. Wenn das i-te Element nicht ausgewählt wird:
     $$
       \text{dp}[i][j] = \text{dp}[i-1][j], 
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
     $$
  2. Wenn das i-te Element ausgewählt wird (vorausgesetzt, dass $ j \ge s_i $):
     $$
       \text{dp}[i][j] 
         = \text{dp}[i-1][j - s_i] + v_i,
       \quad
       \text{ways}[i][j]
         = \text{ways}[i-1][j - s_i]
     $$
  3. Ob ausgewählt oder nicht, am Ende sollte `dp[i][j]` den größeren der beiden Werte annehmen:
     - Wenn
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           > \text{dp}[i-1][j],
       $$
       bedeutet dies, dass der Wert des "Auswählens des i-ten Elements" größer ist:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j - s_i] + v_i,
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j - s_i].
       $$
     - Wenn
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           = \text{dp}[i-1][j],
       $$
       bedeutet dies, dass die beiden Methoden denselben Maximalwert ergeben, und die Anzahl der Lösungen sollte addiert werden:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j], 
         \quad
         \text{ways}[i][j] 
           = \text{ways}[i-1][j] 
             + \text{ways}[i-1][j - s_i].
       $$
     - Wenn
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           < \text{dp}[i-1][j],
       $$
       bedeutet dies, dass der Wert des "Nichtauswählens des i-ten Elements" größer ist, und die Anzahl der Lösungen erbt die Anzahl der Lösungen des Nichtauswählens:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Anfangsbedingungen:
  - `dp[0][j] = 0` bedeutet, dass der maximale Wert, der mit den ersten 0 Elementen bei jeder Kapazität erzielt werden kann, 0 ist.  
  - `ways[0][0] = 1` bedeutet, dass die Situation "die ersten 0 Elemente, Kapazität 0" eine mögliche Lösung ist (d.h. nichts wird ausgewählt), und die **Anzahl der Lösungen** wird auf 1 gesetzt.  
  - Für `j > 0` ist es nicht möglich, einen positiven Wert zu erzielen, wenn keine Elemente ausgewählt werden können und die Kapazität größer als 0 ist, daher ist die entsprechende Anzahl der Lösungen 0, d.h. `ways[0][j] = 0`.

- Endgültige Lösung:  
  - `dp[N][S]` ist der Maximalwert.  
  - `ways[N][S]` ist die Anzahl der Lösungen, die diesen Maximalwert erreichen.
  - Zeitkomplexität: $O(NS)$.
  - Dieses Problem kann auch mit einer 1D-DP optimiert werden.

## Wenn die Situation erforderlich ist, dass die Volumengrenze genau erreicht wird

- Definiere den Zustand: `f[i][j]` stellt den maximalen Wert dar, bei dem die ersten `i` Elemente genau das Volumen $j$ haben.
- Wenn das `i`-te Element nicht mitgenommen wird, ist `f[i][j] = f[i - 1][j]`.
- Wenn das `i`-te Element mitgenommen wird, ist `f[i][j] = f[i - 1][j - s[i]] + v[i]`.
- Es ist zu beachten, dass es keinen Unterschied zum Zustandsübergang des ursprünglichen Problems gibt.
- Die Anfangsbedingungen sind jedoch unterschiedlich. Außer `f[0][0] = 0` ist der Rest `f[0][j]` = $-\infty$, `j` $\in [1, S]$. $-\infty$ stellt einen unmöglichen Zustand dar.

## Wenn die Volumenbeschränkung $S$ besonders groß (1e9) ist, gleichzeitig die Anzahl der Elemente $N$ und der maximale Gesamtwert $V$ relativ klein sind

- Für ein solches Problem gibt es eine Lösung mit einer Komplexität von $O(NV)$.
- Definiere den Zustand: `f[i][j]` stellt das minimale Volumen dar, bei dem einige der ersten `i` Elemente ausgewählt werden und die Summe der Werte genau `j` ist.
    - Wenn das `i`-te Element nicht mitgenommen wird, ist `f[i][j] = f[i - 1][j]`.
    - Wenn das `i`-te Element mitgenommen wird, ist `f[i][j] = f[i - 1][j - v[i]] + s[i]`.
    - Nimm den kleineren der beiden Werte.
- Anfangsbedingung: `f[0][0] = 0`, der Rest `f[0][j]` = $\infty$, `j` $\in [1, V]$. $\infty$ stellt einen unmöglichen Zustand dar. Beachte, dass es nicht $-\infty$ ist.
- Die endgültige Lösung ist das größte `j` in `f[N][j]` mit `f[N][j] <= S`.

## Wenn die Volumenbeschränkung $S$ und der Wert eines einzelnen Elements $v_i$ besonders groß sind (in der Größenordnung von 1e9), während die Anzahl der Elemente $N$ besonders klein ist (maximal 40)

- Wenn $N \leq 20$ ist, können alle Teilmengen direkt aufgezählt werden (Zeitkomplexität $O(2^N)$).
- Wenn $N \leq 40$ ist, ist $2^{40}$ in der Größenordnung von $10^{12}$, so dass eine direkte Brute-Force-Methode auch relativ groß wäre, daher kann **Split-Half-Search** verwendet werden, um die Komplexität grob auf $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$ zu reduzieren. Dies kann in einer akzeptablen Zeit abgeschlossen werden.