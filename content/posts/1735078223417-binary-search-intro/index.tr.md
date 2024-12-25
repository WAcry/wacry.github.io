---
title: "İkili Arama"
date: 2024-12-24
draft: false
description: "İkili arama algoritması nasıl zarif bir şekilde uygulanır."
summary: "İkili arama algoritması nasıl zarif bir şekilde uygulanır."
tags: [ "Algoritma", "İkili Arama", "Algoritma Şablonu" ]
categories: [ "Algoritmalar ve Veri Yapıları" ]
---

Eğer sıralı çözüm uzayı sol ve sağ olmak üzere iki kısma ayrılıyorsa ve bu kısımlardan biri koşulu sağlıyor diğeri ise sağlamıyorsa, sıralı çözüm uzayında kritik noktayı bulmak için ikili arama kullanılabilir.

İkili aramanın temel fikri, arama aralığını sürekli olarak ikiye bölmektir. Her kontrol noktasında orta nokta elemanı kontrol edilir, eğer orta nokta elemanı koşulu sağlamıyorsa aralığın yarısı elenir; aksine, diğer yarısında aramaya devam edilir. Her defasında arama aralığının yarısı atıldığı için arama zaman karmaşıklığı $O(\log n)$'ye ulaşabilir.

## Örnek Problem

**Problem Tanımı:**  
Uzunluğu $n$ olan sıralı bir tam sayı dizisi ve $q$ tane sorgu verilmiştir. Her sorgu bir tam sayı $k$ verir ve dizideki $k$'nin "başlangıç konumunu" ve "bitiş konumunu" bulmamız gerekir (indisler 0'dan başlar). Eğer dizide bu sayı yoksa `-1 -1` döndürün.

### Giriş Formatı

1. İlk satır: Dizi uzunluğunu ve sorgu sayısını gösteren iki tam sayı $n$ ve $q$.
2. İkinci satır: Sıralı bir şekilde düzenlenmiş tüm diziyi gösteren $n$ adet tam sayı.
3. Sonraki $q$ satır: Her biri sorgu elemanını gösteren bir tam sayı $k$ içerir.

## Veri Aralığı

$1 \leq n \leq 100000$

$1 \leq q \leq 10000$

$1 \leq k \leq 10000$

### Çıkış Formatı

Her sorgu için, dizideki elemanın başlangıç ve bitiş konumunu bir satırda yazdırın. Eğer eleman dizide yoksa `-1 -1` yazdırın.

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

- $3$ elemanının aralığı $[3, 4]$'tür;
- $4$ elemanı yalnızca bir kez, $5$ konumunda görünür;
- $5$ elemanı dizide yoktur, bu nedenle $-1$ $-1$ döndürülür.

---

## Çözüm

- **"Başlangıç konumunu" bulmak:**
  Yani, $k$'ye eşit veya büyük olan ilk konumu bulmak. Diziyi iki kısma bölebiliriz:
    - Soldaki tüm sayılar $k$'den "küçük"
    - Sağdaki tüm sayılar $k$'ye "eşit veya büyük"
    - Cevap sağdaki ilk konumdur.

- **"Bitiş konumunu" bulmak:**
  Yani, $k$'ye eşit veya küçük olan son konumu bulmak. Diziyi iki kısma bölebiliriz:
    - Soldaki tüm sayılar $k$'ye "eşit veya küçük"
    - Sağdaki tüm sayılar $k$'den "büyük"
    - Cevap soldaki son konumdur.

---

## Önerilen Şablon

Aşağıda, zarif ve hataya yatkın olmayan bir ikili arama şablonu bulunmaktadır. Bu şablon, $l$ ve $r$'nin yavaşça yakınlaşmasını sağlayarak döngünün her ikisi de bitişik olduğunda sona ermesini garanti eder:

İki işaretçi $l, r$ tanımlanır, sabitler şöyledir: kapalı aralık $[0, l]$ sol yarıya aittir ve kapalı aralık $[r, n - 1]$ sağ yarıya aittir. $l$ ve $r$ başlangıçta $-1$ ve $n$ olarak ayarlanır.

