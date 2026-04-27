import os

# Klasör Yolları
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEVZUAT_DIR = os.path.join(BASE_DIR, "mevzuat")
GELEN_EVRAK_DIR = os.path.join(BASE_DIR, "gelen-evraklar")
CEVAPLAR_DIR = os.path.join(BASE_DIR, "cevaplar")
GECMIS_GORUSLER_DIR = os.path.join(BASE_DIR, "gecmis-gorusler")

# Gerekli klasörleri oluştur
for folder in [MEVZUAT_DIR, GELEN_EVRAK_DIR, CEVAPLAR_DIR, GECMIS_GORUSLER_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Yapay Zeka Ayarları (Gemini API)
# API Anahtarınızı Windows Ortam Değişkenlerine GEMINI_API_KEY olarak ekleyiniz 
# veya buraya doğrudan yazınız.
API_KEY = os.getenv("GEMINI_API_KEY", "BURAYA_API_ANAHTARINIZI_YAZIN")

# Kurum Bilgileri
KURUM_ADI = "T.C.\nGENEL MÜDÜRLÜK"
BIRIM_ADI = "Mevzuat ve Hukuk İşleri Dairesi Başkanlığı"
