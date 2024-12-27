---
title: "01 Sırt Çantası Problemi"
date: 2024-12-24
draft: false
description: "En temel klasik sırt çantası problemi."
summary: "En temel klasik sırt çantası problemi."
tags: [ "Algoritma", "Dinamik Programlama", "Sırt Çantası Problemi" ]
categories: [ "Algoritmalar ve Veri Yapıları" ]
series: [ "Sırt Çantası Dokuz Anlatım" ]
series_order: 1
---

## Problem

https://www.acwing.com/problem/content/2/

$N$ tane eşya var. $i$. eşyanın hacmi $s_i$, değeri $v_i$.
Her eşya sadece bir kez alınabilir. Toplam hacim limiti $S$'yi aşmamak koşuluyla, elde edilebilecek maksimum toplam değer $V$'yi bulun.

## Giriş Formatı

İlk satırda iki tam sayı, $N$ ve $S$, boşlukla ayrılmış olarak verilir. Bunlar sırasıyla eşya sayısını ve maksimum toplam hacim limitini temsil eder.
Sonraki $N$ satırda, her satırda iki tam sayı $s_i$ ve $v_i$, boşlukla ayrılmış olarak verilir. Bunlar sırasıyla $i$. eşyanın hacmini ve değerini temsil eder.

## Çıkış Formatı

Maksimum değeri temsil eden bir tam sayı yazdırın.

## Veri Aralığı

$$0 \le N, S \leq 1000$$

$$0 \le s_i, v_i \leq 1000$$

## Giriş Örneği

```
4 5
1 2
2 4
3 4
4 5
```

## Çıkış Örneği

```
8
```

## Çözüm

- Durum Tanımı: `f[i][j]` ifadesi, ilk $i$ eşya için, hacim limiti $j$ olduğunda elde edilebilecek maksimum değeri temsil eder.
    - Eğer $i$. eşya alınmazsa, `f[i][j] = f[i - 1][j]` olur.
    - Eğer $i$. eşya alınırsa, `f[i][j] = f[i - 1][j - s[i]] + v[i]` olur.
    - Durum geçişini uygularken, tanım aralığına dikkat edilmelidir. Eğer $j < s_i$ ise, $i$. eşyanın alınması durumu dikkate alınmaz. Çünkü $j-s_i$ negatif olursa, dizi indeksi geçersiz olur.
      Bunu şöyle de açıklayabiliriz: $i$. eşyanın hacmi, hacim limitinden büyük olduğu için alınması mümkün değildir.
- Başlangıç Koşulu Tanımı: İlk $0$ eşya için, herhangi bir hacim limitinde elde edilecek değer $0$'dır, yani `f[0][j] = 0`, `j` $\in [0, S]$.
- Zaman Karmaşıklığı: $O(NS)$.

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

## Bir Boyutlu DP Optimizasyonu

- İki boyutlu diziyi bir boyutlu diziye sıkıştırmak, önemli ölçüde yer tasarrufu sağlayabilir ve çalışma hızını bir miktar artırabilir (dezavantajı, bazı problem türlerinin özel gereksinimlerini karşılayamamasıdır).
- Durum geçişinde, `f[i][j]`'nin sadece `f[i - 1][j]` ve `f[i - 1][j - s[i]]` ile ilgili olduğuna dikkat edin. Başka bir deyişle, koddaki iki boyutlu `f` dizisinde,
  `f[i][j]` sadece bir önceki satırda kendisinden daha solda veya aynı sütunda bulunan elemanlarla ilgilidir. Bu nedenle, iki boyutlu dizi bir boyutlu diziye veya kayan diziye sıkıştırılabilir.
- Aşağıdaki kodda, ikinci döngünün ters sırada dolaştığına dikkat edin. Bunun nedeni, `f[i][j]`'yi hesaplarken, `f[i - 1][j - s[i]]`'nin henüz güncellenmemiş olmasını garanti etmektir.

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

## Eğer Çözüm Sayısı İstenirse

Sadece elde edilebilecek maksimum toplam değeri değil, aynı zamanda "bu maksimum toplam değere ulaşabilecek kaç farklı seçim yöntemi olduğunu" da çıktı olarak vermeniz gerekiyorsa. Aşağıda, 01 sırt çantası probleminde **çözüm sayısının nasıl hesaplanacağı** anlatılmaktadır.

https://www.acwing.com/problem/content/11/

### İki Boyutlu DP ile Çözüm Sayısını Hesaplama

Aşağıda, iki boyutlu DP örneği üzerinden anlatım yapılmaktadır.

- Durum Tanımı:
  - `dp[i][j]` ifadesi, "ilk i eşya için, kapasite (hacim limiti) j olduğunda, elde edilebilecek maksimum değeri" temsil eder.
  - `ways[i][j]` ifadesi, "ilk i eşya için, kapasite j olduğunda, maksimum değere ulaşıldığında karşılık gelen **çözüm sayısını**" temsil eder.

