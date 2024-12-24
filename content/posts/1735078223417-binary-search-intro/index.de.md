---
title: "Binäre Suche"
date: 2024-12-24
draft: false
description: "Wie man den binären Suchalgorithmus für Ganzzahlen elegant implementiert"
summary: "Wie man den binären Suchalgorithmus für Ganzzahlen elegant implementiert"
tags: [ "Algorithmus", "Binäre Suche", "Algorithm Vorlage" ]
categories: [ "Algorithmen und Datenstrukturen" ]
---
{{< katex >}}

# Binäre Suche

In einer sortierten Sequenz kann man mit der binären Suche schnell ein bestimmtes Element finden. Im Vergleich zur linearen Suche mit einer Zeitkomplexität von $O(n)$ benötigt die binäre Suche nur $O(\log n)$ Zeit, was sie bei großen Datenmengen sehr effizient macht.

## Das Kernkonzept der binären Suche

Die Grundidee der binären Suche besteht darin, den Suchbereich kontinuierlich zu halbieren. Bei jedem Vergleich wird das Element in der Mitte mit dem Zielwert verglichen. Wenn das Element in der Mitte die Bedingung nicht erfüllt, kann die Hälfte des Bereichs ausgeschlossen werden; andernfalls wird die Suche in der anderen Hälfte fortgesetzt. Da bei jedem Schritt die Hälfte des Suchbereichs verworfen wird, kann eine Zeitkomplexität von $O(\log n)$ erreicht werden.

Die binäre Suche ist sehr nützlich für Probleme, bei denen " **die möglichen Lösungen in einen sortierten Bereich (der Bedingung erfüllt) und einen anderen sortierten Bereich (der Bedingung nicht erfüllt) unterteilt werden können** ". Zum Beispiel:

- Finden, ob ein bestimmtes Element in einem sortierten Array existiert
- Finden der "ersten Position" oder "letzten Position", an der eine Zahl auftritt

## Beispielaufgabe: Finden der Start- und Endpositionen von Elementen

**Aufgabenbeschreibung:**
Gegeben sei ein aufsteigend sortiertes Array von ganzen Zahlen der Länge $n$, sowie $q$ Abfragen. Jede Abfrage gibt eine ganze Zahl $k$ an, und wir müssen die "Startposition" und die "Endposition" von $k$ im Array finden (Indizes beginnen bei 0). Wenn die Zahl im Array nicht existiert, wird $-1$ $-1$ zurückgegeben.

**Eingabeformat:**

1. Erste Zeile: Zwei ganze Zahlen $n$ und $q$, die die Länge des Arrays und die Anzahl der Abfragen angeben.
2. Zweite Zeile: $n$ ganze Zahlen (im Bereich von 1 ~ 10000), die das vollständige Array darstellen, das bereits aufsteigend sortiert ist.
3. Nächste $q$ Zeilen: Jede Zeile enthält eine ganze Zahl $k$, die ein abzufragendes Element darstellt.

**Ausgabeformat:**
Für jede Abfrage soll die Start- und Endposition des Elements im Array in einer Zeile ausgegeben werden. Wenn das Element im Array nicht vorhanden ist, soll $-1$ $-1$ ausgegeben werden.

**Beispiele:**

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

Erläuterung:

- Der Bereich, in dem das Element 3 vorkommt, ist `[3, 4]`;
- Das Element 4 kommt nur einmal an Position 5 vor;
- Das Element 5 ist im Array nicht vorhanden, daher wird `-1 -1` zurückgegeben.

## Die Anwendungsstrategie der binären Suche

In diesem Problem können wir uns bei der Suche nach der "linken Grenze" und der "rechten Grenze" eines bestimmten Wertes auf die binäre Suche verlassen. Der Schlüssel ist zu verstehen, wie man den Suchbereich definiert und wie man die Zeiger entsprechend dem Vergleichsergebnis verschiebt.

- **Suche nach der "linken Grenze":**
  Das heißt, die erste Position zu finden, die größer oder gleich $k$ ist. Wir können das Array in zwei Teile aufteilen:
    - Alle Zahlen auf der linken Seite sind "kleiner" als $k$
    - Alle Zahlen auf der rechten Seite sind "größer oder gleich" $k$

- **Suche nach der "rechten Grenze":**
  Das heißt, die letzte Position zu finden, die kleiner oder gleich $k$ ist. Wir können das Array in zwei Teile aufteilen:
    - Alle Zahlen auf der linken Seite sind "kleiner oder gleich" $k$
    - Alle Zahlen auf der rechten Seite sind "größer" als $k$

Solange diese beiden Bereiche korrekt verwaltet werden, können wir mit der binären Suche schnell zu einem Ergebnis kommen.

## Empfohlene Vorlage: Vermeiden von Endlosschleifen bei der binären Suche

Im Folgenden wird eine elegante und fehlerfreie Vorlage für die binäre Suche vorgestellt. Sie stellt sicher, dass die Schleife immer dann endet, wenn die Zeiger $l$ und $r$ benachbart sind, indem sie diese schrittweise einander annähern:

