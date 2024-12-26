---
title: "Tri Rapide"
date: 2024-12-26
draft: false
description: "Analyse des points clés pour une implémentation correcte de l'algorithme de tri rapide."
summary: "Analyse des points clés pour une implémentation correcte de l'algorithme de tri rapide."
tags: [ "Algorithme", "Algorithme de Tri", "Tri Rapide", "Diviser pour Régner" ]
categories: [ "Algorithmes et Structures de Données" ]
---

# Tri Rapide

Le tri rapide est un algorithme de tri non stable basé sur la comparaison, qui utilise le principe diviser pour régner. Sa complexité temporelle moyenne est de $O(n\log n)$, dans le pire des cas de $O(n^2)$, et sa complexité spatiale est de $O(1)$. Nous allons présenter ci-dessous les détails de son implémentation et les erreurs fréquentes, en prenant l'exemple du tri d'une séquence d'entiers par ordre croissant.

---

## Description du Problème

Étant donné une séquence de $n$ entiers, triez-la par ordre croissant en utilisant le tri rapide et affichez le résultat.

### Format d'Entrée

- La première ligne contient l'entier $n$.
- La deuxième ligne contient $n$ entiers, tous dans la plage $[1, 10^9]$.

### Format de Sortie

- Affichez une ligne contenant la séquence triée.

### Plage de Données

$1 \leq n \leq 100000$

### Exemple d'Entrée

```
5
3 1 2 4 5
```

### Exemple de Sortie

```
1 2 3 4 5
```

---

## Idée du Tri Rapide

À chaque étape de la division, le tri rapide sélectionne un nombre comme pivot (`pivot` ci-dessous est le nombre situé au milieu).

Deux pointeurs, un gauche `L` et un droit `R`, se déplacent respectivement de gauche à droite et de droite à gauche. Le pointeur gauche `L` cherche le premier nombre supérieur ou égal au `pivot`, et le pointeur droit `R` cherche le premier nombre inférieur ou égal au `pivot`. Ensuite, ces deux nombres sont échangés.

Ce processus est répété jusqu'à ce que le pointeur gauche et le pointeur droit se chevauchent, ou que le pointeur gauche dépasse le pointeur droit d'une position. C'est ce qu'on appelle une itération.

Après chaque déplacement de pointeur et chaque échange, on garantit que la structure "partie gauche ≤ pivot, partie droite ≥ pivot" est maintenue, c'est-à-dire l'invariant `[left, L) <= pivot`, `(R, right] >= pivot`.

Dans l'exemple de code ci-dessous, `left` et `right` sont les limites de l'intervalle fermé en cours de traitement, et `pivot` est l'élément situé au milieu de l'intervalle.

```cpp
#include <bits/stdc++.h>
using namespace std;

void quickSort(vector<int> &a, int left, int right) {
    if (left >= right) return;
    
    int pivot = a[(left + right) / 2];
    int l = left, r = right;
    
    while (true) {
        while (a[l] < pivot) l++;
        while (a[r] > pivot) r--;
        if (l >= r) break;
        swap(a[l], a[r]);
        l++; r--;
    }
    
    quickSort(a, left, r);
    quickSort(a, r + 1, right);
}

int main() {
    int n; cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    
    quickSort(a, 0, n - 1);
    
    for (int i = 0; i < n; i++) cout << a[i] << " ";
    return 0;
}
```

---

## Complexité et Choix du `pivot`

Comme le tri rapide a une complexité de $O(n^2)$ dans le pire des cas, le choix du `pivot` est crucial. Si l'on choisit toujours le premier ou le dernier élément, on risque de rencontrer le pire des cas dans un tableau presque trié.

En plus de choisir l'élément du milieu, on peut également choisir un élément aléatoire comme `pivot`, ou prendre la médiane des trois éléments (gauche, milieu, droit) comme `pivot`.

---

## Exemples d'Erreurs Fréquentes

Le code suivant contient plusieurs erreurs courantes.

```cpp
#include <bits/stdc++.h>
using namespace std;

void quickSort(vector<int> &a, int left, int right) {
    if (left == right) return; // 7

    int pivot = (left + right) >> 1; // 1
    int l = left, r = right;

    while (true) {
        while (a[l] <= pivot) l++; // 2
        while (a[r] >= pivot) r--; // 2
        swap(a[l], a[r]);
        if (l >= r) break; // 3
        // 4
    }

    quickSort(a, left, l - 1); // 5, 6
    quickSort(a, l, right);    // 5, 6
}

int main() {
    int n; cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    
    quickSort(a, 0, n - 1);
    
    for (int i = 0; i < n; i++) cout << a[i] << " ";
    return 0;
}
```

**Analyse des erreurs :**

1. `pivot` doit être un nombre du tableau, et non un indice.
2. L'utilisation de `<=` et `>=` au lieu de `<` et `>` peut faire dépasser le pointeur gauche le pointeur droit de plus d'une position, ce qui empêche de diviser correctement le tableau en deux parties.
3. Après avoir constaté que `l >= r`, il faut sortir immédiatement de la boucle sans effectuer d'échange. Sinon, on ne peut pas garantir que les éléments à gauche soient inférieurs ou égaux à `pivot` et que les éléments à droite soient supérieurs ou égaux à `pivot`.
4. Après chaque échange, il faut exécuter `l++` et `r--`.
5. `pivot` prend en fait le nombre du milieu gauche. Si l'on divise le tableau en utilisant $l - 1$ et $l$, en considérant le tableau `[1, 2]`, on observe facilement que cela conduit à une boucle infinie, divisant continuellement le tableau en deux parties de taille 0 et 2. Inversement, à la fin de la boucle, $r$ est nécessairement inférieur à $right$, on peut donc utiliser $r$ et $r + 1$ pour diviser le tableau. Le lecteur peut simuler le processus de l'algorithme pour comprendre pourquoi. Une autre façon simple d'éviter la boucle infinie est de choisir un `pivot` aléatoire ou de gérer spécialement le cas où il n'y a que deux éléments. De même, l'utilisation de $r$ et $l$ pour distinguer le tableau est également incorrecte.
6. De plus, utiliser $l$, $l+1$ ne fonctionne pas non plus, car cette division ne correspond pas à la définition. Lorsque $r$ est à gauche de $l$, utiliser $l$, $l+1$ ne permet pas de diviser correctement le tableau en deux parties : une partie gauche inférieure ou égale à `pivot`, et une partie droite supérieure ou égale à `pivot`.
7. Ce problème suppose que le tableau n'est pas vide, donc il n'y a pas de cas où `left > right`. Cependant, il est recommandé d'utiliser `>=`, pour plus de sécurité.

---

## Compléments

Le tri rapide peut également être transformé en "sélection rapide", qui permet de trouver le $k$-ième plus petit nombre d'un tableau non trié en $O(n)$ en temps espéré. L'idée est similaire à celle du tri rapide, mais à chaque étape, on ne continue la récursion que sur un seul sous-intervalle, ce qui réduit la complexité temporelle.