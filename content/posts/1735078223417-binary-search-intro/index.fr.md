---
title: "Recherche binaire"
date: 2024-12-24
draft: false
description: "Comment implémenter élégamment l'algorithme de recherche binaire pour les entiers"
tags: [ "Algorithme", "Recherche binaire", "Modèle d'algorithme" ]
categories: [ "Algorithmes et structures de données" ]
---
{{< katex >}}

# Recherche binaire

Dans une séquence ordonnée, la recherche binaire peut être utilisée pour trouver rapidement un élément spécifique. Comparée à la complexité temporelle de la recherche linéaire $O(n)$, la recherche binaire ne nécessite que $O(\log n)$ de temps, elle est donc très efficace pour les grandes échelles de données.

## Idée centrale de la recherche binaire

L'idée de base de la recherche binaire est de diviser continuellement l'intervalle de recherche en deux. À chaque comparaison, l'élément du milieu est comparé à la valeur cible. Si l'élément du milieu ne satisfait pas la condition, la moitié de l'intervalle peut être éliminée ; sinon, la recherche se poursuit dans l'autre moitié de l'intervalle. Comme la moitié de l'intervalle de recherche est rejetée à chaque fois, la complexité temporelle de la recherche peut atteindre $O(\log n)$.

La recherche binaire est très utile pour les problèmes où « **les solutions possibles peuvent être divisées en un intervalle ordonné (qui satisfait la condition) et un autre intervalle ordonné (qui ne satisfait pas la condition)** ». Par exemple :

- Trouver si un certain élément existe dans un tableau trié
- Trouver la « première position » ou la « dernière position » où un nombre apparaît

## Exemple de problème : trouver la position de début et de fin d'un élément

**Description du problème :**  
Étant donné un tableau d'entiers de longueur $n$ trié par ordre croissant, ainsi que $q$ requêtes. Chaque requête donne un entier $k$, et nous devons trouver la « position de début » et la « position de fin » de $k$ dans le tableau (indices commençant à 0). Si le nombre n'existe pas dans le tableau, retourner $-1$ $-1$.

**Format d'entrée :**

1.  Première ligne : deux entiers $n$ et $q$, représentant respectivement la longueur du tableau et le nombre de requêtes.
2.  Deuxième ligne : $n$ entiers (dans la plage 1 à 10 000), représentant le tableau complet, déjà trié par ordre croissant.
3.  Les $q$ lignes suivantes : chaque ligne contient un entier $k$, représentant un élément de requête.

**Format de sortie :**  
Pour chaque requête, afficher sur une ligne les positions de début et de fin de l'élément dans le tableau. Si l'élément n'existe pas dans le tableau, afficher $-1$ $-1$.

**Exemple :**

```
Entrée :
6 3
1 2 2 3 3 4
3
4
5

Sortie :
3 4
5 5
-1 -1
```

Explication :

-   L'intervalle où l'élément 3 apparaît est `[3, 4]` ;
-   L'élément 4 n'apparaît qu'une seule fois, à la position 5 ;
-   L'élément 5 n'existe pas dans le tableau, donc on retourne `-1 -1`.

## Idées d'application de la recherche binaire

Dans ce problème, afin de trouver la « limite gauche » et la « limite droite » d'une certaine valeur, nous pouvons nous appuyer sur la recherche binaire. L'essentiel est de comprendre comment définir l'intervalle de recherche et comment déplacer les pointeurs en fonction du résultat de la comparaison.

-   **Trouver la « limite gauche » :**  
    C'est-à-dire, trouver la première position supérieure ou égale à $k$. On peut diviser le tableau en deux parties :
    - Tous les nombres à gauche sont « inférieurs » à $k$
    - Tous les nombres à droite sont « supérieurs ou égaux » à $k$

-   **Trouver la « limite droite » :**  
    C'est-à-dire, trouver la dernière position inférieure ou égale à $k$. On peut diviser le tableau en deux parties :
    - Tous les nombres à gauche sont « inférieurs ou égaux » à $k$
    - Tous les nombres à droite sont « supérieurs » à $k$

Tant que ces deux intervalles peuvent être correctement maintenus, les résultats peuvent être obtenus rapidement grâce à la recherche binaire.

## Modèle recommandé : écrire une recherche binaire qui évite les boucles infinies

Voici un modèle de recherche binaire élégant et peu susceptible d'erreurs. En faisant converger progressivement $l$ et $r$, il garantit que la boucle se termine lorsque les deux sont adjacents :

