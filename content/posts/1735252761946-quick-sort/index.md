# Quick Sort

**Date:** 2024-12-26
**Draft:** false
**Description:** Analysis of key points for correctly implementing the quick sort algorithm.
**Summary:** Analysis of key points for correctly implementing the quick sort algorithm.
**Tags:** [ "Algorithm", "Sorting Algorithm", "Quick Sort", "Divide and Conquer Algorithm" ]
**Categories:** [ "Algorithms and Data Structures" ]

---

## Quick Sort

Quick sort is a comparison-based, unstable sorting algorithm that uses the divide-and-conquer approach. It has an average time complexity of $O(n\log n)$, a worst-case time complexity of $O(n^2)$, and a space complexity of $O(1)$. The following will use sorting an integer sequence in ascending order as an example to introduce its implementation details and common mistakes.

---

## Problem Description

Given an integer sequence of length $n$, sort it in ascending order using quick sort and output the result.

### Input Format

- The first line contains an integer $n$.
- The second line contains $n$ integers, all within the range $[1, 10^9]$.

### Output Format

- Output the sorted sequence on a single line.

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

In each divide step of quick sort, a number is arbitrarily chosen as the pivot (the number in the middle position is chosen below).

Use left and right pointers moving towards each other. The left pointer `L` searches from left to right for the first number greater than or equal to the `pivot`, and the right pointer `R` searches from right to left for the first number less than or equal to the `pivot`. Then, swap these two numbers.

Repeat this process until the left and right pointers overlap or the left pointer is one position to the right of the right pointer. This is called one cycle.

After each pointer movement and swap, ensure that the structure "left part ≤ pivot, right part ≥ pivot" is not broken, i.e., the invariant `[left, L) <= pivot`, `(R, right] >= pivot` holds.

In the example code below, `left` and `right` are the boundaries of the currently processed closed interval, and `pivot` is the element at the midpoint of the interval.

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

Since quick sort has a worst-case complexity of $O(n^2)$, the selection of the `pivot` is crucial. If the first or last element is always chosen, the worst case is likely to occur in nearly sorted arrays.

In addition to taking the element in the middle position, a random element can be selected as the `pivot`, or the median of the left, middle, and right elements can be taken as the `pivot`.

---

## Common Error Examples

The following code contains several common errors.

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

1.  `pivot` should be a number in the array, not an index.
2.  Use `<` and `>` instead of `<=` and `>=`, otherwise the left pointer may move more than one position past the right pointer, which would prevent the array from being divided into two parts.
3.  After finding `l >= r`, the loop should be exited immediately without performing the swap. Otherwise, it cannot be guaranteed that the elements on the left are not greater than `pivot` and the elements on the right are not less than `pivot`.
4.  After each swap, `l++` and `r--` should be executed.
5.  `pivot` actually takes the number in the middle-left position. Therefore, if $l - 1$ and $l$ are used to divide the array, consider the array `[1, 2]`. It is not difficult to see that this will lead to an infinite loop, continuously dividing the array into two parts of size 0 and 2. Similarly, using $r$ and $l$ to divide the array will not work. Instead, at the end of a cycle, $r$ must be less than $right$, so $r$ and $r+1$ can be used to divide the array. The reader can simulate the algorithm process to see why. Another simple way to avoid infinite loops is to randomly select the `pivot` or handle the case of only two elements specially.
6.  Also, using $l$, $l+1$ will not work, because this division does not conform to the definition. When $r$ is to the left of $l$, using $l$, $l+1$ cannot correctly divide the array into two parts: the left part less than or equal to `pivot`, and the right part greater than or equal to `pivot`.
7.  This problem assumes that the array is not empty, so there is no case where `>` is used. However, it is recommended to use `>=`, which is safer.

---

## Supplement

Quick sort can also be evolved into "quick select", which can find the $k$-th smallest number in an unordered array in $O(n)$ expected time. The specific idea is similar to quick sort, except that it only continues to recurse in one sub-interval each time, thus reducing the time complexity.