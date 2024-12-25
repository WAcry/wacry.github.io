---
title: "İkili Arama"
date: 2024-12-24
draft: false
description: "Tamsayı ikili arama algoritmasını nasıl zarif bir şekilde uygulayabiliriz."
summary: "Tamsayı ikili arama algoritmasını nasıl zarif bir şekilde uygulayabiliriz."
tags: [ "algoritma", "ikili arama", "algoritma şablonu" ]
categories: [ "Algoritmalar ve Veri Yapıları" ]
---

{{< katex >}}

# İkili Arama

Eğer sıralı bir çözüm uzayı, bir kısmı koşulu sağlayan ve diğer kısmı sağlamayan iki bölüme ayrılıyorsa, bu sıralı çözüm uzayında kritik noktayı bulmak için ikili arama kullanılabilir.

İkili aramanın temel fikri, arama aralığını sürekli olarak ikiye bölmektir. Her seferinde orta noktadaki elemanı kontrol ederiz. Eğer orta nokta elemanı koşulu sağlamazsa, aralığın yarısını eleriz; aksi takdirde, diğer yarıda aramaya devam ederiz. Her seferinde arama aralığının yarısı atıldığı için, arama zaman karmaşıklığı \\(O(\log n)\\) seviyesine ulaşır.

## Örnek Problem

**Problem Tanımı:**  
\\(n\\) uzunluğunda artan sırada sıralanmış bir tamsayı dizisi ve \\(q\\) sorgu verildiğinde. Her sorguda bir tamsayı \\(k\\) verilir ve dizide \\(k\\) değerinin "başlangıç pozisyonunu" ve "bitiş pozisyonunu" bulmamız gerekir (indeksler 0'dan başlar). Eğer dizide bu sayı yoksa, \\(-1\\) \\(-1\\) döndürülmelidir.

### Giriş Formatı

1. İlk satır: İki tamsayı \\(n\\) ve \\(q\\), sırasıyla dizi uzunluğunu ve sorgu sayısını belirtir.
2. İkinci satır: Tam diziyi temsil eden, artan sırada sıralanmış \\(n\\) adet tamsayı.
3. Sonraki \\(q\\) satır: Her satırda bir sorgu elemanını temsil eden bir tamsayı \\(k\\) bulunur.

## Veri Aralığı

\\(1 \leq n \leq 100000\\)

\\(1 \leq q \leq 10000\\)

\\(1 \leq k \leq 10000\\)

### Çıkış Formatı

Her sorgu için, dizideki elemanın başlangıç ve bitiş pozisyonlarını tek bir satırda yazdırın. Eğer eleman dizide bulunmuyorsa, `-1 -1` çıktısını verin.

**Örnek:**

```
Giriş:
6 3
1 2 2 3 3 4
3
4
5

Çıkış:
3 4
5 5
-1 -1
```

**Açıklama:**

- \\(3\\) elemanı \\([3, 4]\\) aralığında görünür;
- \\(4\\) elemanı sadece bir kez, \\(5\\) pozisyonunda görünür;
- \\(5\\) elemanı dizide bulunmadığı için, \\(-1\\) \\(-1\\) döndürülür.

---

## Çözüm

- **"Başlangıç Pozisyonunu" Bulmak:**
  Yani, \\(k\\)'ye eşit veya ondan büyük olan ilk pozisyonu bulmak. Diziyi iki kısma ayırabiliriz:
    - Sol taraftaki tüm sayılar \\(k\\)'den "küçüktür".
    - Sağ taraftaki tüm sayılar \\(k\\)'ye "eşit veya ondan büyüktür".
    - Cevap sağ tarafın ilk pozisyonudur.

- **"Bitiş Pozisyonunu" Bulmak:**
  Yani, \\(k\\)'ye eşit veya ondan küçük olan son pozisyonu bulmak. Diziyi iki kısma ayırabiliriz:
    - Sol taraftaki tüm sayılar \\(k\\)'ye "eşit veya ondan küçüktür".
    - Sağ taraftaki tüm sayılar \\(k\\)'den "büyüktür".
    - Cevap sol tarafın son pozisyonudur.

---

## Önerilen Şablon

Aşağıda zarif ve hataya yatkın olmayan bir ikili arama şablonu bulunmaktadır. \\(l\\) ve \\(r\\) işaretçilerini yavaşça birbirine yaklaştırarak döngünün kesinlikle birbirine komşu oldukları noktada sona ermesini sağlar:

İki işaretçi \\(l, r\\) tanımlayın. Değişmezler: Kapalı aralık \\([0, l]\\) sol yarıya, kapalı aralık \\([r, n - 1]\\) sağ yarıya aittir. \\(l\\) ve \\(r\\) sırasıyla \\(-1\\) ve \\(n\\) olarak başlatılır.

Algoritma sona erdiğinde, \\(l\\) ve \\(r\\) birbirine komşu olacaktır; \\(l\\) sol yarının son elemanına ve \\(r\\) sağ yarının ilk elemanına işaret eder.

İstediğimiz çözüm olmayabileceği için, eğer problemde çözümün kesinlikle var olduğu belirtilmiyorsa, `l` veya `r`'nin sınırları aşıp aşmadığını ve doğru değeri gösterip göstermediğini kontrol etmeliyiz.

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

        // 1. k'nin başlangıç pozisyonunu bul
        //    Diziyi ikiye ayır, sol taraf < k, sağ taraf >= k.
        //    Cevap sağ tarafın en küçük indeksi.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid;
            else l = mid;
        }

        // Eğer r sınırları aşıyor veya nums[r] != k ise, k yok demektir.
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. k'nin bitiş pozisyonunu bul
        //    Diziyi ikiye ayır, sol taraf <= k, sağ taraf > k.
        //    Cevap sol tarafın en büyük indeksi.
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

