---
title: "İkili Arama"
date: 2024-12-24
draft: false
description: "İkili arama algoritmasının zarif bir şekilde nasıl uygulanacağı."
summary: "İkili arama algoritmasının zarif bir şekilde nasıl uygulanacağı."
tags: [ "Algoritma", "İkili Arama", "Algoritma Şablonu" ]
categories: [ "Algoritmalar ve Veri Yapıları" ]
---

Sıralı bir çözüm uzayı iki parçaya ayrıldığında, bir parça bir koşulu sağlarken diğeri sağlamıyorsa, sıralı çözüm uzayındaki kritik noktayı bulmak için ikili arama kullanılabilir.

İkili aramanın temel fikri, arama aralığını tekrar tekrar yarıya indirmektir. Her seferinde orta eleman kontrol edilir. Orta eleman koşulu sağlamıyorsa, aralığın yarısı elenebilir; aksi takdirde, arama diğer yarısında devam eder. Her seferinde arama aralığının yarısı atıldığı için, arama zaman karmaşıklığı $O(\log n)$'ye ulaşabilir.

## Örnek Problem

**Problem Açıklaması:**
Uzunluğu $n$ olan artan sıralı bir tamsayı dizisi ve $q$ sorgu veriliyor. Her sorgu bir tamsayı $k$ verir ve dizideki $k$'nin "başlangıç pozisyonunu" ve "bitiş pozisyonunu" bulmamız gerekir (indeksler 0'dan başlar). Sayı dizide yoksa, `-1 -1` döndürün.

### Giriş Formatı

1. İlk satır: dizinin uzunluğunu ve sorgu sayısını temsil eden iki tamsayı $n$ ve $q$.
2. İkinci satır: artan sırada sıralanmış tam diziyi temsil eden $n$ tamsayı.
3. Sonraki $q$ satır: her satır bir sorgu elemanını temsil eden bir tamsayı $k$ içerir.

## Veri Aralığı

$1 \leq n \leq 100000$

$1 \leq q \leq 10000$

$1 \leq k \leq 10000$

### Çıkış Formatı

Her sorgu için, dizideki elemanın başlangıç ve bitiş pozisyonlarını tek bir satırda çıktılayın. Eleman dizide yoksa, `-1 -1` çıktılayın.

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

- $3$ elemanının göründüğü aralık $[3, 4]$'tür;
- $4$ elemanı yalnızca bir kez, $5$ pozisyonunda görünür;
- $5$ elemanı dizide yok, bu yüzden $-1$ $-1$ döndürülür.

---

## Çözüm

- **"Başlangıç Pozisyonunu" Bulma:**
  Yani, $k$'ye eşit veya büyük olan ilk pozisyonu bulmak. Dizi iki parçaya ayrılabilir:
    - Soldaki tüm sayılar $k$'den "küçüktür"
    - Sağdaki tüm sayılar $k$'ye "eşit veya büyüktür"
    - Cevap, sağdaki ilk pozisyondur

- **"Bitiş Pozisyonunu" Bulma:**
  Yani, $k$'ye eşit veya küçük olan son pozisyonu bulmak. Dizi iki parçaya ayrılabilir:
    - Soldaki tüm sayılar $k$'ye "eşit veya küçüktür"
    - Sağdaki tüm sayılar $k$'den "büyüktür"
    - Cevap, soldaki son pozisyondur

---

## Önerilen Şablon

Aşağıda zarif ve daha az hataya yatkın bir ikili arama şablonu bulunmaktadır.

İki işaretçi $l, r$ tanımlayın, değişmez: kapalı aralık $[0, l]$ sol parçaya aittir ve kapalı aralık $[r, n - 1]$ sağ parçaya aittir. $l$ ve $r$ sırasıyla $-1$ ve $n$ olarak başlatılır.

Algoritma sona erdiğinde, $l$ ve $r$ bitişiktir, sırasıyla sol parçanın son elemanına ve sağ parçanın ilk elemanına işaret eder.

İstediğimiz çözüm mevcut olmayabileceğinden, problem kesinlikle bir çözümün var olduğunu belirtmiyorsa, `l` veya `r`'nin sınırların dışında olup olmadığını ve doğru değere işaret edip etmediğini kontrol etmemiz gerekir.

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
        //    Diziyi iki parçaya ayır, sol parça tümü < k, ve sağ parça tümü >= k.
        //    Cevap, sağ parçanın en küçük indeksidir.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // Eğer r sınırların dışındaysa veya nums[r] != k ise, bu k'nin mevcut olmadığı anlamına gelir
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r;

        // 2. k'nin bitiş pozisyonunu bul
        //    Diziyi iki parçaya ayır, sol parça tümü <= k, ve sağ parça tümü > k.
        //    Cevap, sol parçanın en büyük indeksidir.
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

1. Bu yaklaşımın kesin olarak tanımlanmış değişmezleri vardır.
2. Ek bir işlem veya değişiklik olmadan hem "başlangıç pozisyonunu" hem de "bitiş pozisyonunu" bulmaya uygulanır.
3. Bazı yaklaşımlar `l == r`'yi sonlandırma koşulu olarak kullanır. $l$ ve $r$ 1 farkla ayrıldığında, $mid$, $l$ veya $r$'ye eşit olacak şekilde hesaplanır. Doğru şekilde ele alınmazsa, $l$ veya $r$'yi $mid$'e güncellemek arama aralığını daraltmaz ve sonsuz döngüye yol açar. Buna karşılık, bu yaklaşım $l$ ve $r$ bitişik olduğunda sona erer, bu da $mid$'in $l$'den küçük ve $r$'den büyük olmasını sağlar ve $l$ veya $r$'yi güncellemek her zaman arama aralığını daraltır.

---

## STL

C++ STL tarafından sağlanan `lower_bound` ve `upper_bound` fonksiyonlarını kullanırsanız, aynı şeyi elde edebilirsiniz:

- `lower_bound(first, last, val)` "val'e eşit veya büyük olan ilk pozisyonu" döndürür
- `upper_bound(first, last, val)` "val'den büyük olan ilk pozisyonu" döndürür

Örneğin, `nums = {1,2,3,4,4,4,4,4,5,5,6}` olduğunu ve 4'ün göründüğü aralığı bilmek istediğimizi varsayalım:

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

- `it1`, değerin $4$'e eşit veya büyük olduğu ilk pozisyona işaret eder.
- `it2`, değerin $4$'ten büyük olduğu ilk pozisyona işaret eder.
  Bu nedenle, `it2 - it1`, $4$'ün dizide kaç kez göründüğüdür; `it2 - nums.begin() - 1`, $4$'ün sağ sınırının pozisyonudur.

---

## Ek Notlar

İkili arama, kayan noktalı aralıklarda arama yapmak (örneğin, bir denklemin köklerini bulmak gibi) ve tek modlu fonksiyonların ekstremalarını bulmak için üçlü arama yapmak için de genişletilebilir.

---

## Alıştırma

LeetCode 33. Rotated Sorted Array'de Arama

İpucu: Önce, dönme noktasını bulmak için ikili arama kullanın ve ardından hedef değeri bulmak için ikili arama kullanın.