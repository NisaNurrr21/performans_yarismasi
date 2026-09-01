# Log İşleme Performans Yarışması (Ödev 3)

Bu proje, 1 GB boyutundaki devasa bir log dosyasında HTTP durum kodlarının sayım (agregasyon) işleminin 4 farklı algoritma ile test edildiği bir performans ölçüm (profiling) çalışmasıdır.

## Performans Karşılaştırması

| Yöntem | İşlem Süresi (Saniye) | Zirve RAM (MB) | Darboğaz (Bottleneck) |
| :--- | :--- | :--- | :--- |
| Naif Döngü | 21.82 | 1654.25 | CPU (Tek Çekirdek) ve Yüksek Bellek |
| Jeneratör + Counter | 20.83 | 0.15 | CPU (Tek Çekirdek) |
| Multiprocessing Chunk | 4.77 | 28.14 | Disk I/O Okuma Hızı |
| Polars | 0.22 | 0.02 | Yok (Donanım Sınırında) |

## Mimari Farkların Nedenleri

* **Naif Döngü (`readlines`):** 1 GB'lık dosyayı tek seferde belleğe alarak listeye çevirir. Yüksek RAM tüketir (1.65 GB) ve Python'daki obje yaratma maliyetleri yüzünden yavaştır.
* **Jeneratör ve Counter:** Veriyi satır satır akıtarak (streaming) RAM tüketimini 0.15 MB'a düşürür. Ancak Python'un Global Interpreter Lock (GIL) kısıtlaması nedeniyle tek çekirdekte çalıştığı için süre naif döngüyle aynı kalır.
* **Multiprocessing (Paralel İşleme):** Veriyi 100.000 satırlık bloklara (chunks) bölüp farklı fiziksel işlemci çekirdeklerine dağıtır. GIL kısıtlamasını aşarak süreyi 4.77 saniyeye indirir.
* **Polars (Rust Gücü):** Rust tabanlı motoru ve Apache Arrow bellek yapısıyla Python'un hantal obje mimarisinden tamamen kaçınır. Çoklu çekirdeği alt seviyede otomatik kullanarak 0.22 saniye gibi benzersiz bir hız ve sıfıra yakın bellek tüketimi (0.02 MB) sunar.