---
title: "Problème du sac à dos 0/1"
date: 2024-12-24
draft: false
description: "Le problème du sac à dos classique le plus basique."
summary: "Le problème du sac à dos classique le plus basique."
tags: [ "Algorithme", "Programmation Dynamique", "Problème du sac à dos" ]
categories: [ "Algorithmes et Structures de Données" ]
---

## Problème

Il y a $N$ objets. Le volume du $i$-ème objet est $s_i$, et sa valeur est $v_i$.
Chaque objet ne peut être pris qu'une seule fois. Sous la condition de ne pas dépasser la limite de volume total maximal $S$, trouvez la valeur totale maximale $V$ qui peut être obtenue.

## Format d'entrée

La première ligne contient deux entiers, $N$ et $S$, séparés par un espace, représentant respectivement le nombre d'objets et la limite de volume total maximal.
Les $N$ lignes suivantes contiennent chacune deux entiers, $s_i$ et $v_i$, séparés par un espace, représentant respectivement le volume et la valeur du $i$-ème objet.

## Format de sortie

Affichez un entier représentant la valeur maximale.

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

- Définir l'état : `f[i][j]` représente la valeur maximale qui peut être obtenue à partir des $i$ premiers objets avec une limite de volume de $j$.
    - Si le $i$-ème objet n'est pas pris, alors `f[i][j] = f[i - 1][j]`
    - Si le $i$-ème objet est pris, alors `f[i][j] = f[i - 1][j - s[i]] + v[i]`
    - Lors de l'implémentation de la transition d'état, faites attention à la plage du domaine. Si $j < s_i$, alors ne considérez pas le cas de la prise du $i$-ème objet. Car si $j - s_i$ est négatif, l'index du tableau est illégal.
      Cela peut aussi être expliqué de cette façon : le volume du $i$-ème objet est supérieur à la limite de volume, donc c'est impossible.
- Définir la condition initiale : Pour les $0$ premiers objets, toute limite de volume donne une valeur de $0$, c'est-à-dire `f[0][j] = 0`, `j` $\in [0, S]$.
- Complexité temporelle : $O(NS)$.

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

- La compression du tableau bidimensionnel en un tableau unidimensionnel peut considérablement économiser de l'espace et améliorer la vitesse d'exécution dans une certaine mesure (l'inconvénient est qu'il ne peut pas répondre aux exigences particulières de certains types de problèmes).
- Notez que dans la transition d'état, `f[i][j]` n'est lié qu'à `f[i - 1][j]` et `f[i - 1][j - s[i]]`. En d'autres termes, dans le tableau bidimensionnel `f` du code,
  `f[i][j]` n'est lié qu'aux éléments de la ligne précédente qui sont à sa gauche ou dans la même colonne. Par conséquent, le tableau bidimensionnel peut être compressé en un tableau unidimensionnel ou un tableau roulant.
- Notez que dans le code ci-dessous, la deuxième boucle itère dans l'ordre inverse. C'est parce que nous voulons nous assurer que lors du calcul de `f[i][j]`, `f[i - 1][j - s[i]]` n'a pas encore été mis à jour.

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

Non seulement la valeur totale maximale qui peut être obtenue doit être affichée, mais aussi "combien de méthodes de sélection différentes peuvent atteindre cette valeur totale maximale". Ce qui suit décrit **comment compter le nombre de schémas** dans le problème du sac à dos 0/1.

### DP 2D pour compter les schémas

Ce qui suit utilise la DP 2D comme exemple pour expliquer.

- Définir l'état :
  - `dp[i][j]` représente "la valeur maximale qui peut être obtenue en considérant les i premiers objets avec une capacité (limite de volume) de j".
  - `ways[i][j]` représente "le **nombre de schémas** correspondant à la valeur maximale obtenue en considérant les i premiers objets avec une capacité de j".

