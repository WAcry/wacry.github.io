---
title: "CAP Teoreminin Derinlemesine Analizi: Yüksek Eşzamanlılık ve Yüksek Erişilebilirlikli Dağıtık Sistemler Oluşturma"
date: 2024-12-27
draft: false
description: "CAP teoreminin dağıtık sistemlerdeki uygulamalarını teoriden pratiğe tartışıyoruz."
summary: "CAP teoreminin dağıtık sistemlerdeki uygulamalarını teoriden pratiğe tartışıyoruz."
tags: [ "Dağıtık Sistemler", "CAP Teoremi", "Sistem Tasarımı", "Tutarlılık Modelleri" ]
categories: [ "Sistem Tasarımı" , "Dağıtık Sistemler" ]
---

## I. CAP Teoremi

### 1.1 CAP Teoremi Nedir?

**CAP teoremi**, Eric Brewer tarafından 2000 yılında ortaya atılmıştır ve temel görüşü şudur:

- **C (Consistency, Tutarlılık)**: Sistemdeki tüm düğümlerin aynı anda gördüğü verilerin aynı olmasıdır. Daha katı bir ifadeyle, bir istemci veri okuduğunda, hangi kopyadan okursa okusun, sonuç en son gönderilen verilerle tutarlı olmalıdır (genellikle güçlü tutarlılık/doğrusal tutarlılık anlamına gelir).
- **A (Availability, Erişilebilirlik)**: Sistem, kısmi arızalar meydana geldiğinde bile normal hizmet sunmaya devam edebilmelidir. Her istek, makul bir süre içinde "geçerli bir yanıt" alabilmelidir (başarılı olmak zorunda değildir, doğru başarısız yanıtları da içerir).
- **P (Partition tolerance, Bölünme Toleransı)**: Sistem, ağ bölünmelerine (düğümler arası iletişimin ulaşılamaz hale gelmesi) dayanabilmelidir. Ağ bölünmesi meydana gelse bile, sistem bir dereceye kadar erişilebilirlik veya tutarlılık sağlayabilmelidir.

Gerçek dağıtık ortamlarda, ağ bölünmeleri kaçınılmazdır, bu nedenle **P** temel olarak "zorunlu bir seçenek" olarak kabul edilir. Ağ bölünmesi meydana geldiğinde, sistem tüm düğümlerin verilerinin **güçlü tutarlılığı** ve **yüksek erişilebilirliği**ni aynı anda sağlayamaz. Bu nedenle, C ve A arasında bir seçim yapmak zorunda kalır ve bu da **CP** ve **AP** olmak üzere iki ana türün ortaya çıkmasına neden olur.

### 1.2 CAP Teoreminin Sınırlamaları

CAP teoreminin kendisinin nispeten üst düzey bir teori olduğunu ve kavramsal rehberlik için kullanıldığını belirtmek gerekir. **"Ya C'yi seç ya da A'yı seç" şeklinde basitçe anlaşılmamalıdır**. Yaygın bazı yanlış anlamalar vardır:

1. **C mutlaka güçlü tutarlılık değildir**
   CAP teoremindeki C genellikle en katı anlamda tutarlılığı (yani doğrusal tutarlılık) ifade eder. Ancak gerçek sistemlerde, zayıf tutarlılık, okunmuş taahhüt (Read Committed), nedensel tutarlılık (Causal Consistency) gibi birçok ince taneli model seçeneğimiz vardır.
2. **Erişilebilirlik 0 veya 1 değildir**
   CP'yi seçmek, erişilebilirliğin tamamen feda edildiği anlamına gelmez; veya AP'yi seçmek, tutarlılığın hiçbir garantisi olmadığı anlamına gelmez. Erişilebilirlik ve tutarlılık, farklı derecelerde ödünleşim alanlarına ve düşürme stratejilerine sahiptir.
3. **Sonunda tutarlılık** CAP'ye aykırı değildir
   Daha yüksek erişilebilirlik ve verim için daha düşük yazma tutarlılığıyla takas edilen ve verileri arka planda eşzamansız olarak bir araya getiren çok yaygın bir uzlaşma çözümüdür.

