---
title: "Búsqueda Binaria"
date: 2024-12-24
draft: false
description: "Cómo implementar elegantemente el algoritmo de búsqueda binaria."
summary: "Cómo implementar elegantemente el algoritmo de búsqueda binaria."
tags: [ "algoritmo", "búsqueda binaria", "plantilla de algoritmo" ]
categories: [ "Algoritmos y Estructuras de Datos" ]
---

Si un espacio de solución ordenado se divide en dos partes, donde una parte satisface la condición y la otra no, entonces se puede usar la búsqueda binaria para encontrar el punto crítico en el espacio de solución ordenado.

La idea básica de la búsqueda binaria es dividir continuamente el intervalo de búsqueda por la mitad. En cada verificación, se inspecciona el elemento del punto medio. Si el elemento del punto medio no satisface la condición, se puede eliminar la mitad del intervalo; de lo contrario, la búsqueda continúa en la otra mitad del intervalo. Dado que la mitad del intervalo de búsqueda se descarta cada vez, la complejidad de tiempo de la búsqueda puede alcanzar $O(\log n)$.

## Ejemplo

**Descripción del problema:**
Dado un arreglo de enteros de longitud $n$ ordenado de forma ascendente y $q$ consultas. Cada consulta proporciona un entero $k$, y necesitamos encontrar la "posición inicial" y la "posición final" de $k$ en el arreglo (los índices comienzan desde 0). Si el número no existe en el arreglo, se debe devolver `-1 -1`.

### Formato de entrada

1. Primera línea: dos enteros $n$ y $q$, que representan la longitud del arreglo y el número de consultas, respectivamente.
2. Segunda línea: $n$ enteros, que representan el arreglo completo, que ya está ordenado en orden ascendente.
3. Siguientes $q$ líneas: cada línea contiene un entero $k$, que representa un elemento de consulta.

## Rango de datos

$1 \leq n \leq 100000$

$1 \leq q \leq 10000$

$1 \leq k \leq 10000$

### Formato de salida

Para cada consulta, imprima en una línea la posición inicial y final del elemento en el arreglo. Si el elemento no existe en el arreglo, imprima `-1 -1`.

**Ejemplo:**

```
Entrada:
6 3
1 2 2 3 3 4
3
4
5

Salida:
3 4
5 5
-1 -1
```

**Explicación:**

- El rango en el que aparece el elemento $3$ es $[3, 4]$.
- El elemento $4$ aparece solo una vez, en la posición $5$.
- El elemento $5$ no existe en el arreglo, por lo que se devuelve $-1$ $-1$.

---

## Solución

- **Encontrar la "posición inicial":**
  Es decir, encontrar la primera posición mayor o igual a $k$. Se puede dividir el arreglo en dos partes:
    - Todos los números a la izquierda son "menores" que $k$.
    - Todos los números a la derecha son "mayores o iguales" que $k$.
    - La respuesta es la primera posición de la derecha.

- **Encontrar la "posición final":**
  Es decir, encontrar la última posición menor o igual a $k$. Se puede dividir el arreglo en dos partes:
    - Todos los números a la izquierda son "menores o iguales" que $k$.
    - Todos los números a la derecha son "mayores" que $k$.
    - La respuesta es la última posición de la izquierda.

---

## Plantilla recomendada

A continuación, se presenta una plantilla de búsqueda binaria elegante y fácil de usar. Al hacer que $l$ y $r$ se acerquen gradualmente, garantiza que el bucle termine cuando estén adyacentes:

Definimos dos punteros $l, r$, con la invariante: el intervalo cerrado $[0, l]$ pertenece a la mitad izquierda, y el intervalo cerrado $[r, n - 1]$ pertenece a la mitad derecha. $l$ y $r$ se inicializan como $-1$ y $n$ respectivamente.

Cuando el algoritmo termina, $l$ y $r$ son adyacentes, apuntando al último elemento de la mitad izquierda y al primer elemento de la mitad derecha respectivamente.

Como la solución que buscamos puede no existir, si el problema no establece que la solución existe, necesitamos comprobar si `l` o `r` están fuera de rango y si apuntan al valor correcto.

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

        // 1. Encontrar la posición inicial de k
        //    Dividir el arreglo en dos partes, la izquierda donde todos son < k, la derecha donde todos son >= k.
        //    La respuesta es el índice mínimo de la mitad derecha.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // Si r está fuera de rango o nums[r] != k, entonces k no existe
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. Encontrar la posición final de k
        //    Dividir el arreglo en dos partes, la izquierda donde todos son <= k, la derecha donde todos son > k.
        //    La respuesta es el índice máximo de la mitad izquierda.
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

### Por qué escribirlo así

1. Esta escritura tiene invariantes estrictamente definidos.
2. Se aplica tanto para encontrar la "posición inicial" como la "posición final", sin necesidad de tratamiento ni cambios adicionales.
3. Algunas formas de escribir utilizan `l == r` como condición de terminación. Cuando $l$ y $r$ difieren en $1$, se calculará $mid$ y será igual a $l$ o $r$. Si no se trata correctamente, al actualizar $l$ o $r$ a $mid$, el intervalo de búsqueda no se reducirá, lo que provocará un bucle infinito. Por el contrario, esta escritura termina cuando $l$ y $r$ son adyacentes, lo que garantiza que $mid$ sea menor que $l$ y mayor que $r$, y que el intervalo de búsqueda se reducirá al actualizar $l$ o $r$.

---

## STL

Si usamos las funciones `lower_bound` y `upper_bound` proporcionadas por C++ STL, también podemos lograr lo mismo:

- `lower_bound(first, last, val)` devuelve "la primera posición mayor o igual que val"
- `upper_bound(first, last, val)` devuelve "la primera posición mayor que val"

Por ejemplo, supongamos que `nums = {1,2,3,4,4,4,4,4,5,5,6}`, y queremos saber el rango en el que aparece 4:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    cout << "4 aparece 0 veces" << endl;
} else {
    cout << "el primer 4 está en " << it1 - nums.begin() << endl;
    cout << "el último 4 está en " << it2 - nums.begin() - 1 << endl;
    cout << "4 aparece " << it2 - it1 << " veces" << endl;
}
```

- `it1` apunta a la primera posición cuyo valor es mayor o igual que $4$.
- `it2` apunta a la primera posición cuyo valor es mayor que $4$.
  Así que `it2 - it1` es la cantidad de veces que $4$ aparece en el arreglo; `it2 - nums.begin() - 1` es el límite derecho de $4$.

---

## Complemento

La búsqueda binaria también se puede extender a la búsqueda en el rango de números de punto flotante (como la búsqueda de raíces de ecuaciones), así como a la búsqueda ternaria para encontrar el máximo o mínimo de funciones unimodales.
Siempre que comprendas el principio central de "**en un intervalo ordenado, la mitad siempre se puede descartar**", descubrirás que la búsqueda binaria puede ayudarte a resolver problemas de manera eficiente en muchos escenarios.

---

## Ejercicios

LeetCode 33. Search in Rotated Sorted Array

Sugerencia: El primer paso es usar la búsqueda binaria para encontrar el punto de rotación, y el segundo paso es usar la búsqueda binaria para encontrar el valor objetivo.