### Neden Bu Şekilde Yazdık?

1. Bu yazım şeklinin kesin olarak tanımlanmış değişmezleri vardır.
2. Hem "başlangıç pozisyonunu" hem de "bitiş pozisyonunu" bulma durumları için uygundur, ekstra işleme veya değişikliğe gerek yoktur.
3. Bazı yazım şekilleri `l == r` koşulunu bitiş koşulu olarak kullanır. \\(l\\) ve \\(r\\) arasındaki fark \\(1\\) olduğunda, \\(mid\\) değeri \\(l\\) veya \\(r\\)'ye eşit hesaplanır. Eğer doğru şekilde işlenmezse, \\(l\\) veya \\(r\\)'yi \\(mid\\) olarak güncelleyerek arama aralığı küçülmez ve sonsuz bir döngüye yol açar. Aksine, buradaki yazım şekli \\(l\\) ve \\(r\\) komşu olduğunda sona erer, \\(mid\\) değerinin \\(l\\)'den küçük ve \\(r\\)'den büyük olmasını garantiler, \\(l\\) veya \\(r\\)'yi güncellerken arama aralığının kesinlikle küçülmesini sağlar.

---

## STL

C++ STL tarafından sağlanan `lower_bound` ve `upper_bound` fonksiyonlarını kullanarak da aynı şeyi yapabiliriz:

- `lower_bound(first, last, val)`, "ilk değeri val'e eşit veya ondan büyük olan pozisyonu" döndürür.
- `upper_bound(first, last, val)`, "ilk değeri val'den büyük olan pozisyonu" döndürür.

Örnek olarak, `nums = {1,2,3,4,4,4,4,4,5,5,6}` olduğunu varsayalım ve 4'ün göründüğü aralığı bilmek istiyoruz:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    cout << "4, 0 kez görünüyor" << endl;
} else {
    cout << "ilk 4'ün yeri " << it1 - nums.begin() << endl;
    cout << "son 4'ün yeri " << it2 - nums.begin() - 1 << endl;
    cout << "4, " << it2 - it1 << " kez görünüyor" << endl;
}
```

- `it1` değeri, ilk değeri \\(4\\)'e eşit veya ondan büyük olan konumu gösterir.
- `it2` değeri, ilk değeri \\(4\\)'den büyük olan konumu gösterir.
  Bu nedenle, `it2 - it1`, dizideki \\(4\\)'ün görünme sayısıdır; `it2 - nums.begin() - 1`, \\(4\\)'ün sağ sınırıdır.

---

## Ek Bilgiler

İkili arama, kayan noktalı sayı aralığında (örneğin, denklem kökleri bulma) arama yapmak ve tek tepeli fonksiyonların en büyük değerini bulmak için de genişletilebilir.
"**Sıralı bir aralıkta, her seferinde yarısını eleyebilirsin**" temel prensibini anladığın sürece, ikili aramanın birçok senaryoda sorunları verimli bir şekilde çözmene yardımcı olacağını göreceksin.

---

## Alıştırma

LeetCode 33. Search in Rotated Sorted Array

İpucu: İlk adımda, dönüş noktasını bulmak için ikili arama kullanın, ikinci adımda hedef değeri bulmak için ikili arama kullanın.