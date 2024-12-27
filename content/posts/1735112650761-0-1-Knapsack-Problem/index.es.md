markdown
---
title: "Problema de la Mochila 0/1"
date: 2024-12-24
draft: false
description: "El problema de la mochila clásico más básico."
summary: "El problema de la mochila clásico más básico."
tags: [ "Algoritmos", "Programación Dinámica", "Problema de la Mochila" ]
categories: [ "Algoritmos y Estructuras de Datos" ]
series: [ "Las Nueve Lecciones de la Mochila" ]
series_order: 1
---

## Problema

Hay $N$ objetos. El volumen del objeto $i$ es $s_i$, y su valor es $v_i$.
Cada objeto solo se puede tomar una vez. Bajo la premisa de no exceder la restricción de volumen total máximo $S$, encuentra el valor total máximo $V$ que se puede obtener.

## Formato de Entrada

La primera línea contiene dos enteros, $N$ y $S$, separados por espacios, que representan el número de objetos y la restricción de volumen total máximo, respectivamente.
Las siguientes $N$ líneas contienen dos enteros cada una, $s_i$ y $v_i$, separados por espacios, que representan el volumen y el valor del objeto $i$, respectivamente.

## Formato de Salida

Imprime un entero, que representa el valor máximo.

## Rango de Datos

$$0 \le N, S \leq 1000$$

$$0 \le s_i, v_i \leq 1000$$

## Ejemplo de Entrada

```
4 5
1 2
2 4
3 4
4 5
```

## Ejemplo de Salida

```
8
```

## Solución

- Definición del estado: `f[i][j]` representa el valor máximo que se puede obtener con los primeros $i$ objetos y una restricción de volumen de $j$.
    - Si no se toma el objeto $i$, entonces `f[i][j] = f[i - 1][j]`
    - Si se toma el objeto $i$, entonces `f[i][j] = f[i - 1][j - s[i]] + v[i]`
    - Al implementar la transición de estado, se debe prestar atención al rango del dominio. Si $j < s_i$, entonces no se considera el caso de tomar el objeto $i$. Esto se debe a que si $j - s_i$ es un número negativo, el índice del array no es válido.
      También se puede explicar de esta manera: el volumen del objeto $i$ es mayor que la restricción de volumen, por lo que es imposible.
- Definición de la condición inicial: con los primeros $0$ objetos, cualquier restricción de volumen obtiene un valor de $0$, es decir, `f[0][j] = 0`, `j` $\in [0, S]$.
- Complejidad temporal: $O(NS)$.

## Código

```cpp
#include<bits/stdc++.h>
using namespace std;
int main() {
    int N, S;
    cin >> N >> S;
    vector<int> s(N + 1), v(N + 1);
    for (int i = 1; i <= N; i++) cin >> s[i] >> v[i];
    vector<vector<int>> f(N + 1, vector<int>(S + 1));
    for (int i = 1; i <= N; i++) {
        for (int j = 0; j <= S; j++) {
            f[i][j] = f[i - 1][j];
            if (j >= s[i]) f[i][j] = max(f[i][j], f[i - 1][j - s[i]] + v[i]);
        }
    }
    cout << f[N][S] << endl;
    return 0;
}
```

## Optimización DP Unidimensional

- Comprimir el array bidimensional en un array unidimensional puede ahorrar espacio significativamente y mejorar la velocidad de ejecución en cierta medida (la desventaja es que no puede satisfacer los requisitos especiales de ciertos tipos de problemas).
- Se observa que en la transición de estado, `f[i][j]` solo está relacionado con `f[i - 1][j]` y `f[i - 1][j - s[i]]`. En otras palabras, en el array bidimensional `f` del código,
  `f[i][j]` solo está relacionado con los elementos de su fila anterior que están más a la izquierda o en la misma columna, por lo que el array bidimensional se puede comprimir en un array unidimensional o un array de desplazamiento.
- Ten en cuenta que en el siguiente código, el segundo bucle itera en orden inverso, esto se debe a que queremos asegurarnos de que al calcular `f[i][j]`, `f[i - 1][j - s[i]]` aún no se haya actualizado.

```cpp
#include<bits/stdc++.h>
using namespace std;
int main() {
    int N, S;
    cin >> N >> S;
    vector<int> s(N + 1), v(N + 1);
    for (int i = 1; i <= N; i++) cin >> s[i] >> v[i];
    vector<int> f(S + 1);
    for (int i = 1; i <= N; i++) {
        for (int j = S; j >= s[i]; j--) {
            f[j] = max(f[j], f[j - s[i]] + v[i]);
        }
    }
    cout << f[S] << endl;
    return 0;
}
```

## Si se requiere el número de soluciones

No solo se debe imprimir el valor total máximo que se puede obtener, sino también "cuántas formas diferentes de selección pueden alcanzar este valor máximo total". A continuación, se presenta cómo **contar el número de soluciones** en el problema de la mochila 0/1.

