---
title: "Binäre Suche"
date: 2024-12-24
draft: false
description: "Wie man den binären Suchalgorithmus elegant implementiert."
summary: "Wie man den binären Suchalgorithmus elegant implementiert."
tags: [ "Algorithmus", "Binäre Suche", "Algorithmusvorlage" ]
categories: [ "Algorithmen und Datenstrukturen" ]
---

Wenn ein sortierter Lösungsraum in zwei Teile geteilt wird, wobei ein Teil die Bedingung erfüllt und der andere Teil nicht, dann kann die binäre Suche verwendet werden, um den kritischen Punkt im sortierten Lösungsraum zu finden.

Die Grundidee der binären Suche ist es, das Suchintervall kontinuierlich zu halbieren. Bei jeder Überprüfung wird das mittlere Element untersucht. Wenn das mittlere Element die Bedingung nicht erfüllt, kann die Hälfte des Intervalls ausgeschlossen werden; andernfalls wird die Suche in der anderen Hälfte des Intervalls fortgesetzt. Da bei jeder Suche die Hälfte des Suchintervalls verworfen wird, kann die Suchzeitkomplexität $O(\log n)$ erreichen.

## Beispielaufgabe

**Aufgabenbeschreibung:**
Gegeben ist ein aufsteigend sortiertes Array von ganzen Zahlen der Länge $n$ sowie $q$ Abfragen. Jede Abfrage gibt eine ganze Zahl $k$ an, und wir müssen die "Startposition" und "Endposition" von $k$ im Array finden (Indizes beginnen bei 0). Wenn die Zahl nicht im Array vorhanden ist, wird `-1 -1` zurückgegeben.

### Eingabeformat

1. Erste Zeile: Zwei ganze Zahlen $n$ und $q$, die die Länge des Arrays bzw. die Anzahl der Abfragen angeben.
2. Zweite Zeile: $n$ ganze Zahlen, die das vollständige Array darstellen, das bereits aufsteigend sortiert ist.
3. Die nächsten $q$ Zeilen: Jede Zeile enthält eine ganze Zahl $k$, die ein Abfrageelement darstellt.

## Datenbereich

$1 \leq n \leq 100000$

$1 \leq q \leq 10000$

$1 \leq k \leq 10000$

### Ausgabeformat

Geben Sie für jede Abfrage die Start- und Endposition des Elements im Array in einer Zeile aus. Wenn das Element nicht im Array vorhanden ist, geben Sie `-1 -1` aus.

**Beispiel:**

```
Eingabe:
6 3
1 2 2 3 3 4
3
4
5

Ausgabe:
3 4
5 5
-1 -1
```

**Erläuterung:**

- Der Bereich, in dem das Element $3$ vorkommt, ist $[3, 4]$;
- Das Element $4$ kommt nur einmal an Position $5$ vor;
- Das Element $5$ ist nicht im Array vorhanden, daher wird $-1$ $-1$ zurückgegeben.

---

## Lösung

- **Suche nach der "Startposition":**
  Das heißt, die erste Position zu finden, die größer oder gleich $k$ ist. Das Array kann in zwei Teile geteilt werden:
    - Alle Zahlen links sind "kleiner" als $k$
    - Alle Zahlen rechts sind "größer oder gleich" $k$
    - Die Antwort ist die erste Position auf der rechten Seite

- **Suche nach der "Endposition":**
  Das heißt, die letzte Position zu finden, die kleiner oder gleich $k$ ist. Das Array kann in zwei Teile geteilt werden:
    - Alle Zahlen links sind "kleiner oder gleich" $k$
    - Alle Zahlen rechts sind "größer" als $k$
    - Die Antwort ist die letzte Position auf der linken Seite

---

## Empfohlene Vorlage

Im Folgenden finden Sie eine elegante und fehlerfreie binäre Suchvorlage.

