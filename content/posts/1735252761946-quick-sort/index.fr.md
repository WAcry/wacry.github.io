---
title: "Tri rapide"
date: 2024-12-26
draft: false
description: "Analyse des points clés pour implémenter correctement l'algorithme de tri rapide."
summary: "Analyse des points clés pour implémenter correctement l'algorithme de tri rapide."
tags: [ "Algorithme", "Algorithme de tri", "Tri rapide", "Algorithme diviser pour régner" ]
categories: [ "Algorithmes et structures de données" ]
---

# Tri rapide

Le tri rapide est un algorithme de tri non stable basé sur la comparaison, qui utilise le principe diviser pour régner. Sa complexité temporelle moyenne est de $O(n\log n)$, et dans le pire des cas, elle est de $O(n^2)$, avec une complexité spatiale de $O(1)$. L'exemple ci-dessous utilise le tri d'une séquence d'entiers par ordre croissant pour illustrer les détails de son implémentation et les erreurs courantes.

---

## Description du problème

Étant donné une séquence d'entiers de longueur $n$, utilisez le tri rapide pour la trier par ordre croissant et affichez le résultat.

### Format d'entrée

- La première ligne contient l'entier $n$.
- La deuxième ligne contient $n$ entiers, tous dans l'intervalle $[1,10^9]$.

### Format de sortie

- Une ligne contenant la séquence triée.

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

## Idée du tri rapide

À chaque étape de division du tri rapide, un nombre est choisi arbitrairement comme pivot (`pivot`, ci-dessous, nous choisissons le nombre au milieu).

Deux pointeurs, gauche `L` et droit `R`, se déplacent l'un vers l'autre. Le pointeur gauche `L` recherche de gauche à droite le premier nombre supérieur ou égal à `pivot`, et le pointeur droit `R` recherche de droite à gauche le premier nombre inférieur ou égal à `pivot`. Ensuite, ces deux nombres sont échangés.

Ce processus est répété jusqu'à ce que les pointeurs gauche et droit se chevauchent ou que le pointeur gauche soit une position après le pointeur droit. Ceci est appelé une itération.

Après chaque déplacement et échange de pointeurs, la structure « partie gauche ≤ pivot, partie droite ≥ pivot » est garantie de ne pas être brisée, c'est-à-dire qu'il existe un invariant `[left, L) <= pivot`, `(R, right] >= pivot`.

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

## Complexité et choix du `pivot`

Étant donné que le tri rapide a une complexité de $O(n^2)$ dans le pire des cas, le choix du `pivot` est crucial. Si l'on choisit toujours le premier ou le dernier élément, le pire des cas est très probable dans un tableau presque trié.

En plus de choisir l'élément au milieu, on peut également choisir un élément aléatoire comme `pivot`, ou prendre la médiane des trois éléments de gauche, du milieu et de droite comme `pivot`.

---

## Exemples d'erreurs courantes

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
2. Utiliser respectivement `<` et `>` au lieu de `<=` et `>=`, sinon le pointeur gauche peut dépasser le pointeur droit de plus d'une position, ce qui empêche de diviser le tableau en deux parties.
3. Après avoir constaté que `l >= r`, la boucle doit être immédiatement quittée, et l'échange ne doit plus être exécuté. Sinon, il n'est pas garanti que les éléments de gauche ne soient pas supérieurs à `pivot` et que les éléments de droite ne soient pas inférieurs à `pivot`.
4. Après chaque échange, `l++` et `r--` doivent être exécutés.
5. `pivot` prend en fait le nombre au milieu gauche. Par conséquent, si l'on utilise $l - 1$ et $l$ pour diviser le tableau, il est facile de constater qu'un tableau comme `[1, 2]` entraînera une boucle infinie, divisant continuellement le tableau en deux parties de taille 0 et 2. De même, il n'est pas possible de distinguer le tableau avec $r$ et $l$. Au contraire, à la fin d'une itération, $r$ est nécessairement inférieur à $right$, donc on peut utiliser $r$ et $r+1$ pour diviser le tableau. Le lecteur peut simuler le processus de l'algorithme pour voir pourquoi. Une autre façon simple d'éviter les boucles infinies est de choisir un `pivot` aléatoire ou de traiter spécialement le cas où il n'y a que deux éléments.
6. De plus, utiliser $l$, $l+1$ ne fonctionne pas non plus, car cette division n'est pas conforme à la définition. Lorsque $r$ est à gauche de $l$, utiliser $l$, $l+1$ ne permet pas de diviser correctement le tableau en deux parties, la partie gauche étant inférieure ou égale à `pivot` et la partie droite étant supérieure ou égale à `pivot`.
7. Ce problème suppose que le tableau n'est pas vide, il n'y a donc pas de cas où `>` est utilisé. Cependant, il est recommandé d'utiliser `>=`, ce qui est plus sûr.

---

## Complément

Le tri rapide peut également être transformé en "sélection rapide", qui permet de trouver le $k$-ième plus petit nombre dans un tableau non trié en un temps d'espérance de $O(n)$. L'idée est similaire à celle du tri rapide, sauf que la récursion n'est poursuivie que dans un seul sous-intervalle à chaque fois, ce qui réduit la complexité temporelle.