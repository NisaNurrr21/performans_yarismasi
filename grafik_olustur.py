import os
import psutil
import time
import matplotlib.pyplot as plt
from yarisma import naif_dongu, generator_counter

def bellek_olc(fonksiyon, dosya_yolu):
    islem = psutil.Process(os.getpid())
    baslangic = islem.memory_info().rss
    fonksiyon(dosya_yolu)
    bitis = islem.memory_info().rss
    return max(0, (bitis - baslangic) / (1024 * 1024))

# Test edilecek satır sayıları (Örn: 1 Milyon, 2 Milyon, 3 Milyon)
satir_sayilari = [1_000_000, 2_000_000, 3_000_000]
dosya_boyutlari_mb = []
naif_bellek = []
jenerator_bellek = []

dosya_adi = "test_log.txt"
ornek_satir = "192.168.1.1 - - [01/Sep/2026:14:00:00 +0300] \"GET /api/veri HTTP/1.1\" 200 1024\n"

print("Performans testleri başlıyor...")
for satir in satir_sayilari:
    # İlgili boyutta test dosyası oluştur
    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.writelines([ornek_satir] * satir)
    
    boyut_mb = os.path.getsize(dosya_adi) / (1024 * 1024)
    dosya_boyutlari_mb.append(boyut_mb)
    
    # Bellekleri ölç
    print(f"{boyut_mb:.0f} MB dosya test ediliyor...")
    naif_bellek.append(bellek_olc(naif_dongu, dosya_adi))
    jenerator_bellek.append(bellek_olc(generator_counter, dosya_adi))

# Test dosyasını temizle
if os.path.exists(dosya_adi):
    os.remove(dosya_adi)

# Grafiği çiz ve kaydet
plt.figure(figsize=(8, 5))
plt.plot(dosya_boyutlari_mb, naif_bellek, marker='o', label="Naif Döngü (RAM Tüketimi Artar)", color='red')
plt.plot(dosya_boyutlari_mb, jenerator_bellek, marker='s', label="Jeneratör (RAM Tüketimi Sabit)", color='green')
plt.title("Dosya Boyutu vs Bellek Tüketimi")
plt.xlabel("Dosya Boyutu (MB)")
plt.ylabel("Zirve Bellek (MB)")
plt.legend()
plt.grid(True)
plt.savefig("bellek_grafigi.png")
print("Grafik 'bellek_grafigi.png' olarak kaydedildi!")