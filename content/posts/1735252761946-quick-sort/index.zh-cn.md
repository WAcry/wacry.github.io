---
title: "快速排序"
date: 2024-12-26
draft: false
description: "正确实现快速排序算法的要点解析。"
summary: "正确实现快速排序算法的要点解析。"
tags: [ "算法", "排序算法", "快速排序", "分治算法" ]
categories: [ "算法与数据结构" ]
---

# 快速排序

快速排序是一种基于比较的非稳定排序算法，采用分治思想，平均时间复杂度为 $O(n\log n)$，最坏情况下为 $O(n^2)$
，空间复杂度为 $O(1)$。下面以从小到大排序一个整数数列为例，介绍其实现细节与常见错误。

---

## 题目描述

给定一个长度为 $n$ 的整数数列，使用快速排序对其从小到大进行排序，并输出结果。

### 输入格式

- 第一行输入整数 $n$
- 第二行输入 $n$ 个整数，均在 $[1,10^9]$ 范围内

### 输出格式

- 一行输出排好序的数列

### 数据范围

$1 \leq n \leq 100000$

### 输入样例

```
5
3 1 2 4 5
```

### 输出样例

```
1 2 3 4 5
```

---

## 快速排序思路

快速排序每次分治时，任选一个数作为基准数 `pivot`（下面选中间位置的数）。

使用左右指针相向而行，左指针 `L` 从左往右寻找第一个大于等于 `pivot` 的数，右指针 `R` 从右往左寻找第一个小于等于 `pivot`
的数，然后交换这两个数。

不断重复这个过程，直到左指针和右指针重叠或者左指针比右指针大一位。这被称为一次循环。

在每次指针移动和交换完成后，都保证「左边部分 ≤ pivot, 右边部分 ≥ pivot」的结构不被破坏，即有不变量 `[left, L) <= pivot`，
`(R, right] >= pivot`。

以下示例代码中，`left` 和 `right` 是当前处理的闭区间边界，`pivot` 则取在区间中点处的元素。

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

## 复杂度与 `pivot` 的选择

由于在最坏情况下快速排序有 $O(n^2)$ 的复杂度，`pivot` 的选取很关键。如果总是选第一个或最后一个元素，在近乎有序的数组中将大概率出现最坏情况。

除了取中间位置的元素，还可以随机选取一个元素作为 `pivot`，或者取左、中、右三个元素的中位数作为 `pivot`。

---

## 常见错误示例

下面这段代码包含了多处常见错误。

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

**错误分析：**

1. `pivot` 应该是数组中的一个数，而不是下标。
2. 分别用 `<` 和 `>` 而不是 `<=` 和 `>=`，否则左指针可能不止超过右指针一位，这样就不能把数组分成两部分。
3. 发现 `l >= r` 后，应立即退出循环，不再执行交换。否则不能保证左侧元素不大于 `pivot`，右侧元素不小于 `pivot`。
4. 每次交换后，应执行 `l++` 和 `r--`。
5. `pivot` 实际上取的是中间偏左的数。如果使用 $l - 1$ 和 $l$ 分割数组，考虑数组 `[1, 2]`，不难发现会导致死循环，不断将数组分成大小为
   0 和 2 的两份。相反地，循环结束时，$r$ 必然小于 $right$，所以可以使用 $r$ 和 $r+1$
   分割数组。读者可以模拟下算法过程看看为什么。另一种简单的避免死循环的方式是随机选
   `pivot`或者特殊处理只有两个元素的情况。类似地，用 $r$ 和 $l$ 区分数组也不行。
6. 另外，用 $l$, $l+1$ 也不行，因为这个分割不合定义，当 $r$ 在 $l$ 左边的情况下，用 $l$, $l+1$ 不能正确地将数组分成左边小于等于
   `pivot`，右边大于等于 `pivot` 的两份。
7. 本题假定数组非空，所以不存在 `>` 的情况。但是建议使用 `>=`, 更安全。

---

## 补充

快速排序还可演变为“快速选择”，在 $O(n)$ 的期望时间内找到无序数组中第 $k$ 小的数，具体思想与快速排序类似，只是每次只在一侧子区间继续递归，从而降低时间复杂度。