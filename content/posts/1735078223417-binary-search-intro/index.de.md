markdown
---
title: "Binäre Suche"
date: 2024-12-24
draft: false
description: "Wie man den binären Suchalgorithmus elegant implementiert."
summary: "Wie man den binären Suchalgorithmus elegant implementiert."
tags: [ "Algorithmus", "Binäre Suche", "Algorithmusvorlage" ]
categories: [ "Algorithmen und Datenstrukturen" ]
---

Wenn ein geordneter Lösungsraum in zwei Teile geteilt wird, wobei ein Teil eine Bedingung erfüllt und der andere nicht, dann kann die binäre Suche verwendet werden, um den kritischen Punkt im geordneten Lösungsraum zu finden.

Die Grundidee der binären Suche ist es, das Suchintervall wiederholt zu halbieren. Jedes Mal wird das mittlere Element überprüft. Wenn das mittlere Element die Bedingung nicht erfüllt, kann die Hälfte des Intervalls eliminiert werden; andernfalls wird die Suche in der anderen Hälfte fortgesetzt. Da jedes Mal die Hälfte des Suchintervalls verworfen wird, kann die Suchzeitkomplexität $O(\log n)$ erreichen.

## Beispielproblem

**Problembeschreibung:**
Gegeben ist ein aufsteigend sortiertes Integer-Array der Länge $n$ und $q$ Abfragen. Jede Abfrage gibt eine ganze Zahl $k$ an, und wir müssen die "Startposition" und "Endposition" von $k$ im Array finden (Indizes beginnen bei 0). Wenn die Zahl nicht im Array existiert, gib `-1 -1` zurück.

### Eingabeformat

1. Erste Zeile: zwei ganze Zahlen $n$ und $q$, die die Länge des Arrays bzw. die Anzahl der Abfragen darstellen.
2. Zweite Zeile: $n$ ganze Zahlen, die das vollständige Array darstellen, bereits aufsteigend sortiert.
3. Nächste $q$ Zeilen: jede Zeile enthält eine ganze Zahl $k$, die ein Abfrageelement darstellt.

## Datenbereich

$1 \leq n \leq 100000$

$1 \leq q \leq 10000$

$1 \leq k \leq 10000$

### Ausgabeformat

Gib für jede Abfrage die Start- und Endpositionen des Elements im Array in einer einzigen Zeile aus. Wenn das Element nicht im Array existiert, gib `-1 -1` aus.

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
- Element $4$ kommt nur einmal vor, an Position $5$;
- Element $5$ existiert nicht im Array, also gib $-1$ $-1$ zurück.

---

## Lösung

- **Finden der "Startposition":**
  Das heißt, die erste Position zu finden, die größer oder gleich $k$ ist. Das Array kann in zwei Teile geteilt werden:
    - Alle Zahlen auf der linken Seite sind "kleiner als" $k$
    - Alle Zahlen auf der rechten Seite sind "größer oder gleich" $k$
    - Die Antwort ist die erste Position auf der rechten Seite

- **Finden der "Endposition":**
  Das heißt, die letzte Position zu finden, die kleiner oder gleich $k$ ist. Das Array kann in zwei Teile geteilt werden:
    - Alle Zahlen auf der linken Seite sind "kleiner oder gleich" $k$
    - Alle Zahlen auf der rechten Seite sind "größer als" $k$
    - Die Antwort ist die letzte Position auf der linken Seite

---

## Empfohlene Vorlage

Nachfolgend ist eine elegante und weniger fehleranfällige Vorlage für die binäre Suche.

Definiere zwei Zeiger $l, r$, mit der Invariante: Das geschlossene Intervall $[0, l]$ gehört zum linken Teil, und das geschlossene Intervall $[r, n - 1]$ gehört zum rechten Teil. $l$ und $r$ werden mit $-1$ bzw. $n$ initialisiert.

Wenn der Algorithmus terminiert, sind $l$ und $r$ benachbart und zeigen auf das letzte Element des linken Teils bzw. das erste Element des rechten Teils.

Da die Lösung, die wir suchen, möglicherweise nicht existiert, müssen wir, wenn das Problem nicht angibt, dass eine Lösung definitiv existiert, überprüfen, ob `l` oder `r` außerhalb der Grenzen liegt und ob es auf den richtigen Wert zeigt.

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

        // 1. Finde die Startposition von k
        //    Teile das Array in zwei Teile, der linke Teil ist alles < k, und der rechte Teil ist alles >= k.
        //    Die Antwort ist der kleinste Index des rechten Teils.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // Wenn r außerhalb der Grenzen liegt oder nums[r] != k, bedeutet das, dass k nicht existiert
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. Finde die Endposition von k
        //    Teile das Array in zwei Teile, der linke Teil ist alles <= k, und der rechte Teil ist alles > k.
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

1. Dieser Ansatz hat streng definierte Invarianten.
2. Er gilt sowohl für das Finden der "Startposition" als auch der "Endposition" ohne zusätzliche Behandlung oder Änderungen.
3. Einige Ansätze verwenden `l == r` als Abbruchbedingung. Wenn $l$ und $r$ sich um $1$ unterscheiden, wird $mid$ so berechnet, dass es gleich $l$ oder $r$ ist. Wenn dies nicht korrekt behandelt wird, wird das Aktualisieren von $l$ oder $r$ auf $mid$ das Suchintervall nicht verkleinern, was zu einer Endlosschleife führt. Im Gegensatz dazu terminiert dieser Ansatz, wenn $l$ und $r$ benachbart sind, wodurch sichergestellt wird, dass $mid$ kleiner als $l$ und größer als $r$ ist, und das Aktualisieren von $l$ oder $r$ das Suchintervall immer verkleinert.

---

## STL

Wenn Sie die von C++ STL bereitgestellten Funktionen `lower_bound` und `upper_bound` verwenden, können Sie dasselbe erreichen:

- `lower_bound(first, last, val)` gibt "die erste Position zurück, die größer oder gleich val ist"
- `upper_bound(first, last, val)` gibt "die erste Position zurück, die größer als val ist"

Nehmen wir zum Beispiel an, `nums = {1,2,3,4,4,4,4,4,5,5,6}`, und wir wollen den Bereich wissen, in dem 4 vorkommt:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    cout << "4 kommt 0 mal vor" << endl;
} else {
    cout << "erste 4 ist bei " << it1 - nums.begin() << endl;
    cout << "letzte 4 ist bei " << it2 - nums.begin() - 1 << endl;
    cout << "4 kommt " << it2 - it1 << " mal vor" << endl;
}
```

- `it1` zeigt auf die erste Position, an der der Wert größer oder gleich $4$ ist.
- `it2` zeigt auf die erste Position, an der der Wert größer als $4$ ist.
  Daher ist `it2 - it1` die Anzahl, wie oft $4$ im Array vorkommt; `it2 - nums.begin() - 1` ist die Position der rechten Grenze von $4$.

---

## Zusätzliche Hinweise

Die binäre Suche kann auch auf die Suche in Gleitkomma-Bereichen erweitert werden (z. B. das Finden der Wurzeln einer Gleichung) und die ternäre Suche zum Finden der Extrema unimodaler Funktionen.

---

## Übung

LeetCode 33. Suche in einem rotierten sortierten Array

Hinweis: Verwenden Sie zuerst die binäre Suche, um den Rotationspunkt zu finden, und verwenden Sie dann die binäre Suche, um den Zielwert zu finden.