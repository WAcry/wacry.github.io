---
title: "Búsqueda Binaria"
date: 2024-12-24
draft: false
description: "Cómo implementar elegantemente el algoritmo de búsqueda binaria en enteros."
summary: "Cómo implementar elegantemente el algoritmo de búsqueda binaria en enteros."
tags: [ "Algoritmo", "Búsqueda Binaria", "Plantilla de Algoritmo" ]
categories: [ "Algoritmos y Estructuras de Datos" ]
---

{{< katex >}}

# Búsqueda Binaria

Si un espacio de soluciones ordenado se divide en dos partes, donde una parte satisface una condición y la otra no, entonces se puede utilizar la búsqueda binaria para encontrar el punto crítico en el espacio de soluciones ordenado.

La idea básica de la búsqueda binaria es dividir continuamente el intervalo de búsqueda por la mitad. En cada verificación, se examina el elemento medio; si el elemento medio no cumple la condición, se puede descartar la mitad del intervalo; de lo contrario, la búsqueda continúa en la otra mitad del intervalo. Debido a que en cada paso se descarta la mitad del intervalo de búsqueda, la complejidad temporal de la búsqueda puede alcanzar \\(O(\log n)\\).

## Ejemplo de Problema

**Descripción del problema:**
Dado un arreglo de enteros de longitud \\(n\\) ordenado ascendentemente, y \\(q\\) consultas. Cada consulta da un entero \\(k\\), necesitamos encontrar la "posición inicial" y "posición final" de \\(k\\) en el arreglo (los índices comienzan desde 0). Si el número no existe en el arreglo, devolver \\(-1\\) \\(-1\\).

### Formato de Entrada

1. Primera línea: dos enteros \\(n\\) y \\(q\\), representando la longitud del arreglo y el número de consultas, respectivamente.
2. Segunda línea: \\(n\\) enteros, representando el arreglo completo, ordenado de forma ascendente.
3. Siguientes \\(q\\) líneas: cada línea contiene un entero \\(k\\), representando un elemento de consulta.

## Rango de Datos

\\(1 \leq n \leq 100000\\)

\\(1 \leq q \leq 10000\\)

\\(1 \leq k \leq 10000\\)

### Formato de Salida

Para cada consulta, imprime en una línea la posición inicial y final del elemento en el arreglo. Si el elemento no existe en el arreglo, imprime `-1 -1`.

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

- El rango de aparición del elemento \\(3\\) es \\([3, 4]\\);
- El elemento \\(4\\) solo aparece una vez, en la posición \\(5\\);
- El elemento \\(5\\) no existe en el arreglo, por lo tanto se devuelve \\(-1\\) \\(-1\\).

---

## Solución

- **Buscar la "posición inicial":**
  Es decir, buscar la primera posición mayor o igual a \\(k\\). Podemos dividir el arreglo en dos partes:
    - Todos los números a la izquierda son "menores" que \\(k\\).
    - Todos los números a la derecha son "mayores o iguales" que \\(k\\).
    - La respuesta es la primera posición de la derecha.

- **Buscar la "posición final":**
  Es decir, buscar la última posición menor o igual a \\(k\\). Podemos dividir el arreglo en dos partes:
    - Todos los números a la izquierda son "menores o iguales" que \\(k\\).
    - Todos los números a la derecha son "mayores" que \\(k\\).
    - La respuesta es la última posición de la izquierda.

---

## Plantilla Recomendada

A continuación se muestra una plantilla de búsqueda binaria elegante y fácil de usar, que evita errores. Al hacer que \\(l\\) y \\(r\\) se acerquen gradualmente, garantiza que el bucle termine cuando ambos estén adyacentes:

Definimos dos punteros \\(l, r\\), con la invariante: el intervalo cerrado \\([0, l]\\) pertenece a la mitad izquierda, y el intervalo cerrado \\([r, n - 1]\\) pertenece a la mitad derecha. \\(l\\) y \\(r\\) se inicializan en \\(-1\\) y \\(n\\), respectivamente.

Cuando el algoritmo termina, \\(l\\) y \\(r\\) son adyacentes, apuntando respectivamente al último elemento de la mitad izquierda y al primer elemento de la mitad derecha.

Dado que la solución que buscamos podría no existir, si el problema no especifica que la solución siempre existe, debemos verificar si `l` o `r` se han salido de los límites o si apuntan al valor correcto.

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

        // 1. Buscar la posición inicial de k
        //    Dividir el arreglo en dos partes, izquierda < k, derecha >= k.
        //    La respuesta es el índice mínimo de la mitad derecha.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // Si r se sale de los límites o nums[r] != k, significa que k no existe
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. Buscar la posición final de k
        //    Dividir el arreglo en dos partes, izquierda <= k, derecha > k.
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

1. Esta escritura tiene invariantes estrictamente definidas.
2. Es aplicable tanto para encontrar la "posición inicial" como la "posición final", sin necesidad de procesamiento o cambios adicionales.
3. Algunas escrituras usan `l == r` como condición de terminación. Cuando \\(l\\) y \\(r\\) difieren en \\(1\\), se calculará un \\(mid\\) igual a \\(l\\) o \\(r\\). Si esto no se gestiona correctamente, y se actualiza \\(l\\) o \\(r\\) con \\(mid\\), el intervalo de búsqueda no se reducirá y conducirá a un bucle infinito. En cambio, esta escritura termina cuando \\(l\\) y \\(r\\) son adyacentes, garantizando que \\(mid\\) sea menor que \\(l\\) y mayor que \\(r\\), y que el intervalo de búsqueda se reduzca al actualizar \\(l\\) o \\(r\\).

---

## STL

Si se usan las funciones `lower_bound` y `upper_bound` proporcionadas por la STL de C++, también se puede lograr lo mismo:

- `lower_bound(first, last, val)` devuelve "la primera posición mayor o igual a val"
- `upper_bound(first, last, val)` devuelve "la primera posición mayor que val"

Por ejemplo, supongamos `nums = {1,2,3,4,4,4,4,4,5,5,6}`, y queremos saber el intervalo donde aparece el 4:

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

- `it1` apunta a la primera posición cuyo valor es mayor o igual a \\(4\\).
- `it2` apunta a la primera posición cuyo valor es mayor que \\(4\\).  
  Por lo tanto, `it2 - it1` es el número de veces que aparece \\(4\\) en el arreglo; `it2 - nums.begin() - 1` es el límite derecho de \\(4\\).

---

## Adicional

La búsqueda binaria también se puede extender a la búsqueda en rangos de números de punto flotante (como encontrar las raíces de una ecuación), así como a la búsqueda ternaria para encontrar los extremos de una función unimodal.
Una vez que entiendas el principio central de "**en un intervalo ordenado, siempre es posible descartar la mitad**", descubrirás que la búsqueda binaria puede ayudarte a resolver problemas de manera eficiente en muchas situaciones.

---

## Ejercicio

LeetCode 33. Search in Rotated Sorted Array

Pista: El primer paso es usar la búsqueda binaria para encontrar el punto de rotación y el segundo paso es usar la búsqueda binaria para encontrar el valor objetivo.