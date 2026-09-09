# Log İşleme Performans Yarışması (Ödev 3)

Bu proje, 1 GB boyutundaki bir log dosyasında HTTP durum kodlarının sayım (agregasyon) işleminin 4 farklı algoritma ile test edildiği bir performans ölçüm (profiling) çalışmasıdır. Hatalı sonuçlar üreten yüzeysel araçlar yerine işletim sistemi seviyesinde (OS-level) RAM ölçümü yapılmıştır.

## Performans Karşılaştırması

| Yöntem | İşlem Süresi (Saniye) | Bellek Farkı (MB) | Karakteristik / Darboğaz |
| :--- | :--- | :--- | :--- |
| Naif Döngü | 3.29 | 105.84 | Yüksek Bellek, Python Obje Maliyeti |
| Jeneratör + Counter | 3.03 | 0.00 | Sabit (O(1)) RAM, GIL Kısıtlaması |
| Multiprocessing Chunk | 2.04 | 43.41 | Çoklu Çekirdek, Worker İletişim Yükü |
| Polars (Rust Gücü) | 0.23 | 271.92 | Benzersiz Hız, Native RAM Tüketimi |

## Mimari Farkların Nedenleri

* **Naif Döngü (`readlines`):** 1 GB'lık veriyi ve metin parçalarını büyük listelerde tutmaya çalışır. Python'un obje (string vb.) yaratma ve çöp toplama (garbage collection) maliyetleri yüzünden verimsizdir.
* **Jeneratör ve Counter:** Veriyi satır satır akıtarak (streaming) bellek tüketimini tamamen sabit (0.00 MB fark) tutar. Ancak Python'un Global Interpreter Lock (GIL) kısıtlaması nedeniyle tek çekirdekte çalıştığı için işlem süresi naif yönteme yakındır.
* **Multiprocessing (Paralel İşleme):** Veriyi 100.000 satırlık bloklara (chunks) bölüp farklı fiziksel işlemci çekirdeklerine dağıtır. GIL darboğazını aşarak süreyi 2.04 saniyeye indirir ancak işçiler (workers) arası serileştirme/kopyalama süreçleri fazladan bellek harcar.
* **Polars:** Rust tabanlı motoru ve Apache Arrow bellek yapısıyla Python'un hantal obje mimarisinden tamamen kaçınır. Çoklu çekirdeği alt seviyede otomatik kullanarak 0.23 saniye gibi muazzam bir hız sunar; ancak vektörel işlemler için veriyi native (C/C++) yığınında belleğe çıkardığından en yüksek RAM tüketimine sahiptir.