---
title: "Problema de la Mochila 01"
date: 2024-12-24
draft: false
description: "El problema de la mochila clásico más básico."
summary: "El problema de la mochila clásico más básico."
tags: [ "Algoritmo", "Programación Dinámica", "Problema de la Mochila" ]
categories: [ "Algoritmos y Estructuras de Datos" ]
---

## Problema

Hay $N$ objetos. El volumen del $i$-ésimo objeto es $s_i$, y su valor es $v_i$.
Cada objeto solo se puede tomar una vez. Bajo la premisa de no exceder el límite máximo de volumen total $S$, encuentra el valor total máximo $V$ que se puede obtener.

## Formato de Entrada

La primera línea contiene dos enteros, $N$ y $S$, separados por un espacio, que representan el número de objetos y el límite máximo de volumen total, respectivamente.
Las siguientes $N$ líneas contienen cada una dos enteros, $s_i$ y $v_i$, separados por un espacio, que representan el volumen y el valor del $i$-ésimo objeto, respectivamente.

## Formato de Salida

Imprime un entero que representa el valor máximo.

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

- Define el estado: `f[i][j]` representa el valor máximo que se puede obtener de los primeros $i$ objetos con un límite de volumen de $j$.
    - Si el $i$-ésimo objeto no se toma, entonces `f[i][j] = f[i - 1][j]`
    - Si el $i$-ésimo objeto se toma, entonces `f[i][j] = f[i - 1][j - s[i]] + v[i]`
    - Al implementar la transición de estado, presta atención al rango del dominio. Si $j < s_i$, entonces no consideres el caso de tomar el $i$-ésimo objeto. Porque si $j - s_i$ es negativo, el índice del array es ilegal.
      También se puede explicar de esta manera: el volumen del $i$-ésimo objeto es mayor que el límite de volumen, por lo que es imposible.
- Define la condición inicial: Para los primeros $0$ objetos, cualquier límite de volumen da un valor de $0$, es decir, `f[0][j] = 0`, `j` $\in [0, S]$.
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

## Optimización DP 1D

- Comprimir el array bidimensional en un array unidimensional puede ahorrar espacio significativamente y mejorar la velocidad de ejecución hasta cierto punto (la desventaja es que no puede cumplir con los requisitos especiales de algunos tipos de problemas).
- Ten en cuenta que en la transición de estado, `f[i][j]` solo está relacionado con `f[i - 1][j]` y `f[i - 1][j - s[i]]`. En otras palabras, en el array bidimensional `f` en el código,
  `f[i][j]` solo está relacionado con los elementos de la fila anterior que están a su izquierda o en la misma columna. Por lo tanto, el array bidimensional se puede comprimir en un array unidimensional o un array rodante.
- Ten en cuenta que en el código de abajo, el segundo bucle itera en orden inverso. Esto se debe a que queremos asegurarnos de que al calcular `f[i][j]`, `f[i - 1][j - s[i]]` aún no se haya actualizado.

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

## Si se Requiere el Número de Esquemas

No solo se debe imprimir el valor total máximo que se puede obtener, sino también "cuántos métodos de selección diferentes pueden lograr este valor total máximo". A continuación, se describe **cómo contar el número de esquemas** en el problema de la mochila 01.

### DP 2D para Contar Esquemas

A continuación, se utiliza DP 2D como ejemplo para explicar.

- Define el estado:
  - `dp[i][j]` representa "el valor máximo que se puede obtener al considerar los primeros i objetos con una capacidad (límite de volumen) de j".
  - `ways[i][j]` representa "el **número de esquemas** correspondientes al valor máximo obtenido al considerar los primeros i objetos con una capacidad de j".

