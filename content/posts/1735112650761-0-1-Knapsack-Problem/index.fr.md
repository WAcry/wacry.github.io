---
title: "Problème du sac à dos 0/1"
date: 2024-12-24
draft: false
description: "Le problème de sac à dos classique le plus fondamental."
summary: "Le problème de sac à dos classique le plus fondamental."
tags: [ "Algorithme", "Programmation dynamique", "Problème du sac à dos" ]
categories: [ "Algorithmes et structures de données" ]
series: [ "Les neuf leçons sur le sac à dos" ]
series_order: 1
---

## Problème

Il y a $N$ objets. Le volume du $i$-ème objet est $s_i$, et sa valeur est $v_i$.
Chaque objet ne peut être pris qu'une seule fois. Sous la contrainte d'un volume total maximal $S$, trouvez la valeur totale maximale $V$ qui peut être obtenue.

## Format d'entrée

La première ligne contient deux entiers, $N$ et $S$, séparés par un espace, représentant respectivement le nombre d'objets et la contrainte de volume total maximal.
Les $N$ lignes suivantes contiennent chacune deux entiers $s_i$ et $v_i$, séparés par un espace, représentant respectivement le volume et la valeur du $i$-ème objet.

## Format de sortie

Sortez un entier, représentant la valeur maximale.

## Plage de données

$$0 \le N, S \leq 1000$$

$$0 \le s_i, v_i \leq 1000$$

## Exemple d'entrée

```
4 5
1 2
2 4
3 4
4 5
```

## Exemple de sortie

```
8
```

## Solution

- Définition de l'état : `f[i][j]` représente la valeur maximale que l'on peut obtenir en considérant les $i$ premiers objets, avec une contrainte de volume de $j$.
    - Si on ne prend pas le $i$-ème objet, alors `f[i][j] = f[i - 1][j]`
    - Si on prend le $i$-ème objet, alors `f[i][j] = f[i - 1][j - s[i]] + v[i]`
    - Lors de la transition d'état, il faut faire attention au domaine de définition. Si $j < s_i$, alors on ne considère pas le cas où l'on prend le $i$-ème objet. Car si $j-s_i$ est négatif, l'indice du tableau n'est pas valide.
      On peut aussi l'expliquer ainsi : le volume du $i$-ème objet est supérieur à la contrainte de volume, donc ce n'est pas possible.
- Définition de la condition initiale : pour les 0 premiers objets, toute contrainte de volume donne une valeur de 0, c'est-à-dire `f[0][j] = 0`, `j` $\in [0, S]$.
- Complexité temporelle : $O(NS)$.

## Code

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

## Optimisation DP 1D

- En compressant le tableau bidimensionnel en un tableau unidimensionnel, on peut économiser considérablement de l'espace et améliorer la vitesse d'exécution dans une certaine mesure (l'inconvénient est qu'il ne peut pas répondre aux exigences particulières de certains types de problèmes)
- On remarque que dans la transition d'état, `f[i][j]` n'est lié qu'à `f[i - 1][j]` et `f[i - 1][j - s[i]]`. En d'autres termes, dans le tableau bidimensionnel `f` du code,
  `f[i][j]` n'est lié qu'aux éléments de sa ligne précédente qui sont plus à gauche ou dans la même colonne, on peut donc compresser le tableau bidimensionnel en un tableau unidimensionnel ou un tableau roulant.
- Notez que dans le code ci-dessous, la deuxième boucle parcourt en ordre inverse, car nous devons nous assurer que lors du calcul de `f[i][j]`, `f[i - 1][j - s[i]]` n'a pas encore été mis à jour.

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

## Si on demande le nombre de solutions

Non seulement il faut sortir la valeur totale maximale qui peut être obtenue, mais il faut aussi sortir "combien de méthodes de sélection différentes peuvent atteindre cette valeur maximale". Voici comment **compter le nombre de solutions** dans le problème du sac à dos 0/1.

### Compter le nombre de solutions avec DP 2D

Voici une explication en utilisant la DP 2D comme exemple.

- Définition de l'état :
  - `dp[i][j]` représente "la valeur maximale que l'on peut obtenir en considérant les i premiers objets, avec une capacité (contrainte de volume) de j".
  - `ways[i][j]` représente "le **nombre de solutions** correspondant à la valeur maximale obtenue en considérant les i premiers objets, avec une capacité de j".

