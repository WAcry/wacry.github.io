---
title: "Tìm kiếm nhị phân"
date: 2024-12-24
draft: false
description: "Cách triển khai một cách thanh lịch thuật toán tìm kiếm nhị phân số nguyên"
summary: "Cách triển khai một cách thanh lịch thuật toán tìm kiếm nhị phân số nguyên"
tags: [ "Thuật toán", "Tìm kiếm nhị phân", "Mẫu thuật toán" ]
categories: [ "Thuật toán và Cấu trúc dữ liệu" ]
---
{{< katex >}}

# Tìm kiếm nhị phân

Tìm kiếm nhị phân có thể được sử dụng để nhanh chóng tìm một phần tử cụ thể trong một chuỗi đã được sắp xếp. So với tìm kiếm tuyến tính với độ phức tạp thời gian là $O(n)$, tìm kiếm nhị phân chỉ yêu cầu thời gian $O(\log n)$, khiến nó rất hiệu quả khi xử lý các tập dữ liệu lớn.

## Ý tưởng cốt lõi của tìm kiếm nhị phân

Ý tưởng cơ bản của tìm kiếm nhị phân là liên tục chia đôi khoảng tìm kiếm. Mỗi lần, phần tử ở giữa được so sánh với giá trị mục tiêu. Nếu phần tử ở giữa không thỏa mãn điều kiện, một nửa khoảng có thể bị loại bỏ; nếu không, việc tìm kiếm tiếp tục trong nửa khoảng còn lại. Vì một nửa khoảng tìm kiếm bị loại bỏ mỗi lần, độ phức tạp thời gian tìm kiếm có thể đạt $O(\log n)$.

Tìm kiếm nhị phân rất hữu ích cho các bài toán mà "**các nghiệm khả thi có thể được chia thành một khoảng được sắp xếp (thỏa mãn điều kiện) và một khoảng được sắp xếp khác (không thỏa mãn điều kiện)**". Ví dụ:

- Tìm xem một phần tử có tồn tại trong một mảng đã sắp xếp hay không
- Tìm "vị trí đầu tiên" hoặc "vị trí cuối cùng" mà một số xuất hiện

## Ví dụ: Tìm vị trí bắt đầu và kết thúc của một phần tử

**Mô tả bài toán:**
Cho một mảng số nguyên đã được sắp xếp tăng dần có độ dài $n$, và $q$ truy vấn. Mỗi truy vấn cho một số nguyên $k$, và chúng ta cần tìm "vị trí bắt đầu" và "vị trí kết thúc" của $k$ trong mảng (chỉ số bắt đầu từ 0). Nếu số đó không tồn tại trong mảng, trả về $-1$ $-1$.

**Định dạng đầu vào:**

1. Dòng đầu tiên: hai số nguyên $n$ và $q$, lần lượt đại diện cho độ dài của mảng và số lượng truy vấn.
2. Dòng thứ hai: $n$ số nguyên (trong phạm vi 1 ~ 10000), đại diện cho toàn bộ mảng, đã được sắp xếp theo thứ tự tăng dần.
3. $q$ dòng tiếp theo: mỗi dòng chứa một số nguyên $k$, đại diện cho một phần tử truy vấn.

**Định dạng đầu ra:**
Đối với mỗi truy vấn, xuất vị trí bắt đầu và kết thúc của phần tử trong mảng trên một dòng duy nhất. Nếu phần tử không tồn tại trong mảng, xuất $-1$ $-1$.

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

Giải thích:

- Phạm vi mà phần tử 3 xuất hiện là `[3, 4]`;
- Phần tử 4 chỉ xuất hiện một lần, tại vị trí 5;
- Phần tử 5 không tồn tại trong mảng, vì vậy trả về `-1 -1`.

## Cách tiếp cận ứng dụng của tìm kiếm nhị phân

Trong bài toán này, chúng ta có thể dựa vào tìm kiếm nhị phân để tìm "biên trái" và "biên phải" của một giá trị nhất định. Điều quan trọng là phải hiểu cách xác định khoảng tìm kiếm và cách di chuyển các con trỏ dựa trên kết quả so sánh.

- **Tìm "biên trái":**
  Tức là tìm vị trí đầu tiên lớn hơn hoặc bằng $k$. Mảng có thể được chia thành hai phần:
    - Tất cả các số ở bên trái đều "nhỏ hơn" $k$
    - Tất cả các số ở bên phải đều "lớn hơn hoặc bằng" $k$

- **Tìm "biên phải":**
  Tức là tìm vị trí cuối cùng nhỏ hơn hoặc bằng $k$. Mảng có thể được chia thành hai phần:
    - Tất cả các số ở bên trái đều "nhỏ hơn hoặc bằng" $k$
    - Tất cả các số ở bên phải đều "lớn hơn" $k$

Chỉ cần duy trì đúng hai khoảng này, kết quả có thể thu được nhanh chóng thông qua tìm kiếm nhị phân.

## Mẫu khuyến nghị: Mã tìm kiếm nhị phân để tránh vòng lặp vô hạn

