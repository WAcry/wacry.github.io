---
title: "Binary Search"
date: 2024-12-24
draft: false
description: "How to elegantly implement the integer binary search algorithm"
tags: [ "Algorithm", "Binary Search", "Algorithm Template" ]
categories: [ "Algorithms and Data Structures" ]
---
{{< katex >}}

# Binary Search

Binary search can be used to quickly find a specific element in an ordered sequence. Compared to the linear search with a time complexity of $O(n)$, binary search only requires $O(\log n)$ time, making it very efficient when dealing with large data sets.

## The Core Idea of Binary Search

The basic idea of binary search is to repeatedly halve the search interval. Each time, the middle element is compared with the target value. If the middle element does not satisfy the condition, half of the interval can be eliminated; otherwise, the search continues in the other half of the interval. Since half of the search interval is discarded each time, the search time complexity can reach $O(\log n)$.

Binary search is very useful for problems where "**feasible solutions can be divided into one ordered interval (satisfying the condition) and another ordered interval (not satisfying the condition)**". For example:

- Finding whether an element exists in an ordered array
- Finding the "first position" or "last position" where a number appears

## Example: Finding the Start and End Positions of an Element

**Problem Description:**
Given an ascendingly sorted integer array of length $n$, and $q$ queries. Each query gives an integer $k$, and we need to find the "starting position" and "ending position" of $k$ in the array (indexes starting from 0). If the number does not exist in the array, return $-1$ $-1$.

**Input Format:**

1. The first line: two integers $n$ and $q$, representing the length of the array and the number of queries, respectively.
2. The second line: $n$ integers (within the range of 1 ~ 10000), representing the complete array, already sorted in ascending order.
3. The following $q$ lines: each line contains an integer $k$, representing a query element.

**Output Format:**
For each query, output the start and end positions of the element in the array on a single line. If the element does not exist in the array, output $-1$ $-1$.

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

Explanation:

- The range where element 3 appears is `[3, 4]`;
- Element 4 appears only once, at position 5;
- Element 5 does not exist in the array, so return `-1 -1`.

## The Application Approach of Binary Search

In this problem, we can rely on binary search to find the "left boundary" and "right boundary" of a certain value. The key is to understand how to define the search interval and how to move the pointers based on the comparison result.

- **Finding the "left boundary":**
  That is, finding the first position that is greater than or equal to $k$. The array can be divided into two parts:
    - All numbers on the left are "less than" $k$
    - All numbers on the right are "greater than or equal to" $k$

- **Finding the "right boundary":**
  That is, finding the last position that is less than or equal to $k$. The array can be divided into two parts:
    - All numbers on the left are "less than or equal to" $k$
    - All numbers on the right are "greater than" $k$

As long as these two intervals can be correctly maintained, the result can be quickly obtained through binary search.

## Recommended Template: Binary Search Code to Avoid Infinite Loops

Here's an elegant and error-resistant binary search template. It ensures the loop terminates when $l$ and $r$ are adjacent by gradually bringing $l$ and $r$ closer:

Define two pointers $l, r$, with the invariants: the closed interval $[0, l]$ all belongs to the left part, the closed interval $[r, n - 1]$ all belongs to the right part. $l$ and $r$ are initialized to $-1$ and $n$, respectively.

When the algorithm terminates, $l$ and $r$ are adjacent, pointing to the maximum value in the left part and the minimum value in the right part, respectively.

Because the desired solution may not exist, when returning $l$ or $r$, it is necessary to check if the corresponding value is the value we want and if it is out of bounds.
For example, $l$ represents the maximum value $\leq k$, and we need to check `l != -1 && nums[l] == k`

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

        // 1. Find the starting position of k (left boundary)
        //    Divide the array into two parts, the left part all < k, and the right part all >= k.
        //    The left boundary is the smallest index of the right part.
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

        int leftPos = r; // Record the left boundary of k

        // 2. Find the ending position of k (right boundary)
        //    Divide the array into two parts, the left part all <= k, and the right part all > k.
        //    The right boundary is the largest index of the left part.
        l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] <= k) l = mid;
            else r = mid;
        }

        // Since we have already verified that k exists, there is no need to verify again here
        int rightPos = l; // Right boundary
        cout << leftPos << " " << rightPos << endl;
    }
    return 0;
}
```

### Why is this method less error-prone?

1. This method has strictly defined invariants.
2. It can find both the left and right boundaries, making it applicable to all scenarios.
3. Some methods use $l == r$ as the termination condition. When $l$ and $r$ differ by 1, the calculated $mid$ will be equal to `l` or `r`. If not handled correctly, updating
   `l` or `r` to `mid` will not shrink the search interval, leading to an infinite loop. In contrast, this method terminates when $l$ and $r$ are adjacent, avoiding this problem.

## STL Solution: `lower_bound` and `upper_bound`

If you use the `lower_bound` and `upper_bound` functions provided by C++ STL, you can easily accomplish the same thing:

- `lower_bound(first, last, val)` returns "the first position greater than or equal to val"
- `upper_bound(first, last, val)` returns "the first position greater than val"

For example, suppose `nums = {1,2,3,4,4,4,4,4,5,5,6}`, and we want to know the interval where 4 appears:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    // Indicates that 4 does not exist in the array
    cout << "4 appears 0 times" << endl;
} else {
    cout << "first 4 is at " << it1 - nums.begin() << endl;
    cout << "last 4 is at " << it2 - nums.begin() - 1 << endl;
    cout << "4 appears " << it2 - it1 << " times" << endl;
}
```

- `it1` points to the first position where the value is greater than or equal to 4.
- `it2` points to the first position where the value is greater than 4.
  Therefore, `it2 - it1` is the number of times 4 appears in the array; `it2 - nums.begin() - 1` is the right boundary of 4.

These two functions are particularly convenient when searching intervals or counting occurrences.

## Supplement

Binary search can also be extended to search within floating-point numbers (e.g., finding the roots of an equation), as well as ternary search to find the extreme values of unimodal functions. As long as you understand the core principle of "**eliminating half in an ordered interval each time**," you will find that binary search can help you solve problems efficiently in many scenarios.

## Homework

LeetCode 33. Search in Rotated Sorted Array

Hint: Use binary search to find the rotation point first, and then use binary search to find the target value.