- Durum Geçişi:
  1. Eğer `i`. eşya seçilmezse:
     $$
       \text{dp}[i][j] = \text{dp}[i-1][j], 
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
     $$
  2. Eğer `i`. eşya seçilirse (ön koşul $ j \ge s_i $):
     $$
       \text{dp}[i][j] 
         = \text{dp}[i-1][j - s_i] + v_i,
       \quad
       \text{ways}[i][j]
         = \text{ways}[i-1][j - s_i]
     $$
  3. Seçme veya seçmeme durumunda, sonuç olarak `dp[i][j]` ikisinin daha büyük olanını almalıdır:
     - Eğer
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           > \text{dp}[i-1][j],
       $$
       ise, bu "i. eşyayı seçmenin" daha büyük bir değer sağladığı anlamına gelir:
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
       ise, bu iki yöntemin de aynı maksimum değeri sağladığı anlamına gelir, bu durumda çözüm sayıları toplanmalıdır:
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
       ise, bu "i. eşyayı seçmemenin" daha büyük bir değer sağladığı anlamına gelir, çözüm sayısı seçmeme durumundaki çözüm sayısını devralır:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Başlangıç Koşulları:
  - `dp[0][j] = 0` ifadesi, ilk 0 eşya için, herhangi bir kapasitede elde edilecek maksimum değerin 0 olduğunu gösterir.
  - `ways[0][0] = 1` ifadesi, "ilk 0 eşya, kapasite 0" durumunun bir geçerli çözüm olduğunu (yani hiçbir şey seçmemek) ve **çözüm sayısının** 1 olarak ayarlandığını gösterir.
  - `j > 0` için, seçilebilecek eşya olmadığında ve kapasite 0'dan büyük olduğunda, herhangi bir pozitif değer elde etmek mümkün değildir, bu duruma karşılık gelen çözüm sayısı 0'dır, yani `ways[0][j] = 0`.

- Son Cevap:
  - `dp[N][S]` maksimum değeri verir.
  - `ways[N][S]` bu maksimum değere ulaşan çözüm sayısını verir.
  - Zaman Karmaşıklığı: $O(NS)$.
  - Bu problem, bir boyutlu DP ile de optimize edilebilir.

## Eğer Hacim Limitine Tam Olarak Ulaşılması İstenirse

- Durum Tanımı: `f[i][j]` ifadesi, ilk `i` eşya için tam olarak $j$ hacmine sahip olmanın maksimum değerini temsil eder.
- Eğer `i`. eşya alınmazsa, `f[i][j] = f[i - 1][j]` olur.
- Eğer `i`. eşya alınırsa, `f[i][j] = f[i - 1][j - s[i]] + v[i]` olur.
- Orijinal problemdeki durum geçişiyle aynı olduğuna dikkat edilebilir.
- Ancak başlangıç koşulları farklıdır. `f[0][0] = 0` dışında, diğer `f[0][j]` = $-\infty$, `j` $\in [1, S]$ olur. $-\infty$ imkansız bir durumu temsil eder.

## Eğer Hacim Limiti $S$ Çok Büyük (1e9) ve Eşya Sayısı $N$ ve Maksimum Toplam Değer $V$ Küçükse

- Bu tür problemler için, karmaşıklığı $O(NV)$ olan bir çözüm vardır.
- Durum Tanımı: `f[i][j]` ifadesi, ilk `i` eşyadan bazılarını seçerek, toplam değeri tam olarak `j` olan minimum hacmi temsil eder.
    - Eğer `i`. eşya alınmazsa, `f[i][j] = f[i - 1][j]` olur.
    - Eğer `i`. eşya alınırsa, `f[i][j] = f[i - 1][j - v[i]] + s[i]` olur.
    - İkisinin minimum değeri alınır.
- Başlangıç Koşulları: `f[0][0] = 0`, diğer `f[0][j]` = $\infty$, `j` $\in [1, V]$ olur. $\infty$ imkansız bir durumu temsil eder. $-\infty$ değil.
- Son cevap, `f[N][j]` içinde `f[N][j] <= S` olacak şekildeki en büyük `j` değeridir.

## Eğer Hacim Limiti $S$ ve Tekil Eşya Değeri $v_i$ Çok Büyükse (1e9 mertebesinde) ve Eşya Sayısı $N$ Çok Küçükse (en fazla 40)

https://www.acwing.com/solution/content/38250/

- $N \leq 20$ olduğunda, tüm alt kümeleri doğrudan kaba kuvvetle sayabilirsiniz (zaman karmaşıklığı $O(2^N)$).
- $N \leq 40$ olduğunda, $2^{40}$ $10^{12}$ mertebesinde olduğundan, doğrudan kaba kuvvet de oldukça büyük olacaktır, bu nedenle **ortadan ikiye bölme araması** kullanılabilir.
  Bu, karmaşıklığı kabaca $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$'ye düşürür.
  Bu, kabul edilebilir bir süre içinde tamamlanabilir.