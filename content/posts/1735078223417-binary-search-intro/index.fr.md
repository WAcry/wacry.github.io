markdown
---
title: "Recherche Binaire"
date: 2024-12-24
draft: false
description: "Comment implémenter élégamment l'algorithme de recherche binaire."
summary: "Comment implémenter élégamment l'algorithme de recherche binaire."
tags: [ "Algorithme", "Recherche Binaire", "Modèle d'Algorithme" ]
categories: [ "Algorithmes et Structures de Données" ]
---

Si un espace de solutions ordonné est divisé en deux parties, où une partie satisfait une condition et l'autre non, alors la recherche binaire peut être utilisée pour trouver le point critique dans l'espace de solutions ordonné.

L'idée de base de la recherche binaire est de diviser répétitivement l'intervalle de recherche par deux. À chaque fois, l'élément du milieu est vérifié. Si l'élément du milieu ne satisfait pas la condition, la moitié de l'intervalle peut être éliminée ; sinon, la recherche continue dans l'autre moitié. Puisque la moitié de l'intervalle de recherche est écartée à chaque fois, la complexité temporelle de la recherche peut atteindre $O(\log n)$.

## Exemple de Problème

**Description du Problème :**
Étant donné un tableau d'entiers trié par ordre croissant de longueur $n$, et $q$ requêtes. Chaque requête donne un entier $k$, et nous devons trouver la "position de départ" et la "position de fin" de $k$ dans le tableau (les indices commencent à 0). Si le nombre n'existe pas dans le tableau, retourner `-1 -1`.

### Format d'Entrée

1. Première ligne : deux entiers $n$ et $q$, représentant respectivement la longueur du tableau et le nombre de requêtes.
2. Deuxième ligne : $n$ entiers, représentant le tableau complet, déjà trié par ordre croissant.
3. Les $q$ lignes suivantes : chaque ligne contient un entier $k$, représentant un élément de requête.

## Plage de Données

$1 \leq n \leq 100000$

$1 \leq q \leq 10000$

$1 \leq k \leq 10000$

### Format de Sortie

Pour chaque requête, afficher les positions de début et de fin de l'élément dans le tableau sur une seule ligne. Si l'élément n'existe pas dans le tableau, afficher `-1 -1`.

**Exemple :**

```
Entrée :
6 3
1 2 2 3 3 4
3
4
5

Sortie :
3 4
5 5
-1 -1
```

**Explication :**

- La plage où l'élément $3$ apparaît est $[3, 4]$ ;
- L'élément $4$ n'apparaît qu'une seule fois, à la position $5$ ;
- L'élément $5$ n'existe pas dans le tableau, donc retourner $-1$ $-1$.

---

## Solution

- **Trouver la "Position de Départ" :**
  C'est-à-dire, trouver la première position qui est supérieure ou égale à $k$. Le tableau peut être divisé en deux parties :
    - Tous les nombres à gauche sont "inférieurs à" $k$
    - Tous les nombres à droite sont "supérieurs ou égaux à" $k$
    - La réponse est la première position à droite

- **Trouver la "Position de Fin" :**
  C'est-à-dire, trouver la dernière position qui est inférieure ou égale à $k$. Le tableau peut être divisé en deux parties :
    - Tous les nombres à gauche sont "inférieurs ou égaux à" $k$
    - Tous les nombres à droite sont "supérieurs à" $k$
    - La réponse est la dernière position à gauche

---

## Modèle Recommandé

Voici un modèle de recherche binaire élégant et moins sujet aux erreurs.

Définissez deux pointeurs $l, r$, avec l'invariant : l'intervalle fermé $[0, l]$ appartient à la partie gauche, et l'intervalle fermé $[r, n - 1]$ appartient à la partie droite. $l$ et $r$ sont initialisés à $-1$ et $n$, respectivement.

Lorsque l'algorithme se termine, $l$ et $r$ sont adjacents, pointant respectivement vers le dernier élément de la partie gauche et le premier élément de la partie droite.

Comme la solution que nous voulons peut ne pas exister, si le problème n'indique pas qu'une solution existe forcément, nous devons vérifier si `l` ou `r` est hors limites et s'il pointe vers la bonne valeur.

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

        // 1. Trouver la position de départ de k
        //    Diviser le tableau en deux parties, la partie gauche est toute < k, et la partie droite est toute >= k.
        //    La réponse est le plus petit indice de la partie droite.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // Si r est hors limites ou nums[r] != k, cela signifie que k n'existe pas
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. Trouver la position de fin de k
        //    Diviser le tableau en deux parties, la partie gauche est toute <= k, et la partie droite est toute > k.
        //    La réponse est le plus grand indice de la partie gauche.
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

### Avantages

1. Cette approche a des invariants strictement définis.
2. Elle s'applique à la fois pour trouver la "position de départ" et la "position de fin" sans traitement ou modifications supplémentaires.
3. Certaines approches utilisent `l == r` comme condition de terminaison. Lorsque $l$ et $r$ diffèrent de $1$, $mid$ sera calculé comme étant égal à $l$ ou $r$. S'il n'est pas géré correctement, la mise à jour de $l$ ou $r$ à $mid$ ne réduira pas l'intervalle de recherche, ce qui entraînera une boucle infinie. En revanche, cette approche se termine lorsque $l$ et $r$ sont adjacents, garantissant que $mid$ est inférieur à $l$ et supérieur à $r$, et la mise à jour de $l$ ou $r$ réduira toujours l'intervalle de recherche.

---

## STL

Si vous utilisez les fonctions `lower_bound` et `upper_bound` fournies par la STL de C++, vous pouvez obtenir le même résultat :

- `lower_bound(first, last, val)` retournera "la première position qui est supérieure ou égale à val"
- `upper_bound(first, last, val)` retournera "la première position qui est supérieure à val"

Par exemple, supposons que `nums = {1,2,3,4,4,4,4,4,5,5,6}`, et nous voulons connaître la plage où 4 apparaît :

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    cout << "4 apparaît 0 fois" << endl;
} else {
    cout << "le premier 4 est à " << it1 - nums.begin() << endl;
    cout << "le dernier 4 est à " << it2 - nums.begin() - 1 << endl;
    cout << "4 apparaît " << it2 - it1 << " fois" << endl;
}
```

- `it1` pointe vers la première position où la valeur est supérieure ou égale à $4$.
- `it2` pointe vers la première position où la valeur est supérieure à $4$.
  Par conséquent, `it2 - it1` est le nombre de fois que $4$ apparaît dans le tableau ; `it2 - nums.begin() - 1` est la position de la limite droite de $4$.

---

## Notes Additionnelles

La recherche binaire peut également être étendue pour rechercher dans des plages de nombres à virgule flottante (comme la recherche des racines d'une équation) et la recherche ternaire pour trouver les extrema de fonctions unimodales.

---

## Pratique

LeetCode 33. Recherche dans un tableau trié pivoté

Indice : Utilisez d'abord la recherche binaire pour trouver le point de rotation, puis utilisez la recherche binaire pour trouver la valeur cible.