---
title: "Búsqueda Binaria"
date: 2024-12-24
draft: false
description: "Cómo implementar elegantemente el algoritmo de búsqueda binaria."
summary: "Cómo implementar elegantemente el algoritmo de búsqueda binaria."
tags: [ "Algoritmo", "Búsqueda Binaria", "Plantilla de Algoritmo" ]
categories: [ "Algoritmos y Estructuras de Datos" ]
---

Si un espacio de solución ordenado se divide en dos partes, donde una parte satisface una condición y la otra no, entonces se puede usar la búsqueda binaria para encontrar el punto crítico en el espacio de solución ordenado.

La idea básica de la búsqueda binaria es reducir repetidamente a la mitad el intervalo de búsqueda. Cada vez, se verifica el elemento medio. Si el elemento medio no satisface la condición, se puede eliminar la mitad del intervalo; de lo contrario, la búsqueda continúa en la otra mitad. Dado que la mitad del intervalo de búsqueda se descarta cada vez, la complejidad temporal de la búsqueda puede alcanzar $O(\log n)$.

## Problema de Ejemplo

**Descripción del Problema:**
Dado un arreglo de enteros ordenado ascendentemente de longitud $n$, y $q$ consultas. Cada consulta da un entero $k$, y necesitamos encontrar la "posición inicial" y la "posición final" de $k$ en el arreglo (los índices comienzan desde 0). Si el número no existe en el arreglo, devolver `-1 -1`.

### Formato de Entrada

1. Primera línea: dos enteros $n$ y $q$, que representan la longitud del arreglo y el número de consultas, respectivamente.
2. Segunda línea: $n$ enteros, que representan el arreglo completo, ya ordenado de forma ascendente.
3. Siguientes $q$ líneas: cada línea contiene un entero $k$, que representa un elemento de consulta.

## Rango de Datos

$1 \leq n \leq 100000$

$1 \leq q \leq 10000$

$1 \leq k \leq 10000$

### Formato de Salida

Para cada consulta, imprima las posiciones inicial y final del elemento en el arreglo en una sola línea. Si el elemento no existe en el arreglo, imprima `-1 -1`.

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

- El rango donde aparece el elemento $3$ es $[3, 4]$;
- El elemento $4$ aparece solo una vez, en la posición $5$;
- El elemento $5$ no existe en el arreglo, por lo que se devuelve $-1$ $-1$.

---

## Solución

- **Encontrar la "Posición Inicial":**
  Es decir, encontrar la primera posición que sea mayor o igual que $k$. El arreglo se puede dividir en dos partes:
    - Todos los números de la izquierda son "menores que" $k$
    - Todos los números de la derecha son "mayores o iguales que" $k$
    - La respuesta es la primera posición de la derecha

- **Encontrar la "Posición Final":**
  Es decir, encontrar la última posición que sea menor o igual que $k$. El arreglo se puede dividir en dos partes:
    - Todos los números de la izquierda son "menores o iguales que" $k$
    - Todos los números de la derecha son "mayores que" $k$
    - La respuesta es la última posición de la izquierda

---

## Plantilla Recomendada

A continuación, se muestra una plantilla de búsqueda binaria elegante y menos propensa a errores.

Defina dos punteros $l, r$, con la invariante: el intervalo cerrado $[0, l]$ pertenece a la parte izquierda, y el intervalo cerrado $[r, n - 1]$ pertenece a la parte derecha. $l$ y $r$ se inicializan a $-1$ y $n$, respectivamente.

Cuando el algoritmo termina, $l$ y $r$ son adyacentes, apuntando al último elemento de la parte izquierda y al primer elemento de la parte derecha, respectivamente.

Debido a que la solución que queremos puede no existir, si el problema no establece que definitivamente existe una solución, necesitamos verificar si `l` o `r` están fuera de los límites y si apuntan al valor correcto.

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
        //    Dividir el arreglo en dos partes, la parte izquierda es toda < k, y la parte derecha es toda >= k.
        //    La respuesta es el índice más pequeño de la parte derecha.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // Si r está fuera de los límites o nums[r] != k, significa que k no existe
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. Encontrar la posición final de k
        //    Dividir el arreglo en dos partes, la parte izquierda es toda <= k, y la parte derecha es toda > k.
        //    La respuesta es el índice más grande de la parte izquierda.
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

### Ventajas

1. Este enfoque tiene invariantes estrictamente definidos.
2. Se aplica tanto para encontrar la "posición inicial" como la "posición final" sin manejo o cambios adicionales.
3. Algunos enfoques usan `l == r` como condición de terminación. Cuando $l$ y $r$ difieren en $1$, $mid$ se calculará para ser igual a $l$ o $r$. Si no se maneja correctamente, actualizar $l$ o $r$ a $mid$ no reducirá el intervalo de búsqueda, lo que provocará un bucle infinito. En contraste, este enfoque termina cuando $l$ y $r$ son adyacentes, asegurando que $mid$ sea menor que $l$ y mayor que $r$, y actualizar $l$ o $r$ siempre reducirá el intervalo de búsqueda.

---

## STL

Si usa las funciones `lower_bound` y `upper_bound` proporcionadas por C++ STL, puede lograr lo mismo:

- `lower_bound(first, last, val)` devolverá "la primera posición que es mayor o igual que val"
- `upper_bound(first, last, val)` devolverá "la primera posición que es mayor que val"

Por ejemplo, supongamos que `nums = {1,2,3,4,4,4,4,4,5,5,6}`, y queremos saber el rango donde aparece 4:

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

- `it1` apunta a la primera posición donde el valor es mayor o igual que $4$.
- `it2` apunta a la primera posición donde el valor es mayor que $4$.
  Por lo tanto, `it2 - it1` es el número de veces que $4$ aparece en el arreglo; `it2 - nums.begin() - 1` es la posición del límite derecho de $4$.

---

## Notas Adicionales

La búsqueda binaria también se puede extender para buscar en rangos de punto flotante (como encontrar las raíces de una ecuación) y la búsqueda ternaria para encontrar los extremos de funciones unimodales.

---

## Práctica

LeetCode 33. Search in Rotated Sorted Array

Pista: Primero, use la búsqueda binaria para encontrar el punto de rotación, y luego use la búsqueda binaria para encontrar el valor objetivo.