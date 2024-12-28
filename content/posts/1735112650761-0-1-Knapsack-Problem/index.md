---
title: 0-1 knapsack problem
date: 2024-12-24
draft: false
description: The most basic classic knapsack problem.
summary: The most basic classic knapsack problem.
series:
  - Classic Knapsack Problem Set
series_order: 1
tags:
  - Algorithm
  - Dynamic programming
  - Knapsack problem
---

## Problem

There are $N$ items. The volume of the $i$-th item is $s_i$, and its value is $v_i$. Each item can be taken only once.
Under the premise of not exceeding the maximum total volume limit $S$, find the maximum total value $V$ that can be
obtained.

## Input Format

The first line contains two integers, $N$ and $S$, separated by a space, representing the number of items and the
maximum total volume limit, respectively.
The following $N$ lines each contain two integers, $s_i$ and $v_i$, separated by a space, representing the volume and
value of the $i$-th item, respectively.

## Output Format

Output an integer representing the maximum value.

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

- Define the state: `f[i][j]` represents the maximum value that can be obtained from the first $i$ items with a volume
  limit of $j$.
    - If the $i$-th item is not taken, then `f[i][j] = f[i - 1][j]`
    - If the $i$-th item is taken, then `f[i][j] = f[i - 1][j - s[i]] + v[i]`
    - When implementing the state transition, pay attention to the domain range. If $j < s_i$, then do not consider
      taking the $i$-th item. Because if $j - s_i$ is negative, the array index is invalid.
      It can also be explained as: the volume of the $i$-th item is greater than the volume limit, so it is impossible.
- Define the initial condition: For the first 0 items, any volume limit yields a value of 0, i.e., `f[0][j] = 0`,
  `j` $\in [0, S]$.
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

- Compressing the two-dimensional array into a one-dimensional array can significantly save space and improve the
  running speed to a certain extent (the disadvantage is that it cannot meet the special requirements of some problem
  types).
- Note that in the state transition, `f[i][j]` is only related to `f[i - 1][j]` and `f[i - 1][j - s[i]]`. In other
  words, in the two-dimensional array `f` in the code,
  `f[i][j]` is only related to the elements in the previous row that are to its left or in the same column. Therefore,
  the two-dimensional array can be compressed into a one-dimensional array or a rolling array.
- Note that in the code below, the second loop iterates in reverse order. This is because we need to ensure that when
  calculating `f[i][j]`, `f[i - 1][j - s[i]]` has not been updated yet.

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

## If the Number of Schemes is Required

Not only should the maximum total value that can be obtained be output, but also "how many different selection methods
can achieve this maximum total value". The following introduces how to count the number of schemes in the 01 knapsack
problem.

### 2D DP for Counting Schemes

The following uses 2D DP as an example for explanation.

- Define the state:
    - `dp[i][j]` represents "the maximum value that can be obtained when considering the first i items with a capacity (
      volume limit) of j".
    - `ways[i][j]` represents "the number of **schemes** corresponding to the maximum value obtained when considering
      the first i items with a capacity of j".

- State transition:
    1. If the $i$-th item is not selected:
       $$
       \text{dp}[i][j] = \text{dp}[i-1][j],
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
       $$
    2. If the $i$-th item is selected (provided that $ j \ge s_i $):
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
          then it means that "selecting the i-th item" has a greater value:
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
          it means that the maximum value obtained by the two methods is the same, then the number of schemes should be
          added:
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
          then it means that "not selecting the i-th item" has a greater value, and the number of schemes inherits the
          number of schemes when not selecting:
          $$
          \text{dp}[i][j] = \text{dp}[i-1][j],
          \quad
          \text{ways}[i][j] = \text{ways}[i-1][j].
          $$

- Initial conditions:
    - `dp[0][j] = 0` means that when there are 0 items, the maximum value obtained for any capacity is 0.
    - `ways[0][0] = 1` means that "0 items, capacity 0" is a feasible scheme (i.e., selecting nothing), and the **number
      of schemes** is set to 1.
    - For `j > 0`, when there are no items to choose from and the capacity is greater than 0, it is impossible to obtain
      any positive value, and the corresponding number of schemes is 0, i.e., `ways[0][j] = 0`.

- Final answer:
    - `dp[N][S]` is the maximum value.
    - `ways[N][S]` is the number of schemes to achieve this maximum value.
    - Time complexity: $O(NS)$.
    - This problem can also be optimized using 1D DP.

## If the Requirement is to Exactly Reach the Volume Limit

- Define the state: `f[i][j]` represents the maximum value when the first `i` items have exactly a volume of $j$.
- If the $i$-th item is not taken, then `f[i][j] = f[i - 1][j]`
- If the $i$-th item is taken, then `f[i][j] = f[i - 1][j - s[i]] + v[i]`
- It can be noted that there is no difference in the state transition from the original problem.
- However, the initial conditions are different. Besides `f[0][0] = 0`, the rest `f[0][j]` = $-\infty$,
  `j` $\in [1, S]$. $-\infty$ represents an impossible state.

## If the Volume Limit $S$ is Very Large (1e9), While the Number of Items $N$ and the Maximum Total Value $V$ are Relatively Small

- For such problems, there is a solution with a complexity of $O(NV)$.
- Define the state: `f[i][j]` represents the minimum volume when selecting several items from the first `i` items, with
  a total value of exactly `j`.
    - If the $i$-th item is not taken, then `f[i][j] = f[i - 1][j]`
    - If the $i$-th item is taken, then `f[i][j] = f[i - 1][j - v[i]] + s[i]`
    - Take the smaller of the two.
- Initial conditions: `f[0][0] = 0`, the rest `f[0][j]` = $\infty$, `j` $\in [1, V]$. $\infty$ represents an impossible
  state. Note that it is not $-\infty$.
- The final answer is the largest `j` in `f[N][j]` such that `f[N][j] <= S`.

## If the Volume Limit $S$ and the Value of a Single Item $v_i$ are Both Very Large (on the order of 1e9), While the Number of Items $N$ is Very Small (no more than 40 at most)

- When $N \leq 20$, all subsets can be directly enumerated by brute force (time complexity $O(2^N)$).
- When $N \leq 40$, since $2^{40}$ is on the order of $10^{12}$, direct brute force will also be relatively large, so *
  *meet-in-the-middle search** can be used to reduce the complexity to
  approximately $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$, which
  can be completed in an acceptable time.