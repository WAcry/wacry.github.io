---
title: "Bài toán Cái túi 01"
date: 2024-12-24
draft: false
description: "Bài toán cái túi cổ điển cơ bản nhất."
summary: "Bài toán cái túi cổ điển cơ bản nhất."
tags: [ "Thuật toán", "Quy hoạch động", "Bài toán cái túi" ]
categories: [ "Thuật toán và Cấu trúc dữ liệu" ]
---

## Bài toán

Có $N$ đồ vật. Thể tích của đồ vật thứ $i$ là $s_i$, và giá trị của nó là $v_i$.
Mỗi đồ vật chỉ có thể được lấy một lần. Với điều kiện không vượt quá giới hạn tổng thể tích tối đa $S$, hãy tìm tổng giá trị tối đa $V$ có thể đạt được.

## Định dạng đầu vào

Dòng đầu tiên chứa hai số nguyên, $N$ và $S$, được phân tách bằng một khoảng trắng, lần lượt biểu thị số lượng đồ vật và giới hạn tổng thể tích tối đa.
$N$ dòng tiếp theo, mỗi dòng chứa hai số nguyên, $s_i$ và $v_i$, được phân tách bằng một khoảng trắng, lần lượt biểu thị thể tích và giá trị của đồ vật thứ $i$.

## Định dạng đầu ra

Xuất ra một số nguyên biểu thị giá trị tối đa.

## Phạm vi dữ liệu

$$0 \le N, S \leq 1000$$

$$0 \le s_i, v_i \leq 1000$$

## Ví dụ đầu vào

```
4 5
1 2
2 4
3 4
4 5
```

## Ví dụ đầu ra

```
8
```

## Lời giải

- Định nghĩa trạng thái: `f[i][j]` biểu thị giá trị tối đa có thể đạt được từ $i$ đồ vật đầu tiên với giới hạn thể tích là $j$.
    - Nếu đồ vật thứ $i$ không được lấy, thì `f[i][j] = f[i - 1][j]`
    - Nếu đồ vật thứ $i$ được lấy, thì `f[i][j] = f[i - 1][j - s[i]] + v[i]`
    - Khi thực hiện chuyển trạng thái, hãy chú ý đến phạm vi miền. Nếu $j < s_i$, thì không xem xét trường hợp lấy đồ vật thứ $i$. Vì nếu $j - s_i$ là số âm, thì chỉ số mảng là không hợp lệ.
      Cũng có thể giải thích theo cách này: thể tích của đồ vật thứ $i$ lớn hơn giới hạn thể tích, vì vậy không thể lấy được.
- Định nghĩa điều kiện ban đầu: Đối với 0 đồ vật đầu tiên, bất kỳ giới hạn thể tích nào cũng cho giá trị là 0, tức là `f[0][j] = 0`, `j` $\in [0, S]$.
- Độ phức tạp thời gian: $O(NS)$.

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

## Tối ưu DP 1D

- Nén mảng hai chiều thành mảng một chiều có thể tiết kiệm đáng kể không gian và cải thiện tốc độ chạy đến một mức độ nhất định (nhược điểm là không thể đáp ứng các yêu cầu đặc biệt của một số loại bài toán).
- Lưu ý rằng trong chuyển trạng thái, `f[i][j]` chỉ liên quan đến `f[i - 1][j]` và `f[i - 1][j - s[i]]`. Nói cách khác, trong mảng hai chiều `f` trong code,
  `f[i][j]` chỉ liên quan đến các phần tử ở hàng trước đó nằm bên trái hoặc cùng cột với nó. Do đó, mảng hai chiều có thể được nén thành mảng một chiều hoặc mảng cuộn.
- Lưu ý rằng trong code bên dưới, vòng lặp thứ hai lặp theo thứ tự ngược lại. Điều này là do chúng ta muốn đảm bảo rằng khi tính toán `f[i][j]`, `f[i - 1][j - s[i]]` chưa được cập nhật.

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

## Nếu Yêu cầu Số Lượng Phương Án

Không chỉ cần xuất ra tổng giá trị tối đa có thể đạt được, mà còn phải xuất ra "có bao nhiêu phương pháp lựa chọn khác nhau có thể đạt được tổng giá trị tối đa này". Phần sau đây mô tả **cách đếm số lượng phương án** trong bài toán cái túi 01.

### DP 2D để Đếm Phương Án

Phần sau đây sử dụng DP 2D làm ví dụ để giải thích.

- Định nghĩa trạng thái:
  - `dp[i][j]` biểu thị "giá trị tối đa có thể đạt được khi xem xét i đồ vật đầu tiên với dung lượng (giới hạn thể tích) là j".
  - `ways[i][j]` biểu thị " **số lượng phương án** tương ứng với giá trị tối đa đạt được khi xem xét i đồ vật đầu tiên với dung lượng là j".