Définir deux pointeurs $l, r$, il existe un invariant : l'intervalle fermé $[0, l]$ appartient à la partie gauche, et l'intervalle fermé $[r, n - 1]$ appartient à la partie droite. $l$ et $r$ sont tous deux initialisés à $-1$ et $n$.

Lorsque l'algorithme se termine, $l$ et $r$ sont adjacents, pointant respectivement vers la valeur maximale de la partie gauche et la valeur minimale de la partie droite.

Étant donné que la solution que nous voulons pourrait ne pas exister, lors du retour de $l$ ou de $r$, il est nécessaire de vérifier si la valeur correspondante est bien la valeur que nous voulons, et si elle est hors limites.
Par exemple, $l$ représente la valeur maximale de $\leq k$, et nous devons vérifier si `l != -1 && nums[l] == k`

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

        // 1. Trouver la position de début de k (limite gauche)
        //    Diviser le tableau en deux parties, à gauche tous < k, à droite tous >= k.
        //    La limite gauche est l'indice minimal de la partie droite.
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

        int leftPos = r; // Enregistrer la limite gauche de k

        // 2. Trouver la position de fin de k (limite droite)
        //    Diviser le tableau en deux parties, à gauche tous <= k, à droite tous > k.
        //    La limite droite est l'indice maximal de la partie gauche.
        l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] <= k) l = mid;
            else r = mid;
        }

        // Comme nous avons déjà vérifié que k existe, nous n'avons pas besoin de vérifier à nouveau ici
        int rightPos = l; // Limite droite
        cout << leftPos << " " << rightPos << endl;
    }
    return 0;
}
```

### Pourquoi cette façon d'écrire est-elle moins susceptible d'erreurs ?

1.  Cette façon d'écrire a des invariants strictement définis.
2.  Elle peut trouver à la fois la limite gauche et la limite droite, ce qui peut être appliqué à tous les scénarios.
3.  Certaines façons d'écrire utilisent $l == r$ comme condition de terminaison. Lorsque $l$ et $r$ sont distants de 1, il en résultera que $mid$ est égal à `l` ou `r`. S'il n'est pas traité correctement, la mise à jour de `l` ou `r` en `mid`, et l'intervalle de recherche ne se rétrécissant pas, cela entraînera une boucle infinie. Au contraire, cette façon d'écrire se termine lorsque $l$ et $r$ sont adjacents, ce qui évite ce problème.

## Solution STL : `lower_bound` et `upper_bound`

Si l'on utilise les fonctions `lower_bound` et `upper_bound` fournies par C++ STL, on peut facilement faire la même chose :

- `lower_bound(first, last, val)` retourne « la première position supérieure ou égale à val »
- `upper_bound(first, last, val)` retourne « la première position supérieure à val »

Par exemple, supposons que `nums = {1,2,3,4,4,4,4,4,5,5,6}`, nous voulons connaître l'intervalle où apparaît 4 :

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    // Cela indique que 4 n'existe pas dans le tableau
    cout << "4 apparaît 0 fois" << endl;
} else {
    cout << "le premier 4 est à " << it1 - nums.begin() << endl;
    cout << "le dernier 4 est à " << it2 - nums.begin() - 1 << endl;
    cout << "4 apparaît " << it2 - it1 << " fois" << endl;
}
```

- `it1` pointe vers la première position dont la valeur est supérieure ou égale à 4.
- `it2` pointe vers la première position dont la valeur est supérieure à 4.  
   Par conséquent, `it2 - it1` est le nombre de fois que 4 apparaît dans le tableau ; `it2 - nums.begin() - 1` est la limite droite de 4.

Ces deux fonctions sont particulièrement pratiques pour rechercher des intervalles ou compter le nombre d'occurrences.

## Supplément

La recherche binaire peut également être étendue à la recherche d'une plage de nombres à virgule flottante (telle que la recherche de la racine d'une équation), ainsi qu'à la recherche ternaire pour rechercher le maximum d'une fonction unimodale. Tant que vous comprenez le principe central de « **dans un intervalle ordonné, chaque fois que l'on peut éliminer la moitié** », vous constaterez que la recherche binaire peut vous aider à résoudre efficacement des problèmes dans de nombreux scénarios.

## Exercices après cours

LeetCode 33. Search in Rotated Sorted Array

Astuce : utilisez d'abord la recherche binaire pour trouver le point de rotation, puis utilisez la recherche binaire pour trouver la valeur cible.