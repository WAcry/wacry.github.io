---
title: "Tìm kiếm nhị phân"
date: 2024-12-24
draft: false
description: "Làm thế nào để thực hiện thuật toán tìm kiếm nhị phân một cách thanh lịch."
summary: "Làm thế nào để thực hiện thuật toán tìm kiếm nhị phân một cách thanh lịch."
tags: [ "Thuật toán", "Tìm kiếm nhị phân", "Mẫu thuật toán" ]
categories: [ "Thuật toán và cấu trúc dữ liệu" ]
---

Nếu không gian nghiệm có thứ tự được chia thành hai phần, trong đó một phần thỏa mãn điều kiện và phần còn lại không thỏa mãn điều kiện. Vậy thì có thể sử dụng tìm kiếm nhị phân để tìm điểm tới hạn trong không gian nghiệm có thứ tự.

Ý tưởng cơ bản của tìm kiếm nhị phân là liên tục chia đôi khoảng tìm kiếm. Mỗi lần kiểm tra phần tử ở giữa, nếu phần tử ở giữa không thỏa mãn điều kiện, thì có thể loại bỏ một nửa khoảng; ngược lại, thì tiếp tục tìm kiếm ở nửa khoảng còn lại. Vì mỗi lần đều loại bỏ một nửa khoảng tìm kiếm, nên độ phức tạp thời gian tìm kiếm có thể đạt được $O(\log n)$.

## Ví dụ

**Mô tả bài toán:**  
Cho một mảng số nguyên có độ dài $n$ được sắp xếp tăng dần, và $q$ truy vấn. Mỗi truy vấn đưa ra một số nguyên $k$, chúng ta cần tìm "vị trí bắt đầu" và "vị trí kết thúc" của $k$ trong mảng (chỉ số bắt đầu từ 0). Nếu số này không tồn tại trong mảng, hãy trả về `-1 -1`.

### Định dạng đầu vào

1. Dòng đầu tiên: Hai số nguyên $n$ và $q$, lần lượt biểu thị độ dài của mảng và số lần truy vấn.
2. Dòng thứ hai: $n$ số nguyên, biểu thị mảng đầy đủ, đã được sắp xếp theo thứ tự tăng dần.
3. $q$ dòng tiếp theo: Mỗi dòng chứa một số nguyên $k$, biểu thị một phần tử truy vấn.

## Phạm vi dữ liệu

$1 \leq n \leq 100000$

$1 \leq q \leq 10000$

$1 \leq k \leq 10000$

### Định dạng đầu ra

Đối với mỗi truy vấn, xuất ra vị trí bắt đầu và kết thúc của phần tử đó trong mảng trên một dòng. Nếu phần tử đó không tồn tại trong mảng, xuất ra `-1 -1`.

**Ví dụ:**

```
Đầu vào:
6 3
1 2 2 3 3 4
3
4
5

Đầu ra:
3 4
5 5
-1 -1
```

**Giải thích:**

- Phạm vi xuất hiện của phần tử $3$ là $[3, 4]$;
- Phần tử $4$ chỉ xuất hiện một lần, ở vị trí $5$;
- Phần tử $5$ không tồn tại trong mảng, do đó trả về $-1$ $-1$.

---

## Giải đáp

- **Tìm "vị trí bắt đầu":**
  Tức là tìm vị trí đầu tiên lớn hơn hoặc bằng $k$. Có thể chia mảng thành hai phần:
    - Tất cả các số ở bên trái đều "nhỏ hơn" $k$
    - Tất cả các số ở bên phải đều "lớn hơn hoặc bằng" $k$
    - Đáp án là vị trí đầu tiên ở bên phải

- **Tìm "vị trí kết thúc":**
  Tức là tìm vị trí cuối cùng nhỏ hơn hoặc bằng $k$. Có thể chia mảng thành hai phần:
    - Tất cả các số ở bên trái đều "nhỏ hơn hoặc bằng" $k$
    - Tất cả các số ở bên phải đều "lớn hơn" $k$
    - Đáp án là vị trí cuối cùng ở bên trái

---

## Mẫu đề xuất

Dưới đây là một mẫu nhị phân thanh lịch và không dễ mắc lỗi. Nó đảm bảo vòng lặp sẽ kết thúc khi hai con trỏ $l$ và $r$ liền kề nhau bằng cách cho $l$ và $r$ từ từ tiến lại gần nhau:

