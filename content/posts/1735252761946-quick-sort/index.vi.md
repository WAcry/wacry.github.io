---
title: "Sắp xếp nhanh"
date: 2024-12-26
draft: false
description: "Phân tích các điểm chính để triển khai đúng thuật toán sắp xếp nhanh."
summary: "Phân tích các điểm chính để triển khai đúng thuật toán sắp xếp nhanh."
tags: [ "Thuật toán", "Thuật toán sắp xếp", "Sắp xếp nhanh", "Thuật toán chia để trị" ]
categories: [ "Thuật toán và Cấu trúc dữ liệu" ]
---

# Sắp xếp nhanh

Sắp xếp nhanh là một thuật toán sắp xếp không ổn định dựa trên so sánh, sử dụng tư tưởng chia để trị, độ phức tạp thời gian trung bình là $O(n\log n)$, trường hợp xấu nhất là $O(n^2)$, độ phức tạp không gian là $O(1)$. Dưới đây, chúng ta sẽ lấy ví dụ sắp xếp một dãy số nguyên theo thứ tự tăng dần để giới thiệu chi tiết cách triển khai và các lỗi thường gặp.

---

## Mô tả bài toán

Cho một dãy số nguyên có độ dài $n$, sử dụng thuật toán sắp xếp nhanh để sắp xếp chúng theo thứ tự tăng dần và in ra kết quả.

### Định dạng đầu vào

- Dòng đầu tiên nhập số nguyên $n$
- Dòng thứ hai nhập $n$ số nguyên, đều nằm trong phạm vi $[1,10^9]$

### Định dạng đầu ra

- Một dòng duy nhất in ra dãy số đã được sắp xếp

### Phạm vi dữ liệu

$1 \leq n \leq 100000$

### Ví dụ đầu vào

```
5
3 1 2 4 5
```

### Ví dụ đầu ra

```
1 2 3 4 5
```

---

## Ý tưởng sắp xếp nhanh

Mỗi lần phân chia của sắp xếp nhanh, chọn ngẫu nhiên một số làm số cơ sở `pivot` (dưới đây chọn số ở vị trí giữa).

Sử dụng hai con trỏ trái `L` và phải `R` di chuyển ngược chiều nhau, con trỏ trái `L` tìm từ trái sang phải số đầu tiên lớn hơn hoặc bằng `pivot`, con trỏ phải `R` tìm từ phải sang trái số đầu tiên nhỏ hơn hoặc bằng `pivot`, sau đó hoán đổi hai số này.

Lặp lại quá trình này liên tục cho đến khi con trỏ trái và con trỏ phải chồng lên nhau hoặc con trỏ trái lớn hơn con trỏ phải một vị trí. Đây được gọi là một vòng lặp.

Sau mỗi lần di chuyển và hoán đổi con trỏ, đảm bảo cấu trúc "phần bên trái ≤ pivot, phần bên phải ≥ pivot" không bị phá vỡ, tức là có bất biến `[left, L) <= pivot`, `(R, right] >= pivot`.

Trong ví dụ mã dưới đây, `left` và `right` là biên của khoảng đóng đang được xử lý, `pivot` lấy phần tử ở vị trí giữa của khoảng.

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

## Độ phức tạp và lựa chọn `pivot`

Vì sắp xếp nhanh có độ phức tạp $O(n^2)$ trong trường hợp xấu nhất, việc chọn `pivot` rất quan trọng. Nếu luôn chọn phần tử đầu tiên hoặc cuối cùng, trong mảng gần như đã được sắp xếp sẽ có khả năng cao xảy ra trường hợp xấu nhất.

Ngoài việc lấy phần tử ở vị trí giữa, có thể chọn ngẫu nhiên một phần tử làm `pivot`, hoặc lấy trung vị của ba phần tử trái, giữa và phải làm `pivot`.

---

## Ví dụ lỗi thường gặp

Đoạn mã dưới đây chứa nhiều lỗi thường gặp.

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

**Phân tích lỗi:**

1. `pivot` phải là một số trong mảng, chứ không phải là chỉ số.
2. Sử dụng `<` và `>` thay vì `<=` và `>=`, nếu không con trỏ trái có thể vượt quá con trỏ phải nhiều hơn một vị trí, như vậy không thể chia mảng thành hai phần.
3. Sau khi phát hiện `l >= r`, nên thoát vòng lặp ngay lập tức, không thực hiện hoán đổi nữa. Nếu không, không thể đảm bảo rằng các phần tử bên trái không lớn hơn `pivot`, các phần tử bên phải không nhỏ hơn `pivot`.
4. Sau mỗi lần hoán đổi, nên thực hiện `l++` và `r--`.
5. `pivot` thực tế lấy số ở giữa lệch về bên trái. Nếu sử dụng $l - 1$ và $l$ để phân chia mảng, xem xét mảng `[1, 2]`, không khó để thấy sẽ dẫn đến vòng lặp vô hạn, liên tục chia mảng thành hai phần có kích thước là 0 và 2. Ngược lại, khi vòng lặp kết thúc, $r$ chắc chắn nhỏ hơn $right$, vì vậy có thể sử dụng $r$ và $r+1$ để phân chia mảng. Bạn đọc có thể mô phỏng quá trình thuật toán để xem tại sao. Một cách đơn giản khác để tránh vòng lặp vô hạn là chọn ngẫu nhiên `pivot` hoặc xử lý đặc biệt trường hợp chỉ có hai phần tử. Tương tự, sử dụng $r$ và $l$ để phân biệt mảng cũng không được.
6. Ngoài ra, dùng $l$, $l+1$ cũng không được, vì cách phân chia này không phù hợp với định nghĩa, khi $r$ ở bên trái $l$, dùng $l$, $l+1$ không thể chia mảng đúng thành hai phần, bên trái nhỏ hơn hoặc bằng `pivot`, bên phải lớn hơn hoặc bằng `pivot`.
7. Bài toán này giả định mảng không rỗng, vì vậy không có trường hợp `>`. Tuy nhiên, nên sử dụng `>=`, an toàn hơn.

---

## Bổ sung

Sắp xếp nhanh còn có thể được biến đổi thành "lựa chọn nhanh", trong thời gian kỳ vọng $O(n)$ để tìm số nhỏ thứ $k$ trong mảng chưa sắp xếp, ý tưởng cụ thể tương tự như sắp xếp nhanh, chỉ là mỗi lần chỉ tiếp tục đệ quy trong một khoảng con, từ đó giảm độ phức tạp thời gian.