Definieren Sie zwei Zeiger $l, r$ mit der Invariante: Das geschlossene Intervall $[0, l]$ gehört zum linken Teil, und das geschlossene Intervall $[r, n - 1]$ gehört zum rechten Teil. $l$ und $r$ werden mit $-1$ bzw. $n$ initialisiert.

Wenn der Algorithmus beendet ist, sind $l$ und $r$ benachbart und zeigen auf das letzte Element des linken Teils bzw. das erste Element des rechten Teils.

Da die gewünschte Lösung möglicherweise nicht existiert, müssen wir, wenn die Aufgabe nicht angibt, dass eine Lösung existiert, überprüfen, ob `l` oder `r` außerhalb des Bereichs liegen oder auf den richtigen Wert zeigen.

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

        // 1. Suche nach der Startposition von k
        //    Teile das Array in zwei Teile, links alle < k, rechts alle >= k.
        //    Die Antwort ist der kleinste Index des rechten Teils.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // Wenn r außerhalb des Bereichs liegt oder nums[r] != k, existiert k nicht
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. Suche nach der Endposition von k
        //    Teile das Array in zwei Teile, links alle <= k, rechts alle > k.
        //    Die Antwort ist der größte Index des linken Teils.
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

### Vorteile

1. Diese Schreibweise hat streng definierte Invarianten.
2. Sie ist sowohl für die Suche nach der "Startposition" als auch nach der "Endposition" geeignet, ohne dass zusätzliche Verarbeitung oder Änderungen erforderlich sind.
3. Einige Schreibweisen verwenden `l == r` als Abbruchbedingung. Wenn $l$ und $r$ um $1$ differieren, wird $mid$ gleich $l$ oder $r$ berechnet. Wenn dies nicht korrekt behandelt wird, wird die Aktualisierung von $l$ oder $r$ auf $mid$ dazu führen, dass sich das Suchintervall nicht verkleinert und eine Endlosschleife entsteht. Im Gegensatz dazu wird die Suche hier beendet, wenn $l$ und $r$ benachbart sind, wodurch sichergestellt wird, dass $mid$ kleiner als $l$ und größer als $r$ ist, und das Suchintervall bei der Aktualisierung von $l$ oder $r$ definitiv verkleinert wird.

---

## STL

Wenn Sie die von C++ STL bereitgestellten Funktionen `lower_bound` und `upper_bound` verwenden, können Sie dasselbe erreichen:

- `lower_bound(first, last, val)` gibt die "erste Position größer oder gleich val" zurück
- `upper_bound(first, last, val)` gibt die "erste Position größer als val" zurück

Nehmen wir zum Beispiel an, `nums = {1,2,3,4,4,4,4,4,5,5,6}`, und wir möchten den Bereich wissen, in dem 4 vorkommt:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    cout << "4 kommt 0 mal vor" << endl;
} else {
    cout << "Die erste 4 ist an Position " << it1 - nums.begin() << endl;
    cout << "Die letzte 4 ist an Position " << it2 - nums.begin() - 1 << endl;
    cout << "4 kommt " << it2 - it1 << " mal vor" << endl;
}
```

- `it1` zeigt auf die erste Position, deren Wert größer oder gleich $4$ ist.
- `it2` zeigt auf die erste Position, deren Wert größer als $4$ ist.
  Daher ist `it2 - it1` die Anzahl, wie oft $4$ im Array vorkommt; `it2 - nums.begin() - 1` ist die Position der rechten Grenze von $4$.

---

## Ergänzung

Die binäre Suche kann auch auf die Suche im Bereich von Gleitkommazahlen (z. B. zum Finden von Wurzeln von Gleichungen) und auf die ternäre Suche zur Bestimmung des Maximums einer unimodalen Funktion erweitert werden.

---

## Übung

LeetCode 33. Search in Rotated Sorted Array

Hinweis: Verwenden Sie im ersten Schritt die binäre Suche, um den Rotationspunkt zu finden, und verwenden Sie im zweiten Schritt die binäre Suche, um den Zielwert zu finden.