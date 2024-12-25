---
title: "Problema de la Mochila 0/1"
date: 2024-12-24
draft: false
description: "El problema de la mochila clásico más básico."
summary: "El problema de la mochila clásico más básico."
tags: [ "Algoritmo", "Programación Dinámica", "Problema de la Mochila" ]
categories: [ "Algoritmos y Estructuras de Datos" ]
series: [ "Nueve Lecciones sobre la Mochila" ]
series_order: 1
---

## Problema

Hay $N$ objetos. El volumen del objeto $i$-ésimo es $s_i$ y su valor es $v_i$.
Cada objeto solo se puede tomar una vez. Bajo la premisa de no exceder el límite máximo de volumen total $S$, calcule el valor total máximo $V$ que se puede obtener.

## Formato de Entrada

La primera línea contiene dos enteros, $N$ y $S$, separados por un espacio, que representan respectivamente el número de objetos y el límite máximo de volumen total.
Las siguientes $N$ líneas contienen cada una dos enteros $s_i$ y $v_i$, separados por un espacio, que representan respectivamente el volumen y el valor del objeto $i$-ésimo.

## Formato de Salida

Imprima un entero, que representa el valor máximo.

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

- Definir el estado: `f[i][j]` representa el valor máximo que se puede obtener con los primeros $i$ objetos, con un límite de volumen de $j$.
    - Si no se toma el objeto $i$, entonces `f[i][j] = f[i - 1][j]`
    - Si se toma el objeto $i$, entonces `f[i][j] = f[i - 1][j - s[i]] + v[i]`
    - Al implementar la transición de estado, se debe prestar atención al rango del dominio. Si $j < s_i$, entonces no se considera el caso de tomar el objeto $i$. Porque si $j-s_i$ es un número negativo, el índice del array no es válido.
      También se puede explicar así: El volumen del objeto $i$ es mayor que el límite de volumen, por lo que es imposible.
- Definir las condiciones iniciales: Con los primeros $0$ objetos, cualquier límite de volumen obtiene un valor de $0$, es decir, `f[0][j] = 0`, `j` $\in [0, S]$.
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

## Optimización de DP unidimensional

- Comprimir el array bidimensional en un array unidimensional, puede ahorrar espacio significativamente y mejorar la velocidad de ejecución en cierta medida (la desventaja es que no puede cumplir con los requisitos especiales de ciertos tipos de problemas)
- Tenga en cuenta que en la transición de estado, `f[i][j]` solo está relacionado con `f[i - 1][j]` y `f[i - 1][j - s[i]]`. En otras palabras, en el array bidimensional `f` del código,
  `f[i][j]` solo está relacionado con los elementos de la fila anterior que están más a la izquierda o en la misma columna, por lo tanto, el array bidimensional se puede comprimir en un array unidimensional o un array de desplazamiento.
- Tenga en cuenta que en el siguiente código, el segundo bucle itera en orden inverso, esto se debe a que debemos asegurarnos de que al calcular `f[i][j]`, `f[i - 1][j - s[i]]` aún no se haya actualizado.

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

## Si se requiere el número de esquemas

No solo se debe imprimir el valor total máximo que se puede obtener, sino que también es necesario imprimir "cuántos métodos diferentes de selección pueden alcanzar este valor total máximo". A continuación, se explica **cómo contar el número de esquemas** en el problema de la mochila 0/1.

### Conteo de Esquemas de DP Bidimensional

A continuación se explica el uso de DP bidimensional como ejemplo.

- Definición del estado:
  - `dp[i][j]` representa el "valor máximo que se puede obtener con los primeros i objetos, cuando la capacidad (límite de volumen) es j".
  - `ways[i][j]` representa el "número de esquemas correspondientes cuando se obtiene el valor máximo con los primeros i objetos, cuando la capacidad es j".

