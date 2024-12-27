---
title: "Ordenamiento Rápido"
date: 2024-12-26
draft: false
description: "Análisis de los puntos clave para implementar correctamente el algoritmo de ordenamiento rápido."
summary: "Análisis de los puntos clave para implementar correctamente el algoritmo de ordenamiento rápido."
tags: [ "Algoritmo", "Algoritmos de Ordenamiento", "Ordenamiento Rápido", "Algoritmo Divide y Vencerás" ]
categories: [ "Algoritmos y Estructuras de Datos" ]
---

# Ordenamiento Rápido

El ordenamiento rápido es un algoritmo de ordenamiento no estable basado en comparaciones, que utiliza la estrategia de divide y vencerás. Su complejidad temporal promedio es de $O(n\log n)$, en el peor caso es de $O(n^2)$, y su complejidad espacial es de $O(1)$. A continuación, se presenta un ejemplo de cómo ordenar una secuencia de números enteros de menor a mayor, junto con los detalles de implementación y errores comunes.

---

## Descripción del Problema

Dado un arreglo de $n$ números enteros, ordénelo de menor a mayor utilizando el algoritmo de ordenamiento rápido y muestre el resultado.

### Formato de Entrada

- La primera línea contiene el entero $n$.
- La segunda línea contiene $n$ enteros, todos dentro del rango $[1,10^9]$.

### Formato de Salida

- Una línea que contiene la secuencia ordenada.

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

En cada paso de divide y vencerás, el ordenamiento rápido elige un número como pivote (`pivot`, en adelante, se elige el número en la posición central).

Se utilizan dos punteros, uno izquierdo `L` y uno derecho `R`, que se mueven en direcciones opuestas. El puntero izquierdo `L` busca de izquierda a derecha el primer número mayor o igual que `pivot`, y el puntero derecho `R` busca de derecha a izquierda el primer número menor o igual que `pivot`. Luego, se intercambian estos dos números.

Este proceso se repite hasta que los punteros se superponen o el puntero izquierdo está una posición a la derecha del puntero derecho. Esto se conoce como una iteración.

Después de cada movimiento e intercambio de punteros, se garantiza que la estructura "parte izquierda ≤ pivote, parte derecha ≥ pivote" no se rompa, es decir, se mantiene el invariante `[left, L) <= pivot`, `(R, right] >= pivot`.

En el siguiente código de ejemplo, `left` y `right` son los límites del intervalo cerrado que se está procesando actualmente, y `pivot` se toma como el elemento en el punto medio del intervalo.

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

Dado que el ordenamiento rápido tiene una complejidad de $O(n^2)$ en el peor caso, la elección del `pivot` es crucial. Si siempre se elige el primer o el último elemento, es muy probable que se produzca el peor caso en un arreglo casi ordenado.

Además de tomar el elemento en la posición central, también se puede elegir un elemento aleatorio como `pivot`, o tomar la mediana de los tres elementos: el izquierdo, el central y el derecho.

---

## Ejemplos de Errores Comunes

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

1. `pivot` debe ser un número del arreglo, no un índice.
2. Se deben usar `<` y `>` en lugar de `<=` y `>=`, de lo contrario, el puntero izquierdo podría sobrepasar al puntero derecho por más de una posición, lo que impediría dividir el arreglo en dos partes.
3. Después de encontrar `l >= r`, se debe salir del bucle inmediatamente, sin realizar más intercambios. De lo contrario, no se garantiza que los elementos de la izquierda no sean mayores que `pivot` y que los elementos de la derecha no sean menores que `pivot`.
4. Después de cada intercambio, se deben ejecutar `l++` y `r--`.
5. `pivot` en realidad toma el número del medio hacia la izquierda. Por lo tanto, si se usa $l - 1$ y $l$ para dividir el arreglo, considerando el arreglo `[1, 2]`, no es difícil ver que esto causará un bucle infinito, dividiendo continuamente el arreglo en dos partes de tamaño 0 y 2. De manera similar, usar $r$ y $l$ para dividir el arreglo tampoco funciona. Por el contrario, al final de una iteración, $r$ es necesariamente menor que $right$, por lo que se puede usar $r$ y $r+1$ para dividir el arreglo. El lector puede simular el proceso del algoritmo para ver por qué. Otra forma sencilla de evitar bucles infinitos es elegir un `pivot` aleatorio o manejar especialmente el caso de que solo haya dos elementos.
6. Además, usar $l$, $l+1$ tampoco funciona, porque esta división no se ajusta a la definición. Cuando $r$ está a la izquierda de $l$, usar $l$, $l+1$ no puede dividir correctamente el arreglo en dos partes: una izquierda menor o igual que `pivot` y una derecha mayor o igual que `pivot`.
7. Este problema asume que el arreglo no está vacío, por lo que no existe el caso de `>`. Sin embargo, se recomienda usar `>=`, es más seguro.

---

## Complemento

El ordenamiento rápido también se puede convertir en "selección rápida", que puede encontrar el $k$-ésimo número más pequeño en un arreglo desordenado en un tiempo esperado de $O(n)$. La idea específica es similar al ordenamiento rápido, pero solo se continúa la recursión en un subintervalo cada vez, lo que reduce la complejidad temporal.