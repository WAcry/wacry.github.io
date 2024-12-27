---
title: "01 Sırt Çantası Problemi"
date: 2024-12-24
draft: false
description: "En temel klasik sırt çantası problemi."
summary: "En temel klasik sırt çantası problemi."
tags: [ "Algoritma", "Dinamik Programlama", "Sırt Çantası Problemi" ]
categories: [ "Algoritmalar ve Veri Yapıları" ]
---

## Problem

$N$ tane eşya var. $i$-inci eşyanın hacmi $s_i$ ve değeri $v_i$'dir.
Her eşya yalnızca bir kez alınabilir. Maksimum toplam hacim sınırı $S$'yi aşmama koşulu altında, elde edilebilecek maksimum toplam değer $V$'yi bulun.

## Girdi Biçimi

İlk satırda, sırasıyla eşya sayısını ve maksimum toplam hacim sınırını temsil eden, boşlukla ayrılmış iki tam sayı $N$ ve $S$ bulunur.
Aşağıdaki $N$ satırın her birinde, sırasıyla $i$-inci eşyanın hacmini ve değerini temsil eden, boşlukla ayrılmış iki tam sayı $s_i$ ve $v_i$ bulunur.

## Çıktı Biçimi

Maksimum değeri temsil eden bir tam sayı çıktısı verin.

## Veri Aralığı

$$0 \le N, S \leq 1000$$

$$0 \le s_i, v_i \leq 1000$$

## Girdi Örneği

```
4 5
1 2
2 4
3 4
4 5
```

## Çıktı Örneği

```
8
```

## Çözüm

- Durumu tanımlayın: `f[i][j]`, ilk $i$ eşyadan, hacim sınırı $j$ ile elde edilebilecek maksimum değeri temsil eder.
    - Eğer $i$-inci eşya alınmazsa, `f[i][j] = f[i - 1][j]`
    - Eğer $i$-inci eşya alınırsa, `f[i][j] = f[i - 1][j - s[i]] + v[i]`
    - Durum geçişini uygularken, alan aralığına dikkat edin. Eğer $j < s_i$ ise, $i$-inci eşyayı alma durumunu göz önünde bulundurmayın. Çünkü eğer $j - s_i$ negatif ise, dizi indeksi geçersiz olur.
      Bu şu şekilde de açıklanabilir: $i$-inci eşyanın hacmi, hacim sınırından daha büyüktür, bu yüzden imkansızdır.
- Başlangıç koşulunu tanımlayın: İlk $0$ eşya için, herhangi bir hacim sınırı $0$ değerini verir, yani `f[0][j] = 0`, `j` $\in [0, S]$.
- Zaman karmaşıklığı: $O(NS)$.

## Kod

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

## 1D DP Optimizasyonu

- İki boyutlu diziyi tek boyutlu bir diziye sıkıştırmak, önemli ölçüde yer tasarrufu sağlayabilir ve çalışma hızını bir dereceye kadar artırabilir (dezavantajı, bazı problem türlerinin özel gereksinimlerini karşılayamamasıdır).
- Durum geçişinde, `f[i][j]`'nin yalnızca `f[i - 1][j]` ve `f[i - 1][j - s[i]]` ile ilgili olduğuna dikkat edin. Başka bir deyişle, koddaki iki boyutlu `f` dizisinde,
  `f[i][j]` yalnızca önceki satırda solunda veya aynı sütunda bulunan elemanlarla ilgilidir. Bu nedenle, iki boyutlu dizi tek boyutlu bir diziye veya kayan bir diziye sıkıştırılabilir.
- Aşağıdaki kodda, ikinci döngünün ters sırada yinelediğine dikkat edin. Bunun nedeni, `f[i][j]`'yi hesaplarken, `f[i - 1][j - s[i]]`'nin henüz güncellenmemiş olmasını sağlamak istememizdir.

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

## Eğer Şema Sayısı Gerekliyse

Yalnızca elde edilebilecek maksimum toplam değer değil, aynı zamanda "bu maksimum toplam değere ulaşabilecek kaç farklı seçim yöntemi var" da çıktı olarak verilmelidir. Aşağıda, 01 sırt çantası probleminde **şema sayısının nasıl sayılacağı** açıklanmaktadır.

### Şemaları Saymak İçin 2D DP

Aşağıda, açıklamak için 2D DP örneği kullanılmaktadır.

- Durumu tanımlayın:
  - `dp[i][j]`, "ilk i eşya, j kapasite (hacim sınırı) ile değerlendirildiğinde elde edilebilecek maksimum değeri" temsil eder.
  - `ways[i][j]`, "ilk i eşya, j kapasite ile değerlendirildiğinde elde edilen maksimum değere karşılık gelen **şema sayısını**" temsil eder.