Định nghĩa hai con trỏ $l, r$, có bất biến: khoảng đóng $[0, l]$ thuộc về nửa bên trái, khoảng đóng $[r, n - 1]$ thuộc về nửa bên phải. $l$ và $r$ đều khởi tạo là $-1$ và $n$.

Khi thuật toán kết thúc, $l$ và $r$ liền kề nhau, lần lượt trỏ đến phần tử cuối cùng của nửa bên trái và phần tử đầu tiên của nửa bên phải.

Vì lời giải chúng ta muốn có thể không tồn tại, nên nếu bài toán không nói rõ là chắc chắn tồn tại lời giải, chúng ta cần phải kiểm tra xem `l` hoặc `r` có vượt quá giới hạn không, có trỏ đến giá trị đúng không.

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

        // 1. Tìm vị trí bắt đầu của k
        //    Chia mảng thành hai phần, bên trái đều < k, bên phải đều >= k.
        //    Đáp án là chỉ số nhỏ nhất của nửa bên phải.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // Nếu r vượt quá giới hạn hoặc nums[r] != k, tức là k không tồn tại
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. Tìm vị trí kết thúc của k
        //    Chia mảng thành hai phần, bên trái đều <= k, bên phải đều > k.
        //    Đáp án là chỉ số lớn nhất của nửa bên trái.
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

### Tại sao lại viết như vậy

1. Cách viết này có bất biến được định nghĩa chặt chẽ.
2. Nó đồng thời áp dụng cho cả hai trường hợp tìm "vị trí bắt đầu" và "vị trí kết thúc", không cần xử lý và thay đổi thêm.
3. Một số cách viết sử dụng `l == r` làm điều kiện dừng. Khi $l$ và $r$ cách nhau $1$, sẽ tính ra $mid$ bằng $l$ hoặc $r$. Nếu không xử lý đúng, cập nhật $l$ hoặc $r$ thành $mid$, khoảng tìm kiếm không thu hẹp, sẽ dẫn đến vòng lặp vô hạn. Ngược lại, cách viết ở đây dừng lại khi $l$ và $r$ liền kề nhau, đảm bảo $mid$ nhỏ hơn $l$ và lớn hơn $r$, khi cập nhật $l$ hoặc $r$, khoảng tìm kiếm chắc chắn sẽ thu hẹp.

---

## STL

Nếu sử dụng các hàm `lower_bound` và `upper_bound` do C++ STL cung cấp, cũng có thể hoàn thành cùng một việc:

- `lower_bound(first, last, val)` sẽ trả về "vị trí đầu tiên lớn hơn hoặc bằng val"
- `upper_bound(first, last, val)` sẽ trả về "vị trí đầu tiên lớn hơn val"

Ví dụ, giả sử `nums = {1,2,3,4,4,4,4,4,5,5,6}`, chúng ta muốn biết khoảng mà 4 xuất hiện:

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

- `it1` trỏ đến vị trí của giá trị đầu tiên lớn hơn hoặc bằng $4$.
- `it2` trỏ đến vị trí của giá trị đầu tiên lớn hơn $4$.
  Vì vậy `it2 - it1` là số lần $4$ xuất hiện trong mảng; `it2 - nums.begin() - 1` là biên phải của $4$.

---

## Bổ sung

Tìm kiếm nhị phân còn có thể mở rộng đến việc tìm kiếm trong phạm vi số thực (ví dụ như tìm nghiệm của phương trình), cũng như tìm kiếm tam phân để tìm giá trị lớn nhất của hàm đơn đỉnh.
Chỉ cần bạn hiểu được nguyên tắc cốt lõi " **Trong khoảng có thứ tự, mỗi lần đều có thể loại bỏ một nửa**", bạn sẽ thấy tìm kiếm nhị phân có thể giúp bạn giải quyết vấn đề một cách hiệu quả trong nhiều trường hợp.

---

## Luyện tập

LeetCode 33. Search in Rotated Sorted Array

Gợi ý: Bước đầu tiên sử dụng tìm kiếm nhị phân để tìm điểm xoay, bước thứ hai lại sử dụng tìm kiếm nhị phân để tìm giá trị mục tiêu.