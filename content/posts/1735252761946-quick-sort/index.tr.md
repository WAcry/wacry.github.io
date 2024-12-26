---
title: "Hızlı Sıralama"
date: 2024-12-26
draft: false
description: "Hızlı sıralama algoritmasının doğru bir şekilde uygulanmasının önemli noktalarının analizi."
summary: "Hızlı sıralama algoritmasının doğru bir şekilde uygulanmasının önemli noktalarının analizi."
tags: [ "Algoritma", "Sıralama Algoritması", "Hızlı Sıralama", "Böl ve Fethet Algoritması" ]
categories: [ "Algoritmalar ve Veri Yapıları" ]
---

# Hızlı Sıralama

Hızlı sıralama, karşılaştırmaya dayalı, kararlı olmayan bir sıralama algoritmasıdır. Böl ve fethet ilkesini kullanır. Ortalama zaman karmaşıklığı $O(n\log n)$'dir, en kötü durumdaki karmaşıklığı ise $O(n^2)$'dir. Alan karmaşıklığı $O(1)$'dir. Aşağıda, bir tam sayı dizisini küçükten büyüğe sıralama örneği verilerek, algoritmanın uygulama detayları ve yaygın hataları tanıtılmaktadır.

---

## Problem Tanımı

$n$ uzunluğunda bir tam sayı dizisi veriliyor. Hızlı sıralama algoritmasını kullanarak diziyi küçükten büyüğe sıralayın ve sonucu çıktı olarak verin.

### Giriş Formatı

- İlk satırda tam sayı $n$ girilir.
- İkinci satırda $[1,10^9]$ aralığında $n$ adet tam sayı girilir.

### Çıkış Formatı

- Sıralanmış diziyi tek bir satırda çıktı olarak verin.

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

## Hızlı Sıralama Yaklaşımı

Hızlı sıralama, her bölme aşamasında bir pivot (temel) sayı seçer (aşağıdaki örnekte orta konumdaki sayı seçilmiştir).

Sol ve sağ işaretçiler kullanarak birbirine doğru ilerleyin. Sol işaretçi `L` soldan sağa doğru `pivot` sayısından büyük veya eşit olan ilk sayıyı arar, sağ işaretçi `R` ise sağdan sola doğru `pivot` sayısından küçük veya eşit olan ilk sayıyı arar ve ardından bu iki sayıyı yer değiştirir.

Sol işaretçi sağ işaretçiyi geçene veya sol işaretçi sağ işaretçiden bir birim daha büyük olana kadar bu süreç tekrarlanır. Bu işleme bir döngü denir.

Her işaretçi hareketinden ve takastan sonra, "sol kısım ≤ pivot, sağ kısım ≥ pivot" yapısının bozulmaması sağlanır. Yani değişmezler `[left, L) <= pivot` ve `(R, right] >= pivot` vardır.

Aşağıdaki örnek kodda, `left` ve `right` şu anda işlenen kapalı aralığın sınırlarıdır ve `pivot` aralığın orta noktasındaki elemanı alır.

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

Hızlı sıralamanın en kötü durumdaki karmaşıklığı $O(n^2)$ olduğundan, `pivot` seçimi çok önemlidir. Her zaman ilk veya son elemanı seçmek, neredeyse sıralı dizilerde büyük olasılıkla en kötü durumun ortaya çıkmasına neden olacaktır.

Orta konumdaki elemanı almak dışında, rastgele bir elemanı `pivot` olarak seçmek veya sol, orta ve sağ elemanların medyanını `pivot` olarak almak da mümkündür.

---

## Yaygın Hata Örnekleri

Aşağıdaki kod birkaç yaygın hata içermektedir.

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

1. `pivot` bir dizi elemanı olmalıdır, indeks değil.
2. `<` ve `>` yerine `<=` ve `>=` kullanıldığında, sol işaretçi sağ işaretçiden bir birimden fazla geçebilir, bu da diziyi iki parçaya bölmeyi imkansız kılar.
3. `l >= r` durumu bulunduktan sonra döngüden hemen çıkılmalıdır ve takas yapılmamalıdır. Aksi takdirde, sol kısımdaki elemanların `pivot`tan büyük olmaması ve sağ kısımdaki elemanların `pivot`tan küçük olmaması garanti edilemez.
4. Her takastan sonra `l++` ve `r--` yapılmalıdır.
5. `pivot` aslında ortanın solunda kalan bir sayı olarak alınır. Eğer diziyi $l - 1$ ve $l$ kullanarak bölerseniz, `[1, 2]` dizisinde sonsuz döngü oluştuğunu göreceksiniz ve dizi sürekli olarak 0 ve 2 boyutlu parçalara ayrılacaktır. Bunun aksine, döngü bittiğinde $r$, $right$tan kesinlikle küçük olacaktır. Bu nedenle diziyi $r$ ve $r+1$ kullanarak bölmek mümkündür. Okuyucular, neden olduğunu görmek için algoritma sürecini simüle edebilirler. Sonsuz döngüden kaçınmanın bir başka basit yolu da rastgele bir `pivot` seçmek veya sadece iki eleman olduğu durumları özel olarak ele almaktır. Benzer şekilde, diziyi $r$ ve $l$ ile bölmek de çalışmaz.
6. Ayrıca, $l$, $l+1$ kullanmak da işe yaramaz, çünkü bu bölme tanıma uygun değildir. $r$'nin $l$'nin solunda olduğu durumda, $l$, $l+1$ kullanmak diziyi doğru bir şekilde sol taraf `pivot`tan küçük veya eşit, sağ taraf `pivot`tan büyük veya eşit olacak şekilde iki parçaya ayıramaz.
7. Bu soruda dizinin boş olmadığı varsayılmaktadır, bu nedenle `>` durumu mevcut değildir. Ancak `>=`, kullanılması daha güvenlidir.

---

## Ek Bilgiler

Hızlı sıralama, "hızlı seçim"e de dönüştürülebilir. $O(n)$ beklenen sürede sıralanmamış bir dizideki $k$'inci en küçük sayıyı bulmak için hızlı sıralamaya benzer bir fikir kullanılır, ancak her seferinde sadece bir alt aralıkta yineleme yapılmasıyla zaman karmaşıklığı düşürülür.