Bu nedenle, CAP teoremi, çeşitli **tutarlılık modelleri** ve **yüksek erişilebilirlik mimari modelleri** ile belirli senaryolarda birleştirilmelidir, ancak o zaman gerçek uygulama rehberliği değeri üretebilir.

------

## II. Dağıtık Sistemlerin Tutarlılık Modelleri

Tutarlılık modellerinin sınıflandırılması çok zengindir, ancak yaygın ana akım modeller kabaca **güçlü tutarlılık** ve **zayıf tutarlılık** (sonunda tutarlılık, nedensel tutarlılık vb. dahil) olarak ayrılabilir. Bu makale, esas olarak **güçlü tutarlılık** ve **sonunda tutarlılığı** tanıtacak ve bunların CP veya AP modlarındaki yaygın uygulamalarını açıklayacaktır.

### 2.1 Güçlü Tutarlılık

**Güçlü tutarlılık (Strong Consistency)**, aynı zamanda **doğrusal tutarlılık (Linearizability)** olarak da bilinir. Bir yazma işlemi tamamlanıp başarıyla döndüğünde, sonraki tüm okuma işlemlerinin bu güncellenmiş içeriği okuyabilmesi anlamına gelir. Yani, sistem dışarıdan tüm işlemlerin seri olarak yürütüldüğü gibi davranır.

- **Yaygın Uygulamalar**: Eşzamanlı çoğaltmaya ve bir hakem (çoğunluk) mekanizmasına dayanır. Protokoller (Paxos/Raft gibi) aracılığıyla sistemde yalnızca geçerli bir liderin (Leader) olmasını sağlar. Tüm işlemler, günlüğe sırayla yazılır ve çoğunluk düğümüne kopyalanır.
- Avantajları ve Dezavantajları:
    - Avantajları: En katı veri doğruluğunu garanti eder, herhangi bir zamanda okunan verilerde "geri dönüş" olmaz.
    - Dezavantajları: Ağ dalgalanmaları, bölünmeler veya lider arızaları durumunda, tutarlılığı korumak için genellikle yazma işlemlerini engeller, bu da genel erişilebilirliğin düşmesine neden olur; performans ve verim de nispeten düşüktür.

### 2.2 Sonunda Tutarlılık

**Sonunda tutarlılık (Eventual Consistency)**, zayıf tutarlılığın tipik bir biçimidir. Yalnızca sistemde artık yeni güncelleme işlemleri yoksa, zamanla tüm kopyaların verilerinin kademeli olarak aynı duruma yakınsaması gerektiğini gerektirir. Bu süre zarfında, kullanıcılar kopya verilerini okurken eski değerler görebilir, ancak sonunda tutarlı hale gelir.

- **Yaygın Uygulamalar**: Gossip protokolü, çoklu kopya eşzamansız çoğaltma, CRDT (Çakışmasız Çoğaltılmış Veri Türü) vb.
- Avantajları ve Dezavantajları:
    - Avantajları: Yüksek erişilebilirlik, yüksek verim, düşük yazma işlemi gecikmesi, ağ bölünmelerine karşı yüksek tolerans.
    - Dezavantajları: Kısa süreli veri tutarsızlığına tolerans göstermesi gerekir, uygulama mantığı daha karmaşıktır, çakışma tespiti ve birleştirme yapılması gerekebilir.

------

## III. Yaygın Tutarlılık Protokolleri ve Algoritmaları

Dağıtık sistem kopyalarının tutarlı kalmasını sağlamak için sektörde birçok klasik algoritma ve protokol önerilmiştir. Aşağıda birkaç tanesi kısaca tanıtılmaktadır:

### 3.1 Paxos

Paxos, Leslie Lamport tarafından 1990'larda önerilen ve esas olarak güçlü tutarlılık veya doğrusal tutarlılık uygulamak için kullanılan bir dağıtık tutarlılık algoritmasıdır.