- Transition d'état :
  1. Si le `i`-ème objet n'est pas sélectionné :
     $$
       \text{dp}[i][j] = \text{dp}[i-1][j], 
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
     $$
  2. Si le `i`-ème objet est sélectionné (à condition que $ j \ge s_i $) :
     $$
       \text{dp}[i][j] 
         = \text{dp}[i-1][j - s_i] + v_i,
       \quad
       \text{ways}[i][j]
         = \text{ways}[i-1][j - s_i]
     $$
  3. Qu'il faille sélectionner ou non, le `dp[i][j]` final doit prendre le plus grand des deux :
     - Si
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           > \text{dp}[i-1][j],
       $$
       alors cela signifie que "la sélection du i-ème objet" a une plus grande valeur :
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
       cela signifie que la valeur maximale obtenue par les deux méthodes est la même, alors le nombre de schémas doit être ajouté :
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
       alors cela signifie que "ne pas sélectionner le i-ème objet" a une plus grande valeur, et le nombre de schémas hérite du nombre de schémas lors de la non-sélection :
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Conditions initiales :
  - `dp[0][j] = 0` signifie que lorsqu'il y a 0 objet, la valeur maximale obtenue pour toute capacité est 0.
  - `ways[0][0] = 1` signifie que le cas de "0 objet, capacité 0" est un schéma réalisable (c'est-à-dire ne rien sélectionner), et le **nombre de schémas** est défini sur 1.
  - Pour `j > 0`, lorsqu'il n'y a pas d'objet à choisir et que la capacité est supérieure à 0, il est impossible d'obtenir une valeur positive, et le nombre de schémas correspondant est 0, c'est-à-dire `ways[0][j] = 0`.

- Réponse finale :
  - `dp[N][S]` est la valeur maximale.
  - `ways[N][S]` est le nombre de schémas pour atteindre cette valeur maximale.
  - Complexité temporelle : $O(NS)$.
  - Ce problème peut également être optimisé en utilisant la DP 1D.

## Si l'exigence est d'atteindre exactement la limite de volume

- Définir l'état : `f[i][j]` représente la valeur maximale lorsque les `i` premiers objets ont exactement un volume de $j$.
- Si le `i`-ème objet n'est pas pris, alors `f[i][j] = f[i - 1][j]`
- Si le `i`-ème objet est pris, alors `f[i][j] = f[i - 1][j - s[i]] + v[i]`
- On peut noter qu'il n'y a pas de différence dans la transition d'état par rapport au problème d'origine.
- Cependant, les conditions initiales sont différentes. À l'exception de `f[0][0] = 0`, le reste `f[0][j]` = $-\infty$, `j` $\in [1, S]$. $-\infty$ représente un état impossible.

## Si la limite de volume $S$ est très grande (1e9), tandis que le nombre d'objets $N$ et la valeur totale maximale $V$ sont relativement petits

- Pour de tels problèmes, il existe une solution avec une complexité de $O(NV)$.
- Définir l'état : `f[i][j]` représente le volume minimal lors de la sélection de plusieurs objets parmi les `i` premiers objets, et la valeur totale est exactement `j`.
    - Si le `i`-ème objet n'est pas pris, alors `f[i][j] = f[i - 1][j]`
    - Si le `i`-ème objet est pris, alors `f[i][j] = f[i - 1][j - v[i]] + s[i]`
    - Prendre le plus petit des deux.
- Conditions initiales : `f[0][0] = 0`, le reste `f[0][j]` = $\infty$, `j` $\in [1, V]$. $\infty$ représente un état impossible. Notez que ce n'est pas $-\infty$.
- La réponse finale est le plus grand `j` dans `f[N][j]` tel que `f[N][j] <= S`.

## Si la limite de volume $S$ et la valeur d'un seul objet $v_i$ sont toutes deux très grandes (de l'ordre de 1e9), tandis que le nombre d'objets $N$ est très petit (pas plus de 40)

- Lorsque $N \leq 20$, tous les sous-ensembles peuvent être directement énumérés par force brute (complexité temporelle $O(2^N)$).
- Lorsque $N \leq 40$, puisque $2^{40}$ est de l'ordre de $10^{12}$, la force brute directe sera également relativement importante, donc la **recherche par rencontre au milieu** peut être utilisée pour réduire la complexité à environ $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$, ce qui peut être réalisé dans un temps acceptable.