---
title: "01 Sırt Çantası Problemi"
date: 2024-12-24
draft: false
description: "En temel klasik sırt çantası problemi."
summary: "En temel klasik sırt çantası problemi."
tags: [ "algoritma", "dinamik programlama", "sırt çantası problemi" ]
categories: [ "Algoritmalar ve Veri Yapıları" ]
series: [ "Sırt Çantası Dokuz Ders" ]
series_order: 1
---

## Problem

$N$ adet eşya var. $i$. eşyanın hacmi $s_i$, değeri $v_i$.
Her eşya yalnızca bir kez alınabilir. Toplam hacim sınırını aşmamak ($S$) koşuluyla, elde edilebilecek maksimum toplam değeri ($V$) bulun.

## Giriş Formatı

İlk satırda iki tam sayı bulunur, $N$ ve $S$, boşlukla ayrılmış olarak, sırasıyla eşya sayısını ve maksimum toplam hacim sınırını belirtir.
Sonraki $N$ satırda, her satırda iki tam sayı bulunur, $s_i$ ve $v_i$, boşlukla ayrılmış olarak, sırasıyla $i$. eşyanın hacmini ve değerini belirtir.

## Çıkış Formatı

Maksimum değeri temsil eden bir tam sayı çıktısı verin.

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

- Durumları tanımlama: `f[i][j]`, ilk $i$ eşya için, hacim sınırı $j$ iken elde edilebilecek maksimum değeri temsil eder.
    - Eğer $i$. eşyayı almazsak, o zaman `f[i][j] = f[i - 1][j]`
    - Eğer $i$. eşyayı alırsak, o zaman `f[i][j] = f[i - 1][j - s[i]] + v[i]`
    - Durum geçişini uygularken, tanım aralığına dikkat edilmelidir. Eğer $j < s_i$ ise, $i$. eşyayı alma durumu dikkate alınmaz. Çünkü eğer $j-s_i$ negatif olursa, dizi indeksi geçersiz olur.
      Veya şöyle de açıklanabilir: $i$. eşyanın hacmi, hacim sınırından daha büyüktür, bu yüzden mümkün değildir.
- Başlangıç koşullarını tanımlama: İlk 0 eşya için, herhangi bir hacim sınırında elde edilen değer 0'dır, yani `f[0][j] = 0`, `j` $\in [0, S]$.
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

## Bir Boyutlu DP Optimizasyonu

- İki boyutlu diziyi bir boyutlu diziye sıkıştırmak, yerden tasarruf sağlayabilir ve çalışma hızını bir dereceye kadar artırabilir (dezavantajı, bazı problem türlerinin özel gereksinimlerini karşılayamamasıdır).
- Durum geçişinde, `f[i][j]`'nin yalnızca `f[i - 1][j]` ve `f[i - 1][j - s[i]]` ile ilişkili olduğuna dikkat edin. Başka bir deyişle, koddaki iki boyutlu dizi `f`'de,
  `f[i][j]` yalnızca bir önceki satırda kendinden daha solda veya aynı sütundaki elemanlarla ilişkilidir, bu nedenle iki boyutlu dizi bir boyutlu diziye veya kayan diziye sıkıştırılabilir.
- Aşağıdaki kodda, ikinci döngünün ters sırada geçtiğine dikkat edin, çünkü `f[i][j]`'yi hesaplarken, `f[i - 1][j - s[i]]`'nin henüz güncellenmemiş olmasını sağlamak istiyoruz.

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

Sadece elde edilebilecek maksimum toplam değeri değil, "bu maksimum toplam değere ulaşmak için kaç farklı seçim yöntemi olduğu" da çıktı olarak verilmesi gerekiyorsa. Şimdi 01 sırt çantası probleminde **çözüm sayısının nasıl sayılacağını** anlatacağız.

### İki Boyutlu DP ile Çözüm Sayısı Sayımı

Aşağıda iki boyutlu DP örneği ile açıklayacağız.

- Durum tanımlama:
  - `dp[i][j]`, "ilk i eşya için, kapasite (hacim sınırı) j iken, elde edilebilecek maksimum değer" anlamına gelir.
  - `ways[i][j]`, "ilk i eşya için, kapasite j iken, maksimum değere ulaşılırkenki **çözüm sayısı**" anlamına gelir.

