---
title: "Tri Rapide"
date: 2024-12-26
draft: false
description: "Analyse des points clés pour implémenter correctement l'algorithme de tri rapide."
summary: "Analyse des points clés pour implémenter correctement l'algorithme de tri rapide."
tags: [ "Algorithme", "Algorithmes de tri", "Tri rapide", "Algorithme diviser pour régner" ]
categories: [ "Algorithmes et structures de données" ]
---

# Tri Rapide

Le tri rapide est un algorithme de tri non stable basé sur la comparaison, qui utilise le principe "diviser pour régner". Sa complexité temporelle moyenne est de $O(n\log n)$, et de $O(n^2)$ dans le pire des cas, avec une complexité spatiale de $O(1)$. Nous allons prendre l'exemple du tri d'une suite d'entiers par ordre croissant pour illustrer les détails de son implémentation et les erreurs courantes.

---

## Description du Problème

Étant donnée une suite d'entiers de longueur $n$, utilisez le tri rapide pour la trier par ordre croissant et affichez le résultat.

### Format d'entrée

- La première ligne contient l'entier $n$.
- La deuxième ligne contient $n$ entiers, tous dans l'intervalle $[1,10^9]$.

### Format de sortie

- Une ligne contenant la suite triée.

### Plage de données

$1 \leq n \leq 100000$

### Exemple d'entrée

```
5
3 1 2 4 5
```

### Exemple de sortie

```
1 2 3 4 5
```

---

## Idée du Tri Rapide

À chaque étape de division du tri rapide, un nombre est choisi comme pivot (ici, nous choisissons le nombre au milieu).

Deux pointeurs, gauche `L` et droit `R`, se déplacent l'un vers l'autre. Le pointeur gauche `L` cherche de gauche à droite le premier nombre supérieur ou égal au `pivot`, et le pointeur droit `R` cherche de droite à gauche le premier nombre inférieur ou égal au `pivot`. Ensuite, ces deux nombres sont échangés.

Ce processus est répété jusqu'à ce que les pointeurs gauche et droit se chevauchent ou que le pointeur gauche dépasse le pointeur droit d'une position. Ceci est appelé une itération.

Après chaque déplacement et échange de pointeurs, la structure "partie gauche ≤ pivot, partie droite ≥ pivot" est maintenue, c'est-à-dire qu'il y a un invariant `[left, L) <= pivot`, `(R, right] >= pivot`.

Dans l'exemple de code ci-dessous, `left` et `right` sont les limites de l'intervalle fermé en cours de traitement, et `pivot` est l'élément au milieu de l'intervalle.

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

Étant donné que le tri rapide a une complexité de $O(n^2)$ dans le pire des cas, le choix du `pivot` est crucial. Si l'on choisit toujours le premier ou le dernier élément, le pire des cas se produira probablement dans un tableau presque trié.

En plus de choisir l'élément au milieu, on peut également choisir un élément aléatoire comme `pivot`, ou prendre la médiane des trois éléments de gauche, du milieu et de droite comme `pivot`.

---

## Exemples d'Erreurs Courantes

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
2. Utiliser respectivement `<` et `>` au lieu de `<=` et `>=`, sinon le pointeur gauche pourrait dépasser le pointeur droit de plus d'une position, ce qui empêcherait de diviser le tableau en deux parties.
3. Après avoir constaté que `l >= r`, il faut immédiatement sortir de la boucle et ne plus effectuer d'échange. Sinon, on ne peut pas garantir que les éléments de gauche ne sont pas supérieurs à `pivot` et que les éléments de droite ne sont pas inférieurs à `pivot`.
4. Après chaque échange, il faut exécuter `l++` et `r--`.
5. `pivot` prend en fait le nombre du milieu gauche. Par conséquent, si l'on utilise $l - 1$ et $l$ pour diviser le tableau, il est facile de constater qu'un tableau comme `[1, 2]` conduira à une boucle infinie, divisant continuellement le tableau en deux parties de taille 0 et 2. De même, utiliser $r$ et $l$ pour diviser le tableau ne fonctionne pas non plus. Au contraire, à la fin d'une itération, $r$ est nécessairement inférieur à $right$, on peut donc utiliser $r$ et $r+1$ pour diviser le tableau. Le lecteur peut simuler le processus de l'algorithme pour voir pourquoi. Une autre façon simple d'éviter les boucles infinies est de choisir un `pivot` aléatoire ou de traiter spécialement le cas où il n'y a que deux éléments.
6. De plus, utiliser $l$, $l+1$ ne fonctionne pas non plus, car cette division ne correspond pas à la définition. Lorsque $r$ est à gauche de $l$, utiliser $l$, $l+1$ ne permet pas de diviser correctement le tableau en deux parties : une partie gauche inférieure ou égale à `pivot` et une partie droite supérieure ou égale à `pivot`.
7. Ce problème suppose que le tableau n'est pas vide, il n'y a donc pas de cas où `>` est utilisé. Cependant, il est recommandé d'utiliser `>=`, ce qui est plus sûr.

---

## Complément

Le tri rapide peut également être transformé en "sélection rapide", qui permet de trouver le $k$-ième plus petit nombre dans un tableau non trié en un temps espéré de $O(n)$. L'idée est similaire à celle du tri rapide, sauf qu'à chaque étape, on ne continue la récursion que dans un seul sous-intervalle, ce qui réduit la complexité temporelle.