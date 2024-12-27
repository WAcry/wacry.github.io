---
title: "Quicksort"
date: 2024-12-26
draft: false
description: "Analyse der wichtigsten Punkte für die korrekte Implementierung des Quicksort-Algorithmus."
summary: "Analyse der wichtigsten Punkte für die korrekte Implementierung des Quicksort-Algorithmus."
tags: [ "Algorithmus", "Sortieralgorithmus", "Quicksort", "Divide-and-Conquer-Algorithmus" ]
categories: [ "Algorithmen und Datenstrukturen" ]
---

# Quicksort

Quicksort ist ein vergleichsbasierter, nicht stabiler Sortieralgorithmus, der auf dem Divide-and-Conquer-Prinzip basiert. Die durchschnittliche Zeitkomplexität beträgt $O(n\log n)$, im schlechtesten Fall $O(n^2)$, und die Raumkomplexität ist $O(1)$. Im Folgenden wird die Implementierung anhand eines Beispiels zum Sortieren einer Integer-Sequenz in aufsteigender Reihenfolge erläutert, einschließlich Details und häufiger Fehler.

---

## Aufgabenbeschreibung

Gegeben ist eine Integer-Sequenz der Länge $n$. Sortiere diese mit Quicksort in aufsteigender Reihenfolge und gib das Ergebnis aus.

### Eingabeformat

- Die erste Zeile enthält die ganze Zahl $n$.
- Die zweite Zeile enthält $n$ ganze Zahlen im Bereich $[1,10^9]$.

### Ausgabeformat

- Eine Zeile mit der sortierten Sequenz.

### Datenbereich

$1 \leq n \leq 100000$

### Eingabebeispiel

```
5
3 1 2 4 5
```

### Ausgabebeispiel

```
1 2 3 4 5
```

---

## Quicksort-Ansatz

Bei jeder Divide-and-Conquer-Operation in Quicksort wird eine beliebige Zahl als Pivot-Element `pivot` ausgewählt (im Folgenden wird die Zahl in der Mitte gewählt).

Zwei Zeiger, ein linker Zeiger `L` und ein rechter Zeiger `R`, bewegen sich aufeinander zu. Der linke Zeiger `L` sucht von links nach rechts die erste Zahl, die größer oder gleich `pivot` ist, und der rechte Zeiger `R` sucht von rechts nach links die erste Zahl, die kleiner oder gleich `pivot` ist. Dann werden diese beiden Zahlen vertauscht.

Dieser Vorgang wird so lange wiederholt, bis sich der linke und der rechte Zeiger überlappen oder der linke Zeiger um eine Position größer ist als der rechte Zeiger. Dies wird als eine Iteration bezeichnet.

Nach jeder Zeigerbewegung und jedem Tausch wird sichergestellt, dass die Struktur "linker Teil ≤ pivot, rechter Teil ≥ pivot" nicht verletzt wird, d. h. es gibt die Invariante `[left, L) <= pivot`, `(R, right] >= pivot`.

Im folgenden Beispielcode sind `left` und `right` die Grenzen des aktuellen geschlossenen Intervalls, und `pivot` ist das Element in der Mitte des Intervalls.

```cpp
#include <bits/stdc++.h>
using namespace std;

void quickSort(vector<int> &a, int left, int right) {
    if (left >= right) return;
    
    int pivot = a[(left + right) / 2];
    int l = left, r = right;
    
    while (true) {
        while (a[l] < pivot) l++;
        while (a[r] > pivot) r--;
        if (l >= r) break;
        swap(a[l], a[r]);
        l++; r--;
    }
    
    quickSort(a, left, r);
    quickSort(a, r + 1, right);
}

int main() {
    int n; cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    
    quickSort(a, 0, n - 1);
    
    for (int i = 0; i < n; i++) cout << a[i] << " ";
    return 0;
}
```

---

## Komplexität und Auswahl des `pivot`

