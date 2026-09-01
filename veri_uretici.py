import os
import random

def log_dosyasi_uret(dosya_adi: str = "buyuk_log.txt", hedef_gb: float = 1.0):
    hedef_byte = int(hedef_gb * 1024 * 1024 * 1024)
    durum_kodlari = ["200", "302", "404", "403", "500"]
    agirliklar = [0.70, 0.10, 0.10, 0.05, 0.05] # %70 ihtimalle 200 dönecek
    
    # Yazma işlemini hızlandırmak için 10.000 satırlık bir blok hazırlıyoruz
    ornek_satirlar = []
    for _ in range(10_000):
        kod = random.choices(durum_kodlari, weights=agirliklar)[0]
        ip = f"192.168.1.{random.randint(1, 255)}"
        # Standart web sunucusu log formatı
        satir = f"{ip} - - [01/Sep/2026:14:00:00 +0300] \"GET /api/veri HTTP/1.1\" {kod} {random.randint(100, 5000)}\n"
        ornek_satirlar.append(satir)
        
    blok_verisi = "".join(ornek_satirlar).encode("utf-8")
    blok_boyutu = len(blok_verisi)
    
    print(f"'{dosya_adi}' oluşturuluyor... (Hedef: {hedef_gb} GB)")
    
    # Dosya 1 GB olana kadar hazırladığımız bloğu art arda yazıyoruz
    yazilan_byte = 0
    with open(dosya_adi, "wb") as dosya:
        while yazilan_byte < hedef_byte:
            dosya.write(blok_verisi)
            yazilan_byte += blok_boyutu
            
    print(f"İşlem tamam! Dosya boyutu: {yazilan_byte / (1024**3):.2f} GB")

if __name__ == "__main__":
    log_dosyasi_uret()