- Transición de estado:
  1. Si el objeto `i`-ésimo no se selecciona:
     $$
       \text{dp}[i][j] = \text{dp}[i-1][j], 
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
     $$
  2. Si el objeto `i`-ésimo se selecciona (siempre que $ j \ge s_i $):
     $$
       \text{dp}[i][j] 
         = \text{dp}[i-1][j - s_i] + v_i,
       \quad
       \text{ways}[i][j]
         = \text{ways}[i-1][j - s_i]
     $$
  3. Ya sea que se seleccione o no, el `dp[i][j]` final debe tomar el mayor de los dos:
     - Si
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           > \text{dp}[i-1][j],
       $$
       entonces significa que "seleccionar el i-ésimo objeto" tiene un valor mayor:
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
       significa que el valor máximo obtenido por los dos métodos es el mismo, entonces se debe sumar el número de esquemas:
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
       entonces significa que "no seleccionar el i-ésimo objeto" tiene un valor mayor, y el número de esquemas hereda el número de esquemas cuando no se selecciona:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Condiciones iniciales:
  - `dp[0][j] = 0` significa que cuando hay 0 objetos, el valor máximo obtenido para cualquier capacidad es 0.
  - `ways[0][0] = 1` significa que el caso de "0 objetos, capacidad 0" es un esquema factible (es decir, no seleccionar nada), y el **número de esquemas** se establece en 1.
  - Para `j > 0`, cuando no hay objetos para elegir y la capacidad es mayor que 0, es imposible obtener ningún valor positivo, y el número de esquemas correspondiente es 0, es decir, `ways[0][j] = 0`.

- Respuesta final:
  - `dp[N][S]` es el valor máximo.
  - `ways[N][S]` es el número de esquemas para lograr este valor máximo.
  - Complejidad temporal: $O(NS)$.
  - Este problema también se puede optimizar utilizando DP 1D.

## Si el Requisito es Alcanzar Exactamente el Límite de Volumen

- Define el estado: `f[i][j]` representa el valor máximo cuando los primeros `i` objetos tienen exactamente un volumen de $j$.
- Si el objeto `i`-ésimo no se toma, entonces `f[i][j] = f[i - 1][j]`
- Si el objeto `i`-ésimo se toma, entonces `f[i][j] = f[i - 1][j - s[i]] + v[i]`
- Se puede observar que no hay diferencia en la transición de estado con respecto al problema original.
- Sin embargo, las condiciones iniciales son diferentes. Excepto por `f[0][0] = 0`, el resto `f[0][j]` = $-\infty$, `j` $\in [1, S]$. $-\infty$ representa un estado imposible.

## Si el Límite de Volumen $S$ es Muy Grande (1e9), Mientras que el Número de Objetos $N$ y el Valor Total Máximo $V$ son Relativamente Pequeños

- Para tales problemas, existe una solución con una complejidad de $O(NV)$.
- Define el estado: `f[i][j]` representa el volumen mínimo al seleccionar varios objetos de los primeros `i` objetos, y el valor total es exactamente `j`.
    - Si el objeto `i`-ésimo no se toma, entonces `f[i][j] = f[i - 1][j]`
    - Si el objeto `i`-ésimo se toma, entonces `f[i][j] = f[i - 1][j - v[i]] + s[i]`
    - Toma el menor de los dos.
- Condiciones iniciales: `f[0][0] = 0`, el resto `f[0][j]` = $\infty$, `j` $\in [1, V]$. $\infty$ representa un estado imposible. Ten en cuenta que no es $-\infty$.
- La respuesta final es el `j` más grande en `f[N][j]` tal que `f[N][j] <= S`.

## Si el Límite de Volumen $S$ y el Valor de un Solo Objeto $v_i$ son Ambos Muy Grandes (del orden de 1e9), Mientras que el Número de Objetos $N$ es Muy Pequeño (no más de 40)

- Cuando $N \leq 20$, todos los subconjuntos se pueden enumerar directamente por fuerza bruta (complejidad temporal $O(2^N)$).
- Cuando $N \leq 40$, dado que $2^{40}$ es del orden de $10^{12}$, la fuerza bruta directa también será relativamente grande, por lo que se puede utilizar la **búsqueda de encuentro en el medio** para reducir la complejidad a aproximadamente $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$, que se puede completar en un tiempo aceptable.