Algoritma bittiğinde, $l$ ve $r$ bitişiktir, sırasıyla sol yarıdaki son elemanı ve sağ yarıdaki ilk elemanı işaret eder.

İstediğimiz çözüm mevcut olmayabileceğinden, eğer soruda mutlaka bir çözüm olduğu belirtilmemişse, `l` veya `r`'nin sınırların dışına çıkıp çıkmadığını ve doğru değeri işaret edip etmediğini kontrol etmemiz gerekir.

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

        // 1. k'nin başlangıç konumunu bul
        //    Diziyi iki kısma ayır, sol taraf < k, sağ taraf >= k.
        //    Cevap sağ tarafın en küçük indeksidir.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // Eğer r sınırların dışına çıktıysa veya nums[r] != k ise, k'nin mevcut olmadığını belirtir
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. k'nin bitiş konumunu bul
        //    Diziyi iki kısma ayır, sol taraf <= k, sağ taraf > k.
        //    Cevap sol tarafın en büyük indeksidir.
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

### Neden Böyle Yazıyoruz

1. Bu yazımın kesin olarak tanımlanmış değişmezleri vardır.
2. Hem "başlangıç konumunu" hem de "bitiş konumunu" bulma durumlarına aynı anda uygulanabilir, ek işlem ve değişikliklere gerek kalmaz.
3. Bazı yazımlarda durdurma koşulu olarak `l == r` kullanılır. $l$ ve $r$ arasındaki fark $1$ olduğunda, $mid$ $l$ veya $r$'ye eşit olarak hesaplanır. Doğru işlenmezse, $l$ veya $r$'yi $mid$ olarak güncelleyerek, arama aralığı daralmaz ve sonsuz döngüye yol açar. Aksine, buradaki yazım $l$ ve $r$ bitişik olduğunda durdurulur, $mid$'in $l$'den küçük ve $r$'den büyük olmasını sağlayarak, $l$ veya $r$ güncellendiğinde arama aralığının kesinlikle daralmasını sağlar.

---

## STL

C++ STL tarafından sağlanan `lower_bound` ve `upper_bound` işlevlerini kullanırsak, aynı işi tamamlayabiliriz:

- `lower_bound(first, last, val)` "val'e eşit veya büyük olan ilk konumu" döndürür.
- `upper_bound(first, last, val)` "val'den büyük olan ilk konumu" döndürür.

Örnek olarak, `nums = {1,2,3,4,4,4,4,4,5,5,6}` olduğunu ve 4'ün aralığını öğrenmek istediğimizi varsayalım:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    cout << "4, 0 kere görünüyor" << endl;
} else {
    cout << "ilk 4, " << it1 - nums.begin() << " konumunda" << endl;
    cout << "son 4, " << it2 - nums.begin() - 1 << " konumunda" << endl;
    cout << "4, " << it2 - it1 << " kere görünüyor" << endl;
}
```

- `it1`, değeri $4$'e eşit veya büyük olan ilk konumu işaret eder.
- `it2`, değeri $4$'ten büyük olan ilk konumu işaret eder.
  Bu nedenle `it2 - it1`, $4$'ün dizide kaç kez göründüğüdür; `it2 - nums.begin() - 1` ise $4$'ün sağ sınırıdır.

---

## Ek

İkili arama, kayan noktalı sayı aralığında arama yapmaya (örneğin, bir denklemin köklerini bulmaya) ve tek tepeli fonksiyonun maksimum değerini bulmak için üçlü arama yapmaya kadar genişletilebilir.
"**Sıralı bir aralıkta her seferinde yarısını eleyebildiğiniz**" temel ilkesini anladığınız sürece, ikili aramanın birçok senaryoda sorunları verimli bir şekilde çözmenize yardımcı olacağını göreceksiniz.

---

## Alıştırma

LeetCode 33. Search in Rotated Sorted Array

İpucu: İlk adımda, dönme noktasını bulmak için ikili arama kullanın, ikinci adımda ise hedef değeri bulmak için ikili arama kullanın.