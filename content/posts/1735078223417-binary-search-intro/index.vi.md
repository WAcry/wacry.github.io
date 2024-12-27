---
title: "Tìm kiếm nhị phân"
date: 2024-12-24
draft: false
description: "Cách triển khai thuật toán tìm kiếm nhị phân một cách thanh lịch."
summary: "Cách triển khai thuật toán tìm kiếm nhị phân một cách thanh lịch."
tags: [ "Thuật toán", "Tìm kiếm nhị phân", "Mẫu thuật toán" ]
categories: [ "Thuật toán và Cấu trúc dữ liệu" ]
---

Nếu một không gian nghiệm có thứ tự được chia thành hai phần, trong đó một phần thỏa mãn một điều kiện và phần còn lại thì không, thì có thể sử dụng tìm kiếm nhị phân để tìm điểm tới hạn trong không gian nghiệm có thứ tự đó.

Ý tưởng cơ bản của tìm kiếm nhị phân là liên tục chia đôi khoảng tìm kiếm. Mỗi lần, phần tử ở giữa được kiểm tra. Nếu phần tử ở giữa không thỏa mãn điều kiện, một nửa khoảng có thể bị loại bỏ; nếu không, việc tìm kiếm tiếp tục ở nửa còn lại. Vì một nửa khoảng tìm kiếm bị loại bỏ mỗi lần, độ phức tạp thời gian tìm kiếm có thể đạt $O(\log n)$.

## Bài toán ví dụ

**Mô tả bài toán:**
Cho một mảng số nguyên được sắp xếp tăng dần có độ dài $n$, và $q$ truy vấn. Mỗi truy vấn cho một số nguyên $k$, và chúng ta cần tìm "vị trí bắt đầu" và "vị trí kết thúc" của $k$ trong mảng (chỉ số bắt đầu từ 0). Nếu số đó không tồn tại trong mảng, trả về `-1 -1`.

### Định dạng đầu vào

1. Dòng đầu tiên: hai số nguyên $n$ và $q$, lần lượt biểu thị độ dài của mảng và số lượng truy vấn.
2. Dòng thứ hai: $n$ số nguyên, biểu thị mảng hoàn chỉnh, đã được sắp xếp theo thứ tự tăng dần.
3. $q$ dòng tiếp theo: mỗi dòng chứa một số nguyên $k$, biểu thị một phần tử truy vấn.

## Phạm vi dữ liệu

$1 \leq n \leq 100000$

$1 \leq q \leq 10000$

$1 \leq k \leq 10000$

### Định dạng đầu ra

Đối với mỗi truy vấn, xuất ra vị trí bắt đầu và kết thúc của phần tử trong mảng trên một dòng duy nhất. Nếu phần tử không tồn tại trong mảng, xuất ra `-1 -1`.

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

- Phạm vi mà phần tử $3$ xuất hiện là $[3, 4]$;
- Phần tử $4$ chỉ xuất hiện một lần, tại vị trí $5$;
- Phần tử $5$ không tồn tại trong mảng, vì vậy trả về $-1$ $-1$.

---

## Giải pháp

- **Tìm "Vị trí bắt đầu":**
  Tức là, tìm vị trí đầu tiên lớn hơn hoặc bằng $k$. Mảng có thể được chia thành hai phần:
    - Tất cả các số bên trái đều "nhỏ hơn" $k$
    - Tất cả các số bên phải đều "lớn hơn hoặc bằng" $k$
    - Câu trả lời là vị trí đầu tiên ở bên phải

- **Tìm "Vị trí kết thúc":**
  Tức là, tìm vị trí cuối cùng nhỏ hơn hoặc bằng $k$. Mảng có thể được chia thành hai phần:
    - Tất cả các số bên trái đều "nhỏ hơn hoặc bằng" $k$
    - Tất cả các số bên phải đều "lớn hơn" $k$
    - Câu trả lời là vị trí cuối cùng ở bên trái

---

## Mẫu khuyến nghị

Dưới đây là một mẫu tìm kiếm nhị phân thanh lịch và ít lỗi hơn.

