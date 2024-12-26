---
title: "Ordenamiento Rápido"
date: 2024-12-26
draft: false
description: "Análisis de los puntos clave para implementar correctamente el algoritmo de ordenamiento rápido."
summary: "Análisis de los puntos clave para implementar correctamente el algoritmo de ordenamiento rápido."
tags: [ "Algoritmo", "Algoritmos de ordenamiento", "Ordenamiento rápido", "Algoritmo divide y vencerás" ]
categories: [ "Algoritmos y estructuras de datos" ]
---

# Ordenamiento Rápido

El ordenamiento rápido es un algoritmo de ordenamiento no estable basado en comparación, que utiliza el principio de divide y vencerás. Su complejidad de tiempo promedio es $O(n\log n)$, siendo $O(n^2)$ en el peor de los casos, y su complejidad espacial es $O(1)$. A continuación, tomaremos como ejemplo la ordenación de menor a mayor de una secuencia de números enteros para explicar los detalles de su implementación y los errores comunes.

---

## Descripción del Problema

Dada una secuencia de $n$ números enteros, ordénela de menor a mayor usando el ordenamiento rápido e imprima el resultado.

### Formato de Entrada

- La primera línea contiene un entero $n$.
- La segunda línea contiene $n$ enteros, todos en el rango $[1, 10^9]$.

### Formato de Salida

- Una línea que contenga la secuencia ordenada.

### Rango de Datos

$1 \leq n \leq 100000$

### Ejemplo de Entrada

```
5
3 1 2 4 5
```

### Ejemplo de Salida

```
1 2 3 4 5
```

---

## Idea del Ordenamiento Rápido

En cada paso de división y conquista del ordenamiento rápido, se elige un número como pivote `pivot` (a continuación, seleccionamos el número en la posición central).

Se utilizan dos punteros, izquierdo `L` y derecho `R`, que se mueven uno hacia el otro. El puntero izquierdo `L` busca de izquierda a derecha el primer número mayor o igual que `pivot`, mientras que el puntero derecho `R` busca de derecha a izquierda el primer número menor o igual que `pivot`. Luego, se intercambian estos dos números.

Este proceso se repite continuamente hasta que los punteros izquierdo y derecho se superponen o el puntero izquierdo sea mayor que el derecho en una posición. Esto se conoce como una iteración.

Después de cada movimiento e intercambio de punteros, se garantiza que la estructura "parte izquierda ≤ pivot, parte derecha ≥ pivot" no se vea afectada, es decir, se mantiene el invariante `[left, L) <= pivot`, `(R, right] >= pivot`.

En el siguiente ejemplo de código, `left` y `right` son los límites del intervalo cerrado que se está procesando actualmente, y `pivot` se toma como el elemento en el punto medio del intervalo.

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

## Complejidad y Selección del `pivot`

Dado que en el peor de los casos el ordenamiento rápido tiene una complejidad de $O(n^2)$, la elección del `pivot` es crucial. Si siempre se selecciona el primer o el último elemento, es probable que se produzca el peor de los casos en arreglos casi ordenados.

Además de seleccionar el elemento en la posición central, también se puede seleccionar aleatoriamente un elemento como `pivot`, o tomar la mediana de los elementos de la izquierda, el centro y la derecha como `pivot`.

---

## Ejemplos Comunes de Errores

El siguiente código contiene varios errores comunes.

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

**Análisis de Errores:**

1. `pivot` debería ser un número del arreglo, no un índice.
2. Se utilizan `<=` y `>=` en lugar de `<` y `>`, de lo contrario el puntero izquierdo podría avanzar más de una posición después del puntero derecho, lo que impediría la división correcta del arreglo en dos partes.
3. Una vez que se encuentra que `l >= r`, el ciclo debería salir inmediatamente, sin realizar más intercambios. De lo contrario, no se garantiza que los elementos de la izquierda no sean mayores que `pivot`, y que los elementos de la derecha no sean menores que `pivot`.
4. Después de cada intercambio, deberían ejecutarse `l++` y `r--`.
5. `pivot` en realidad toma el número que está ligeramente a la izquierda del centro. Si se usa $l - 1$ y $l$ para dividir el arreglo, considerando el arreglo `[1, 2]`, no es difícil ver que esto provocaría un bucle infinito, dividiendo constantemente el arreglo en dos partes de tamaño 0 y 2. Por el contrario, cuando termina el ciclo, $r$ debe ser menor que $right$, por lo que se pueden usar $r$ y $r+1$ para dividir el arreglo. El lector puede simular el proceso del algoritmo para ver por qué. Otra forma sencilla de evitar el bucle infinito es seleccionar un `pivot` aleatorio o manejar especialmente el caso en que solo hay dos elementos. De manera similar, no se puede usar $r$ y $l$ para diferenciar el arreglo.
6. Además, tampoco se puede usar $l$, $l+1$, ya que esta división no se ajusta a la definición. Cuando $r$ está a la izquierda de $l$, usar $l$, $l+1$ no puede dividir correctamente el arreglo en dos partes, donde la parte izquierda es menor o igual que `pivot`, y la parte derecha es mayor o igual que `pivot`.
7. Este problema asume que el arreglo no está vacío, por lo que no existe el caso `>`. Sin embargo, es recomendable usar `>=`, es más seguro.

---

## Complemento

El ordenamiento rápido también puede evolucionar en "selección rápida", que encuentra el k-ésimo número más pequeño en un arreglo desordenado en un tiempo esperado de $O(n)$. La idea específica es similar a la del ordenamiento rápido, solo que cada vez solo continúa la recursión en un subintervalo, lo que reduce la complejidad del tiempo.