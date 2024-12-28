---
title: "Hızlı Sıralama"
date: 2024-12-26
draft: false
description: "Hızlı sıralama algoritmasının doğru şekilde uygulanmasının anahtar noktalarının analizi."
summary: "Hızlı sıralama algoritmasının doğru şekilde uygulanmasının anahtar noktalarının analizi."
tags: [ "Algoritma", "Sıralama Algoritması", "Hızlı Sıralama", "Böl ve Fethet Algoritması" ]
categories: [ "Algoritmalar ve Veri Yapıları" ]
---

Hızlı sıralama, karşılaştırmaya dayalı, kararlı olmayan bir sıralama algoritmasıdır. Böl ve fethet yaklaşımını kullanır. Ortalama zaman karmaşıklığı $O(n\log n)$'dir, en kötü durumda $O(n^2)$'dir ve uzay karmaşıklığı $O(1)$'dir. Aşağıda, bir tamsayı dizisini küçükten büyüğe sıralama örneği üzerinden uygulama detayları ve yaygın hatalar tanıtılmaktadır.

---

## Problem Tanımı

$n$ uzunluğunda bir tamsayı dizisi verildiğinde, hızlı sıralama kullanarak küçükten büyüğe sıralayın ve sonucu çıktılayın.

### Giriş Formatı

- İlk satırda $n$ tamsayısı girilir.
- İkinci satırda, her biri $[1,10^9]$ aralığında olan $n$ tamsayı girilir.

### Çıkış Formatı

- Sıralanmış diziyi tek satırda çıktılayın.

### Veri Aralığı

$1 \leq n \leq 100000$

### Giriş Örneği

```
5
3 1 2 4 5
```

### Çıkış Örneği

```
1 2 3 4 5
```

---

## Hızlı Sıralama Mantığı

Hızlı sıralama, her bölme adımında bir sayı seçerek `pivot` (aşağıda orta konumdaki sayı seçilmiştir) olarak kullanır.

Sol işaretçi `L` soldan sağa doğru `pivot`'a eşit veya büyük ilk sayıyı ararken, sağ işaretçi `R` sağdan sola doğru `pivot`'a eşit veya küçük ilk sayıyı arar ve ardından bu iki sayıyı değiştirir.

Sol işaretçi ve sağ işaretçi çakışana veya sol işaretçi sağ işaretçiden bir pozisyon büyük olana kadar bu işlemi tekrarlayın. Bu bir döngü olarak adlandırılır.

Her işaretçi hareketi ve takas işleminden sonra, "sol kısım ≤ pivot, sağ kısım ≥ pivot" yapısının bozulmadığı, yani `[left, L) <= pivot` ve `(R, right] >= pivot` değişmezlerinin korunduğu garanti edilir.

Aşağıdaki örnek kodda, `left` ve `right` mevcut işlenen kapalı aralığın sınırlarıdır ve `pivot` aralığın orta noktasındaki elemanı alır.

```cpp
#include <bits/stdc++.h>
using namespace std;

void quickSort(vector<int> &a, int left, int right) {
    if (left >= right) return;
    
    int pivot = a[(left + right) / 2];
    int l = left, r = right;
    
    while (true) {
        while (a[l] < pivot) l++;
        while (a[r] > pivot) r--;
        if (l >= r) break;
        swap(a[l], a[r]);
        l++; r--;
    }
    
    quickSort(a, left, r);
    quickSort(a, r + 1, right);
}

int main() {
    int n; cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    
    quickSort(a, 0, n - 1);
    
    for (int i = 0; i < n; i++) cout << a[i] << " ";
    return 0;
}
```

---

## Karmaşıklık ve `pivot` Seçimi

Hızlı sıralamanın en kötü durumda $O(n^2)$ karmaşıklığına sahip olması nedeniyle, `pivot` seçimi çok önemlidir. Her zaman ilk veya son elemanı seçerseniz, neredeyse sıralı dizilerde büyük olasılıkla en kötü durum ortaya çıkacaktır.

Orta konumdaki elemanı almanın yanı sıra, `pivot` olarak rastgele bir eleman seçebilir veya sol, orta ve sağdaki üç elemanın medyanını `pivot` olarak alabilirsiniz.

---

## Yaygın Hata Örnekleri

Aşağıdaki kod, birkaç yaygın hata içermektedir.

```cpp
#include <bits/stdc++.h>
using namespace std;

void quickSort(vector<int> &a, int left, int right) {
    if (left == right) return; // 7

    int pivot = (left + right) >> 1; // 1
    int l = left, r = right;

    while (true) {
        while (a[l] <= pivot) l++; // 2
        while (a[r] >= pivot) r--; // 2
        swap(a[l], a[r]);
        if (l >= r) break; // 3
        // 4
    }

    quickSort(a, left, l - 1); // 5, 6
    quickSort(a, l, right);    // 5, 6
}

int main() {
    int n; cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    quickSort(a, 0, n - 1);

    for (int i = 0; i < n; i++) cout << a[i] << " ";

    return 0;
}
```

**Hata Analizi:**

1. `pivot` bir dizi elemanı olmalı, indeks değil.
2. `<` ve `>` yerine `<=` ve `>=` kullanmak, sol işaretçinin sağ işaretçiyi birden fazla geçmesine neden olabilir, bu da diziyi ikiye bölmeyi imkansız hale getirir.
3. `l >= r` bulunduktan sonra, takas işlemini yapmadan döngüden hemen çıkılmalıdır. Aksi takdirde, sol taraftaki elemanların `pivot`'tan büyük olmadığı ve sağ taraftaki elemanların `pivot`'tan küçük olmadığı garanti edilemez.
4. Her takastan sonra `l++` ve `r--` yapılmalıdır.
5. `pivot` aslında ortanın solundaki sayıyı alır. Bu nedenle, diziyi $l - 1$ ve $l$ kullanarak bölerseniz, `[1, 2]` dizisi için sonsuz döngüye neden olacağı ve diziyi sürekli olarak 0 ve 2 boyutlarında iki parçaya böleceği kolayca görülebilir. Benzer şekilde, diziyi $r$ ve $l$ kullanarak bölmek de işe yaramaz. Aksine, bir döngü bittiğinde, $r$ kesinlikle $right$'tan küçük olacaktır, bu nedenle diziyi $r$ ve $r+1$ kullanarak bölebilirsiniz. Okuyucular nedenini görmek için algoritma sürecini simüle edebilirler. Sonsuz döngüden kaçınmanın bir başka basit yolu da rastgele bir `pivot` seçmek veya yalnızca iki eleman olduğunda özel işlem yapmaktır.
6. Ayrıca, $l$, $l+1$ kullanmak da işe yaramaz, çünkü bu bölme tanıma uygun değildir. $r$'nin $l$'nin solunda olduğu durumda, $l$, $l+1$ kullanmak diziyi doğru şekilde sol tarafı `pivot`'a eşit veya küçük ve sağ tarafı `pivot`'a eşit veya büyük olacak şekilde ikiye bölemez.
7. Bu problem dizinin boş olmadığını varsayar, bu nedenle `>` durumu yoktur. Ancak, daha güvenli olması için `>=` kullanılması önerilir.

---

## Ek Bilgiler

Hızlı sıralama, $O(n)$ beklenen sürede sıralanmamış bir dizideki $k$'inci en küçük sayıyı bulmak için "hızlı seçim"e de dönüştürülebilir. Temel fikir hızlı sıralamaya benzer, ancak her seferinde yalnızca bir alt aralıkta özyinelemeli olarak devam ederek zaman karmaşıklığını azaltır.