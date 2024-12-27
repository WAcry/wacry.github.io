---
title: "01背包problem"
date: 2024-12-24
draft: false
description: "Das grundlegendste klassische Rucksackproblem."
summary: "Das grundlegendste klassische Rucksackproblem."
tags: [ "Algorithmus", "Dynamische Programmierung", "Rucksackproblem" ]
categories: [ "Algorithmen und Datenstrukturen" ]
series: [ "Neun Lektionen zum Rucksackproblem" ]
series_order: 1
---

## Aufgabe

Es gibt $N$ Gegenstände. Das Volumen des $i$-ten Gegenstands ist $s_i$, der Wert ist $v_i$.
Jeder Gegenstand kann nur einmal genommen werden. Unter der Voraussetzung, dass das maximale Gesamtvolumen $S$ nicht überschritten wird, finde den maximalen Gesamtwert $V$, der erreicht werden kann.

## Eingabeformat

Die erste Zeile enthält zwei ganze Zahlen, $N, S$, getrennt durch ein Leerzeichen, die die Anzahl der Gegenstände bzw. die maximale Gesamtvolumenbegrenzung angeben.
Die nächsten $N$ Zeilen enthalten jeweils zwei ganze Zahlen $s_i, v_i$, getrennt durch ein Leerzeichen, die das Volumen bzw. den Wert des $i$-ten Gegenstands angeben.

## Ausgabeformat

Geben Sie eine ganze Zahl aus, die den maximalen Wert darstellt.

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

- Definition des Zustands: `f[i][j]` stellt den maximalen Wert dar, der mit den ersten $i$ Gegenständen und einer Volumenbegrenzung von $j$ erzielt werden kann.
    - Wenn der $i$-te Gegenstand nicht genommen wird, dann `f[i][j] = f[i - 1][j]`
    - Wenn der $i$-te Gegenstand genommen wird, dann `f[i][j] = f[i - 1][j - s[i]] + v[i]`
    - Bei der Implementierung des Zustandsübergangs ist auf den Definitionsbereich zu achten. Wenn $j < s_i$, dann wird der Fall, dass der $i$-te Gegenstand genommen wird, nicht berücksichtigt. Denn wenn $j-s_i$ negativ ist, ist der Array-Index ungültig.
      Man kann es auch so erklären: Das Volumen des $i$-ten Gegenstands ist größer als die Volumenbegrenzung, daher ist es unmöglich.
- Definition der Anfangsbedingungen: Mit den ersten $0$ Gegenständen wird bei jeder Volumenbegrenzung ein Wert von $0$ erzielt, d.h. `f[0][j] = 0`, `j` $\in [0, S]$.
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

## 1D-DP-Optimierung

- Durch das Komprimieren des zweidimensionalen Arrays in ein eindimensionales Array kann erheblich Speicherplatz gespart und die Laufgeschwindigkeit bis zu einem gewissen Grad erhöht werden (der Nachteil ist, dass bestimmte spezielle Anforderungen von Aufgabentypen nicht erfüllt werden können).
- Es ist zu beachten, dass im Zustandsübergang `f[i][j]` nur von `f[i - 1][j]` und `f[i - 1][j - s[i]]` abhängt. Mit anderen Worten, im zweidimensionalen Array `f` im Code hängt `f[i][j]` nur von den Elementen in der vorherigen Zeile ab, die sich weiter links oder in derselben Spalte befinden. Daher kann das zweidimensionale Array in ein eindimensionales Array oder ein Rolling Array komprimiert werden.
- Beachten Sie, dass in dem folgenden Code die zweite Schleife in umgekehrter Reihenfolge durchlaufen wird, da wir sicherstellen müssen, dass `f[i - 1][j - s[i]]` noch nicht aktualisiert wurde, wenn `f[i][j]` berechnet wird.

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

Es soll nicht nur der maximal erreichbare Gesamtwert ausgegeben werden, sondern auch "wie viele verschiedene Auswahlmethoden es gibt, um diesen maximalen Gesamtwert zu erreichen". Im Folgenden wird erläutert, wie man die **Anzahl der Lösungen** im 01-Rucksackproblem zählt.

### 2D-DP zum Zählen der Anzahl der Lösungen

Im Folgenden wird dies am Beispiel von 2D-DP erläutert.

- Definition des Zustands:
  - `dp[i][j]` stellt den "maximalen Wert dar, der mit den ersten i Gegenständen und einer Kapazität (Volumenbegrenzung) von j erzielt werden kann".
  - `ways[i][j]` stellt die "Anzahl der **Lösungen** dar, die dem maximalen Wert entsprechen, wenn die ersten i Gegenstände eine Kapazität von j haben".