- Chuyển trạng thái:
  1. Nếu đồ vật thứ `i` không được chọn:
     $$
       \text{dp}[i][j] = \text{dp}[i-1][j], 
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
     $$
  2. Nếu đồ vật thứ `i` được chọn (với điều kiện $ j \ge s_i $):
     $$
       \text{dp}[i][j] 
         = \text{dp}[i-1][j - s_i] + v_i,
       \quad
       \text{ways}[i][j]
         = \text{ways}[i-1][j - s_i]
     $$
  3. Dù chọn hay không, `dp[i][j]` cuối cùng phải lấy giá trị lớn hơn trong hai giá trị:
     - Nếu
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           > \text{dp}[i-1][j],
       $$
       thì có nghĩa là "chọn đồ vật thứ i" có giá trị lớn hơn:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j - s_i] + v_i,
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j - s_i].
       $$
     - Nếu
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           = \text{dp}[i-1][j],
       $$
       thì có nghĩa là giá trị tối đa đạt được bằng hai phương pháp là như nhau, thì số lượng phương án nên được cộng vào:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j], 
         \quad
         \text{ways}[i][j] 
           = \text{ways}[i-1][j] 
             + \text{ways}[i-1][j - s_i].
       $$
     - Nếu
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           < \text{dp}[i-1][j],
       $$
       thì có nghĩa là "không chọn đồ vật thứ i" có giá trị lớn hơn, và số lượng phương án kế thừa số lượng phương án khi không chọn:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Điều kiện ban đầu:
  - `dp[0][j] = 0` có nghĩa là khi có 0 đồ vật, giá trị tối đa đạt được cho bất kỳ dung lượng nào là 0.
  - `ways[0][0] = 1` có nghĩa là trường hợp "0 đồ vật, dung lượng 0" là một phương án khả thi (tức là không chọn gì), và **số lượng phương án** được đặt thành 1.
  - Đối với `j > 0`, khi không có đồ vật nào để chọn và dung lượng lớn hơn 0, thì không thể đạt được bất kỳ giá trị dương nào, và số lượng phương án tương ứng là 0, tức là `ways[0][j] = 0`.

- Câu trả lời cuối cùng:
  - `dp[N][S]` là giá trị tối đa.
  - `ways[N][S]` là số lượng phương án để đạt được giá trị tối đa này.
  - Độ phức tạp thời gian: $O(NS)$.
  - Bài toán này cũng có thể được tối ưu hóa bằng cách sử dụng DP 1D.

## Nếu Yêu Cầu Phải Đạt Chính Xác Giới Hạn Thể Tích

- Định nghĩa trạng thái: `f[i][j]` biểu thị giá trị tối đa khi $i$ đồ vật đầu tiên có chính xác thể tích là $j$.
- Nếu đồ vật thứ `i` không được lấy, thì `f[i][j] = f[i - 1][j]`
- Nếu đồ vật thứ `i` được lấy, thì `f[i][j] = f[i - 1][j - s[i]] + v[i]`
- Có thể thấy rằng không có sự khác biệt trong chuyển trạng thái so với bài toán ban đầu.
- Tuy nhiên, các điều kiện ban đầu là khác nhau. Ngoại trừ `f[0][0] = 0`, phần còn lại `f[0][j]` = $-\infty$, `j` $\in [1, S]$. $-\infty$ biểu thị một trạng thái không thể xảy ra.

## Nếu Giới Hạn Thể Tích $S$ Rất Lớn (1e9), Trong Khi Số Lượng Đồ Vật $N$ và Tổng Giá Trị Tối Đa $V$ Tương Đối Nhỏ

- Đối với các bài toán như vậy, có một giải pháp với độ phức tạp là $O(NV)$.
- Định nghĩa trạng thái: `f[i][j]` biểu thị thể tích tối thiểu khi chọn một số đồ vật từ `i` đồ vật đầu tiên, và tổng giá trị chính xác là `j`.
    - Nếu đồ vật thứ `i` không được lấy, thì `f[i][j] = f[i - 1][j]`
    - Nếu đồ vật thứ `i` được lấy, thì `f[i][j] = f[i - 1][j - v[i]] + s[i]`
    - Lấy giá trị nhỏ hơn trong hai giá trị.
- Điều kiện ban đầu: `f[0][0] = 0`, phần còn lại `f[0][j]` = $\infty$, `j` $\in [1, V]$. $\infty$ biểu thị một trạng thái không thể xảy ra. Lưu ý rằng nó không phải là $-\infty$.
- Câu trả lời cuối cùng là `j` lớn nhất trong `f[N][j]` sao cho `f[N][j] <= S`.

## Nếu Giới Hạn Thể Tích $S$ và Giá Trị của Một Đồ Vật $v_i$ Đều Rất Lớn (cỡ 1e9), Trong Khi Số Lượng Đồ Vật $N$ Rất Nhỏ (không quá 40)

- Khi $N \leq 20$, tất cả các tập con có thể được liệt kê trực tiếp bằng vét cạn (độ phức tạp thời gian $O(2^N)$).
- Khi $N \leq 40$, vì $2^{40}$ có cỡ $10^{12}$, vét cạn trực tiếp cũng sẽ tương đối lớn, vì vậy **tìm kiếm meet-in-the-middle** có thể được sử dụng để giảm độ phức tạp xuống xấp xỉ $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$, có thể hoàn thành trong một thời gian chấp nhận được.