Definieren Sie zwei Zeiger $l, r$, die die Invariante erfüllen: Das geschlossene Intervall $[0, l]$ gehört zum linken Teil und das geschlossene Intervall $[r, n - 1]$ gehört zum rechten Teil. $l$ und $r$ werden mit $-1$ bzw. $n$ initialisiert.

Wenn der Algorithmus beendet ist, sind $l$ und $r$ benachbart und zeigen auf den größten Wert des linken Teils bzw. den kleinsten Wert des rechten Teils.

Da die gewünschte Lösung möglicherweise nicht existiert, muss bei der Rückgabe von $l$ oder $r$ geprüft werden, ob der entsprechende Wert der gewünschte Wert ist und ob er außerhalb des Bereichs liegt.
Zum Beispiel steht $l$ für den größten Wert $\leq k$, und wir müssen `l != -1 && nums[l] == k` prüfen.

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

        // 1. Finde die Startposition von k (linke Grenze)
        //    Teile das Array in zwei Teile auf, links alle < k, rechts alle >= k.
        //    Die linke Grenze ist der kleinste Index des rechten Teils.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // Wenn r außerhalb des Bereichs liegt oder nums[r] != k, dann existiert k nicht
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r; // Speichere die linke Grenze von k

        // 2. Finde die Endposition von k (rechte Grenze)
        //    Teile das Array in zwei Teile auf, links alle <= k, rechts alle > k.
        //    Die rechte Grenze ist der größte Index des linken Teils.
        l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] <= k) l = mid;
            else r = mid;
        }

        // Da wir bereits überprüft haben, dass k existiert, muss hier nicht erneut geprüft werden
        int rightPos = l; // Rechte Grenze
        cout << leftPos << " " << rightPos << endl;
    }
    return 0;
}
```

### Warum ist es weniger fehleranfällig, so zu schreiben?

1. Diese Schreibweise hat eine streng definierte Invariante.
2. Sie kann sowohl die linke als auch die rechte Grenze finden und ist somit in allen Szenarien anwendbar.
3. Einige Schreibweisen verwenden $l == r$ als Abbruchbedingung. Wenn $l$ und $r$ sich um 1 unterscheiden, berechnet man $mid$ mit `l` oder `r` gleich. Wenn die Aktualisierung von `l` oder `r` nicht korrekt behandelt wird, wird der Suchbereich nicht verkleinert und es kommt zu einer Endlosschleife. Im Gegensatz dazu endet die hier gezeigte Schreibweise, wenn $l$ und $r$ benachbart sind, wodurch dieses Problem vermieden wird.

## STL-Lösung: `lower_bound` und `upper_bound`

Wenn Sie die von C++ STL bereitgestellten Funktionen `lower_bound` und `upper_bound` verwenden, können Sie die gleichen Dinge problemlos erledigen:

- `lower_bound(first, last, val)` gibt die "erste Position größer oder gleich val" zurück
- `upper_bound(first, last, val)` gibt die "erste Position größer als val" zurück

Nehmen wir zum Beispiel an, dass `nums = {1,2,3,4,4,4,4,4,5,5,6}` und wir wollen das Intervall finden, in dem 4 vorkommt:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    // Zeigt an, dass 4 nicht im Array existiert
    cout << "4 kommt 0 mal vor" << endl;
} else {
    cout << "Erste 4 befindet sich an " << it1 - nums.begin() << endl;
    cout << "Letzte 4 befindet sich an " << it2 - nums.begin() - 1 << endl;
    cout << "4 kommt " << it2 - it1 << " mal vor" << endl;
}
```

- `it1` zeigt auf die erste Position, deren Wert größer oder gleich 4 ist.
- `it2` zeigt auf die erste Position, deren Wert größer als 4 ist.
  Daher ist `it2 - it1` die Häufigkeit, mit der 4 im Array vorkommt; `it2 - nums.begin() - 1` ist die rechte Grenze von 4.

Diese beiden Funktionen sind besonders nützlich, wenn man Bereiche sucht oder die Häufigkeit des Auftretens zählt.

## Ergänzung

Die binäre Suche kann auch auf die Suche nach Floating-Point-Bereichen erweitert werden (z. B. zur Suche nach den Wurzeln von Gleichungen) sowie auf die ternäre Suche zur Suche nach dem Maximalwert einer unimodalen Funktion. Solange Sie das Kernprinzip " **bei jedem Schritt kann in einem sortierten Bereich die Hälfte ausgeschlossen werden**" verstehen, werden Sie feststellen, dass die binäre Suche Ihnen helfen kann, Probleme in vielen Szenarien effizient zu lösen.

## Übungsaufgaben

LeetCode 33. Search in Rotated Sorted Array

Hinweis: Verwenden Sie im ersten Schritt die binäre Suche, um den Drehpunkt zu finden, und verwenden Sie im zweiten Schritt erneut die binäre Suche, um den Zielwert zu finden.