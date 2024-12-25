---
title: "Bài toán cái túi 01"
date: 2024-12-24
draft: false
description: "Bài toán cái túi cổ điển cơ bản nhất."
summary: "Bài toán cái túi cổ điển cơ bản nhất."
tags: [ "Thuật toán", "Quy hoạch động", "Bài toán cái túi" ]
categories: [ "Thuật toán và cấu trúc dữ liệu" ]
series: [ "Chín bài giảng về cái túi" ]
---

## Đề bài

Có $N$ đồ vật. Đồ vật thứ $i$ có thể tích là $s_i$, giá trị là $v_i$.
Mỗi đồ vật chỉ được lấy một lần. Trong giới hạn tổng thể tích tối đa $S$, hãy tìm tổng giá trị lớn nhất $V$ có thể đạt được.

## Định dạng đầu vào

Dòng đầu tiên gồm hai số nguyên, $N, S$, cách nhau bằng dấu cách, lần lượt biểu thị số lượng đồ vật và giới hạn tổng thể tích tối đa.
Tiếp theo có $N$ dòng, mỗi dòng gồm hai số nguyên $s_i, v_i$, cách nhau bằng dấu cách, lần lượt biểu thị thể tích và giá trị của đồ vật thứ $i$.

## Định dạng đầu ra

In ra một số nguyên, biểu thị giá trị lớn nhất.

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

- Định nghĩa trạng thái: `f[i][j]` biểu thị giá trị lớn nhất có thể nhận được khi xét $i$ đồ vật đầu tiên với giới hạn thể tích là $j$.
    - Nếu không lấy đồ vật thứ $i$, thì `f[i][j] = f[i - 1][j]`
    - Nếu lấy đồ vật thứ $i$, thì `f[i][j] = f[i - 1][j - s[i]] + v[i]`
    - Khi thực hiện chuyển trạng thái, cần chú ý đến phạm vi định nghĩa. Nếu $j < s_i$, thì không xét trường hợp lấy đồ vật thứ $i$. Bởi vì nếu $j - s_i$ là số âm, thì chỉ số mảng không hợp lệ.
      Cũng có thể giải thích như sau: Thể tích của đồ vật thứ $i$ lớn hơn giới hạn thể tích, nên không thể lấy được.
- Định nghĩa điều kiện ban đầu: Với $0$ đồ vật đầu tiên, mọi giới hạn thể tích đều nhận được giá trị $0$, tức là `f[0][j] = 0`, `j` $\in [0, S]$.
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

## Tối ưu DP một chiều

- Nén mảng hai chiều thành mảng một chiều, có thể tiết kiệm không gian đáng kể và tăng tốc độ chạy ở một mức độ nhất định (nhược điểm là không thể đáp ứng các yêu cầu đặc biệt của một số dạng bài)
- Lưu ý rằng trong chuyển trạng thái, `f[i][j]` chỉ liên quan đến `f[i - 1][j]` và `f[i - 1][j - s[i]]`. Nói cách khác, trong mảng hai chiều `f` trong code,
  `f[i][j]` chỉ liên quan đến các phần tử ở hàng trên nó và ở bên trái hoặc cùng cột, do đó có thể nén mảng hai chiều thành mảng một chiều hoặc mảng cuộn.
- Lưu ý rằng trong code dưới đây, vòng lặp thứ hai duyệt ngược, điều này là để đảm bảo rằng khi tính `f[i][j]`, `f[i - 1][j - s[i]]` chưa bị cập nhật.

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

## Nếu yêu cầu số lượng phương án

Không chỉ phải in ra tổng giá trị lớn nhất có thể đạt được, mà còn phải in ra "có bao nhiêu cách chọn khác nhau để đạt được tổng giá trị lớn nhất này". Dưới đây giới thiệu cách **thống kê số lượng phương án** trong bài toán cái túi 01.

### Thống kê số lượng phương án bằng DP hai chiều

Dưới đây lấy DP hai chiều làm ví dụ để giải thích.

- Định nghĩa trạng thái:
  - `dp[i][j]` biểu thị "khi xét $i$ đồ vật đầu tiên, với dung lượng (giới hạn thể tích) là $j$, giá trị lớn nhất có thể đạt được".
  - `ways[i][j]` biểu thị "khi xét $i$ đồ vật đầu tiên, với dung lượng là $j$, **số lượng phương án** tương ứng khi đạt được giá trị lớn nhất".

