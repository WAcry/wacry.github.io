---
title: "Quick Sort"
date: 2024-12-26
draft: false
description: "Analysis of key points for correctly implementing the quick sort algorithm."
summary: "Analysis of key points for correctly implementing the quick sort algorithm."
tags: [ "Algorithm", "Sorting Algorithm", "Quick Sort", "Divide and Conquer" ]
categories: [ "Algorithms and Data Structures" ]
---

# Quick Sort

Quick sort is a comparison-based, unstable sorting algorithm that employs the divide-and-conquer paradigm. Its average time complexity is $O(n\log n)$, with a worst-case complexity of $O(n^2)$, and a space complexity of $O(1)$. Below, we will use sorting an integer array in ascending order as an example to introduce its implementation details and common mistakes.

---

## Problem Description

Given an integer array of length $n$, use quick sort to sort it in ascending order and output the result.

### Input Format

- The first line inputs the integer $n$.
- The second line inputs $n$ integers, all within the range $[1, 10^9]$.

### Output Format

- Output the sorted array in a single line.

### Data Range

$1 \leq n \leq 100000$

### Input Example

```
5
3 1 2 4 5
```

### Output Example

```
1 2 3 4 5
```

---

## Quick Sort Approach

Each time quick sort divides, it arbitrarily selects a number as the pivot (below, we choose the number at the middle position).

Use left and right pointers that move towards each other. The left pointer `L` searches from left to right for the first number greater than or equal to `pivot`, and the right pointer `R` searches from right to left for the first number less than or equal to `pivot`. Then, swap these two numbers.

Repeat this process until the left and right pointers overlap or the left pointer is one position past the right pointer. This is called one cycle.

After each pointer movement and swap, the structure "left part ≤ pivot, right part ≥ pivot" is guaranteed to be preserved, i.e., there is an invariant `[left, L) <= pivot`, `(R, right] >= pivot`.

In the example code below, `left` and `right` are the boundaries of the currently processed closed interval, and `pivot` takes the element at the midpoint of the interval.

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

## Complexity and `pivot` Selection

Since quick sort has a complexity of $O(n^2)$ in the worst case, the selection of `pivot` is crucial. If the first or last element is always chosen, the worst case will likely occur in nearly sorted arrays.

Besides taking the element at the middle position, you can also randomly select an element as the `pivot`, or take the median of the left, middle, and right elements as the `pivot`.

---

## Common Mistake Examples

The following code contains several common mistakes.

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

**Error Analysis:**

1. `pivot` should be a number in the array, not an index.
2. Using `<=` and `>=` instead of `<` and `>` respectively, otherwise the left pointer might move more than one position past the right pointer, so the array can't be split into two parts correctly.
3. After `l >= r` is detected, the loop should terminate immediately, and no more swaps should be performed. Otherwise, it cannot be guaranteed that the left elements are not greater than `pivot` and that the right elements are not less than `pivot`.
4. After each swap, `l++` and `r--` should be executed.
5. `pivot` actually takes the number in the middle slightly towards the left. If you use $l - 1$ and $l$ to split the array, consider the array `[1, 2]`. It is not difficult to see that it will lead to an infinite loop, constantly dividing the array into parts of size 0 and 2. On the contrary, when the loop ends, $r$ must be less than $right$, so you can use $r$ and $r+1$ to split the array. Readers can simulate the algorithm process to see why. Another simple way to avoid the infinite loop is to randomly select `pivot` or handle the case with only two elements specially. Similarly, using $r$ and $l$ to distinguish the array will also not work.
6. Additionally, using $l$, $l+1$ won't work either, because this division does not meet the definition. When $r$ is to the left of $l$, using $l$, $l+1$ cannot correctly divide the array into two parts: left part less than or equal to `pivot`, and right part greater than or equal to `pivot`.
7. This problem assumes the array is not empty, so there is no case where `>` will occur. However, it is safer to use `>=`, which is recommended.

---

## Supplement

Quick sort can also be evolved into "quick select", which can find the $k$-th smallest number in an unsorted array in expected $O(n)$ time. The specific idea is similar to quick sort, but it only continues recursion in one side of the sub-intervals each time, thus reducing the time complexity.