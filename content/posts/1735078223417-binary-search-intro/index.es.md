---
title: "Búsqueda Binaria"
date: 2024-12-24
draft: false
description: "Cómo implementar elegantemente el algoritmo de búsqueda binaria en enteros"
tags: [ "Algoritmos", "Búsqueda Binaria", "Plantillas de Algoritmos" ]
categories: [ "Algoritmos y Estructuras de Datos" ]
---
{{< katex >}}

# Búsqueda Binaria

En una secuencia ordenada, se puede utilizar la búsqueda binaria para encontrar un elemento específico rápidamente. Comparado con la complejidad temporal de $O(n)$ de la búsqueda lineal, la búsqueda binaria solo necesita un tiempo de $O(\log n)$, por lo que es muy eficiente en casos de grandes volúmenes de datos.

## La idea central de la búsqueda binaria

La idea básica de la búsqueda binaria es dividir continuamente el intervalo de búsqueda por la mitad. En cada comparación, se compara el elemento del punto medio con el valor objetivo. Si el elemento del punto medio no cumple la condición, se puede excluir la mitad del intervalo; de lo contrario, se continúa la búsqueda en la otra mitad del intervalo. Dado que cada vez se descarta la mitad del intervalo de búsqueda, la complejidad temporal de búsqueda puede alcanzar $O(\log n)$.

La búsqueda binaria es muy útil para problemas donde " **las soluciones factibles se pueden dividir en un intervalo ordenado (que satisface la condición) y otro intervalo ordenado (que no satisface la condición)** ". Por ejemplo:

- Encontrar si existe un elemento en una matriz ordenada.
- Encontrar la "primera posición" o la "última posición" en la que aparece un número.

## Ejemplo de problema: Encontrar la posición inicial y final de un elemento

**Descripción del problema:**
Dado un array de enteros de longitud $n$ ordenado ascendentemente y $q$ consultas. Cada consulta proporciona un entero $k$, necesitamos encontrar la "posición inicial" y la "posición final" de $k$ en la matriz (los índices comienzan desde 0). Si el número no existe en el array, devolver $-1$ $-1$.

**Formato de entrada:**

1. Primera línea: dos enteros $n$ y $q$, que representan la longitud del array y el número de consultas respectivamente.
2. Segunda línea: $n$ enteros (en el rango de 1 ~ 10000), que representan el array completo, que ya está ordenado en orden ascendente.
3. Siguientes $q$ líneas: cada línea contiene un entero $k$, que representa un elemento de consulta.

**Formato de salida:**
Para cada consulta, imprimir en una línea la posición inicial y final del elemento en el array. Si el elemento no existe en el array, imprimir $-1$ $-1$.

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

Explicación:

- El rango donde aparece el elemento 3 es `[3, 4]`;
- El elemento 4 aparece solo una vez, en la posición 5;
- El elemento 5 no existe en el array, por lo que devuelve `-1 -1`.

## Ideas de aplicación de la búsqueda binaria

En este problema, para encontrar el "límite izquierdo" y el "límite derecho" de un valor dado, podemos recurrir a la búsqueda binaria. La clave es comprender cómo definir el intervalo de búsqueda y cómo mover los punteros de acuerdo con el resultado de la comparación.

- **Encontrar el "límite izquierdo":**
    Es decir, encontrar la primera posición mayor o igual a $k$. El array se puede dividir en dos partes:
    - Todos los números de la izquierda son "menores" que $k$.
    - Todos los números de la derecha son "mayores o iguales" que $k$.

- **Encontrar el "límite derecho":**
    Es decir, encontrar la última posición menor o igual a $k$. El array se puede dividir en dos partes:
    - Todos los números de la izquierda son "menores o iguales" que $k$.
    - Todos los números de la derecha son "mayores" que $k$.

Siempre que se puedan mantener correctamente estos dos intervalos, se pueden obtener los resultados rápidamente mediante la búsqueda binaria.

## Plantilla recomendada: Escritura de búsqueda binaria para evitar bucles infinitos

La siguiente es una plantilla de búsqueda binaria elegante y menos propensa a errores. Al permitir que $l$ y $r$ converjan gradualmente, garantiza que el bucle termine cuando ambos son adyacentes:

Definir dos punteros $l, r$, con invariante: el intervalo cerrado $[0, l]$ pertenece a la mitad izquierda y el intervalo cerrado $[r, n - 1]$ pertenece a la mitad derecha. $l$ y $r$ se inicializan en $-1$ y $n$.

Cuando el algoritmo finaliza, $l$ y $r$ son adyacentes, apuntando al valor máximo de la mitad izquierda y al valor mínimo de la mitad derecha, respectivamente.

Dado que la solución que queremos podría no existir, al devolver $l$ o $r$, es necesario verificar si el valor correspondiente es el valor que queremos y si está fuera de rango. Por ejemplo, $l$ representa el valor máximo $\leq k$, y necesitamos verificar `l != -1 && nums[l] == k`

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

        // 1. Buscar la posición inicial de k (límite izquierdo)
        //    Dividir el array en dos partes, la izquierda toda < k, la derecha toda >= k.
        //    El límite izquierdo es el índice mínimo de la parte derecha.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // Si r está fuera de rango o nums[r] != k, significa que k no existe
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r; // Registrar el límite izquierdo de k

        // 2. Buscar la posición final de k (límite derecho)
        //    Dividir el array en dos partes, la izquierda toda <= k, la derecha toda > k.
        //    El límite derecho es el índice máximo de la parte izquierda.
        l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] <= k) l = mid;
            else r = mid;
        }

        // Dado que ya hemos verificado que k existe, no es necesario verificarlo de nuevo aquí
        int rightPos = l; // Límite derecho
        cout << leftPos << " " << rightPos << endl;
    }
    return 0;
}
```

### ¿Por qué esta forma de escribir es menos propensa a errores?

1. Esta forma de escribir tiene invariantes estrictamente definidos.
2. Puede encontrar tanto el límite izquierdo como el límite derecho, y puede aplicarse a todos los escenarios.
3. Algunas formas de escribir usan $l == r$ como condición de terminación. Cuando $l$ y $r$ difieren en 1, se calculará $mid$ y será igual a `l` o `r`. Si no se maneja correctamente y se actualiza `l` o `r` a `mid`, el intervalo de búsqueda no se reducirá, lo que provocará un bucle infinito. Por el contrario, esta forma de escribir termina cuando $l$ y $r$ son adyacentes, evitando este problema.

## Solución con STL: `lower_bound` y `upper_bound`

Si se utilizan las funciones `lower_bound` y `upper_bound` proporcionadas por C++ STL, también se puede lograr lo mismo fácilmente:

- `lower_bound(first, last, val)` devuelve "la primera posición mayor o igual que val"
- `upper_bound(first, last, val)` devuelve "la primera posición mayor que val"

Por ejemplo, supongamos que `nums = {1,2,3,4,4,4,4,4,5,5,6}`, y queremos saber el intervalo donde aparece 4:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    // Indica que 4 no existe en el array
    cout << "4 aparece 0 veces" << endl;
} else {
    cout << "El primer 4 está en " << it1 - nums.begin() << endl;
    cout << "El último 4 está en " << it2 - nums.begin() - 1 << endl;
    cout << "4 aparece " << it2 - it1 << " veces" << endl;
}
```

- `it1` apunta a la primera posición con un valor mayor o igual que 4.
- `it2` apunta a la primera posición con un valor mayor que 4.
Por lo tanto, `it2 - it1` es el número de veces que aparece 4 en el array; `it2 - nums.begin() - 1` es el límite derecho de 4.

Estas dos funciones son especialmente convenientes para buscar intervalos o contar el número de ocurrencias.

## Complemento

La búsqueda binaria también se puede extender a la búsqueda en el rango de números de punto flotante (como encontrar la raíz de una ecuación) y la búsqueda ternaria para encontrar el valor máximo de una función unimodal. Mientras comprendas el principio central de " **en un intervalo ordenado, siempre se puede descartar la mitad** ", encontrarás que la búsqueda binaria puede ayudarte a resolver problemas de manera eficiente en muchos escenarios.

## Ejercicio después de clase

LeetCode 33. Search in Rotated Sorted Array

Pista: En el primer paso, utiliza la búsqueda binaria para encontrar el punto de rotación y en el segundo paso, vuelve a utilizar la búsqueda binaria para encontrar el valor objetivo.