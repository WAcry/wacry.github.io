---
title: "01 Rucksackproblem"
date: 2024-12-24
draft: false
description: "Das grundlegendste klassische Rucksackproblem."
summary: "Das grundlegendste klassische Rucksackproblem."
tags: [ "Algorithmus", "Dynamische Programmierung", "Rucksackproblem" ]
categories: [ "Algorithmen und Datenstrukturen" ]
---

## Problem

Es gibt $N$ Gegenstände. Das Volumen des $i$-ten Gegenstands ist $s_i$ und sein Wert ist $v_i$.
Jeder Gegenstand kann nur einmal genommen werden. Finde unter der Voraussetzung, dass das maximale Gesamtvolumen $S$ nicht überschritten wird, den maximalen Gesamtwert $V$, der erzielt werden kann.

## Eingabeformat

Die erste Zeile enthält zwei ganze Zahlen, $N$ und $S$, getrennt durch ein Leerzeichen, die die Anzahl der Gegenstände bzw. das maximale Gesamtvolumen darstellen.
Die folgenden $N$ Zeilen enthalten jeweils zwei ganze Zahlen, $s_i$ und $v_i$, getrennt durch ein Leerzeichen, die das Volumen bzw. den Wert des $i$-ten Gegenstands darstellen.

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

## Lösung

- Definiere den Zustand: `f[i][j]` repräsentiert den maximalen Wert, der mit den ersten $i$ Gegenständen bei einem Volumenlimit von $j$ erzielt werden kann.
    - Wenn der $i$-te Gegenstand nicht genommen wird, dann gilt `f[i][j] = f[i - 1][j]`
    - Wenn der $i$-te Gegenstand genommen wird, dann gilt `f[i][j] = f[i - 1][j - s[i]] + v[i]`
    - Achte bei der Implementierung des Zustandsübergangs auf den Definitionsbereich. Wenn $j < s_i$, dann betrachte den Fall der Entnahme des $i$-ten Gegenstands nicht. Denn wenn $j - s_i$ negativ ist, ist der Array-Index ungültig.
      Es kann auch so erklärt werden: Das Volumen des $i$-ten Gegenstands ist größer als das Volumenlimit, daher ist es unmöglich.
- Definiere die Anfangsbedingung: Für die ersten $0$ Gegenstände ergibt jedes Volumenlimit einen Wert von $0$, d.h. `f[0][j] = 0`, `j` $\in [0, S]$.
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

## 1D DP Optimierung

- Das Komprimieren des zweidimensionalen Arrays in ein eindimensionales Array kann erheblich Speicherplatz sparen und die Laufgeschwindigkeit bis zu einem gewissen Grad verbessern (der Nachteil ist, dass es die speziellen Anforderungen einiger Problemtypen nicht erfüllen kann).
- Beachte, dass im Zustandsübergang `f[i][j]` nur mit `f[i - 1][j]` und `f[i - 1][j - s[i]]` zusammenhängt. Mit anderen Worten, im zweidimensionalen Array `f` im Code,
  `f[i][j]` hängt nur mit den Elementen in der vorherigen Zeile zusammen, die sich links davon oder in derselben Spalte befinden. Daher kann das zweidimensionale Array in ein eindimensionales Array oder ein Rolling Array komprimiert werden.
- Beachte, dass in dem folgenden Code die zweite Schleife in umgekehrter Reihenfolge iteriert. Dies liegt daran, dass wir sicherstellen wollen, dass bei der Berechnung von `f[i][j]` `f[i - 1][j - s[i]]` noch nicht aktualisiert wurde.

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

## Wenn die Anzahl der Schemata erforderlich ist

Es sollte nicht nur der maximale Gesamtwert ausgegeben werden, der erzielt werden kann, sondern auch "wie viele verschiedene Auswahlmethoden diesen maximalen Gesamtwert erreichen können". Im Folgenden wird beschrieben, **wie man die Anzahl der Schemata** im 01-Rucksackproblem zählt.

### 2D DP zum Zählen von Schemata

Das Folgende verwendet 2D DP als Beispiel zur Erläuterung.

- Definiere den Zustand:
  - `dp[i][j]` repräsentiert "den maximalen Wert, der erzielt werden kann, wenn man die ersten i Gegenstände mit einer Kapazität (Volumenlimit) von j betrachtet".
  - `ways[i][j]` repräsentiert "die **Anzahl der Schemata**, die dem maximalen Wert entsprechen, der erzielt wird, wenn man die ersten i Gegenstände mit einer Kapazität von j betrachtet".

