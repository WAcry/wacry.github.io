---
title: "Binary Search"
date: 2024-12-24
draft: false
description: "How to elegantly implement the binary search algorithm."
summary: "How to elegantly implement the binary search algorithm."
tags: [ "Algorithm", "Binary Search", "Algorithm Template" ]
categories: [ "Algorithms and Data Structures" ]
---

If an ordered solution space is divided into two parts, where one part satisfies a condition and the other does not, then binary search can be used to find the critical point in the ordered solution space.

The basic idea of binary search is to repeatedly halve the search interval. Each time, the middle element is checked. If the middle element does not satisfy the condition, half of the interval can be eliminated; otherwise, the search continues in the other half. Since half of the search interval is discarded each time, the search time complexity can reach $O(\log n)$.

## Example Problem

**Problem Description:**
Given an ascendingly sorted integer array of length $n$, and $q$ queries. Each query gives an integer $k$, and we need to find the "starting position" and "ending position" of $k$ in the array (indices start from 0). If the number does not exist in the array, return `-1 -1`.

### Input Format

1. First line: two integers $n$ and $q$, representing the length of the array and the number of queries, respectively.
2. Second line: $n$ integers, representing the complete array, already sorted in ascending order.
3. Next $q$ lines: each line contains an integer $k$, representing a query element.

## Data Range

$1 \leq n \leq 100000$

$1 \leq q \leq 10000$

$1 \leq k \leq 10000$

### Output Format

For each query, output the starting and ending positions of the element in the array on a single line. If the element does not exist in the array, output `-1 -1`.

**Example:**

```
Input:
6 3
1 2 2 3 3 4
3
4
5

Output:
3 4
5 5
-1 -1
```

**Explanation:**

- The range where element $3$ appears is $[3, 4]$;
- Element $4$ appears only once, at position $5$;
- Element $5$ does not exist in the array, so return $-1$ $-1$.

---

## Solution

- **Finding the "Starting Position":**
  That is, finding the first position that is greater than or equal to $k$. The array can be divided into two parts:
    - All numbers on the left are "less than" $k$
    - All numbers on the right are "greater than or equal to" $k$
    - The answer is the first position on the right

- **Finding the "Ending Position":**
  That is, finding the last position that is less than or equal to $k$. The array can be divided into two parts:
    - All numbers on the left are "less than or equal to" $k$
    - All numbers on the right are "greater than" $k$
    - The answer is the last position on the left

---

## Recommended Template

Below is an elegant and less error-prone binary search template.

Define two pointers $l, r$, with the invariant: the closed interval $[0, l]$ belongs to the left part, and the closed interval $[r, n - 1]$ belongs to the right part. $l$ and $r$ are initialized to $-1$ and $n$, respectively.

When the algorithm terminates, $l$ and $r$ are adjacent, pointing to the last element of the left part and the first element of the right part, respectively.

Because the solution we want may not exist, if the problem does not state that a solution definitely exists, we need to check if `l` or `r` is out of bounds and if it points to the correct value.

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

        // 1. Find the starting position of k
        //    Divide the array into two parts, the left part is all < k, and the right part is all >= k.
        //    The answer is the smallest index of the right part.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // If r is out of bounds or nums[r] != k, it means k does not exist
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. Find the ending position of k
        //    Divide the array into two parts, the left part is all <= k, and the right part is all > k.
        //    The answer is the largest index of the left part.
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

### Advantages

1. This approach has strictly defined invariants.
2. It applies to both finding the "starting position" and the "ending position" without extra handling or changes.
3. Some approaches use `l == r` as the termination condition. When $l$ and $r$ differ by $1$, $mid$ will be calculated to be equal to $l$ or $r$. If not handled correctly, updating $l$ or $r$ to $mid$ will not shrink the search interval, leading to an infinite loop. In contrast, this approach terminates when $l$ and $r$ are adjacent, ensuring that $mid$ is less than $l$ and greater than $r$, and updating $l$ or $r$ will always shrink the search interval.

---

## STL

If you use the `lower_bound` and `upper_bound` functions provided by C++ STL, you can achieve the same thing:

- `lower_bound(first, last, val)` will return "the first position that is greater than or equal to val"
- `upper_bound(first, last, val)` will return "the first position that is greater than val"

For example, suppose `nums = {1,2,3,4,4,4,4,4,5,5,6}`, and we want to know the range where 4 appears:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    cout << "4 appears 0 times" << endl;
} else {
    cout << "first 4 is at " << it1 - nums.begin() << endl;
    cout << "last 4 is at " << it2 - nums.begin() - 1 << endl;
    cout << "4 appears " << it2 - it1 << " times" << endl;
}
```

- `it1` points to the first position where the value is greater than or equal to $4$.
- `it2` points to the first position where the value is greater than $4$.
  Therefore, `it2 - it1` is the number of times $4$ appears in the array; `it2 - nums.begin() - 1` is the position of the right boundary of $4$.

---

## Additional Notes

Binary search can also be extended to search in floating-point ranges (such as finding the roots of an equation) and ternary search for finding the extrema of unimodal functions.

---

## Practice

LeetCode 33. Search in Rotated Sorted Array

Hint: First, use binary search to find the rotation point, and then use binary search to find the target value.