- Durum geçişi:
  1. Eğer `i`'inci eşya seçilmezse:
     $$
       \text{dp}[i][j] = \text{dp}[i-1][j], 
       \quad
       \text{ways}[i][j] = \text{ways}[i-1][j]
     $$
  2. Eğer `i`'inci eşya seçilirse (ön koşul $ j \ge s_i $):
     $$
       \text{dp}[i][j] 
         = \text{dp}[i-1][j - s_i] + v_i,
       \quad
       \text{ways}[i][j]
         = \text{ways}[i-1][j - s_i]
     $$
  3. Seçme veya seçmeme durumunda, nihai `dp[i][j]` iki değerin daha büyük olanını almalıdır:
     - Eğer
       $$
         \text{dp}[i-1][j - s_i] + v_i 
           > \text{dp}[i-1][j],
       $$
       o zaman "i'inci eşyayı seçmenin" değeri daha büyük demektir:
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
       o zaman iki şekilde de elde edilen maksimum değer aynıdır, bu durumda çözüm sayıları toplanmalıdır:
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
       o zaman "i'inci eşyayı seçmemenin" değeri daha büyüktür, bu durumda çözüm sayısı, seçmeme durumundaki çözüm sayısını devralır:
       $$
         \text{dp}[i][j] = \text{dp}[i-1][j],
         \quad
         \text{ways}[i][j] = \text{ways}[i-1][j].
       $$

- Başlangıç koşulları:
  - `dp[0][j] = 0`, ilk 0 eşya için, herhangi bir kapasitede elde edilen maksimum değerin 0 olduğunu belirtir.
  - `ways[0][0] = 1`, "ilk 0 eşya, kapasite 0" durumu için bir uygun çözüm olduğunu (yani hiçbir şey seçmemek) ve **çözüm sayısının** 1 olarak ayarlanması gerektiğini belirtir.
  - `j > 0` için, seçilecek eşya olmadığında kapasite 0'dan büyükse, herhangi bir pozitif değer elde etmek mümkün değildir ve karşılık gelen çözüm sayısı 0'dır, yani `ways[0][j] = 0`.

- Nihai cevap:
  - `dp[N][S]` maksimum değerdir.
  - `ways[N][S]` bu maksimum değere ulaşmanın çözüm sayısıdır.
  - Zaman karmaşıklığı: $O(NS)$.
  - Bu problem bir boyutlu DP ile de optimize edilebilir.

## Eğer Hacim Sınırına Tam Olarak Ulaşmak İstenirse

- Durumları tanımlama: `f[i][j]`, ilk `i` eşya için tam olarak `j` hacmine sahipken elde edilen maksimum değeri temsil eder.
- Eğer `i`'inci eşya seçilmezse, o zaman `f[i][j] = f[i - 1][j]`
- Eğer `i`'inci eşya seçilirse, o zaman `f[i][j] = f[i - 1][j - s[i]] + v[i]`
- Orijinal problemle durum geçişinin aynı olduğuna dikkat edin.
- Ancak başlangıç koşulları farklıdır. `f[0][0] = 0` hariç, diğer tüm `f[0][j]` = $-\infty$, `j` $\in [1, S]$ olur. $-\infty$ imkansız bir durumu temsil eder.

## Eğer Hacim Sınırı $S$ Çok Büyük (1e9) ve Aynı Zamanda Eşya Sayısı $N$ ve Maksimum Toplam Değer $V$ Küçükse

- Bu tür bir problem için $O(NV)$ karmaşıklığına sahip bir çözüm vardır.
- Durumları tanımlama: `f[i][j]`, ilk `i` eşyadan birkaç tanesini seçerek, toplam değerin tam olarak `j` olduğu en küçük hacmi temsil eder.
    - Eğer `i`'inci eşya seçilmezse, o zaman `f[i][j] = f[i - 1][j]`
    - Eğer `i`'inci eşya seçilirse, o zaman `f[i][j] = f[i - 1][j - v[i]] + s[i]`
    - İkisinin daha küçüğü alınır.
- Başlangıç koşulları: `f[0][0] = 0`, diğer tüm `f[0][j]` = $\infty$, `j` $\in [1, V]$. $\infty$ imkansız bir durumu temsil eder. $-\infty$ değil.
- Nihai cevap, `f[N][j]` içinde `f[N][j] <= S` olan en büyük `j` olur.

## Eğer Hacim Sınırı $S$ ve Tek Eşya Değerleri $v_i$ Çok Büyükse (1e9 mertebesinde) ve Aynı Zamanda Eşya Sayısı $N$ Çok Küçükse (en fazla 40)

- $N \leq 20$ olduğunda, tüm alt kümeler doğrudan kabaca numaralandırılabilir (zaman karmaşıklığı $O(2^N)$).
- $N \leq 40$ olduğunda, $2^{40}$ $10^{12}$ mertebesinde olduğu için, doğrudan kabaca numaralandırma da büyük olacaktır, bu nedenle **ortadan bölme araması** kullanılabilir.
  , bu da karmaşıklığı kabaca $O\bigl(2^{\frac{N}{2}} \times \log(2^{\frac{N}{2}})\bigr) \approx O(N \cdot 2^{\frac{N}{2}})$'ye düşürür.
  , bu da kabul edilebilir bir süre içinde tamamlanabilir.