- Transición del estado:
  1. Si no se selecciona el objeto `i`-ésimo:
     $$
       \text{dp}[i][j] = \text{dp}[i-1][j], 
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
     $$
  2. Si se selecciona el objeto `i`-ésimo (con la condición de que $ j \ge s_i $):
     $$
       \text{dp}[i][j] 
         = \text{dp}[i-1][j - s_i] + v_i,
       \quad
       \text{ways}[i][j]
         = \text{ways}[i-1][j - s_i]
     $$
  3. Ya sea que se seleccione o no, al final `dp[i][j]` debe tomar el valor mayor entre los dos:
     - Si
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           > \text{dp}[i-1][j],
       $$
       eso indica que "seleccionar el objeto i-ésimo" tiene un valor mayor:
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
       indica que el valor máximo obtenido por los dos métodos es el mismo, entonces el número de esquemas debe superponerse:
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
       eso indica que el valor de "no seleccionar el objeto i-ésimo" es mayor, y el número de esquemas hereda el número de esquemas cuando no se selecciona:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Condiciones iniciales:
  - `dp[0][j] = 0` indica que el valor máximo que se obtiene con los primeros 0 objetos es 0 para cualquier capacidad.  
  - `ways[0][0] = 1` indica que "los primeros 0 objetos, con capacidad 0" es un esquema factible (es decir, no se selecciona nada), y el **número de esquemas** se establece en 1.  
  - Para `j > 0`, cuando no hay objetos seleccionables y la capacidad es mayor que 0, es imposible obtener un valor positivo, por lo que el número de esquemas correspondiente es 0, es decir, `ways[0][j] = 0`.

- Respuesta final:
  - `dp[N][S]` es el valor máximo.  
  - `ways[N][S]` es el número de esquemas para alcanzar ese valor máximo.
  - Complejidad temporal: $O(NS)$.
  - Este problema también se puede optimizar con DP unidimensional.

## Si se requiere que el límite de volumen se alcance exactamente

- Definir el estado: `f[i][j]` representa el valor máximo de los primeros `i` objetos con un volumen exactamente de $j$.
- Si no se toma el objeto `i`, entonces `f[i][j] = f[i - 1][j]`
- Si se toma el objeto `i`, entonces `f[i][j] = f[i - 1][j - s[i]] + v[i]`
- Se puede notar que no hay diferencia con la transición de estado del problema original.
- Sin embargo, las condiciones iniciales son diferentes. Además de `f[0][0] = 0`, el resto `f[0][j]` = $-\infty$, `j` $\in [1, S]$. $-\infty$ representa un estado imposible.

## Si el límite de volumen $S$ es muy grande (1e9), mientras que el número de objetos $N$ y el valor total máximo $V$ son pequeños

- Para este tipo de problemas, existe una solución con complejidad $O(NV)$.
- Definir el estado: `f[i][j]` representa el volumen mínimo de los primeros `i` objetos seleccionando varios, cuando la suma de valores es exactamente `j`.
    - Si no se toma el objeto `i`, entonces `f[i][j] = f[i - 1][j]`
    - Si se toma el objeto `i`, entonces `f[i][j] = f[i - 1][j - v[i]] + s[i]`
    - Se toma el valor menor entre ambos.
- Condiciones iniciales: `f[0][0] = 0`, el resto `f[0][j]` = $\infty$, `j` $\in [1, V]$. $\infty$ representa un estado imposible. Tenga en cuenta que no es $-\infty$.
- La respuesta final es el `j` más grande en `f[N][j]` tal que `f[N][j] <= S`.

## Si el límite de volumen $S$ y el valor de los objetos individuales $v_i$ son muy grandes (orden de magnitud de $1e9$), mientras que el número de objetos $N$ es muy pequeño (no más de 40)

- Cuando $N \leq 20$, se puede enumerar directamente todos los subconjuntos (complejidad temporal $O(2^N)$).
- Cuando $N \leq 40$, debido a que $2^{40}$ está en el orden de magnitud de $10^{12}$, la enumeración directa también sería demasiado grande, por lo que se puede utilizar la **búsqueda por la mitad**
  , para reducir la complejidad aproximadamente a $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$
  , lo que se puede completar en un tiempo aceptable.