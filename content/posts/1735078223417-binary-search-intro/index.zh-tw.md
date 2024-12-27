markdown
---
title: "二分搜尋"
date: 2024-12-24
draft: false
description: "如何優雅地實現二分搜尋演算法。"
summary: "如何優雅地實現二分搜尋演算法。"
tags: [ "演算法", "二分搜尋", "演算法模板" ]
categories: [ "演算法與資料結構" ]
---

如果有序解空間被分成左右兩部分，其中一個部分滿足條件，另一個部分不滿足條件。那麼能夠使用二分搜尋來在有序解空間中查找臨界點。

二分搜尋的基本思路是不斷地將搜尋區間對半分。每次檢查中點元素，如果中點元素不滿足條件，就可以排除一半區間；
反之，則在另一半區間繼續搜尋。由於每次都拋棄一半的搜尋區間，搜尋時間複雜度可達到 $O(\log n)$。

## 例題

**題目描述：**  
給定一個升序排列的長度為 $n$ 的整數數組，還有 $q$ 個查詢。每個查詢給出一個整數 $k$，我們需要找出在數組中 $
k$ 的「起始位置」和「終止位置」（下標從 0 開始）。如果數組中不存在這個數，則返回 `-1 -1`。

### 輸入格式

1. 第一行：兩個整數 $n$ 和 $q$，分別表示數組長度和查詢次數。
2. 第二行：$n$ 個整數，表示完整數組，已按升序排列。
3. 接下來 $q$ 行：每行包含一個整數 $k$，表示一個查詢元素。

## 數據範圍

$1 \leq n \leq 100000$

$1 \leq q \leq 10000$

$1 \leq k \leq 10000$

### 輸出格式

對每個查詢，在一行裡輸出該元素在數組中的起始和結束位置。如果數組中不存在該元素，則輸出 `-1 -1`。

**樣例：**

```
輸入：
6 3
1 2 2 3 3 4
3
4
5

輸出：
3 4
5 5
-1 -1
```

**解釋：**

- 元素 $3$ 出現的範圍為 $[3, 4]$；
- 元素 $4$ 只出現了一次，在位置 $5$；
- 元素 $5$ 在數組裡不存在，因此返回 $-1$ $-1$。

---

## 解答

- **找「起始位置」：**
  即找第一個大於等於 $k$ 的位置。可以把數組分成兩部分：
    - 左邊所有數都「小於」 $k$
    - 右邊所有數都「大於等於」 $k$
    - 答案為右邊的第一個位置

- **找「終止位置」：**
  即找最後一個小於等於 $k$ 的位置。可以把數組分成兩部分：
    - 左邊所有數都「小於等於」 $k$
    - 右邊所有數都「大於」 $k$
    - 答案為左邊的最後一個位置

---

## 推薦模板

下面是一種優雅且不易犯錯的二分模板。

定義兩個指針 $l, r$，有不變量：閉區間 $[0, l]$ 都屬於左半部分，閉區間 $[r, n - 1]$ 都屬於右半部分。$l$
和 $r$ 都初始化為 $-1$ 和 $n$。

演算法終止時，$l$ 和 $r$ 相鄰，分別指向左半部分的最後一個元素和右半部分的第一個元素。

因為我們想要的解可能不存在，所以如果題目沒有說明一定存在解，我們需要判斷一下 `l` 或 `r` 是否越界，是否指向正確的值。

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

        // 1. 找 k 的起始位置
        //    將數組分成兩部分，左邊都 < k，右邊都 >= k。
        //    答案為右半部分的最小下標。
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // 如果 r 越界或者 nums[r] != k，說明不存在 k
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. 找 k 的終止位置
        //    將數組分成兩部分，左邊都 <= k，右邊都 > k。
        //    答案為左半部分的最大下標。
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

### 優勢

1. 這個寫法有嚴格定義的不變量。
2. 它同時適用於找「起始位置」和「終止位置」兩種情況，不需要額外的處理和變化。
3. 有一些寫法使用 `l == r` 作為終止條件。當 $l$ 和 $r$ 相差 $1$ 時，會計算出 $mid$ 和 $l$ 或 $r$
   相等。如果沒有正確處理，更新 $l$ 或 $r$ 為 $mid$，搜尋區間沒有縮小，會導致死循環。相反地，這裡的寫法在 $l$
   和 $r$ 相鄰時終止，保證 $mid$ 小於 $l$ 且大於 $r$，更新 $l$ 或 $r$ 時搜尋區間一定會縮小。

---

## STL

如果使用 C++ STL 提供的 `lower_bound` 和 `upper_bound` 函數，也能完成同樣的事情：

- `lower_bound(first, last, val)` 會返回「第一個大於等於 val 的位置」
- `upper_bound(first, last, val)` 會返回「第一個大於 val 的位置」

舉個例子，假設 `nums = {1,2,3,4,4,4,4,4,5,5,6}`，我們想知道 4 出現的區間：

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

- `it1` 指向第一個值大於等於 $4$ 的位置。
- `it2` 指向第一個值大於 $4$ 的位置。  
  所以 `it2 - it1` 就是 $4$ 在數組中出現的次數；`it2 - nums.begin() - 1` 就是 $4$ 的右邊界的位置。

---

## 補充

二分搜尋還可以擴展到浮點數範圍的搜尋（如求方程根）、以及三分搜尋求單峰函數的最值。

---

## 練習

LeetCode 33. Search in Rotated Sorted Array

提示：第一步使用二分搜尋找到旋轉點，第二步再使用二分搜尋找到目標值。