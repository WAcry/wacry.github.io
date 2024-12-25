---
title: "Binäre Suche"
date: 2024-12-24
draft: false
description: "Wie man den binären Suchalgorithmus für ganze Zahlen elegant implementiert."
summary: "Wie man den binären Suchalgorithmus für ganze Zahlen elegant implementiert."
tags: [ "Algorithmus", "Binäre Suche", "Algorithmusvorlage" ]
categories: [ "Algorithmen und Datenstrukturen" ]
---

{{< katex >}}

# Binäre Suche

Wenn ein sortierter Lösungsraum in zwei Teile aufgeteilt wird, wobei ein Teil die Bedingung erfüllt und der andere Teil die Bedingung nicht erfüllt, dann kann die binäre Suche verwendet werden, um den kritischen Punkt im sortierten Lösungsraum zu finden.

Die Grundidee der binären Suche besteht darin, den Suchbereich kontinuierlich zu halbieren. Bei jeder Überprüfung wird das mittlere Element überprüft. Wenn das mittlere Element die Bedingung nicht erfüllt, kann die Hälfte des Bereichs ausgeschlossen werden;
andernfalls wird die Suche im anderen Teil des Bereichs fortgesetzt. Da bei jeder Suche die Hälfte des Suchbereichs verworfen wird, kann die Suchzeitkomplexität \\(O(\log n)\\) erreichen.

## Beispielaufgabe

**Aufgabenbeschreibung:**
Gegeben ist ein aufsteigend sortiertes Array von ganzen Zahlen der Länge \\(n\\) sowie \\(q\\) Abfragen. Jede Abfrage gibt eine ganze Zahl \\(k\\) an, und wir müssen die "Startposition" und "Endposition" von \\(k\\) im Array finden (Indizes beginnen bei 0). Wenn die Zahl nicht im Array existiert, gib \\(-1\\) \\(-1\\) zurück.

### Eingabeformat

1. Erste Zeile: Zwei ganze Zahlen \\(n\\) und \\(q\\), die die Länge des Arrays und die Anzahl der Abfragen angeben.
2. Zweite Zeile: \\(n\\) ganze Zahlen, die das vollständige Array darstellen und bereits aufsteigend sortiert sind.
3. Die nächsten \\(q\\) Zeilen: Jede Zeile enthält eine ganze Zahl \\(k\\), die ein Abfrageelement darstellt.

## Datenbereich

\\(1 \leq n \leq 100000\\)

\\(1 \leq q \leq 10000\\)

\\(1 \leq k \leq 10000\\)

### Ausgabeformat

Für jede Abfrage geben Sie in einer Zeile die Start- und Endposition des Elements im Array aus. Wenn das Element nicht im Array existiert, geben Sie `-1 -1` aus.

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

- Der Bereich, in dem das Element \\(3\\) vorkommt, ist \\([3, 4]\\);
- Das Element \\(4\\) kommt nur einmal vor, an Position \\(5\\);
- Das Element \\(5\\) existiert nicht im Array, daher wird \\(-1\\) \\(-1\\) zurückgegeben.

---

## Lösung

- **Finden der "Startposition":**
  Das heißt, die erste Position zu finden, die größer oder gleich \\(k\\) ist. Das Array kann in zwei Teile aufgeteilt werden:
    - Alle Zahlen links sind "kleiner als" \\(k\\)
    - Alle Zahlen rechts sind "größer oder gleich" \\(k\\)
    - Die Antwort ist die erste Position auf der rechten Seite.

- **Finden der "Endposition":**
  Das heißt, die letzte Position zu finden, die kleiner oder gleich \\(k\\) ist. Das Array kann in zwei Teile aufgeteilt werden:
    - Alle Zahlen links sind "kleiner oder gleich" \\(k\\)
    - Alle Zahlen rechts sind "größer als" \\(k\\)
    - Die Antwort ist die letzte Position auf der linken Seite.

---

## Empfohlene Vorlage

Nachfolgend finden Sie eine elegante und fehlerfreie Binärsuchvorlage. Sie sorgt dafür, dass die Schleife aufhört, sobald \\(l\\) und \\(r\\) nebeneinander liegen, indem \\(l\\) und \\(r\\) schrittweise angenähert werden:

