---
title: "İkili Arama"
date: 2024-12-24
draft: false
description: "Tamsayı ikili arama algoritmasını zarif bir şekilde nasıl uygularız?"
tags: [ "Algoritma", "İkili Arama", "Algoritma Şablonu" ]
categories: [ "Algoritmalar ve Veri Yapıları" ]
---
{{< katex >}}

# İkili Arama

Sıralı bir dizide belirli bir elemanı aramak için ikili arama kullanılabilir. Doğrusal aramanın $O(n)$ zaman karmaşıklığına kıyasla, ikili arama sadece $O(\log n)$ zaman gerektirir, bu nedenle büyük veri boyutlarında çok verimlidir.

## İkili Aramanın Temel Düşüncesi

İkili aramanın temel fikri, arama aralığını sürekli olarak ikiye bölmektir. Her karşılaştırmada, orta nokta elemanının hedef değerden büyük veya küçük olup olmadığı kontrol edilir. Orta nokta elemanı koşulu karşılamıyorsa, aralığın yarısı elenebilir; aksi takdirde, diğer yarısında aramaya devam edilir. Her seferinde arama aralığının yarısı atıldığı için arama zaman karmaşıklığı $O(\log n)$'e ulaşabilir.

**"Mümkün çözümlerin sıralı bir aralığa (koşulu sağlayan) ve başka bir sıralı aralığa (koşulu sağlamayan) bölünebildiği"** problemler için ikili arama çok kullanışlıdır. Örneğin:

- Sıralı bir dizide belirli bir elemanın var olup olmadığını bulma
- Belirli bir sayının "ilk konumunu" veya "son konumunu" bulma

## Örnek Problem: Elemanların Başlangıç ve Bitiş Konumlarını Bulma

**Problem Tanımı:**  
Uzunluğu $n$ olan sıralı bir tamsayı dizisi ve $q$ tane sorgu verilmiştir. Her sorgu bir $k$ tamsayısı verir. Dizide $k$'nin "başlangıç konumunu" ve "bitiş konumunu" bulmamız gerekir (indeksler 0'dan başlar). Eğer dizide bu sayı yoksa $-1$ $-1$ döndürün.

**Giriş Formatı:**

1. İlk satır: Dizi uzunluğunu ve sorgu sayısını temsil eden iki tamsayı $n$ ve $q$.
2. İkinci satır: Tam diziyi temsil eden $n$ tane tamsayı (1 ~ 10000 aralığında), artan sırada sıralanmıştır.
3. Sonraki $q$ satır: Her satır bir sorgu elemanı temsil eden bir $k$ tamsayısı içerir.

**Çıkış Formatı:**  
Her sorgu için, elemanın dizideki başlangıç ve bitiş konumlarını bir satırda çıktı olarak verin. Eğer dizide böyle bir eleman yoksa, çıktı olarak $-1$ $-1$ verin.

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

Açıklama:

- 3 elemanının aralığı `[3, 4]`'dür.
- 4 elemanı sadece bir kez, 5. konumda görünür.
- 5 elemanı dizide yoktur, bu nedenle `-1 -1` döndürülür.

## İkili Aramanın Uygulama Düşüncesi

Bu problemde, bir değerin "sol sınırını" ve "sağ sınırını" bulmak için ikili aramaya güvenebiliriz. Önemli olan, arama aralığını nasıl tanımlayacağımızı ve karşılaştırma sonuçlarına göre işaretçileri nasıl hareket ettireceğimizi anlamaktır.

- **"Sol Sınır"ı Bulma:**  
  Yani, $k$'ye eşit veya ondan büyük ilk konumu bulma. Dizi iki kısma ayrılabilir:
    - Soldaki tüm sayılar $k$'den "küçüktür"
    - Sağdaki tüm sayılar $k$'ye "eşit veya ondan büyüktür"

- **"Sağ Sınır"ı Bulma:**  
  Yani, $k$'ye eşit veya ondan küçük son konumu bulma. Dizi iki kısma ayrılabilir:
    - Soldaki tüm sayılar $k$'ye "eşit veya ondan küçüktür"
    - Sağdaki tüm sayılar $k$'den "büyüktür"

Bu iki aralığı doğru bir şekilde koruyabildiğimiz sürece, ikili arama yoluyla hızlı bir şekilde sonuca ulaşabiliriz.

## Önerilen Şablon: Sonsuz Döngüden Kaçınan İkili Arama Yazımı

Aşağıda zarif ve hataya yatkın olmayan bir ikili arama şablonu bulunmaktadır. $l$ ve $r$'nin adım adım yakınlaşmasını sağlayarak döngünün ikisi yan yana geldiğinde mutlaka sona ermesini garanti eder:

İki işaretçi $l$ ve $r$ tanımlayın, değişmez şu şekilde olsun: kapalı aralık $[0, l]$ sol yarıya aittir ve kapalı aralık $[r, n - 1]$ sağ yarıya aittir. $l$ ve $r$ başlangıçta $-1$ ve $n$ olarak başlatılır.