- **Temel İlke**: Bir işlemin veya değerin çoğunluk düğümü tarafından kabul edilip edilmediğine karar vermek için rol bölümü (Önerici Proposer, Kabul Edici Acceptor, Öğrenici Learner) aracılığıyla çok turlu oylama yapılır.
- Avantajları ve Dezavantajları:
    - Avantajları: Ağ bölünmeleri ve düğüm arızaları altında bile tutarlılığa ulaşabilir, yüksek güvenlik sağlar.
    - Dezavantajları: Uygulaması karmaşıktır, hata ayıklama ve sorun giderme zordur, çok turlu oylama performansı sınırlar. Endüstride genellikle varyantları (Multi-Paxos vb.) kullanılır.

### 3.2 Raft

Raft, 2013 yılında resmi olarak önerilmiştir ve amacı, **Paxos ile aynı güvenlik seviyesini sağlarken, uygulama ve anlama zorluğunu basitleştirmektir**. Kararlı bir **lider (Leader)** rolü oluşturarak, günlük çoğaltma ve arıza kurtarmayı merkezi olarak gerçekleştirir:

- **Temel Aşamalar**: Lider Seçimi (Leader Election), Günlük Çoğaltma (Log Replication), Güvenlik (Safety) vb.
- **Yaygın Uygulamalar**: Etcd, Consul, TiKV, LogCabin vb. güçlü tutarlı çoğaltmayı uygulamak için Raft'ı temel alır.
- Avantajları ve Dezavantajları:
    - Avantajları: Anlaşılması nispeten kolaydır, daha az kod satırı gerektirir; küçük ve orta ölçekli kümeler için performansı iyidir.
    - Dezavantajları: Ana düğüme (Lider) bağımlıdır, ana düğüm arızası veya bölünmesi kısa süreli yazma engellemesine neden olur; büyük ölçekli kümelerde veya coğrafi olarak dağıtılmış dağıtımlarda gecikme ve erişilebilirlik etkilenecektir.

### 3.3 Gossip Protokolü

Gossip (dedikodu) protokolü, geleneksel bir fikir birliği protokolü değildir. Esas olarak, merkezi olmayan senaryolarda, düğümlerin rastgele etkileşimi yoluyla meta verileri veya durum bilgilerini değiştirmek ve böylece tüm ağda yayılma ve yakınsama sağlamak için kullanılır.

- **Özellikler**: Merkezi olmayan, düşük maliyetli, düğümler arasında periyodik ve rastgele mesaj alışverişi.
- **Yaygın Uygulamalar**: Cassandra, Riak, dağıtık üye yönetimi (Serf gibi) vb., sonunda tutarlılık, kopya durumu senkronizasyonu vb. uygulamak için kullanılır.
- Avantajları ve Dezavantajları:
    - Avantajları: Ölçeklenebilirliği iyidir, uygulaması kolaydır, tutarlılık gereksinimlerinin yüksek olmadığı, ölçeklenebilirlik gereksinimlerinin yüksek olduğu senaryolar için uygundur.
    - Dezavantajları: Tutarlılık garantisi zayıftır, çakışmaları nihai olarak çözmek için daha üst düzey çakışma işleme yöntemleri (CRDT, sürüm numarası birleştirme vb.) gerektirir.

### 3.4 2PC / 3PC

Dağıtık işlem senaryolarında, yaygın taahhüt protokolleri **2PC (İki Aşamalı Taahhüt)** ve **3PC (Üç Aşamalı Taahhüt)**'dir:

- **2PC**: Koordinatör, tüm katılımcılara "ön taahhüt (prepare)" bildirimi gönderir, hepsi başarılı olursa "taahhüt (commit)" yayınlar, aksi takdirde "geri alma (abort)" yayınlar.
- **3PC**: 2PC'ye ek olarak bir aşama ekler, tek nokta arızasının neden olduğu engellemeyi azaltır, ancak uygulaması daha karmaşıktır ve hala aşırı ağ bölünmesi veya arıza senaryolarında kullanılamazlık sorunları vardır.
- Avantajları ve Dezavantajları:
    - Avantajları: Anlaşılması kolaydır, işlem anlamı açıktır, dağıtık veritabanlarında, mesaj kuyruklarında vb. yaygın olarak kullanılır.
    - Dezavantajları: Koordinatöre güçlü bir bağımlılığı vardır, engelleme riski vardır; ağda uzun süreli bölünme olduğunda işlemleri ilerletemeyebilir.