- Zustandsübergang:
  1. Wenn der `i`-te Gegenstand nicht ausgewählt wird:
     $$
       \text{dp}[i][j] = \text{dp}[i-1][j], 
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
     $$
  2. Wenn der `i`-te Gegenstand ausgewählt wird (vorausgesetzt, dass $ j \ge s_i $):
     $$
       \text{dp}[i][j] 
         = \text{dp}[i-1][j - s_i] + v_i,
       \quad
       \text{ways}[i][j]
         = \text{ways}[i-1][j - s_i]
     $$
  3. Ob ausgewählt wird oder nicht, das endgültige `dp[i][j]` sollte das größere der beiden annehmen:
     - Wenn
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           > \text{dp}[i-1][j],
       $$
       dann bedeutet dies, dass "die Auswahl des i-ten Gegenstands" einen größeren Wert hat:
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
       bedeutet dies, dass der maximale Wert, der durch die beiden Methoden erzielt wird, derselbe ist, dann sollte die Anzahl der Schemata addiert werden:
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
       dann bedeutet dies, dass "die Nichtauswahl des i-ten Gegenstands" einen größeren Wert hat, und die Anzahl der Schemata erbt die Anzahl der Schemata, wenn nicht ausgewählt wird:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Anfangsbedingungen:
  - `dp[0][j] = 0` bedeutet, dass, wenn es 0 Gegenstände gibt, der maximale Wert, der für jede Kapazität erzielt wird, 0 ist.
  - `ways[0][0] = 1` bedeutet, dass der Fall "0 Gegenstände, Kapazität 0" ein machbares Schema ist (d.h. nichts auswählen), und die **Anzahl der Schemata** auf 1 gesetzt wird.
  - Für `j > 0`, wenn es keine Gegenstände zur Auswahl gibt und die Kapazität größer als 0 ist, ist es unmöglich, einen positiven Wert zu erhalten, und die entsprechende Anzahl von Schemata ist 0, d.h. `ways[0][j] = 0`.

- Endgültige Antwort:
  - `dp[N][S]` ist der maximale Wert.
  - `ways[N][S]` ist die Anzahl der Schemata, um diesen maximalen Wert zu erreichen.
  - Zeitkomplexität: $O(NS)$.
  - Dieses Problem kann auch mit 1D DP optimiert werden.

## Wenn die Anforderung darin besteht, das Volumenlimit genau zu erreichen

- Definiere den Zustand: `f[i][j]` repräsentiert den maximalen Wert, wenn die ersten `i` Gegenstände genau ein Volumen von $j$ haben.
- Wenn der `i`-te Gegenstand nicht genommen wird, dann gilt `f[i][j] = f[i - 1][j]`
- Wenn der `i`-te Gegenstand genommen wird, dann gilt `f[i][j] = f[i - 1][j - s[i]] + v[i]`
- Es ist zu beachten, dass es keinen Unterschied im Zustandsübergang zum ursprünglichen Problem gibt.
- Die Anfangsbedingungen sind jedoch unterschiedlich. Mit Ausnahme von `f[0][0] = 0` ist der Rest `f[0][j]` = $-\infty$, `j` $\in [1, S]$. $-\infty$ repräsentiert einen unmöglichen Zustand.

## Wenn das Volumenlimit $S$ sehr groß ist (1e9), während die Anzahl der Gegenstände $N$ und der maximale Gesamtwert $V$ relativ klein sind

- Für solche Probleme gibt es eine Lösung mit einer Komplexität von $O(NV)$.
- Definiere den Zustand: `f[i][j]` repräsentiert das minimale Volumen, wenn man mehrere Gegenstände aus den ersten `i` Gegenständen auswählt und der Gesamtwert genau `j` ist.
    - Wenn der `i`-te Gegenstand nicht genommen wird, dann gilt `f[i][j] = f[i - 1][j]`
    - Wenn der `i`-te Gegenstand genommen wird, dann gilt `f[i][j] = f[i - 1][j - v[i]] + s[i]`
    - Nimm den kleineren der beiden.
- Anfangsbedingungen: `f[0][0] = 0`, der Rest `f[0][j]` = $\infty$, `j` $\in [1, V]$. $\infty$ repräsentiert einen unmöglichen Zustand. Beachte, dass es nicht $-\infty$ ist.
- Die endgültige Antwort ist das größte `j` in `f[N][j]`, so dass `f[N][j] <= S`.

## Wenn das Volumenlimit $S$ und der Wert eines einzelnen Gegenstands $v_i$ beide sehr groß sind (in der Größenordnung von 1e9), während die Anzahl der Gegenstände $N$ sehr klein ist (nicht mehr als 40)

- Wenn $N \leq 20$, können alle Teilmengen direkt durch Brute Force aufgezählt werden (Zeitkomplexität $O(2^N)$).
- Wenn $N \leq 40$, da $2^{40}$ in der Größenordnung von $10^{12}$ liegt, wird auch die direkte Brute Force relativ groß sein, daher kann **Meet-in-the-Middle-Suche** verwendet werden, um die Komplexität auf ungefähr $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$ zu reduzieren, was in einer akzeptablen Zeit abgeschlossen werden kann.