Algoritma sona erdiğinde $l$ ve $r$ bitişiktir; sırasıyla sol yarıdaki maksimum değeri ve sağ yarıdaki minimum değeri gösterirler.

İstediğimiz çözüm mevcut olmayabileceğinden, $l$ veya $r$ döndürülürken, ilgili değerin istediğimiz değer olup olmadığını ve sınırları aşıp aşmadığını kontrol etmemiz gerekir.
Örneğin, $l$, $\leq k$'nin maksimum değerini temsil eder ve `l != -1 && nums[l] == k` kontrol etmemiz gerekir.

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

        // 1. k'nin başlangıç konumunu (sol sınırı) bulma
        //    Diziyi iki kısma ayırın, solda < k olanlar, sağda >= k olanlar.
        //    Sol sınır, sağ kısmın minimum indeksidir.
        int l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] >= k) r = mid; 
            else l = mid;
        }

        // Eğer r sınırı aşıyorsa veya nums[r] != k ise, k'nin olmadığını gösterir.
        if (r == n || nums[r] != k) {
            cout << -1 << " " << -1 << endl;
            continue;
        }

        int leftPos = r; // k'nin sol sınırını kaydet

        // 2. k'nin bitiş konumunu (sağ sınırı) bulma
        //    Diziyi iki kısma ayırın, solda <= k olanlar, sağda > k olanlar.
        //    Sağ sınır, sol kısmın maksimum indeksidir.
        l = -1, r = n;
        while(l < r - 1) {
            int mid = (l + r) / 2;
            if(nums[mid] <= k) l = mid;
            else r = mid;
        }

        // k'nin varlığını zaten kontrol ettiğimiz için burada tekrar kontrol etmeye gerek yok.
        int rightPos = l; // Sağ sınır
        cout << leftPos << " " << rightPos << endl;
    }
    return 0;
}
```

### Neden böyle yazmak hataya daha az yatkındır?

1. Bu yazımın kesin tanımlanmış değişmezleri vardır.
2. Hem sol sınırı hem de sağ sınırı bulabilir, bu nedenle tüm senaryolara uygulanabilir.
3. Bazı yazımlar $l == r$'yi bitiş koşulu olarak kullanır. $l$ ve $r$ arasındaki fark 1 olduğunda, $mid$ değeri $l$ veya $r$'ye eşit hesaplanır. Doğru şekilde işlenmezse, `l` veya `r`'yi `mid` olarak güncellemek arama aralığını daraltmaz ve sonsuz döngüye neden olur. Bunun yerine, buradaki yazım $l$ ve $r$ bitişik olduğunda sonlanır ve bu sorunu önler.

## STL Çözümü: `lower_bound` ve `upper_bound`

Eğer C++ STL tarafından sağlanan `lower_bound` ve `upper_bound` işlevlerini kullanırsanız, aynı şeyi kolayca yapabilirsiniz:

- `lower_bound(first, last, val)` "val'e eşit veya ondan büyük ilk konumu" döndürür.
- `upper_bound(first, last, val)` "val'den büyük ilk konumu" döndürür.

Örneğin, `nums = {1,2,3,4,4,4,4,4,5,5,6}` olduğunu ve 4'ün göründüğü aralığı bilmek istediğimizi varsayalım:

```cpp
vector<int> nums = {1,2,3,4,4,4,4,4,5,5,6};
auto it1 = lower_bound(nums.begin(), nums.end(), 4);
auto it2 = upper_bound(nums.begin(), nums.end(), 4);

if (it1 == nums.end() || *it1 != 4) {
    // Dizi içinde 4 yok demektir
    cout << "4 appears 0 times" << endl;
} else {
    cout << "first 4 is at " << it1 - nums.begin() << endl;
    cout << "last 4 is at " << it2 - nums.begin() - 1 << endl;
    cout << "4 appears " << it2 - it1 << " times" << endl;
}
```

- `it1`, 4'e eşit veya 4'ten büyük ilk değerin konumunu gösterir.
- `it2`, 4'ten büyük ilk değerin konumunu gösterir.  
  Bu nedenle `it2 - it1`, 4'ün dizide kaç kez göründüğüdür; `it2 - nums.begin() - 1`, 4'ün sağ sınırıdır.

Bu iki fonksiyon, aralıkları ararken veya görünme sayısını sayarken özellikle kullanışlıdır.

## Ek

İkili arama, kayan nokta aralıklarında (denklemlerin köklerini bulmak gibi) ve tek modlu bir fonksiyonun maksimum değerini bulmak için üçlü arama olarak genişletilebilir. **"Sıralı bir aralıkta her seferinde yarısını eleyebiliyorum"** şeklindeki temel ilkeyi anladığınız sürece, ikili aramanın birçok durumda sorunları verimli bir şekilde çözmenize yardımcı olabileceğini göreceksiniz.

## Ev Ödevi

LeetCode 33. Search in Rotated Sorted Array

İpucu: İlk adımda dönme noktasını bulmak için ikili aramayı kullanın, ikinci adımda hedef değeri bulmak için tekrar ikili aramayı kullanın.