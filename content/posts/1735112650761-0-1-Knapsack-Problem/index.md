---
title: "01 Knapsack Problem"
date: 2024-12-24
draft: false
description: "The most basic classic knapsack problem."
summary: "The most basic classic knapsack problem."
tags: [ "Algorithm", "Dynamic Programming", "Knapsack Problem" ]
categories: [ "Algorithms and Data Structures" ]
series: [ "Nine Chapters on Knapsack Problems" ]
series_order: 1
---

## Problem

There are $N$ items. The volume of the $i$-th item is $s_i$, and its value is $v_i$.
Each item can be taken only once. Find the maximum total value $V$ that can be obtained without exceeding the maximum total volume limit $S$.

## Input Format

The first line contains two integers, $N$ and $S$, separated by a space, representing the number of items and the maximum total volume limit, respectively.
The following $N$ lines each contain two integers, $s_i$ and $v_i$, separated by a space, representing the volume and value of the $i$-th item, respectively.

## Output Format

Output an integer, representing the maximum value.

## Data Range

$$0 \le N, S \leq 1000$$

$$0 \le s_i, v_i \leq 1000$$

## Input Example

```
4 5
1 2
2 4
3 4
4 5
```

## Output Example

```
8
```

## Solution

- Define state: `f[i][j]` represents the maximum value that can be obtained using the first $i$ items with a volume limit of $j$.
    - If we don't take the $i$-th item, then `f[i][j] = f[i - 1][j]`
    - If we take the $i$-th item, then `f[i][j] = f[i - 1][j - s[i]] + v[i]`
    - When implementing state transitions, pay attention to the domain. If $j < s_i$, then we do not consider taking the $i$-th item because if $j - s_i$ is negative, the array index would be invalid.
      Alternatively, we can explain this by saying that if the volume of the $i$-th item is greater than the volume limit, it is impossible to take it.
- Define initial conditions: The maximum value that can be obtained using the first 0 items with any volume limit is 0, i.e., `f[0][j] = 0`, `j` $\in [0, S]$.
- Time complexity: $O(NS)$.

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

## 1D DP Optimization

- Compressing a two-dimensional array into a one-dimensional array can significantly save space and increase the running speed to some extent (the disadvantage is that it cannot meet the special requirements of some problem types).
- Notice that in the state transition, `f[i][j]` is only related to `f[i - 1][j]` and `f[i - 1][j - s[i]]`. In other words, in the two-dimensional array `f` in the code, `f[i][j]` is only related to the elements in the previous row that are to its left or in the same column. Therefore, we can compress the two-dimensional array into a one-dimensional array or a rolling array.
- Notice that in the code below, the second loop iterates in reverse order. This is because we need to ensure that when calculating `f[i][j]`, `f[i - 1][j - s[i]]` has not been updated yet.

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

## If the number of solutions is required

In addition to outputting the maximum total value that can be obtained, we also need to output "how many different selection methods can achieve this maximum total value". The following introduces **how to count the number of solutions** in the 01 knapsack problem.

### 2D DP Counting Solutions

The following explains using 2D DP as an example.

- Define state:
  - `dp[i][j]` represents "the maximum value that can be obtained when considering the first i items and the capacity (volume limit) is j."
  - `ways[i][j]` represents "the **number of solutions** corresponding to obtaining the maximum value when considering the first i items and the capacity is j."

- State Transition:
  1. If the i-th item is not selected:
     $$
       \text{dp}[i][j] = \text{dp}[i-1][j], 
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
     $$
  2. If the i-th item is selected (provided $ j \ge s_i $):
     $$
       \text{dp}[i][j] 
         = \text{dp}[i-1][j - s_i] + v_i,
       \quad
       \text{ways}[i][j]
         = \text{ways}[i-1][j - s_i]
     $$
  3. Whether to select or not, the final `dp[i][j]` should take the larger of the two:
     - If
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           > \text{dp}[i-1][j],
       $$
       then it indicates that the "value of selecting the i-th item" is greater:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j - s_i] + v_i,
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j - s_i].
       $$
     - If
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           = \text{dp}[i-1][j],
       $$
       it indicates that the maximum value obtained by the two methods is the same, so the number of solutions should be added up:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j], 
         \quad
         \text{ways}[i][j] 
           = \text{ways}[i-1][j] 
             + \text{ways}[i-1][j - s_i].
       $$
     - If
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           < \text{dp}[i-1][j],
       $$
       then it indicates that the "value of not selecting the i-th item" is greater, and the number of solutions inherits the number of solutions when not selecting:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Initial Conditions:
  - `dp[0][j] = 0` indicates that when considering the first 0 items, the maximum value obtained for any capacity is 0.
  - `ways[0][0] = 1` indicates that "the case of considering the first 0 items with a capacity of 0" is a feasible solution (i.e., selecting nothing), and the **number of solutions** is set to 1.
  - For `j > 0`, when there are no items to choose from and the capacity is greater than 0, it is impossible to obtain any positive value, and the corresponding number of solutions is 0, i.e., `ways[0][j] = 0`.

- Final Answer:
  - `dp[N][S]` is the maximum value.
  - `ways[N][S]` is the number of solutions to achieve this maximum value.
  - Time complexity: $O(NS)$.
  - This problem can also be optimized using 1D DP.

## If it is required to reach the exact volume limit

- Define state: `f[i][j]` represents the maximum value when the first `i` items have exactly a volume of $j$.
- If we don't take the $i$-th item, then `f[i][j] = f[i - 1][j]`
- If we take the $i$-th item, then `f[i][j] = f[i - 1][j - s[i]] + v[i]`
- Notice that the state transition is the same as the original problem.
- However, the initial conditions are different. Besides `f[0][0] = 0`, the rest `f[0][j]` = $-\infty$, `j` $\in [1, S]$. $-\infty$ represents an impossible state.

## If the volume limit $S$ is very large (1e9), while the number of items $N$ and the maximum total value $V$ are relatively small

- For this type of problem, there is a solution with a time complexity of $O(NV)$.
- Define state: `f[i][j]` represents the minimum volume when selecting some of the first `i` items with a total value of exactly `j`.
    - If we don't take the $i$-th item, then `f[i][j] = f[i - 1][j]`
    - If we take the $i$-th item, then `f[i][j] = f[i - 1][j - v[i]] + s[i]`
    - Take the smaller of the two.
- Initial conditions: `f[0][0] = 0`, the rest `f[0][j]` = $\infty$, `j` $\in [1, V]$. $\infty$ represents an impossible state. Note that it is not $-\infty$.
- The final answer is the largest `j` such that `f[N][j] <= S` among all `f[N][j]`.

## If the volume limit $S$ and the value of a single item $v_i$ are both very large (on the order of $1e9$), while the number of items $N$ is very small (no more than 40)

- When $N \leq 20$, we can directly enumerate all subsets (time complexity $O(2^N)$).
- When $N \leq 40$, since $2^{40}$ is on the order of $10^{12}$, directly brute force is also quite large, so we can use **meet-in-the-middle search**, which roughly reduces the complexity to $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$, which can be completed within an acceptable time.