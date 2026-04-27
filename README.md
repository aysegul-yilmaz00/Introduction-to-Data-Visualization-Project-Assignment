# MEVZUAT OTOMASYON SİSTEMİ - KULLANIM KILAVUZU

Bu sistem, mevzuat dosyalarını analiz ederek gelen evraklara otomatik olarak resmi görüş yazısı hazırlamak için tasarlanmıştır.

## Kurulum ve Hazırlık

1. **Bağımlılıkları Kurun:**
   Sistem için gerekli Python kütüphanelerini şu komutla kurun:
   pip install pymupdf watchdog python-docx google-generativeai

2. **Mevzuat Klasörü (mevzuat/):**
   Hangi kanun, yönetmelik veya mevzuat baz alınacaksa, bu PDF dosyalarını 'mevzuat' klasörüne kopyalayın.

3. **Gemini API Anahtarı (Opsiyonel ama Önerilir):**
   Yapay zekanın resmi dil kalitesini artırmak için bir Gemini API anahtarı edinin.
   - API anahtarınızı 'config.py' dosyasındaki 'API_KEY' kısmına yapıştırın.
   - API anahtarı olmazsa sistem sabit bir şablon cevap kullanacaktır.

## Çalıştırma

Programı başlatmak için terminale şu komutu yazın:
python baslat.py

## Süreç Nasıl İşler?

1. Program çalıştığında 'gelen-evraklar' klasörünü dinlemeye başlar.
2. Bu klasöre yeni bir PDF dosyası (Örn: Talep_Dilekcesi.pdf) attığınızda sistem otomatik olarak dosyayı fark eder.
3. Arka planda mevzuat dosyalarını tarar ve gelen evraktaki konuyla eşleştirir.
4. Gemini AI aracılığıyla resmi bir üslupla cevap taslağı oluşturur.
5. Sonucu 'cevaplar' klasörüne Word (.docx) olarak kaydeder.

## İletişim ve Destek
Herhangi bir sorun yaşarsanız lütfen sistem yöneticisine danışın.
