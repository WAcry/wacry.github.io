---
title: "Binäre Suche"
date: 2024-12-24
draft: false
description: "Wie man den binären Suchalgorithmus elegant implementiert."
summary: "Wie man den binären Suchalgorithmus elegant implementiert."
tags: [ "Algorithmus", "Binäre Suche", "Algorithmusvorlage" ]
categories: [ "Algorithmen und Datenstrukturen" ]
---

# Binäre Suche

Wenn ein sortierter Lösungsraum in zwei Teile unterteilt wird, von denen einer die Bedingung erfüllt und der andere nicht, kann die binäre Suche verwendet werden, um den kritischen Punkt im sortierten Lösungsraum zu finden.

Die Grundidee der binären Suche besteht darin, das Suchintervall wiederholt zu halbieren. Bei jeder Überprüfung wird das Element in der Mitte geprüft. Wenn das mittlere Element die Bedingung nicht erfüllt, kann die Hälfte des Intervalls verworfen werden. Andernfalls wird die Suche in der anderen Hälfte des Intervalls fortgesetzt. Da bei jeder Operation die Hälfte des Suchintervalls verworfen wird, kann die Zeitkomplexität der Suche $O(\log n)$ erreichen.

## Beispielaufgabe

**Aufgabenbeschreibung:**
Gegeben ist ein aufsteigend sortiertes Array von Ganzzahlen der Länge $n$ und $q$ Abfragen. Jede Abfrage gibt eine Ganzzahl $k$ an. Wir müssen die „Startposition“ und die „Endposition“ von $k$ im Array finden (Indizes beginnen bei 0). Wenn die Zahl nicht im Array vorhanden ist, wird `-1 -1` zurückgegeben.

### Eingabeformat

1. Erste Zeile: Zwei Ganzzahlen $n$ und $q$, die die Länge des Arrays und die Anzahl der Abfragen darstellen.
2. Zweite Zeile: $n$ Ganzzahlen, die das vollständige, aufsteigend sortierte Array darstellen.
3. Nächste $q$ Zeilen: Jede Zeile enthält eine Ganzzahl $k$, die ein Such-Element darstellt.

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

- Der Bereich, in dem das Element $3$ vorkommt, ist $[3, 4]$.
- Das Element $4$ kommt nur einmal an Position $5$ vor.
- Das Element $5$ ist nicht im Array vorhanden, daher wird $-1$ $-1$ zurückgegeben.

---

## Lösung

- **Finde die "Startposition":**
  Das ist die Position des ersten Elements, das größer oder gleich $k$ ist. Das Array kann in zwei Teile unterteilt werden:
    - Alle Zahlen auf der linken Seite sind "kleiner" als $k$.
    - Alle Zahlen auf der rechten Seite sind "größer oder gleich" $k$.
    - Die Antwort ist die erste Position auf der rechten Seite.

- **Finde die "Endposition":**
  Das ist die Position des letzten Elements, das kleiner oder gleich $k$ ist. Das Array kann in zwei Teile unterteilt werden:
    - Alle Zahlen auf der linken Seite sind "kleiner oder gleich" $k$.
    - Alle Zahlen auf der rechten Seite sind "größer" als $k$.
    - Die Antwort ist die letzte Position auf der linken Seite.

---

## Empfohlene Vorlage

Im Folgenden ist eine elegante und fehleranfällige Binärsuchvorlage dargestellt. Sie stellt sicher, dass die Schleife endet, wenn $l$ und $r$ benachbart sind, indem sie $l$ und $r$ schrittweise zusammenführt:

Definiere zwei Zeiger $l, r$ mit der Invariante: das geschlossene Intervall $[0, l]$ gehört zum linken Teil, und das geschlossene Intervall $[r, n - 1]$ gehört zum rechten Teil. $l$ und $r$ werden mit $-1$ und $n$ initialisiert.

Wenn der Algorithmus endet, sind $l$ und $r$ benachbart und zeigen auf das letzte Element des linken Teils bzw. auf das erste Element des rechten Teils.

Da die von uns gesuchte Lösung möglicherweise nicht existiert, müssen wir, wenn die Aufgabe nicht angibt, dass eine Lösung existiert, prüfen, ob `l` oder `r` außerhalb der Grenzen liegt und ob sie auf den richtigen Wert zeigen.

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
        //    Teile das Array in zwei Teile, links < k, rechts >= k.
        //    Die Antwort ist der kleinste Index des rechten Teils.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // Wenn r außerhalb der Grenzen liegt oder nums[r] != k, existiert k nicht
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. Finde die Endposition von k
        //    Teile das Array in zwei Teile, links <= k, rechts > k.
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

### Warum diese Schreibweise

1. Diese Schreibweise hat eine streng definierte Invariante.
2. Sie gilt sowohl für das Finden der "Startposition" als auch der "Endposition", ohne dass zusätzliche Verarbeitung oder Änderungen erforderlich sind.
3. Einige Schreibweisen verwenden `l == r` als Abbruchbedingung. Wenn $l$ und $r$ um $1$ unterschiedlich sind, ergibt sich ein $mid$, der gleich $l$ oder $r$ ist. Wenn dies nicht korrekt behandelt wird und $l$ oder $r$ auf $mid$ aktualisiert wird, wird sich das Suchintervall nicht verkleinern, was zu einer Endlosschleife führen kann. Im Gegensatz dazu bricht diese Schreibweise ab, wenn $l$ und $r$ benachbart sind, wodurch sichergestellt ist, dass $mid$ kleiner als $l$ und größer als $r$ ist, und das Suchintervall bei der Aktualisierung von $l$ oder $r$ immer verkleinert wird.

---

## STL

Wenn die von C++ STL bereitgestellten Funktionen `lower_bound` und `upper_bound` verwendet werden, kann das gleiche Ergebnis erzielt werden:

- `lower_bound(first, last, val)` gibt die "Position des ersten Elements, das größer oder gleich val ist" zurück.
- `upper_bound(first, last, val)` gibt die "Position des ersten Elements, das größer als val ist" zurück.

Nehmen wir beispielsweise an, `nums = {1,2,3,4,4,4,4,4,5,5,6}` und wir möchten den Bereich ermitteln, in dem 4 vorkommt:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    cout << "4 appears 0 times" << endl;
} else {
    cout << "first 4 is at " << it1 - nums.begin() << endl;
    cout << "last 4 is at " << it2 - nums.begin() - 1 << endl;
    cout << "4 appears " << it2 - it1 << " times" << endl;
}
```

- `it1` zeigt auf die Position des ersten Wertes, der größer oder gleich $4$ ist.
- `it2` zeigt auf die Position des ersten Wertes, der größer als $4$ ist.
  Daher ist `it2 - it1` die Anzahl der Vorkommen von $4$ im Array; `it2 - nums.begin() - 1` ist die rechte Grenze von $4$.

---

## Zusätzliche Informationen

Die binäre Suche kann auch auf die Suche nach Fließkommazahlenbereichen erweitert werden (z. B. das Finden von Gleichungswurzeln) sowie die ternäre Suche nach den Extremwerten unipolarer Funktionen.
Solange Sie das Kernprinzip "in einem sortierten Intervall ist es möglich, jedes Mal die Hälfte zu eliminieren" verstehen, werden Sie feststellen, dass die binäre Suche Ihnen helfen kann, Probleme in vielen Szenarien effizient zu lösen.

---

## Übung

LeetCode 33. Search in Rotated Sorted Array

Hinweis: Finden Sie im ersten Schritt mit binärer Suche den Drehpunkt, und finden Sie im zweiten Schritt mit binärer Suche den Zielwert.