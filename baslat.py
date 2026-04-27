import time
import os
import config
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pdf_isleyici import PdfIsleyici
from analiz_merkezi import AnalizMerkezi
from word_olusturucu import word_kaydet

class GelenEvrakHandler(FileSystemEventHandler):
    def __init__(self, analizci):
        self.analizci = analizci

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(".pdf"):
            print(f"\n[+] Yeni evrak algılandı: {os.path.basename(event.src_path)}")
            self.isle(event.src_path)

    def isle(self, dosya_yolu):
        print("[-] Mevzuat taranıyor ve analiz ediliyor...")
        
        # 1. Mevzuatı oku
        mevzuat = PdfIsleyici.mevzuat_yukle(config.MEVZUAT_DIR)
        
        # 2. Gelen belgeyi oku
        evrak_metni = PdfIsleyici.metin_cikar(dosya_yolu)
        
        # 3. Analiz et ve cevap üret
        cevap = self.analizci.resmi_cevap_uret(evrak_metni, mevzuat)
        
        # 4. Word olarak kaydet
        dosya_adi = os.path.basename(dosya_yolu).replace(".pdf", "_Cevap.docx")
        kayit_yolu = word_kaydet(cevap, dosya_adi)
        
        print(f"[OK] Cevap yazısı oluşturuldu: {kayit_yolu}")

def ana_dongu():
    print("="*40)
    print("MEVZUAT OTOMASYON SİSTEMİ BAŞLATILDI")
    print(f"İzlenen Klasör: {config.GELEN_EVRAK_DIR}")
    print("Mevzuat Klasörü: ", config.MEVZUAT_DIR)
    print("Çıkmak için Ctrl+C tuşlarına basın.")
    print("="*40)

    analizci = AnalizMerkezi()
    event_handler = GelenEvrakHandler(analizci)
    
    print("\n[-] Mevcut dosyalar kontrol ediliyor...")
    try:
        mevcut_dosyalar = [f for f in os.listdir(config.GELEN_EVRAK_DIR) if f.lower().endswith('.pdf')]
        if mevcut_dosyalar:
            for dosya in mevcut_dosyalar:
                dosya_yolu = os.path.join(config.GELEN_EVRAK_DIR, dosya)
                print(f"[+] Mevcut evrak bulundu, isleniyor: {dosya}")
                # Cevap dosyasının zaten olup olmadığını kontrol et
                dosya_adi = dosya.replace(".pdf", "_Cevap.docx")
                beklenen_cevap = os.path.join(config.CEVAPLAR_DIR, dosya_adi)
                if not os.path.exists(beklenen_cevap):
                    event_handler.isle(dosya_yolu)
                else:
                    print(f"[i] {dosya} için cevap zaten üretilmiş, atlanıyor.")
        else:
            print("[i] İşlenecek hazır evrak bulunamadı. Yeni evraklar bekleniyor...")
    except Exception as e:
        print(f"Hata oluştu: {e}")

    observer = Observer()
    observer.schedule(event_handler, config.GELEN_EVRAK_DIR, recursive=False)
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    ana_dongu()