Đây là một mẫu tìm kiếm nhị phân thanh lịch và chống lỗi. Nó đảm bảo vòng lặp kết thúc khi $l$ và $r$ liền kề nhau bằng cách dần dần đưa $l$ và $r$ đến gần nhau hơn:

Xác định hai con trỏ $l, r$, với các bất biến: khoảng đóng $[0, l]$ đều thuộc phần bên trái, khoảng đóng $[r, n - 1]$ đều thuộc phần bên phải. $l$ và $r$ được khởi tạo lần lượt là $-1$ và $n$.

Khi thuật toán kết thúc, $l$ và $r$ liền kề nhau, trỏ đến giá trị lớn nhất trong phần bên trái và giá trị nhỏ nhất trong phần bên phải.

Vì nghiệm mong muốn có thể không tồn tại, khi trả về $l$ hoặc $r$, cần phải kiểm tra xem giá trị tương ứng có phải là giá trị chúng ta muốn hay không và có nằm ngoài giới hạn hay không.
Ví dụ: $l$ đại diện cho giá trị lớn nhất $\leq k$, và chúng ta cần kiểm tra `l != -1 && nums[l] == k`

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

        // 1. Tìm vị trí bắt đầu của k (biên trái)
        //    Chia mảng thành hai phần, phần bên trái tất cả < k, và phần bên phải tất cả >= k.
        //    Biên trái là chỉ số nhỏ nhất của phần bên phải.
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

        int leftPos = r; // Ghi lại biên trái của k

        // 2. Tìm vị trí kết thúc của k (biên phải)
        //    Chia mảng thành hai phần, phần bên trái tất cả <= k, và phần bên phải tất cả > k.
        //    Biên phải là chỉ số lớn nhất của phần bên trái.
        l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] <= k) l = mid;
            else r = mid;
        }

        // Vì chúng ta đã xác minh rằng k tồn tại, không cần phải xác minh lại ở đây
        int rightPos = l; // Biên phải
        cout << leftPos << " " << rightPos << endl;
    }
    return 0;
}
```

### Tại sao phương pháp này ít gây lỗi hơn?

1. Phương pháp này có các bất biến được xác định nghiêm ngặt.
2. Nó có thể tìm thấy cả biên trái và biên phải, giúp nó áp dụng được cho tất cả các tình huống.
3. Một số phương pháp sử dụng $l == r$ làm điều kiện kết thúc. Khi $l$ và $r$ khác nhau 1, $mid$ được tính toán sẽ bằng `l` hoặc `r`. Nếu không được xử lý đúng cách, việc cập nhật
   `l` hoặc `r` thành `mid` sẽ không thu hẹp khoảng tìm kiếm, dẫn đến vòng lặp vô hạn. Ngược lại, phương pháp này kết thúc khi $l$ và $r$ liền kề nhau, tránh được vấn đề này.

## Giải pháp STL: `lower_bound` và `upper_bound`

Nếu bạn sử dụng các hàm `lower_bound` và `upper_bound` do C++ STL cung cấp, bạn có thể dễ dàng hoàn thành điều tương tự:

- `lower_bound(first, last, val)` trả về "vị trí đầu tiên lớn hơn hoặc bằng val"
- `upper_bound(first, last, val)` trả về "vị trí đầu tiên lớn hơn val"

Ví dụ: giả sử `nums = {1,2,3,4,4,4,4,4,5,5,6}`, và chúng ta muốn biết khoảng mà 4 xuất hiện:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    // Cho biết rằng 4 không tồn tại trong mảng
    cout << "4 xuất hiện 0 lần" << endl;
} else {
    cout << "Số 4 đầu tiên ở " << it1 - nums.begin() << endl;
    cout << "Số 4 cuối cùng ở " << it2 - nums.begin() - 1 << endl;
    cout << "4 xuất hiện " << it2 - it1 << " lần" << endl;
}
```

- `it1` trỏ đến vị trí đầu tiên mà giá trị lớn hơn hoặc bằng 4.
- `it2` trỏ đến vị trí đầu tiên mà giá trị lớn hơn 4.
  Do đó, `it2 - it1` là số lần 4 xuất hiện trong mảng; `it2 - nums.begin() - 1` là biên phải của 4.

Hai hàm này đặc biệt thuận tiện khi tìm kiếm khoảng hoặc đếm số lần xuất hiện.

## Bổ sung

Tìm kiếm nhị phân cũng có thể được mở rộng để tìm kiếm trong các số dấu phẩy động (ví dụ: tìm nghiệm của một phương trình), cũng như tìm kiếm tam phân để tìm giá trị cực trị của các hàm đơn mode. Chỉ cần bạn hiểu nguyên tắc cốt lõi của việc "**mỗi lần loại bỏ một nửa trong một khoảng được sắp xếp**", bạn sẽ thấy rằng tìm kiếm nhị phân có thể giúp bạn giải quyết vấn đề một cách hiệu quả trong nhiều tình huống.

## Bài tập về nhà

LeetCode 33. Tìm kiếm trong mảng đã sắp xếp bị xoay vòng

Gợi ý: Sử dụng tìm kiếm nhị phân để tìm điểm xoay trước, sau đó sử dụng tìm kiếm nhị phân để tìm giá trị mục tiêu.