Xác định hai con trỏ $l, r$, với bất biến: khoảng đóng $[0, l]$ thuộc phần bên trái và khoảng đóng $[r, n - 1]$ thuộc phần bên phải. $l$ và $r$ được khởi tạo lần lượt là $-1$ và $n$.

Khi thuật toán kết thúc, $l$ và $r$ liền kề nhau, trỏ đến phần tử cuối cùng của phần bên trái và phần tử đầu tiên của phần bên phải.

Vì giải pháp chúng ta muốn có thể không tồn tại, nếu bài toán không nói rằng một giải pháp chắc chắn tồn tại, chúng ta cần kiểm tra xem `l` hoặc `r` có nằm ngoài giới hạn hay không và liệu nó có trỏ đến giá trị chính xác hay không.

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
        //    Chia mảng thành hai phần, phần bên trái là tất cả < k, và phần bên phải là tất cả >= k.
        //    Câu trả lời là chỉ số nhỏ nhất của phần bên phải.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // Nếu r nằm ngoài giới hạn hoặc nums[r] != k, có nghĩa là k không tồn tại
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. Tìm vị trí kết thúc của k
        //    Chia mảng thành hai phần, phần bên trái là tất cả <= k, và phần bên phải là tất cả > k.
        //    Câu trả lời là chỉ số lớn nhất của phần bên trái.
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

### Ưu điểm

1. Cách tiếp cận này có các bất biến được xác định chặt chẽ.
2. Nó áp dụng cho cả việc tìm "vị trí bắt đầu" và "vị trí kết thúc" mà không cần xử lý hoặc thay đổi thêm.
3. Một số cách tiếp cận sử dụng `l == r` làm điều kiện kết thúc. Khi $l$ và $r$ khác nhau $1$, $mid$ sẽ được tính bằng $l$ hoặc $r$. Nếu không được xử lý đúng cách, việc cập nhật $l$ hoặc $r$ thành $mid$ sẽ không thu hẹp khoảng tìm kiếm, dẫn đến vòng lặp vô hạn. Ngược lại, cách tiếp cận này kết thúc khi $l$ và $r$ liền kề nhau, đảm bảo rằng $mid$ nhỏ hơn $l$ và lớn hơn $r$, và việc cập nhật $l$ hoặc $r$ sẽ luôn thu hẹp khoảng tìm kiếm.

---

## STL

Nếu bạn sử dụng các hàm `lower_bound` và `upper_bound` do C++ STL cung cấp, bạn có thể đạt được điều tương tự:

- `lower_bound(first, last, val)` sẽ trả về "vị trí đầu tiên lớn hơn hoặc bằng val"
- `upper_bound(first, last, val)` sẽ trả về "vị trí đầu tiên lớn hơn val"

Ví dụ, giả sử `nums = {1,2,3,4,4,4,4,4,5,5,6}`, và chúng ta muốn biết phạm vi mà 4 xuất hiện:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    cout << "4 xuất hiện 0 lần" << endl;
} else {
    cout << "số 4 đầu tiên ở vị trí " << it1 - nums.begin() << endl;
    cout << "số 4 cuối cùng ở vị trí " << it2 - nums.begin() - 1 << endl;
    cout << "4 xuất hiện " << it2 - it1 << " lần" << endl;
}
```

- `it1` trỏ đến vị trí đầu tiên mà giá trị lớn hơn hoặc bằng $4$.
- `it2` trỏ đến vị trí đầu tiên mà giá trị lớn hơn $4$.
  Do đó, `it2 - it1` là số lần $4$ xuất hiện trong mảng; `it2 - nums.begin() - 1` là vị trí của ranh giới bên phải của $4$.

---

## Ghi chú bổ sung

Tìm kiếm nhị phân cũng có thể được mở rộng để tìm kiếm trong các phạm vi số thực (chẳng hạn như tìm nghiệm của một phương trình) và tìm kiếm tam phân để tìm cực trị của các hàm đơn mode.

---

## Luyện tập

LeetCode 33. Search in Rotated Sorted Array

Gợi ý: Đầu tiên, sử dụng tìm kiếm nhị phân để tìm điểm xoay, sau đó sử dụng tìm kiếm nhị phân để tìm giá trị mục tiêu.