---
title: "快速排序"
date: 2024-12-26
draft: false
description: "正確實現快速排序演算法的要點解析。"
summary: "正確實現快速排序演算法的要點解析。"
tags: [ "演算法", "排序演算法", "快速排序", "分治演算法" ]
categories: [ "演算法與資料結構" ]
---

# 快速排序

快速排序是一種基於比較的非穩定排序演算法，採用分治思想，平均時間複雜度為 $O(n\log n)$，最壞情況下為 $O(n^2)$
，空間複雜度為 $O(1)$。下面以從小到大排序一個整數數列為例，介紹其實現細節與常見錯誤。

---

## 題目描述

給定一個長度為 $n$ 的整數數列，使用快速排序對其從小到大進行排序，並輸出結果。

### 輸入格式

- 第一行輸入整數 $n$
- 第二行輸入 $n$ 個整數，均在 $[1,10^9]$ 範圍內

### 輸出格式

- 一行輸出排好序的數列

### 數據範圍

$1 \leq n \leq 100000$

### 輸入範例

```
5
3 1 2 4 5
```

### 輸出範例

```
1 2 3 4 5
```

---

## 快速排序思路

快速排序每次分治時，任選一個數作為基準數 `pivot`（下面選中間位置的數）。

使用左右指針相向而行，左指針 `L` 從左往右尋找第一個大於等於 `pivot` 的數，右指針 `R` 從右往左尋找第一個小於等於 `pivot`
的數，然後交換這兩個數。

不斷重複這個過程，直到左指針和右指針重疊或者左指針比右指針大一位。這被稱為一次循環。

在每次指針移動和交換完成後，都保證「左邊部分 ≤ pivot, 右邊部分 ≥ pivot」的結構不被破壞，即有不變量 `[left, L) <= pivot`，
`(R, right] >= pivot`。

以下示例程式碼中，`left` 和 `right` 是當前處理的閉區間邊界，`pivot` 則取在區間中點處的元素。

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

## 複雜度與 `pivot` 的選擇

由於在最壞情況下快速排序有 $O(n^2)$ 的複雜度，`pivot` 的選取很關鍵。如果總是選第一個或最後一個元素，在近乎有序的陣列中將大概率出現最壞情況。

除了取中間位置的元素，還可以隨機選取一個元素作為 `pivot`，或者取左、中、右三個元素的中位數作為 `pivot`。

---

## 常見錯誤示例

下面這段程式碼包含了多處常見錯誤。

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

**錯誤分析：**

1. `pivot` 應該是陣列中的一個數，而不是下標。
2. 分別用 `<` 和 `>` 而不是 `<=` 和 `>=`，否則左指針可能不止超過右指針一位，這樣就不能把陣列分成兩部分。
3. 發現 `l >= r` 後，應立即退出循環，不再執行交換。否則不能保證左側元素不大於 `pivot`，右側元素不小於 `pivot`。
4. 每次交換後，應執行 `l++` 和 `r--`。
5. `pivot` 實際上取的是中間偏左的數。因此如果使用 $l - 1$ 和 $l$ 分割陣列，考慮陣列 `[1, 2]`，不難發現會導致死循環，不斷將陣列分成大小為
   0 和 2 的兩份。類似地，用 $r$ 和 $l$ 區分陣列也不行。相反地，一輪循環結束時，$r$ 必然小於 $right$，所以可以使用 $r$ 和 $r+1$
   分割陣列。讀者可以模擬下演算法過程看看為什麼。另一種簡單的避免死循環的方式是隨機選 `pivot`或者特殊處理只有兩個元素的情況。
6. 另外，用 $l$, $l+1$ 也不行，因為這個分割不合定義，當 $r$ 在 $l$ 左邊的情況下，用 $l$, $l+1$ 不能正確地將陣列分成左邊小於等於
   `pivot`，右邊大於等於 `pivot` 的兩份。
7. 本題假定陣列非空，所以不存在 `>` 的情況。但是建議使用 `>=`, 更安全。

---

## 補充

快速排序還可演變為“快速選擇”，在 $O(n)$ 的期望時間內找到無序陣列中第 $k$ 小的數，具體思想與快速排序類似，只是每次只在一側子區間繼續遞迴，從而降低時間複雜度。