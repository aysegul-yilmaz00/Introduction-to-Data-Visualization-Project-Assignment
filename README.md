
# MEVZUAT OTOMASYON SİSTEMİ

## Proje Amacı ve Genel Bakış

Bu sistem, kamu kurumlarında veya özel kuruluşlarda gelen evraklara mevzuat taraması yaparak otomatik ve resmi cevap yazısı üretmek için geliştirilmiştir. Yapay zeka destekli altyapısı sayesinde, mevzuat klasöründeki PDF dosyalarını analiz eder, gelen evrak ile ilişkilendirir ve resmi yazışma kurallarına uygun Word (.docx) formatında cevaplar oluşturur.

---

## Klasör ve Dosya Yapısı

```
├── analiz_merkezi.py         # Yapay zeka ve metin analiz merkezi
├── baslat.py                # Ana başlatıcı ve izleyici döngü
├── config.py                # Sistem ayarları ve klasör yolları
├── pdf_isleyici.py          # PDF/TXT dosya okuma yardımcıları
├── word_olusturucu.py       # Word dosyası şablon ve kayıt işlemleri
├── cevaplar/                # Üretilen resmi cevaplar (Word)
├── gelen-evraklar/          # İzlenen klasör, yeni evraklar buraya eklenir
├── mevzuat/                 # Mevzuat PDF dosyaları (kanun, yönetmelik vb.)
├── gecmis-gorusler/         # Geçmiş görüş ve cevap örnekleri (vektör arama için)
└── README.md                # Detaylı kullanım ve teknik dokümantasyon
```

---

## Kurulum

1. **Python Bağımlılıkları:**
   ```bash
   pip install pymupdf watchdog python-docx google-generativeai
   ```

2. **Mevzuat Dosyaları:**
   - Kullanmak istediğiniz mevzuat PDF dosyalarını `mevzuat/` klasörüne ekleyin.

3. **Gemini API Anahtarı (Opsiyonel):**
   - Daha kaliteli ve mevzuata uygun cevaplar için [Gemini API](https://ai.google.dev/) anahtarınızı alın.
   - `config.py` dosyasındaki `API_KEY` alanına ekleyin veya ortam değişkeni olarak tanımlayın.
   - API anahtarı girilmezse sistem sabit bir şablon cevap üretir.

---

## Kullanım

1. Terminalde proje klasörüne gelin:
   ```bash
   cd Introduction-to-Data-Visualization-Project-Assignment
   ```
2. Programı başlatın:
   ```bash
   python baslat.py
   ```
3. `gelen-evraklar/` klasörüne PDF formatında bir evrak ekleyin.
4. Sistem otomatik olarak dosyayı algılar, mevzuatı tarar ve cevabı `cevaplar/` klasörüne Word dosyası olarak kaydeder.

---

## Sistem Akışı

1. **Klasör İzleme:**
   - `baslat.py`, `gelen-evraklar/` klasörünü sürekli izler.
2. **Evrak Okuma:**
   - Yeni bir PDF geldiğinde, `pdf_isleyici.py` ile metin çıkarılır.
3. **Mevzuat Analizi:**
   - `mevzuat/` klasöründeki tüm PDF'ler taranır ve külliyat oluşturulur.
4. **Yapay Zeka ile Cevap Üretimi:**
   - `analiz_merkezi.py`, Gemini AI ile mevzuat ve geçmiş görüşleri dikkate alarak resmi cevap taslağı üretir.
5. **Word Şablonuna Aktarma:**
   - `word_olusturucu.py`, cevabı resmi yazı formatında Word dosyasına dönüştürür.
6. **Kayıt:**
   - Sonuç, `cevaplar/` klasörüne kaydedilir.

---

## Temel Dosya ve Fonksiyon Açıklamaları

### baslat.py
- Ana döngü ve klasör izleme.
- `GelenEvrakHandler`: Yeni evrak algılandığında tüm süreci tetikler.

### analiz_merkezi.py
- `AnalizMerkezi`: Yapay zeka ile metin analizi, geçmiş görüşlerin vektörleştirilmesi, benzerlik arama ve cevap üretimi.
- `resmi_cevap_uret`: Evrak ve mevzuat ile resmi cevap üretir.

### pdf_isleyici.py
- `PdfIsleyici`: PDF/TXT dosyalarından metin çıkarma ve mevzuat külliyatı oluşturma.

### word_olusturucu.py
- `word_kaydet`: JSON veya metni resmi Word şablonuna dönüştürüp kaydeder.

### config.py
- Klasör yolları, kurum/birim adı ve API anahtarı ayarları.

---

## Klasörler ve İçerikleri

- **mevzuat/**: Kanun, yönetmelik vb. PDF dosyaları.
- **gelen-evraklar/**: Sistemin izlediği, yeni evrakların ekleneceği klasör.
- **cevaplar/**: Üretilen Word cevap dosyaları.
- **gecmis-gorusler/**: Geçmiş evrak ve cevap örnekleri (vektör arama için).

---

## Örnek Kullanım Senaryosu

1. `mevzuat/` klasörüne "Kamu İhale Kanunu.pdf" ve "Disiplin Yönetmeliği.pdf" ekleyin.
2. `gelen-evraklar/` klasörüne "Talep_Dilekcesi.pdf" yükleyin.
3. Sistem, mevzuatı tarar, evrakı analiz eder ve cevabı otomatik olarak `cevaplar/` klasörüne "Talep_Dilekcesi_Cevap.docx" olarak kaydeder.

---

## Teknik Detaylar

- **Yapay Zeka:** Google Gemini API ile doğal dil işleme ve metin üretimi.
- **Vektör Arama:** Geçmiş görüşler vektörleştirilir, yeni evraklarla benzerlik analizi yapılır.
- **Resmi Yazı Şablonu:** Word dosyası, kurum/birim adı, sayı, tarih, konu, ilgi, içerik ve imza alanlarını otomatik oluşturur.
- **Hata Yönetimi:** API anahtarı yoksa sabit şablon cevap döner.

---

## Sıkça Sorulan Sorular (SSS)

**S: API anahtarı olmadan çalışır mı?**
**C:** Evet, ancak cevaplar sabit bir şablon olur. Yapay zeka ile üretilmiş detaylı cevaplar için API anahtarı gereklidir.

**S: Farklı formatta evrak ekleyebilir miyim?**
**C:** Şu an sadece PDF (ve .txt) desteklenmektedir.

**S: Mevzuat dosyalarını güncelleyince sistem otomatik algılar mı?**
**C:** Evet, yeni evrak işlendiğinde güncel mevzuat taranır.

---

## İletişim ve Destek

Herhangi bir sorun, öneri veya katkı için sistem yöneticisine veya proje sorumlusuna ulaşabilirsiniz.
