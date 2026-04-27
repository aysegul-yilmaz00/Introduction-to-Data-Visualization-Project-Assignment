import fitz  # PyMuPDF
import os

class PdfIsleyici:
    """PDF dosyalarından metin çıkarmak için kullanılan yardımcı sınıf."""
    
    @staticmethod
    def metin_cikar(dosya_yolu):
        """Verilen PDF veya TXT dosyasındaki tüm metni döner."""
        if not os.path.exists(dosya_yolu):
            return ""
            
        metin = ""
        try:
            if dosya_yolu.lower().endswith(".txt"):
                with open(dosya_yolu, 'r', encoding='utf-8') as f:
                    metin = f.read()
            else:
                doc = fitz.open(dosya_yolu)
                for sayfa in doc:
                    metin += sayfa.get_text()
                doc.close()
        except Exception as e:
            print(f"Dosya Okuma Hatası ({dosya_yolu}): {e}")
        
        return metin


    @staticmethod
    def mevzuat_yukle(mevzuat_dizini):
        """Mevzuat klasöründeki tüm PDF'leri okuyup tek bir külliyat oluşturur."""
        kulliyat = []
        for dosya in os.listdir(mevzuat_dizini):
            if dosya.lower().endswith(".pdf"):
                yol = os.path.join(mevzuat_dizini, dosya)
                icerik = PdfIsleyici.metin_cikar(yol)
                if icerik:
                    kulliyat.append({
                        "dosya": dosya,
                        "icerik": icerik
                    })
        return kulliyat
