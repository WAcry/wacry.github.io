---
title: "Problème du sac à dos 0/1"
date: 2024-12-24
draft: false
description: "Le problème de sac à dos classique le plus fondamental."
summary: "Le problème de sac à dos classique le plus fondamental."
tags: [ "Algorithme", "Programmation dynamique", "Problème du sac à dos" ]
categories: [ "Algorithmes et Structures de Données" ]
series: [ "Neuf conférences sur les sacs à dos" ]
series_order: 1
---

## Énoncé du problème

Il y a $N$ objets. Le volume du $i$-ème objet est $s_i$, et sa valeur est $v_i$.
Chaque objet ne peut être pris qu'une seule fois. Sous la contrainte que le volume total ne dépasse pas $S$, trouvez la valeur totale maximale $V$ qui peut être obtenue.

## Format d'entrée

La première ligne contient deux entiers, $N$ et $S$, séparés par un espace, représentant respectivement le nombre d'objets et la contrainte maximale de volume total.
Les $N$ lignes suivantes contiennent deux entiers, $s_i$ et $v_i$, séparés par un espace, représentant respectivement le volume et la valeur du $i$-ème objet.

## Format de sortie

Affichez un entier, représentant la valeur maximale.

## Intervalle de données

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

- Définir l'état : `f[i][j]` représente la valeur maximale qui peut être obtenue avec les $i$ premiers objets, avec une limite de volume de $j$.
    - Si le $i$-ème objet n'est pas pris, alors `f[i][j] = f[i - 1][j]`
    - Si le $i$-ème objet est pris, alors `f[i][j] = f[i - 1][j - s[i]] + v[i]`
    - Lors de l'implémentation de la transition d'état, il faut faire attention au domaine de définition. Si $j < s_i$, on ne considère pas le cas où le $i$-ème objet est pris. Parce que si $j-s_i$ est négatif, l'indice du tableau n'est pas valide.
      On peut aussi l'expliquer ainsi : le volume du $i$-ème objet est supérieur à la limite de volume, donc il est impossible de le prendre.
- Définir les conditions initiales : avec 0 objet, la valeur obtenue est 0 quelle que soit la limite de volume, c'est-à-dire `f[0][j] = 0`, `j` $\in [0, S]$.
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

## Optimisation DP unidimensionnelle

- La compression du tableau bidimensionnel en un tableau unidimensionnel peut économiser considérablement de l'espace et améliorer la vitesse d'exécution dans une certaine mesure (l'inconvénient est qu'il est impossible de répondre aux exigences spécifiques de certains types de problèmes).
- Il est à noter que dans la transition d'état, `f[i][j]` n'est lié qu'à `f[i - 1][j]` et `f[i - 1][j - s[i]]`. En d'autres termes, dans le tableau bidimensionnel `f` du code, `f[i][j]` n'est lié qu'aux éléments de sa ligne précédente qui sont plus à gauche ou dans la même colonne. Par conséquent, le tableau bidimensionnel peut être compressé en un tableau unidimensionnel ou en un tableau déroulant.
- Notez que dans le code ci-dessous, la deuxième boucle est une itération inverse, car nous devons nous assurer que lors du calcul de `f[i][j]`, `f[i - 1][j - s[i]]` n'a pas encore été mis à jour.

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

## Si le nombre de schémas est requis

Il faut non seulement afficher la valeur totale maximale qui peut être obtenue, mais aussi afficher "combien de méthodes de sélection différentes permettent d'atteindre cette valeur totale maximale". Voici une introduction à **la façon de calculer le nombre de schémas** dans le problème du sac à dos 0/1.

### Calcul du nombre de schémas avec la programmation dynamique bidimensionnelle

L'exemple suivant prend la programmation dynamique bidimensionnelle comme exemple pour l'expliquer.

- Définition des états :
  - `dp[i][j]` représente « la valeur maximale qui peut être obtenue avec les i premiers objets, lorsque la capacité (limite de volume) est j ».
  - `ways[i][j]` représente « le **nombre de schémas** correspondant pour obtenir la valeur maximale, avec les i premiers objets et une capacité de j ».