- Durum geçişi:
  1. Eğer `i`-inci eşya seçilmezse:
     $$
       \text{dp}[i][j] = \text{dp}[i-1][j], 
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
     $$
  2. Eğer `i`-inci eşya seçilirse ( $ j \ge s_i $ olması koşuluyla):
     $$
       \text{dp}[i][j] 
         = \text{dp}[i-1][j - s_i] + v_i,
       \quad
       \text{ways}[i][j]
         = \text{ways}[i-1][j - s_i]
     $$
  3. Seçilip seçilmemesine bakılmaksızın, nihai `dp[i][j]` ikisinin daha büyüğünü almalıdır:
     - Eğer
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           > \text{dp}[i-1][j],
       $$
       ise, bu "i-inci eşyayı seçmenin" daha büyük bir değere sahip olduğu anlamına gelir:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j - s_i] + v_i,
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j - s_i].
       $$
     - Eğer
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           = \text{dp}[i-1][j],
       $$
       ise, bu iki yöntemle elde edilen maksimum değerin aynı olduğu anlamına gelir, bu durumda şema sayısı eklenmelidir:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j], 
         \quad
         \text{ways}[i][j] 
           = \text{ways}[i-1][j] 
             + \text{ways}[i-1][j - s_i].
       $$
     - Eğer
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           < \text{dp}[i-1][j],
       $$
       ise, bu "i-inci eşyayı seçmemenin" daha büyük bir değere sahip olduğu anlamına gelir ve şema sayısı, seçilmediğinde şema sayısını devralır:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Başlangıç koşulları:
  - `dp[0][j] = 0`, 0 eşya olduğunda, herhangi bir kapasite için elde edilen maksimum değerin 0 olduğu anlamına gelir.
  - `ways[0][0] = 1`, "0 eşya, 0 kapasite" durumunun uygulanabilir bir şema olduğu (yani, hiçbir şey seçmemek) ve **şema sayısının** 1 olarak ayarlandığı anlamına gelir.
  - `j > 0` için, seçilecek eşya olmadığında ve kapasite 0'dan büyük olduğunda, herhangi bir pozitif değer elde etmek imkansızdır ve karşılık gelen şema sayısı 0'dır, yani `ways[0][j] = 0`.

- Nihai cevap:
  - `dp[N][S]` maksimum değerdir.
  - `ways[N][S]` bu maksimum değere ulaşmak için kullanılan şema sayısıdır.
  - Zaman karmaşıklığı: $O(NS)$.
  - Bu problem 1D DP kullanılarak da optimize edilebilir.

## Eğer Hacim Sınırına Tam Olarak Ulaşılması Gerekiyorsa

- Durumu tanımlayın: `f[i][j]`, ilk `i` eşyanın tam olarak $j$ hacmine sahip olduğunda elde edilen maksimum değeri temsil eder.
- Eğer `i`-inci eşya alınmazsa, `f[i][j] = f[i - 1][j]`
- Eğer `i`-inci eşya alınırsa, `f[i][j] = f[i - 1][j - s[i]] + v[i]`
- Durum geçişinde orijinal problemden bir fark olmadığı görülebilir.
- Ancak, başlangıç koşulları farklıdır. `f[0][0] = 0` dışında, geri kalan `f[0][j]` = $-\infty$, `j` $\in [1, S]$. $-\infty$ imkansız bir durumu temsil eder.

## Eğer Hacim Sınırı $S$ Çok Büyükse (1e9), Eşya Sayısı $N$ ve Maksimum Toplam Değer $V$ Nispeten Küçükse

- Bu tür problemler için, $O(NV)$ karmaşıklığına sahip bir çözüm vardır.
- Durumu tanımlayın: `f[i][j]`, ilk `i` eşyadan birkaç eşya seçerken, toplam değerin tam olarak `j` olması durumunda minimum hacmi temsil eder.
    - Eğer `i`-inci eşya alınmazsa, `f[i][j] = f[i - 1][j]`
    - Eğer `i`-inci eşya alınırsa, `f[i][j] = f[i - 1][j - v[i]] + s[i]`
    - İkisinin daha küçüğünü alın.
- Başlangıç koşulları: `f[0][0] = 0`, geri kalan `f[0][j]` = $\infty$, `j` $\in [1, V]$. $\infty$ imkansız bir durumu temsil eder. $-\infty$ olmadığını unutmayın.
- Nihai cevap, `f[N][j]` içinde `f[N][j] <= S` olacak şekildeki en büyük `j`'dir.

## Eğer Hacim Sınırı $S$ ve Tek Bir Eşyanın Değeri $v_i$ Her İkisi de Çok Büyükse (1e9 mertebesinde), Eşya Sayısı $N$ Çok Küçükse (40'tan fazla değil)

- $N \leq 20$ olduğunda, tüm alt kümeler doğrudan kaba kuvvetle numaralandırılabilir (zaman karmaşıklığı $O(2^N)$).
- $N \leq 40$ olduğunda, $2^{40}$ $10^{12}$ mertebesinde olduğundan, doğrudan kaba kuvvet de nispeten büyük olacaktır, bu nedenle karmaşıklığı yaklaşık olarak $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$'ye düşürmek için **ortada buluşma araması** kullanılabilir, bu da kabul edilebilir bir sürede tamamlanabilir.