Da Quicksort im schlechtesten Fall eine Komplexität von $O(n^2)$ hat, ist die Wahl des `pivot` entscheidend. Wenn immer das erste oder letzte Element gewählt wird, tritt bei fast sortierten Arrays mit hoher Wahrscheinlichkeit der schlechteste Fall ein.

Neben der Wahl des Elements in der Mitte kann auch ein zufälliges Element als `pivot` gewählt werden, oder der Median aus dem linken, mittleren und rechten Element.

---

## Häufige Fehlerbeispiele

Der folgende Code enthält mehrere häufige Fehler.

```cpp
#include <bits/stdc++.h>
using namespace std;

void quickSort(vector<int> &a, int left, int right) {
    if (left == right) return; // 7

    int pivot = (left + right) >> 1; // 1
    int l = left, r = right;

    while (true) {
        while (a[l] <= pivot) l++; // 2
        while (a[r] >= pivot) r--; // 2
        swap(a[l], a[r]);
        if (l >= r) break; // 3
        // 4
    }

    quickSort(a, left, l - 1); // 5, 6
    quickSort(a, l, right);    // 5, 6
}

int main() {
    int n; cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    quickSort(a, 0, n - 1);

    for (int i = 0; i < n; i++) cout << a[i] << " ";

    return 0;
}
```

**Fehleranalyse:**

1. `pivot` sollte eine Zahl im Array sein, nicht ein Index.
2. Verwende `<` und `>` anstelle von `<=` und `>=`, da sonst der linke Zeiger möglicherweise mehr als eine Position über den rechten Zeiger hinausgeht, wodurch das Array nicht in zwei Teile geteilt werden kann.
3. Wenn `l >= r` gefunden wird, sollte die Schleife sofort verlassen werden, ohne weitere Tauschoperationen durchzuführen. Andernfalls kann nicht garantiert werden, dass die Elemente auf der linken Seite nicht größer als `pivot` und die Elemente auf der rechten Seite nicht kleiner als `pivot` sind.
4. Nach jedem Tausch sollten `l++` und `r--` ausgeführt werden.
5. `pivot` ist eigentlich die Zahl in der Mitte, die nach links verschoben ist. Wenn das Array also mit $l - 1$ und $l$ geteilt wird, führt dies bei einem Array wie `[1, 2]` zu einer Endlosschleife, da das Array immer wieder in zwei Teile der Größe 0 und 2 aufgeteilt wird. Ähnlich verhält es sich, wenn das Array mit $r$ und $l$ geteilt wird. Wenn die Schleife jedoch beendet ist, ist $r$ immer kleiner als $right$, sodass das Array mit $r$ und $r+1$ geteilt werden kann. Der Leser kann den Algorithmus simulieren, um zu sehen, warum. Eine andere einfache Möglichkeit, Endlosschleifen zu vermeiden, ist die zufällige Auswahl von `pivot` oder die Sonderbehandlung von Arrays mit nur zwei Elementen.
6. Außerdem ist die Verwendung von $l$, $l+1$ nicht möglich, da diese Aufteilung nicht der Definition entspricht. Wenn $r$ links von $l$ liegt, kann das Array mit $l$, $l+1$ nicht korrekt in zwei Teile aufgeteilt werden, wobei der linke Teil kleiner oder gleich `pivot` und der rechte Teil größer oder gleich `pivot` ist.
7. In dieser Aufgabe wird davon ausgegangen, dass das Array nicht leer ist, sodass der Fall `>` nicht existiert. Es wird jedoch empfohlen, `>=` zu verwenden, da dies sicherer ist.

---

## Ergänzung

Quicksort kann auch zu "Quickselect" weiterentwickelt werden, um das $k$-kleinste Element in einem unsortierten Array in einer erwarteten Zeit von $O(n)$ zu finden. Die Idee ist ähnlich wie bei Quicksort, nur dass die Rekursion jedes Mal nur in einem Teilintervall fortgesetzt wird, wodurch die Zeitkomplexität reduziert wird.