------

## IV. CAP'in İki Ana Akım Seçeneği: CP ve AP

**P**'nin "zorunlu" bir özellik olduğunu kabul ettiğimizde, dağıtık sistemler ağ bölünmesi sırasında hizmet sunmaya devam etmek istiyorsa, **C** ve **A** arasında bir seçim yapmalıdır. Yaygın sistem tasarımları bu nedenle **CP** ve **AP** olmak üzere iki ana kampa ayrılır.

### 4.1 CP Sistemi

**CP (Tutarlılık + Bölünme Toleransı)**: Ağ bölünmesiyle karşılaşıldığında, sistem **öncelikle tutarlılığı garanti etmeyi** seçer ve gerektiğinde **erişilebilirliği feda eder**.

- Tipik Uygulamalar:
    - Çoğunluk fikir birliği (Paxos, Raft vb.), yazmaya izin vermek için düğümlerin yarısından fazlasının hayatta kalması ve fikir birliğine varması gerekir.
    - Mevcut durumda quorum (yasal çoğunluk) sağlanamazsa veya ana düğüm arızalanırsa, sistem beyin bölünmesinin neden olduğu veri tutarsızlığını önlemek için yazma işlemlerini engeller veya reddeder.
- Yaygın Uygulamalar:
    - Zookeeper, Etcd, Consul, dağıtık kilit hizmetleri, dağıtık meta veri yönetimi vb.
    - Finansal işlem çekirdek süreçleri, banka muhasebe sistemleri gibi yüksek tutarlılık gerektiren senaryolar.
- Özellikler:
    - Katı veri garantisine sahiptir: Çift ana veya veri karışıklığı olmaktansa kapanmayı tercih eder.
    - Belirli bir erişilebilirliği feda eder: Ağ bölünmesi veya arıza geçişi meydana geldiğinde, bir süre hizmet kullanılamaz veya yazma işlemlerini reddeder.

### 4.2 AP Sistemi

**AP (Erişilebilirlik + Bölünme Toleransı)**: Ağ bölünmesiyle karşılaşıldığında, sistem **öncelikle erişilebilirliği garanti etmeyi** seçer ve aynı zamanda **tutarlılığı gevşetir**.

- Tipik Uygulamalar:
    - Sonunda tutarlılık, çoklu ana çoğaltma, Gossip protokolü, Dynamo tarzı ayarlanabilir tutarlılık stratejileri vb.
- Yaygın Uygulamalar:
    - NoSQL veritabanları (Cassandra, Riak, DynamoDB vb.), dağıtık önbellek sistemleri (Redis Cluster) vb.
    - Sosyal ağlar, günlük toplama, öneri sistemleri gibi yüksek erişilebilirlik, yüksek verim ve veri tutarlılığı gereksinimlerinin nispeten esnek olduğu işler.
- Özellikler:
    - Bölünme olsa bile, tüm düğümler okuma ve yazma isteklerini almaya devam eder ve sistemin "mümkün olduğunca kullanılabilir" olmasını sağlar.
    - Verilerde kısa süreli tutarsızlıklar olabilir, ancak arka planda eşzamansız senkronizasyon, çakışma birleştirme vb. yöntemlerle kademeli olarak yakınsar.

------

## V. CP ve AP Arasında Nasıl Seçim Yapılır?

Gerçek büyük ölçekli dağıtık sistemlerde, genellikle **tek bir modele güvenmek yerine**, farklı veri veya iş senaryoları için katmanlı işlem yapılır, böylece **tutarlılık** ve **erişilebilirlik** arasında en iyi denge sağlanır.

1. **Çekirdek Veriler için CP'yi Seçin**
    - Kullanıcı hesap bakiyeleri, sipariş ödemeleri, finansal işlem akışları vb. gibi tutarlılık gereksinimleri çok yüksektir.
    - Ağ dalgalanmalarının neden olduğu kısa süreli yazılamazlığı tolere eder, ancak bakiye veya işlem tutarlarındaki hataları tolere edemez.
