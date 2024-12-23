---
title: "hello-world"
date: 2024-12-23
draft: true
description: "une description"
tags: [ "exemple", "tag" ]
categories: [ "exemple c" ]
series: [ "exemple s" ]
series_order: 5
---
{{< katex >}}

un exemple pour vous aider à démarrer.

# Ceci est un titre

## Ceci est un sous-titre

### Ceci est un sous-sous-titre

#### Ceci est un sous-sous-sous-titre

Ceci est un paragraphe avec du texte en **gras** et *italique*.
Consultez plus d'informations dans la [documentation de Blowfish](https://blowfish.page/)
non défini

## Mathématiques

Notation en ligne : \\(\varphi = \dfrac{1+\sqrt5}{2}= 1.6180339887…\\)

Mathématiques en bloc :

$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$

## Mot-clé
{{< keyword >}} Super compétence {{< /keyword >}}

## Code

Code en ligne : `a = b + c`
Code en bloc :

```python
print("Bonjour, le monde !")
# très longue ligne :
a = 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10 + 11 + 12 + 13 + 14 + 15 + 16 + 17 + 18 + 19 + 20 + 21
```

{{< highlight html "linenos=table,hl_lines=4 7-9" >}}

<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Exemple de document HTML5</title>
</head>
<body>
  <p>Test</p>
</body>
</html>
{{< /highlight >}}

{{< highlight python "linenos=table" >}}
print("Bonjour, le monde !")
print(1 + 3)
{{< /highlight >}}

## Listes

1. Premier élément
2. Deuxième élément
3. Troisième élément

- Premier élément
- Deuxième élément
- Troisième élément

## Citations

> Ceci est une citation.

## Tableaux

| En-tête 1 | En-tête 2 |
|----------|----------|
| Ligne 1    | Ligne 1    |

## Mermaid2

{{< mermaid >}}
graph LR;
A[Citrons]-->B[Limonade];
B-->C[Profit]
{{< /mermaid >}}

## Typeit

{{< typeit >}}
Lorem ipsum dolor sit amet 
{{< /typeit >}}