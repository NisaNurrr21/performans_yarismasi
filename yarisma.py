import os
import psutil
import time
import multiprocessing as mp
import polars as pl
from collections import Counter
from functools import wraps

# 1. HAKEM (Profiler Decorator)
def profil_olcer(fonksiyon):
    @wraps(fonksiyon)
    def sarmalayici(*args, **kwargs):
        islem = psutil.Process(os.getpid())
        
        # Çalışma öncesi bellek (RSS - Resident Set Size)
        baslangic_bellek = islem.memory_info().rss
        baslangic_zaman = time.perf_counter()
        
        sonuc = fonksiyon(*args, **kwargs)
        
        bitis_zaman = time.perf_counter()
        bitis_bellek = islem.memory_info().rss
        
        sure = bitis_zaman - baslangic_zaman
        # Harcanan net bellek miktarını MB cinsinden hesaplıyoruz
        zirve_mb = max(0, (bitis_bellek - baslangic_bellek) / (1024 * 1024))
        
        print(f"[{fonksiyon.__name__.upper()}]")
        print(f"Süre: {sure:.2f} saniye")
        print(f"Bellek Farkı: {zirve_mb:.2f} MB")
        print(f"Sonuç: {sonuc}\n" + "-"*40)
        return sonuc
    return sarmalayici

# 2. YARIŞMACI 1: Naif Yaklaşım (Tüm dosyayı belleğe al)
@profil_olcer
def naif_dongu(dosya_yolu: str):
    durum_kodlari = {}
    
    # readlines() dosyayı tek seferde okuyup devasa bir liste oluşturur
    with open(dosya_yolu, "r", encoding="utf-8") as f:
        tum_satirlar = f.readlines()
        
    for satir in tum_satirlar:
        parcalar = satir.split()
        if len(parcalar) > 2:
            kod = parcalar[-2]
            durum_kodlari[kod] = durum_kodlari.get(kod, 0) + 1
            
    return durum_kodlari

# 3. YARIŞMACI 2: Jeneratör ve Counter (Satır satır akıt)
@profil_olcer
def generator_counter(dosya_yolu: str):
    def satir_uretici():
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            for satir in f:
                parcalar = satir.split()
                if len(parcalar) > 2:
                    yield parcalar[-2]
                    
    # Counter, jeneratörden gelen veriyi bellekte biriktirmeden sayar
    return dict(Counter(satir_uretici()))

# İşçi fonksiyonu (multiprocessing için en üst seviyede tanımlanmalı)
def isci_fonksiyon(satirlar):
    sayac = Counter()
    for satir in satirlar:
        parcalar = satir.split()
        if len(parcalar) > 2:
            sayac[parcalar[-2]] += 1
    return sayac

# 4. YARIŞMACI 3: Multiprocessing (Paralel İşleme)
@profil_olcer
def multiprocessing_chunk(dosya_yolu: str, chunk_boyutu: int = 100_000):
    cekirdek_sayisi = mp.cpu_count()
    
    def chunk_uretici():
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            chunk = []
            for satir in f:
                chunk.append(satir)
                if len(chunk) >= chunk_boyutu:
                    yield chunk
                    chunk = []
            if chunk:
                yield chunk

    toplam_sayac = Counter()
    # Chunk'ları işlemcinin farklı çekirdeklerine dağıt
    with mp.Pool(processes=cekirdek_sayisi) as havuz:
        for sonuc in havuz.imap_unordered(isci_fonksiyon, chunk_uretici()):
            toplam_sayac.update(sonuc)

    return dict(toplam_sayac)

# 5. YARIŞMACI 4: Polars (Rust Gücü)
@profil_olcer
def polars_yontemi(dosya_yolu: str):
    # Log dosyasını boşluklardan ayırarak okur, 7. sütun (durum kodu) üzerinde işlem yapar
    df = (
        pl.scan_csv(dosya_yolu, separator=" ", has_header=False)
        .group_by("column_7")
        .agg(pl.len().alias("sayi"))
        .collect()
    )
    
    # Çıktıyı standart Python sözlüğüne çevir
    return dict(zip(df["column_7"].to_list(), df["sayi"].to_list()))


if __name__ == "__main__":
    dosya = "buyuk_log.txt"
    print("Yarışma Başlıyor...\n" + "="*40)
    
    # Sırasıyla algoritmaları çalıştırıp profil sonuçlarını ekrana yazdır
    naif_dongu(dosya)
    generator_counter(dosya)
    multiprocessing_chunk(dosya)
    polars_yontemi(dosya)