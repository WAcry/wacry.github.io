---
title: "Schnellsortierung"
date: 2024-12-26
draft: false
description: "Analyse der Schlüsselpunkte für die korrekte Implementierung des Schnellsortierungsalgorithmus."
summary: "Analyse der Schlüsselpunkte für die korrekte Implementierung des Schnellsortierungsalgorithmus."
tags: [ "Algorithmus", "Sortieralgorithmus", "Schnellsortierung", "Teile-und-Herrsche-Algorithmus" ]
categories: [ "Algorithmen und Datenstrukturen" ]
---

# Schnellsortierung

Schnellsortierung ist ein vergleichsbasierter, instabiler Sortieralgorithmus, der das Teile-und-Herrsche-Prinzip verwendet. Die durchschnittliche Zeitkomplexität beträgt $O(n\log n)$, im schlechtesten Fall $O(n^2)$, und die Raumkomplexität ist $O(1)$. Im Folgenden wird anhand des Beispiels einer aufsteigenden Sortierung einer Integer-Zahlenfolge die Implementierungsdetails und häufige Fehler vorgestellt.

---

## Aufgabenbeschreibung

Gegeben sei eine Integer-Zahlenfolge der Länge $n$. Verwende Schnellsortierung, um diese aufsteigend zu sortieren, und gib das Ergebnis aus.

### Eingabeformat

- Die erste Zeile enthält die ganze Zahl $n$.
- Die zweite Zeile enthält $n$ ganze Zahlen, alle im Bereich $[1,10^9]$.

### Ausgabeformat

- Gib die sortierte Zahlenfolge in einer Zeile aus.

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

## Konzept der Schnellsortierung

Bei jeder Teilung der Schnellsortierung wird eine beliebige Zahl als Bezugszahl `pivot` ausgewählt (im Folgenden wird die Zahl an der mittleren Position gewählt).

Es werden linke und rechte Zeiger verwendet, die sich aufeinander zu bewegen. Der linke Zeiger `L` sucht von links nach rechts nach der ersten Zahl, die größer oder gleich `pivot` ist, und der rechte Zeiger `R` sucht von rechts nach links nach der ersten Zahl, die kleiner oder gleich `pivot` ist. Dann werden diese beiden Zahlen ausgetauscht.

Dieser Prozess wird so lange wiederholt, bis der linke und der rechte Zeiger überlappen oder der linke Zeiger eine Position größer ist als der rechte Zeiger. Dies wird als eine Iteration bezeichnet.

Nach jeder Zeigerbewegung und jedem Austausch wird sichergestellt, dass die Struktur "linker Teil ≤ pivot, rechter Teil ≥ pivot" nicht beschädigt wird, d. h. es gilt die Invariante `[left, L) <= pivot`, `(R, right] >= pivot`.

Im folgenden Beispielcode sind `left` und `right` die Grenzen des aktuell verarbeiteten abgeschlossenen Intervalls, und `pivot` wird als das Element in der Mitte des Intervalls genommen.

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

## Komplexität und `pivot`-Auswahl

Da die Schnellsortierung im schlechtesten Fall eine Komplexität von $O(n^2)$ aufweist, ist die Auswahl von `pivot` entscheidend. Wenn immer das erste oder letzte Element ausgewählt wird, ist es bei nahezu sortierten Arrays wahrscheinlich, dass der schlechteste Fall eintritt.

Zusätzlich zur Auswahl des Elements an der mittleren Position kann auch ein zufälliges Element als `pivot` ausgewählt oder der Median aus den drei Elementen links, in der Mitte und rechts als `pivot` genommen werden.

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
2. Es sollten `<` und `>` statt `<=` und `>=` verwendet werden, da sonst der linke Zeiger möglicherweise mehr als eine Position am rechten Zeiger vorbeizieht, was die Aufteilung des Arrays in zwei Teile verhindert.
3. Wenn `l >= r` gefunden wird, sollte die Schleife sofort verlassen werden, ohne weitere Austausche vorzunehmen. Andernfalls kann nicht garantiert werden, dass die Elemente auf der linken Seite nicht größer als `pivot` und die Elemente auf der rechten Seite nicht kleiner als `pivot` sind.
4. Nach jedem Austausch sollten `l++` und `r--` ausgeführt werden.
5. `pivot` nimmt tatsächlich die Zahl in der linken Mitte ein. Wenn das Array mit $l - 1$ und $l$ geteilt wird, wird bei einem Array `[1, 2]` leicht eine Endlosschleife entdeckt, da das Array immer wieder in zwei Teile der Größe 0 und 2 aufgeteilt wird. Umgekehrt muss $r$ am Ende der Schleife kleiner als $right$ sein, daher kann das Array mit $r$ und $r+1$ aufgeteilt werden. Die Leser können den Algorithmus simulieren, um zu sehen, warum das so ist. Eine andere einfache Möglichkeit, Endlosschleifen zu vermeiden, ist die zufällige Auswahl von `pivot` oder die Sonderbehandlung des Falls mit nur zwei Elementen. Analog dazu ist die Verwendung von $r$ und $l$ zur Unterscheidung des Arrays nicht möglich.
6. Außerdem ist die Verwendung von $l$, $l+1$ nicht möglich, da diese Aufteilung nicht der Definition entspricht. Wenn sich $r$ links von $l$ befindet, kann das Array mit $l$, $l+1$ nicht korrekt in zwei Teile geteilt werden, wobei die linke Seite kleiner oder gleich `pivot` und die rechte Seite größer oder gleich `pivot` ist.
7. In dieser Aufgabe wird davon ausgegangen, dass das Array nicht leer ist, sodass der Fall mit `>` nicht existiert. Es wird jedoch empfohlen, `>=` zu verwenden, da dies sicherer ist.

---

## Ergänzung

Schnellsortierung kann auch zu "Schnellauswahl" weiterentwickelt werden, um die $k$-kleinste Zahl in einem unsortierten Array in einer erwarteten Zeit von $O(n)$ zu finden. Das spezifische Konzept ist ähnlich wie bei der Schnellsortierung, wobei jedoch jedes Mal nur in einem Teilintervall weiter rekursiv aufgerufen wird, wodurch die Zeitkomplexität reduziert wird.