2. **Kenar veya Önbellek Verileri için AP'yi Seçin**
    - Ürün detay sayfalarının önbelleği, kullanıcı davranış günlükleri, öneri aday listeleri vb. gibi tutarlılık gereksinimleri düşüktür.
    - Yüksek eşzamanlılığa, yüksek erişilebilirliğe daha çok önem verir, belirli bir süre gecikmeli güncellemeyi veya kirli okumayı tolere edebilir.

Birçok internet şirketi **karma mimari** kullanır: Çekirdek işlem süreçleri CP tarzı depolama (dağıtık ilişkisel veritabanları veya güçlü tutarlılığa sahip dağıtık depolama gibi) kullanır; dış işler veya "çok okuma az yazma" senaryoları AP tarzı depolama veya önbellek çözümleri kullanır.

------

## VI. CP ve AP Yüksek Eşzamanlılık ve Sonunda Tutarlılık Nasıl Uygulanır?

### 6.1 CP Sistemleri Yüksek Eşzamanlılıkla Nasıl Başa Çıkar?

Fikir birliği protokolleri, tek bir küme düğüm ölçeğinde ve büyük yazma isteği hacminde yüksek gecikme ve düşük verimle karşılaşsa da, eşzamanlılığı ve ölçeklenebilirliği aşağıdaki yöntemlerle artırabilir:

1. Toplu Okuma ve Yazma
    - Birden çok yazma işlemini istemcide veya ara katmanda paketleyerek, lider düğüme tek seferde yazarak ağ gidiş gelişlerini ve protokol turlarını azaltır.
2. Veritabanı Bölme ve Tablo Bölme & Çoklu Küme
    - Verileri mantıksal veya karma yoluyla birden çok kümeye (parçalama) böler, her küme içinde hala CP protokolü çalışır; istekler yönlendirme veya proxy katmanı aracılığıyla farklı parçalara dağıtılır.
    - Genel eşzamanlılık yeteneğini artırır ve arıza etkisini tek bir parça aralığıyla sınırlar.

> CP sistemlerinin tek parça küme verimi genellikle AP sistemlerinden 2 ila 10 kat daha düşüktür.

### 6.2 AP Sistemleri Sonunda Tutarlılığı Nasıl Garanti Eder?

AP sistemleri genellikle yüksek yazma verimi ve okuma erişilebilirliği sağlayabilir, ancak tutarlılığı gevşetir, bu nedenle arka planda veya iş mantığı katmanında tutarlılık yakınsama garantisi uygulaması gerekir:

1. Sürüm Numarası (Vektör Saati) veya Mantıksal Zaman Damgası
    - Her güncelleme işlemine bir sürüm numarası (veya Lamport Saati / Hibrit Saat tabanlı) atar, çakışma senaryolarında birleştirme veya zaman damgası tabanlı kazanma stratejisi (Son Yazma Kazanır) uygular.
2. Gossip Protokolü / Anti-entropi Mekanizması
    - Düğümler periyodik olarak en son verileri veya meta verileri değiştirir, çakışma bulursa birleştirir.
3. Ayarlanabilir Tutarlılık Stratejisi
    - Dynamo modeliyle temsil edilir, istemci `R`, `W` gibi parametreleri (çoğunluğa yazma, kopya onayı gibi) yapılandırabilir, böylece tutarlılık ve erişilebilirlik arasında esnek bir şekilde ayar yapabilir.
4. Özel Çakışma Çözme Stratejisi
    - İş anlamıyla birleştirme yapar, örneğin alışveriş sepeti "birleşim" ile birleştirilir, sayaçlar CRDT (G-sayaç, PN-sayaç vb.) ile verilerin monotonluğunu garanti eder.

------

## VII. CP'nin Parçalar Arası Güçlü Tutarlılık Uygulaması

