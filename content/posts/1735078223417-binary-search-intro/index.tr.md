---
title: "İkili Arama"
date: 2024-12-24
draft: false
description: "İkili arama algoritmasını nasıl zarif bir şekilde uygularız."
summary: "İkili arama algoritmasını nasıl zarif bir şekilde uygularız."
tags: [ "algoritma", "ikili arama", "algoritma şablonu" ]
categories: [ "Algoritmalar ve Veri Yapıları" ]
---

Eğer sıralı çözüm uzayı, bir kısmı koşulu sağlayan, diğer kısmı sağlamayan iki kısma ayrılıyorsa, o zaman sıralı çözüm uzayında kritik noktayı bulmak için ikili arama kullanılabilir.

İkili aramanın temel fikri, arama aralığını sürekli olarak ikiye bölmektir. Her kontrol sırasında orta nokta elemanı incelenir. Eğer orta nokta elemanı koşulu sağlamıyorsa, aralığın yarısı elenebilir; aksi takdirde, diğer yarısında aramaya devam edilir. Her seferinde arama aralığının yarısı atıldığı için, arama zaman karmaşıklığı $O(\log n)$'ye ulaşabilir.

## Örnek Soru

**Soru Açıklaması:**  
$n$ uzunluğunda, artan sırada sıralanmış bir tam sayı dizisi ve $q$ tane sorgu veriliyor. Her sorgu bir tam sayı $k$ veriyor. Dizide $k$'nin "başlangıç konumunu" ve "bitiş konumunu" (indeksler 0'dan başlıyor) bulmamız gerekiyor. Eğer dizide bu sayı yoksa, `-1 -1` döndürülmelidir.

### Giriş Formatı

1. İlk satır: Dizi uzunluğunu ve sorgu sayısını temsil eden iki tam sayı $n$ ve $q$.
2. İkinci satır: Artan sırada sıralanmış tam diziyi temsil eden $n$ tam sayı.
3. Sonraki $q$ satır: Her satırda bir sorgu elemanını temsil eden bir tam sayı $k$.

## Veri Aralığı

$1 \leq n \leq 100000$

$1 \leq q \leq 10000$

$1 \leq k \leq 10000$

### Çıkış Formatı

Her sorgu için, elemanın dizideki başlangıç ve bitiş konumlarını bir satırda yazdırın. Eğer dizide bu eleman yoksa, `-1 -1` yazdırın.

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
- $4$ elemanı sadece bir kez, $5$ konumunda görünür;
- $5$ elemanı dizide bulunmadığı için $-1$ $-1$ döndürülür.

---

## Çözüm

- **"Başlangıç Konumunu" Bulma:**
  Yani, $k$'ye eşit veya büyük olan ilk konumu bulmak. Diziyi iki kısma ayırabiliriz:
    - Soldaki tüm sayılar $k$'den "küçüktür"
    - Sağdaki tüm sayılar $k$'ye "eşit veya büyüktür"
    - Cevap, sağdaki ilk konumdur

- **"Bitiş Konumunu" Bulma:**
  Yani, $k$'ye eşit veya küçük olan son konumu bulmak. Diziyi iki kısma ayırabiliriz:
    - Soldaki tüm sayılar $k$'ye "eşit veya küçüktür"
    - Sağdaki tüm sayılar $k$'den "büyüktür"
    - Cevap, soldaki son konumdur

---

## Önerilen Şablon

Aşağıda zarif ve hataya yatkın olmayan bir ikili arama şablonu bulunmaktadır.

İki işaretçi $l, r$ tanımlayın, değişmezler: kapalı aralık $[0, l]$ sol yarıya aittir, kapalı aralık $[r, n - 1]$ sağ yarıya aittir. $l$ ve $r$, $-1$ ve $n$ olarak başlatılır.

Algoritma sona erdiğinde, $l$ ve $r$ bitişiktir, sırasıyla sol yarının son elemanını ve sağ yarının ilk elemanını gösterir.

İstediğimiz çözüm mevcut olmayabileceğinden, eğer soruda mutlaka bir çözümün var olduğu belirtilmemişse, `l` veya `r`'nin sınırların dışına çıkıp çıkmadığını, doğru değeri gösterip göstermediğini kontrol etmemiz gerekir.

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
        //    Cevap, sağ yarının minimum indeksidir.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // Eğer r sınırların dışındaysa veya nums[r] != k ise, k'nin olmadığını gösterir
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. k'nin bitiş konumunu bul
        //    Diziyi iki kısma ayır, sol taraf <= k, sağ taraf > k.
        //    Cevap, sol yarının maksimum indeksidir.
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

### Avantajları

1. Bu yazımın kesin olarak tanımlanmış değişmezleri vardır.
2. Hem "başlangıç konumu" hem de "bitiş konumu" bulma durumları için uygundur, ek işlem veya değişiklik gerektirmez.
3. Bazı yazımlar, durdurma koşulu olarak `l == r` kullanır. $l$ ve $r$ arasındaki fark $1$ olduğunda, $mid$, $l$ veya $r$'ye eşit olarak hesaplanır. Eğer doğru şekilde ele alınmazsa, $l$ veya $r$'yi $mid$ olarak güncelleyerek, arama aralığı küçülmez ve sonsuz döngüye yol açar. Aksine, buradaki yazım $l$ ve $r$ bitişik olduğunda durur, $mid$'in $l$'den küçük ve $r$'den büyük olmasını garanti eder, $l$ veya $r$ güncellendiğinde arama aralığının mutlaka küçülmesini sağlar.

---

## STL

Eğer C++ STL tarafından sağlanan `lower_bound` ve `upper_bound` fonksiyonları kullanılırsa, aynı şey yapılabilir:

- `lower_bound(first, last, val)` "val'e eşit veya büyük olan ilk konumu" döndürür
- `upper_bound(first, last, val)` "val'den büyük olan ilk konumu" döndürür

Örneğin, `nums = {1,2,3,4,4,4,4,4,5,5,6}` olduğunu varsayalım, 4'ün göründüğü aralığı bilmek istiyoruz:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    cout << "4, 0 kez görünüyor" << endl;
} else {
    cout << "ilk 4, " << it1 - nums.begin() << " konumunda" << endl;
    cout << "son 4, " << it2 - nums.begin() - 1 << " konumunda" << endl;
    cout << "4, " << it2 - it1 << " kez görünüyor" << endl;
}
```

- `it1`, değeri $4$'e eşit veya büyük olan ilk konumu gösterir.
- `it2`, değeri $4$'ten büyük olan ilk konumu gösterir.  
  Bu nedenle `it2 - it1`, $4$'ün dizide kaç kez göründüğüdür; `it2 - nums.begin() - 1`, $4$'ün sağ sınırının konumudur.

---

## Ek Bilgiler

İkili arama, kayan noktalı sayı aralığında arama (örneğin, denklem köklerini bulma) ve tek tepeli fonksiyonların maksimum değerini bulmak için üçlü arama gibi durumlara da genişletilebilir.

---

## Alıştırma

LeetCode 33. Search in Rotated Sorted Array

İpucu: İlk adımda dönme noktasını bulmak için ikili arama kullanın, ikinci adımda hedef değeri bulmak için tekrar ikili arama kullanın.