- Chuyển trạng thái:
  1. Nếu không chọn đồ vật thứ `i`:
     $$
       \text{dp}[i][j] = \text{dp}[i-1][j], 
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
     $$
  2. Nếu chọn đồ vật thứ `i` (với điều kiện $ j \ge s_i $):
     $$
       \text{dp}[i][j] 
         = \text{dp}[i-1][j - s_i] + v_i,
       \quad
       \text{ways}[i][j]
         = \text{ways}[i-1][j - s_i]
     $$
  3. Chọn hoặc không chọn, cuối cùng `dp[i][j]` nên lấy giá trị lớn hơn trong hai giá trị:
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
       thì có nghĩa là hai cách đều đạt được giá trị lớn nhất giống nhau, thì số lượng phương án nên được cộng vào:
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
       thì có nghĩa là "không chọn đồ vật thứ i" có giá trị lớn hơn, số lượng phương án được kế thừa từ phương án không chọn:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Điều kiện ban đầu:
  - `dp[0][j] = 0` biểu thị khi xét 0 đồ vật đầu tiên, mọi dung lượng đều nhận được giá trị lớn nhất là 0.  
  - `ways[0][0] = 1` biểu thị "0 đồ vật đầu tiên, dung lượng là 0" là một phương án khả thi (tức là không chọn gì cả), **số lượng phương án** được đặt là 1.  
  - Với `j > 0`, khi không có đồ vật nào để chọn mà dung lượng lại lớn hơn 0, thì không thể đạt được bất kỳ giá trị dương nào, số lượng phương án tương ứng là 0, tức là `ways[0][j] = 0`.

- Đáp án cuối cùng:  
  - `dp[N][S]` chính là giá trị lớn nhất.  
  - `ways[N][S]` chính là số lượng phương án để đạt được giá trị lớn nhất đó.
  - Độ phức tạp thời gian: $O(NS)$.
  - Bài này cũng có thể dùng DP một chiều để tối ưu.

## Nếu yêu cầu đạt đúng giới hạn thể tích

- Định nghĩa trạng thái: `f[i][j]` biểu thị giá trị lớn nhất khi chọn `i` đồ vật đầu tiên có tổng thể tích đúng bằng `j`.
- Nếu không lấy đồ vật thứ `i`, thì `f[i][j] = f[i - 1][j]`
- Nếu lấy đồ vật thứ `i`, thì `f[i][j] = f[i - 1][j - s[i]] + v[i]`
- Có thể nhận thấy rằng việc chuyển trạng thái không khác gì bài toán gốc.
- Nhưng điều kiện ban đầu lại khác. Ngoài `f[0][0] = 0`, các `f[0][j]` còn lại đều bằng $-\infty$, `j` $\in [1, S]$. $-\infty$ biểu thị trạng thái không thể xảy ra.

## Nếu giới hạn thể tích $S$ quá lớn (1e9), đồng thời số lượng đồ vật $N$ và tổng giá trị lớn nhất $V$ lại nhỏ

- Với các bài như vậy, có một cách giải với độ phức tạp $O(NV)$.
- Định nghĩa trạng thái: `f[i][j]` biểu thị thể tích nhỏ nhất khi chọn một số đồ vật trong `i` đồ vật đầu tiên mà có tổng giá trị đúng bằng `j`.
    - Nếu không lấy đồ vật thứ `i`, thì `f[i][j] = f[i - 1][j]`
    - Nếu lấy đồ vật thứ `i`, thì `f[i][j] = f[i - 1][j - v[i]] + s[i]`
    - Lấy giá trị nhỏ hơn trong hai giá trị.
- Điều kiện ban đầu: `f[0][0] = 0`, các `f[0][j]` còn lại bằng $\infty$, `j` $\in [1, V]$. $\infty$ biểu thị trạng thái không thể xảy ra. Lưu ý không phải là $-\infty$.
- Đáp án cuối cùng là giá trị `j` lớn nhất trong các `f[N][j]` sao cho `f[N][j] <= S`.

## Nếu giới hạn thể tích $S$ và giá trị của từng đồ vật $v_i$ đều rất lớn (cỡ $1e9$), đồng thời số lượng đồ vật $N$ lại rất nhỏ (tối đa không quá 40)

- Khi $N \leq 20$, có thể trực tiếp duyệt trâu tất cả các tập con (độ phức tạp thời gian $O(2^N)$).
- Khi $N \leq 40$, vì $2^{40}$ ở cỡ $10^{12}$, duyệt trâu trực tiếp cũng sẽ khá lớn, vì vậy có thể sử dụng **tìm kiếm chia đôi**
  , giảm độ phức tạp xuống xấp xỉ $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$
  , có thể hoàn thành trong thời gian chấp nhận được.