VII. bölümde belirtildiği gibi, **veritabanı bölme ve tablo bölme (Sharding)**, tek bir CP kümesinin basıncını birden çok alt kümeye "bölerek" daha yüksek eşzamanlılığı desteklemesini sağlayabilir. Ancak, işin parçalar arası işlem yürütmesi gerektiğinde (yani birden çok veritabanı veya tablo güncellemesi içerdiğinde), hala **çoklu parça tutarlılığı** zorluğuyla karşı karşıyayız. Genellikle aşağıdaki fikirler vardır:

1. **Dağıtık İşlemler: 2PC / 3PC**
    - Uygulamanın birden çok parça arasında atomik güncelleme yapması gerekiyorsa, genellikle her parçanın taahhüdünü veya geri almasını koordine etmek için dağıtık işlem protokolleri (2PC, 3PC gibi) kullanılır.
    - Sorunlar ve Çözümler:
        - 2PC/3PC'nin her ikisi de tek bir koordinatör düğümüne bağlıdır ve tek nokta darboğazı haline gelebilir.
        - Ağ bölünmesinin ciddi olduğu veya koordinatörün arızalandığı aşırı durumlarda, engelleme meydana gelebilir.
        - Genellikle ana-yedek geçişi, kalp atışı algılama ve zaman aşımı mekanizması, idempotent yeniden deneme, MVCC vb. ile engelleme etkisini ve veri tutarsızlığı riskini azaltır.
2. **Hücre Tabanlı Mimari**
    - İşi birden çok özerk birime böler, her birimdeki veriler aynı parça kümesindedir, çoğu işlemin yalnızca tek bir birimde tamamlanmasını sağlar ve parça arası işlemleri azaltır.
    - Birim sınırında eşzamansız veya sonunda tutarlılık mekanizması kullanarak veri alışverişi yapar, genel yüksek erişilebilirliği ve tutarlılığı dengeler.
3. **Küresel Dağıtık Veritabanı + Küresel Fikir Birliği Protokolü**
    - Örneğin, Google Spanner, her parçada (Shard) Paxos aracılığıyla kopya güçlü tutarlı çoğaltma uygular ve ardından TrueTime API'sini kullanarak parça arası tutarlılığı sağlamak için küresel zaman damgaları sağlar.
    - Bu çözümün uygulama karmaşıklığı çok yüksektir, ancak küresel ölçekte güçlü tutarlılığa yakın dağıtık işlem yeteneği sağlayabilir.

> **Özet**: Güçlü tutarlılık gerektiren parçalar arası işlemler için, **2PC/3PC + koordinatör** hala yaygın bir çözümdür ve koordinatörün yüksek erişilebilirliğini mümkün olduğunca artırarak arıza olasılığını azaltır. Ancak, mühendislik uygulamasında parça arası yazma işlemlerini en aza indirmek veya birimleştirme fikriyle çoğu işlemi tek bir parça aralığıyla sınırlayarak sistem karmaşıklığını azaltmak gerekir.

------

## VIII. Ünlü Vaka Tartışmaları

Aşağıda, sektörde sıkça bahsedilen birkaç dağıtık sistemi kısaca tartışalım ve bunların CAP'deki ödünleşimlerini ve uygulama yöntemlerini görelim:

1. **Google Spanner**
    - Tipik bir **CP** sistemidir (hatta dış dünyanın sıkça bahsettiği "CA" yanılsamasını bile yapabilir, ancak özünde hala bir miktar erişilebilirliği feda etmesi gerekir).
    - TrueTime tarafından sağlanan harici kesin zaman damgalarını + her parça içindeki Paxos çoğaltmasını kullanarak, veri merkezleri arası güçlü tutarlılığı garanti eder.
    - Küresel finansal işlemler veya yüksek tutarlılık gerektiren senaryolar için uygundur, ancak altyapı maliyeti çok yüksektir.
2. **BigTable / HBase**
    - Yüzeyde **CP**'ye daha yatkındır, RegionServer ve Master arasında meta verilerin tutarlılığını sağlamak için dağıtık koordinasyon kullanır.
    - Ancak gerçek okuma ve yazma yollarında, çoklu kopya eşzamansız çoğaltma yoluyla belirli bir yüksek erişilebilirlik aracı da sağlayabilir ve okuma tutarlılığı uygulama gereksinimlerine göre ayarlanabilir.