Definieren Sie zwei Zeiger \\(l, r\\) mit der Invariante: Das geschlossene Intervall \\([0, l]\\) gehört zum linken Teil, das geschlossene Intervall \\([r, n - 1]\\) gehört zum rechten Teil. \\(l\\)
und \\(r\\) werden mit \\(-1\\) bzw. \\(n\\) initialisiert.

Wenn der Algorithmus terminiert, sind \\(l\\) und \\(r\\) benachbart und zeigen auf das letzte Element des linken Teils bzw. das erste Element des rechten Teils.

Da die gewünschte Lösung möglicherweise nicht existiert, müssen wir, wenn die Aufgabe nicht angibt, dass eine Lösung existiert, prüfen, ob `l` oder `r` außerhalb des Bereichs liegen oder ob sie auf den richtigen Wert zeigen.

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
        //    Teile das Array in zwei Teile auf, links alle < k, rechts alle >= k.
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

        // 2. Finde die Endposition von k
        //    Teile das Array in zwei Teile auf, links alle <= k, rechts alle > k.
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

### Warum diese Schreibweise?

1. Diese Schreibweise hat streng definierte Invarianten.
2. Sie ist gleichzeitig geeignet, um die "Startposition" und die "Endposition" zu finden, ohne dass zusätzliche Verarbeitung oder Änderungen erforderlich sind.
3. Einige Schreibweisen verwenden `l == r` als Abbruchbedingung. Wenn \\(l\\) und \\(r\\) einen Abstand von \\(1\\) haben, wird \\(mid\\) gleich \\(l\\) oder \\(r\\) berechnet. Wenn dies nicht korrekt verarbeitet wird, indem \\(l\\) oder \\(r\\) auf \\(mid\\) aktualisiert wird, verkleinert sich der Suchbereich nicht und es kommt zu einer Endlosschleife. Im Gegenteil, diese Schreibweise beendet sich, wenn \\(l\\) und \\(r\\) benachbart sind, wodurch sichergestellt wird, dass \\(mid\\) kleiner als \\(l\\) und größer als \\(r\\) ist, und der Suchbereich wird bei der Aktualisierung von \\(l\\) oder \\(r\\) garantiert verkleinert.

---

## STL

Wenn Sie die von C++ STL bereitgestellten Funktionen `lower_bound` und `upper_bound` verwenden, können Sie das gleiche Ergebnis erzielen:

- `lower_bound(first, last, val)` gibt die "erste Position zurück, die größer oder gleich val ist"
- `upper_bound(first, last, val)` gibt die "erste Position zurück, die größer als val ist"

Nehmen wir zum Beispiel an, `nums = {1,2,3,4,4,4,4,4,5,5,6}`, und wir möchten den Bereich wissen, in dem 4 vorkommt:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    cout << "4 kommt 0 Mal vor" << endl;
} else {
    cout << "Die erste 4 ist an Position " << it1 - nums.begin() << endl;
    cout << "Die letzte 4 ist an Position " << it2 - nums.begin() - 1 << endl;
    cout << "4 kommt " << it2 - it1 << " Mal vor" << endl;
}
```

- `it1` zeigt auf die erste Position, deren Wert größer oder gleich \\(4\\) ist.
- `it2` zeigt auf die erste Position, deren Wert größer als \\(4\\) ist.  
  Also ist `it2 - it1` die Anzahl, wie oft \\(4\\) im Array vorkommt; `it2 - nums.begin() - 1` ist die rechte Grenze von \\(4\\).

---

## Ergänzung

Die binäre Suche kann auch auf die Suche nach Gleitkommazahlenbereichen (z. B. zum Finden von Wurzeln von Gleichungen) und auf die ternäre Suche zum Finden von Maximalwerten einer unimodalen Funktion erweitert werden.
Sobald Sie das Kernprinzip " **In einem sortierten Intervall kann bei jedem Schritt die Hälfte ausgeschlossen werden**" verstanden haben, werden Sie feststellen, dass die binäre Suche Ihnen in vielen Szenarien helfen kann, Probleme effizient zu lösen.

---

## Übung

LeetCode 33. Suche in einem rotierten sortierten Array

Hinweis: Verwenden Sie im ersten Schritt die binäre Suche, um den Rotationspunkt zu finden, und verwenden Sie im zweiten Schritt die binäre Suche, um den Zielwert zu finden.