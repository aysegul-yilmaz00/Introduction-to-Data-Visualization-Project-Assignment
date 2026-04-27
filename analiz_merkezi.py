import google.generativeai as genai
import config
import os
import math
from pdf_isleyici import PdfIsleyici

class AnalizMerkezi:
    def __init__(self):
        self.api_key = config.API_KEY
        self.hazir = False
        self.gecmis_gorusler = []
        
        if self.api_key and self.api_key != "BURAYA_API_ANAHTARINIZI_YAZIN":
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.0-flash')
                self.hazir = True
                self._gecmis_gorusleri_yukle()
            except Exception as e:
                print(f"Gemini API Yapılandırma Hatası: {e}")

    def _gecmis_gorusleri_yukle(self):
        print("[-] Geçmiş görüşler yükleniyor ve indeksleniyor...")
        if not os.path.exists(config.GECMIS_GORUSLER_DIR):
            return
            
        for alt_dizin in os.listdir(config.GECMIS_GORUSLER_DIR):
            dizin_yolu = os.path.join(config.GECMIS_GORUSLER_DIR, alt_dizin)
            if os.path.isdir(dizin_yolu):
                gorus_metni = ""
                cevap_metni = ""
                
                for dosya in os.listdir(dizin_yolu):
                    dosya_yolu = os.path.join(dizin_yolu, dosya)
                    if dosya.lower().endswith(('.pdf', '.txt')):
                        metin = PdfIsleyici.metin_cikar(dosya_yolu)
                        if "cevap" in dosya.lower():
                            cevap_metni += metin + "\n"
                        else:
                            gorus_metni += metin + "\n"
                
                if gorus_metni.strip() and cevap_metni.strip():
                    try:
                        # Vektör yerleştirmesini hesapla
                        embedding = genai.embed_content(
                            model="models/text-embedding-004",
                            content=gorus_metni[:1000]
                        )
                        self.gecmis_gorusler.append({
                            "gorus": gorus_metni,
                            "cevap": cevap_metni,
                            "vektor": embedding['embedding']
                        })
                    except Exception as e:
                        print(f"Embedding hatası ({alt_dizin}): {e}")
        print(f"[+] Toplam {len(self.gecmis_gorusler)} geçmiş görüş örneği yüklendi.")

    def _benzer_gorus_bul(self, yeni_gorus_metni):
        if not self.gecmis_gorusler or not self.hazir:
            return None
            
        try:
            yeni_embedding = genai.embed_content(
                model="models/text-embedding-004",
                content=yeni_gorus_metni[:1000]
            )['embedding']
            
            en_iyi_skor = -1
            en_iyi_eslesme = None
            
            for gecmis in self.gecmis_gorusler:
                g, y = gecmis["vektor"], yeni_embedding
                dot = sum(a*b for a, b in zip(g, y))
                mag_g = math.sqrt(sum(a*a for a in g))
                mag_y = math.sqrt(sum(a*a for a in y))
                skor = dot / (mag_g * mag_y) if mag_g * mag_y != 0 else 0
                
                if skor > en_iyi_skor:
                    en_iyi_skor = skor
                    en_iyi_eslesme = gecmis
            
            if en_iyi_skor > 0.5:
                print(f"[i] Geçmiş benzer görüş bulundu (Skor: {en_iyi_skor:.2f})")
                return en_iyi_eslesme
        except Exception as e:
            print(f"Benzer görüş arama hatası: {e}")
            
        return None

    def resmi_cevap_uret(self, gelen_evrak_metni, mevzuat_kulliyati):
        """
        Gelen evrağı analiz eder, mevzuatı tarar ve resmi bir dile cevap yazar.
        """
        benzer_gorus = self._benzer_gorus_bul(gelen_evrak_metni)
        prompt = self._prompt_hazirla(gelen_evrak_metni, mevzuat_kulliyati, benzer_gorus)
        
        if self.hazir:
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                return f"Hata: Yapay zeka yanit üretemedi. Detay: {e}"
        else:
            return self._basit_cevap_sablonu(gelen_evrak_metni)

    def _prompt_hazirla(self, evrak, kulliyat, benzer_gorus=None):
        mevzuat_metni = "\n---\n".join([f"Dosya: {m['dosya']}\nİçerik: {m['icerik']}" for m in kulliyat])
        
        benzer_gorus_metni = ""
        if benzer_gorus:
            benzer_gorus_metni = f"""
ÖNCEKİ BENZER GÖRÜŞ TALEBİ:
{benzer_gorus['gorus'][:2000]}

BU TALEBE KURUMUMUZCA VERİLEN GEÇMİŞ CEVAP (ÜSLUP VE YAPI ÖRNEĞİ OLARAK KULLANILACAKTIR):
{benzer_gorus['cevap'][:2000]}

!!! YENİ YAZACAĞIN CEVAP, YUKARIDAKİ 'GEÇMİŞ CEVAP' İLE AYNI ÜSLUBA, FORMA VE MAKAM YAPISINA SAHİP OLMALIDIR !!!
"""

        prompt = f"""
Sen resmi yazışma kurallarına hakim bir hukuk ve mevzuat uzmanısın.
Aşağıdaki "Gelen Evrak" metnini oku, "Mevzuat" içeriklerine bakarak bu konudaki ilgili maddeleri bul ve resmi bir kurum diliyle cevap yaz.
{benzer_gorus_metni}

GELEN EVRAK:
{evrak}

ELDEKİ MEVZUAT BİLGİLERİ:
{mevzuat_metni}

TALİMATLAR:
1. Yanıt Türkçe ve son derece resmi (bürokratik) bir dille olmalıdır.
2. Yazışma kurallarına uygun bir yapı kur.
3. Mevzuattaki ilgili maddelere atıf yap (Örn: "... sayılı yönetmeliğin ... maddesi uyarınca").
4. "Gereğini bilgilerinize arz/rica ederim." gibi hiyerarşiye uygun resmi kapanış cümleleri kullan.
5. ÇIKTI OLARAK SADECE AŞAĞIDAKİ FORMATTA BİR JSON DÖNDÜR, BAŞKA HİÇBİR AÇIKLAMA VEYA GİRİŞ YAZISI YAZMA:

{{
  "makam": "GÖNDERİLECEK YER/MAKAM ADI (Tamamı büyük harflerle, örn: ANKARA İL SAĞLIK MÜDÜRLÜĞÜNE)",
  "konu": "Yazının Konusu (Örn: ... Hk.)",
  "ilgi": "Gelen evraka veya önceki yazışmalara atıf, varsa",
  "icerik": "Resmi yazının ana gövde metni (paragraflar halinde)"
}}
"""
        return prompt

    def _basit_cevap_sablonu(self, evrak):
        import json
        return json.dumps({
            "makam": "İLGİLİ MAKAMA",
            "konu": "Ön Değerlendirme Sonucu",
            "ilgi": "",
            "icerik": "Tarafımıza ulaşan yazınız incelenmiş olup, talebiniz/sorunuz kayıtlarımıza alınmıştır.\nMevzuat hükümlerimiz çerçevesinde yapılan ön değerlendirmede konunun tetkikine devam edilmektedir.\n\nİlgili mevzuat uyarınca işleminiz sonuçlandırıldığında tarafınıza bilgi verilecektir.\n\nGereğini bilgilerinize rica ederim."
        }, ensure_ascii=False)