- Zustandsübergang:
  1. Wenn der i-te Gegenstand nicht ausgewählt wird:
     $$
       \text{dp}[i][j] = \text{dp}[i-1][j], 
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
     $$
  2. Wenn der i-te Gegenstand ausgewählt wird (vorausgesetzt $ j \ge s_i $):
     $$
       \text{dp}[i][j] 
         = \text{dp}[i-1][j - s_i] + v_i,
       \quad
       \text{ways}[i][j]
         = \text{ways}[i-1][j - s_i]
     $$
  3. Ob ausgewählt oder nicht, `dp[i][j]` sollte schließlich den größeren der beiden Werte annehmen:
     - Wenn
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           > \text{dp}[i-1][j],
       $$
       dann bedeutet dies, dass der Wert "Auswählen des i-ten Gegenstands" größer ist:
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
       dann bedeutet dies, dass die beiden Methoden den gleichen maximalen Wert erzielen, und die Anzahl der Lösungen sollte addiert werden:
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
       dann bedeutet dies, dass der Wert "Auswählen des i-ten Gegenstands nicht" größer ist, und die Anzahl der Lösungen erbt die Anzahl der Lösungen, wenn nicht ausgewählt wird:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Anfangsbedingungen:
  - `dp[0][j] = 0` bedeutet, dass der maximale Wert, der mit den ersten 0 Gegenständen bei jeder Kapazität erzielt wird, 0 ist.
  - `ways[0][0] = 1` bedeutet, dass der Fall "erste 0 Gegenstände, Kapazität 0" eine mögliche Lösung ist (d. h. nichts auswählen), und die **Anzahl der Lösungen** wird auf 1 gesetzt.
  - Für `j > 0` ist es unmöglich, einen positiven Wert zu erzielen, wenn keine Gegenstände ausgewählt werden können und die Kapazität größer als 0 ist, und die entsprechende Anzahl der Lösungen ist 0, d. h. `ways[0][j] = 0`.

- Endgültige Antwort:
  - `dp[N][S]` ist der maximale Wert.
  - `ways[N][S]` ist die Anzahl der Lösungen, die diesen maximalen Wert erreichen.
  - Zeitkomplexität: $O(NS)$.
  - Diese Aufgabe kann auch mit 1D-DP optimiert werden.

## Wenn genau die Volumenbegrenzung erreicht werden muss

- Definition des Zustands: `f[i][j]` stellt den maximalen Wert dar, wenn die ersten `i` Gegenstände genau das Volumen $j$ haben.
- Wenn der `i`-te Gegenstand nicht genommen wird, dann `f[i][j] = f[i - 1][j]`
- Wenn der `i`-te Gegenstand genommen wird, dann `f[i][j] = f[i - 1][j - s[i]] + v[i]`
- Es ist zu beachten, dass es keinen Unterschied zum Zustandsübergang des ursprünglichen Problems gibt.
- Die Anfangsbedingungen sind jedoch unterschiedlich. Außer `f[0][0] = 0` ist der Rest `f[0][j]` = $-\infty$, `j` $\in [1, S]$. $-\infty$ stellt einen unmöglichen Zustand dar.

## Wenn die Volumenbegrenzung $S$ besonders groß ist (1e9), während die Anzahl der Gegenstände $N$ und der maximale Gesamtwert $V$ relativ klein sind

- Für solche Aufgaben gibt es eine Lösung mit einer Komplexität von $O(NV)$.
- Definition des Zustands: `f[i][j]` stellt das minimale Volumen dar, wenn aus den ersten `i` Gegenständen einige ausgewählt werden und die Summe der Werte genau `j` beträgt.
    - Wenn der `i`-te Gegenstand nicht genommen wird, dann `f[i][j] = f[i - 1][j]`
    - Wenn der `i`-te Gegenstand genommen wird, dann `f[i][j] = f[i - 1][j - v[i]] + s[i]`
    - Nehmen Sie den kleineren der beiden Werte.
- Anfangsbedingungen: `f[0][0] = 0`, der Rest `f[0][j]` = $\infty$, `j` $\in [1, V]$. $\infty$ stellt einen unmöglichen Zustand dar. Beachten Sie, dass es nicht $-\infty$ ist.
- Die endgültige Antwort ist das größte `j` in `f[N][j]`, so dass `f[N][j] <= S`.

## Wenn die Volumenbegrenzung $S$ und der Wert eines einzelnen Gegenstands $v_i$ beide besonders groß sind (Größenordnung 1e9), während die Anzahl der Gegenstände $N$ besonders klein ist (maximal nicht mehr als 40)

- Wenn $N \leq 20$ ist, können alle Teilmengen direkt mit Brute-Force aufgezählt werden (Zeitkomplexität $O(2^N)$).
- Wenn $N \leq 40$ ist, ist $2^{40}$ in der Größenordnung von $10^{12}$, und die direkte Brute-Force-Methode ist ebenfalls relativ groß, daher kann **Halbierungssuche** verwendet werden, um die Komplexität grob auf $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$ zu reduzieren, was in einer akzeptablen Zeit abgeschlossen werden kann.