- Transition d'état :
  1. Si on ne sélectionne pas le `i`-ème objet :
     $$
       \text{dp}[i][j] = \text{dp}[i-1][j], 
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
     $$
  2. Si on sélectionne le `i`-ème objet (à condition que $ j \ge s_i $) :
     $$
       \text{dp}[i][j] 
         = \text{dp}[i-1][j - s_i] + v_i,
       \quad
       \text{ways}[i][j]
         = \text{ways}[i-1][j - s_i]
     $$
  3. Que l'on sélectionne ou non, `dp[i][j]` doit finalement prendre la plus grande des deux valeurs :
     - Si
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           > \text{dp}[i-1][j],
       $$
       alors cela signifie que la valeur de "sélectionner le i-ème objet" est plus grande :
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
       cela signifie que les deux méthodes donnent la même valeur maximale, alors le nombre de solutions doit être additionné :
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
       alors cela signifie que la valeur de "ne pas sélectionner le i-ème objet" est plus grande, le nombre de solutions hérite du nombre de solutions lorsque l'on ne sélectionne pas :
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Condition initiale :
  - `dp[0][j] = 0` signifie que pour les 0 premiers objets, la valeur maximale obtenue pour toute capacité est 0.
  - `ways[0][0] = 1` signifie que "0 premiers objets, capacité 0" est une solution possible (c'est-à-dire ne rien sélectionner), le **nombre de solutions** est fixé à 1.
  - Pour `j > 0`, lorsqu'il n'y a pas d'objets à sélectionner et que la capacité est supérieure à 0, il est impossible d'obtenir une valeur positive, le nombre de solutions correspondant est 0, c'est-à-dire `ways[0][j] = 0`.

- Réponse finale :
  - `dp[N][S]` est la valeur maximale.
  - `ways[N][S]` est le nombre de solutions pour atteindre cette valeur maximale.
  - Complexité temporelle : $O(NS)$.
  - Ce problème peut également être optimisé en utilisant la DP 1D.

## Si on demande d'atteindre exactement la contrainte de volume

- Définition de l'état : `f[i][j]` représente la valeur maximale des `i` premiers objets avec un volume exactement égal à $j$.
- Si on ne prend pas le `i`-ème objet, alors `f[i][j] = f[i - 1][j]`
- Si on prend le `i`-ème objet, alors `f[i][j] = f[i - 1][j - s[i]] + v[i]`
- On peut remarquer qu'il n'y a pas de différence avec la transition d'état du problème original.
- Mais les conditions initiales sont différentes. En plus de `f[0][0] = 0`, le reste `f[0][j]` = $-\infty$, `j` $\in [1, S]$. $-\infty$ représente un état impossible.

## Si la contrainte de volume $S$ est très grande (1e9), et que le nombre d'objets $N$ et la valeur totale maximale $V$ sont relativement petits

- Pour ce type de problème, il existe une solution de complexité $O(NV)$.
- Définition de l'état : `f[i][j]` représente le volume minimal des `i` premiers objets en sélectionnant plusieurs objets, avec une valeur totale exactement égale à `j`.
    - Si on ne prend pas le `i`-ème objet, alors `f[i][j] = f[i - 1][j]`
    - Si on prend le `i`-ème objet, alors `f[i][j] = f[i - 1][j - v[i]] + s[i]`
    - On prend la plus petite des deux valeurs.
- Condition initiale : `f[0][0] = 0`, le reste `f[0][j]` = $\infty$, `j` $\in [1, V]$. $\infty$ représente un état impossible. Attention, ce n'est pas $-\infty$.
- La réponse finale est le plus grand `j` dans `f[N][j]` tel que `f[N][j] <= S`.

## Si la contrainte de volume $S$ et la valeur d'un seul objet $v_i$ sont toutes deux très grandes (de l'ordre de 1e9), et que le nombre d'objets $N$ est très petit (pas plus de 40)

- Lorsque $N \leq 20$, on peut directement énumérer tous les sous-ensembles (complexité temporelle $O(2^N)$).
- Lorsque $N \leq 40$, comme $2^{40}$ est de l'ordre de $10^{12}$, l'énumération directe est également assez grande, on peut donc utiliser la **recherche par moitié**, ce qui réduit approximativement la complexité à $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$
  , ce qui peut être fait dans un temps acceptable.