3. **AWS DynamoDB**
    - **AP**'ye eğilimlidir, erken tasarım ilhamı Dynamo makalesinden alınmıştır ve `R`, `W` gibi parametrelerle tutarlılık seviyesini ayarlayabilir.
    - Varsayılan modda son derece yüksek erişilebilirlik ve sonunda tutarlılık sağlar, ayrıca "güçlü tutarlı okuma" da açılabilir (ancak yalnızca tek bir parça için güçlü tutarlılığı garanti eder, parça arası olmayabilir).
4. **Cassandra**
    - Aynı şekilde **AP** eğilimlidir, altta yatan Gossip protokolü düğüm topoloji durumunu korur.
    - Okuma ve yazma tutarlılığı, sonunda tutarlılıktan daha güçlü tutarlılığa yumuşak bir geçiş sağlamak için okuma ve yazma kopya sayısı `R` / `W` ile yapılandırılabilir.

> **Karşılaştırmadan görülebilir**: Mühendislikte mutlak "AP veya CP" yoktur, daha çok çeşitli tutarlılık stratejilerinin bir karışımıdır; çoğu sistem, farklı uygulama senaryolarına uyum sağlamak için belirli bir ölçüde ayarlanabilir tutarlılık sağlar.

------

## IX. Özet

1. **CAP Teoremi Tek Bir Çözüm Değildir**
    - Gerçek dağıtık sistemler basitçe "C'yi seçiyorum, A'dan vazgeçiyorum" veya "A'yı seçiyorum, C'den vazgeçiyorum" diyemez.
    - Sektörde daha yaygın olan, farklı veri boyutları, farklı işlem türleri için esnek bir şekilde **CP** veya **AP** modunu seçmek, hatta aynı sistem içinde farklı tablolar/farklı işlevler için farklı hata toleransı ve tutarlılık stratejileri kullanmaktır.
2. **AP Mutlak %100 Kullanılabilir Değildir**
    - Örneğin, Cassandra, DynamoDB vb. aşırı ağ bölünmesi veya düğümlerin büyük bir bölümünün arızalanması durumunda, istekleri karşılayamama durumu da ortaya çıkabilir.
    - AP sistemleri yalnızca tasarımda "kopya yazılabilir olduğu sürece önce yaz" eğilimindedir ve nispeten daha yüksek erişilebilirlik ve verim karşılığında bir miktar tutarlılık garantisini feda eder.
3. **CP de Mümkün Olduğunca Yüksek Erişilebilirliğe Ulaşabilir**
    - Paxos/Raft normal koşullar altında %99,99 veya daha yüksek erişilebilirlik sağlayabilir, ancak daha fazla ağ, donanım ve mühendislik maliyeti gerektirir ve aşırı ağ bölünmesi durumunda yazmayı engelleme, tutarlılığı korumak için erişilebilirliği feda etme durumu hala ortaya çıkacaktır.
4. **Karma Mimari Ana Akımdır**
    - Çekirdek işlem senaryoları güçlü tutarlılık (CP) gerektirir, dış yardımcı senaryolar veya önbellek kanalları zayıf tutarlılık (AP) kullanır ve ikisi birbirini tamamlar.
    - İş toleransı, ağ ortamı, maliyet yatırımı, ekip teknik rezervi ile birlikte kapsamlı bir şekilde değerlendirilmelidir.

CAP teoremi, dağıtık sistemlerin tasarımı için üst düzey bir düşünce çerçevesi sağlar ve ağ bölünmesi gibi kaçınılmaz bir gerçeklik karşısında rasyonel kararlar almamıza yardımcı olur. Gerçek sistemlerde, daha zengin **tutarlılık modelleri**, **fikir birliği protokolleri**, **çoklu kopya çoğaltma mekanizmaları** ve mühendislik uygulamaları (felaket kurtarma, düşürme, idempotent, çakışma birleştirme vb.) aracılığıyla tutarlılık ve erişilebilirliği dengelemek gerekir.