- Transition d'état :
  1. Si le i-ème objet n'est pas sélectionné :
     $$
       \text{dp}[i][j] = \text{dp}[i-1][j], 
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
     $$
  2. Si le i-ème objet est sélectionné (à condition que $j \ge s_i$) :
     $$
       \text{dp}[i][j] 
         = \text{dp}[i-1][j - s_i] + v_i,
       \quad
       \text{ways}[i][j]
         = \text{ways}[i-1][j - s_i]
     $$
  3. Sélectionner ou ne pas sélectionner, la valeur finale de `dp[i][j]` doit prendre la plus grande des deux :
     - Si
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           > \text{dp}[i-1][j],
       $$
       alors cela indique que « la sélection du i-ème objet » donne une plus grande valeur :
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
       alors cela indique que les deux méthodes obtiennent la même valeur maximale, le nombre de schémas doit être additionné :
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
       alors cela indique que « la non-sélection du i-ème objet » donne une plus grande valeur, le nombre de schémas hérite du nombre de schémas en cas de non-sélection :
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Condition initiale :
  - `dp[0][j] = 0` signifie que lorsqu'il n'y a aucun objet, la valeur maximale obtenue avec une capacité quelconque est 0.
  - `ways[0][0] = 1` signifie que le cas « 0 objet sélectionné, capacité 0 » est un schéma réalisable (c'est-à-dire ne rien sélectionner), et le **nombre de schémas** est défini sur 1.
  - Pour `j > 0`, lorsque aucun objet n'est sélectionnable et que la capacité est supérieure à 0, il est impossible d'obtenir une valeur positive. Le nombre de schémas correspondant est 0, c'est-à-dire `ways[0][j] = 0`.

- Réponse finale :
  - `dp[N][S]` est la valeur maximale.
  - `ways[N][S]` est le nombre de schémas pour atteindre cette valeur maximale.
  - Complexité temporelle : $O(NS)$.
  - Ce problème peut également être optimisé avec la programmation dynamique unidimensionnelle.

## Si la limite de volume exacte est requise

- Définir l'état : `f[i][j]` représente la valeur maximale avec les `i` premiers objets avec un volume exactement égal à `j`.
- Si le `i`-ème objet n'est pas pris, alors `f[i][j] = f[i - 1][j]`
- Si le `i`-ème objet est pris, alors `f[i][j] = f[i - 1][j - s[i]] + v[i]`
- On peut noter qu'il n'y a pas de différence avec la transition d'état du problème initial.
- Cependant, les conditions initiales sont différentes. À l'exception de `f[0][0] = 0`, le reste `f[0][j]` = $-\infty$, `j` $\in [1, S]$. $-\infty$ représente un état impossible.

## Si la limite de volume $S$ est très grande (1e9), alors que le nombre d'objets $N$ et la valeur totale maximale $V$ sont relativement petits

- Pour ce type de problème, il existe une solution avec une complexité de $O(NV)$.
- Définir l'état : `f[i][j]` représente le volume minimal lorsque l'on choisit plusieurs objets parmi les `i` premiers objets dont la somme de valeur est exactement `j`.
    - Si le `i`-ème objet n'est pas pris, alors `f[i][j] = f[i - 1][j]`
    - Si le `i`-ème objet est pris, alors `f[i][j] = f[i - 1][j - v[i]] + s[i]`
    - Prendre la plus petite des deux valeurs.
- Condition initiale : `f[0][0] = 0`, le reste `f[0][j]` = $\infty$, `j` $\in [1, V]$. $\infty$ représente un état impossible. Attention, ce n'est pas $-\infty$.
- La réponse finale est le plus grand `j` parmi les `f[N][j]` tels que `f[N][j] <= S`.

## Si la limite de volume $S$ et la valeur de chaque objet $v_i$ sont toutes deux très grandes (à l'ordre de 1e9), alors que le nombre d'objets $N$ est très petit (au plus 40)

- Lorsque $N \leq 20$, on peut énumérer directement tous les sous-ensembles de manière exhaustive (complexité temporelle $O(2^N)$).
- Lorsque $N \leq 40$, comme $2^{40}$ est de l'ordre de $10^{12}$, l'énumération exhaustive directe serait également très importante. On peut alors utiliser la **recherche de milieu** pour réduire grossièrement la complexité à $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$, qui peut être complétée dans un temps acceptable.