### Conteo de Soluciones con DP Bidimensional

A continuación, se explica con un ejemplo de DP bidimensional.

- Definición del estado:
  - `dp[i][j]` representa "el valor máximo que se puede obtener con los primeros i objetos y una capacidad (restricción de volumen) de j".
  - `ways[i][j]` representa "el **número de soluciones** correspondientes cuando se obtiene el valor máximo con los primeros i objetos y una capacidad de j".

- Transición de estado:
  1. Si no se selecciona el objeto `i`:
     $$
       \text{dp}[i][j] = \text{dp}[i-1][j], 
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
     $$
  2. Si se selecciona el objeto `i` (siempre que $ j \ge s_i $):
     $$
       \text{dp}[i][j] 
         = \text{dp}[i-1][j - s_i] + v_i,
       \quad
       \text{ways}[i][j]
         = \text{ways}[i-1][j - s_i]
     $$
  3. Seleccionar o no, al final `dp[i][j]` debe tomar el valor más grande de los dos:
     - Si
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           > \text{dp}[i-1][j],
       $$
       entonces indica que el valor de "seleccionar el objeto i" es mayor:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j - s_i] + v_i,
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j - s_i].
       $$
     - Si
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           = \text{dp}[i-1][j],
       $$
       indica que el valor máximo obtenido por las dos formas es el mismo, entonces el número de soluciones debe superponerse:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j], 
         \quad
         \text{ways}[i][j] 
           = \text{ways}[i-1][j] 
             + \text{ways}[i-1][j - s_i].
       $$
     - Si
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           < \text{dp}[i-1][j],
       $$
       entonces indica que el valor de "no seleccionar el objeto i" es mayor, el número de soluciones hereda el número de soluciones cuando no se selecciona:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Condición inicial:
  - `dp[0][j] = 0` indica que cuando hay 0 objetos, el valor máximo obtenido con cualquier capacidad es 0.
  - `ways[0][0] = 1` indica que "0 objetos, capacidad 0" es una solución factible (es decir, no seleccionar nada), el **número de soluciones** se establece en 1.
  - Para `j > 0`, cuando no hay objetos para seleccionar y la capacidad es mayor que 0, es imposible obtener ningún valor positivo, el número de soluciones correspondiente es 0, es decir, `ways[0][j] = 0`.

- Respuesta final:
  - `dp[N][S]` es el valor máximo.
  - `ways[N][S]` es el número de soluciones para alcanzar este valor máximo.
  - Complejidad temporal: $O(NS)$.
  - Este problema también se puede optimizar utilizando DP unidimensional.

## Si se requiere alcanzar exactamente la restricción de volumen

- Definición del estado: `f[i][j]` representa el valor máximo de los primeros `i` objetos con un volumen exactamente igual a $j$.
- Si no se toma el objeto `i`, entonces `f[i][j] = f[i - 1][j]`
- Si se toma el objeto `i`, entonces `f[i][j] = f[i - 1][j - s[i]] + v[i]`
- Se puede observar que no hay diferencia con la transición de estado del problema original.
- Pero las condiciones iniciales son diferentes. Además de `f[0][0] = 0`, el resto de `f[0][j]` = $-\infty$, `j` $\in [1, S]$. $-\infty$ representa un estado imposible.

## Si la restricción de volumen $S$ es muy grande (1e9), mientras que el número de objetos $N$ y el valor total máximo $V$ son relativamente pequeños

- Para este tipo de problema, existe una solución con una complejidad de $O(NV)$.
- Definición del estado: `f[i][j]` representa el volumen mínimo de los primeros `i` objetos seleccionando algunos, cuyo valor total es exactamente `j`.
    - Si no se toma el objeto `i`, entonces `f[i][j] = f[i - 1][j]`
    - Si se toma el objeto `i`, entonces `f[i][j] = f[i - 1][j - v[i]] + s[i]`
    - Se toma el valor más pequeño de los dos.
- Condición inicial: `f[0][0] = 0`, el resto de `f[0][j]` = $\infty$, `j` $\in [1, V]$. $\infty$ representa un estado imposible. Ten en cuenta que no es $-\infty$.
- La respuesta final es el `j` más grande en `f[N][j]` tal que `f[N][j] <= S`.

## Si la restricción de volumen $S$ y el valor de un solo objeto $v_i$ son muy grandes (del orden de $1e9$), mientras que el número de objetos $N$ es muy pequeño (no más de 40)

- Cuando $N \leq 20$, se pueden enumerar directamente todos los subconjuntos (complejidad temporal $O(2^N)$).
- Cuando $N \leq 40$, dado que $2^{40}$ está en el orden de $10^{12}$, la enumeración directa también sería relativamente grande, por lo que se puede utilizar la **búsqueda de punto medio**,
  lo que reduce la complejidad aproximadamente a $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$
  , que se puede completar en un tiempo aceptable.