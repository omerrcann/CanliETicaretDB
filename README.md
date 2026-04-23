# 🌐 E-Ticaret Operasyon Merkezi (Canlı Veri Pipeline)

Bu proje, Python tabanlı bir e-ticaret veri simülasyonu ve gerçek zamanlı analitik panelidir. Sistemin temel amacı; veritabanı mimarisi, SQL entegrasyonu ve canlı veri görselleştirme süreçlerini uçtan uca (End-to-End) sergilemektir.

![Project Status](https://img.shields.io/badge/Status-Live-brightgreen)
![Python Version](https://img.shields.io/badge/Python-3.9+-blue)
![Framework](https://img.shields.io/badge/Framework-Streamlit-ff4b4b)

## 🚀 Proje Hakkında
Proje, arka planda milisaniyeler içinde sipariş üreten bir **hayalet bot** ile beslenen, Türkiye'nin 81 iline yayılmış bir satış ağını simüle eder. Veriler bir SQLite veritabanında saklanır ve Streamlit Dashboard üzerinden anlık olarak analiz edilir.

### 🛠️ Teknik Mimari
- **Backend:** Python & SQLAlchemy (ORM)
- **Veritabanı:** SQLite3 (İlişkisel Veri Modeli)
- **Frontend:** Streamlit & Custom CSS
- **Görselleştirme:** Plotly Express (Interaktif Grafikler)
- **Veri Simülasyonu:** Rastgele Olasılıksal Algoritmalar

## 📊 Öne Çıkan Özellikler
- **Canlı Radar Haritası:** Türkiye'nin 81 ilindeki sipariş yoğunluğunu gösteren Mapbox tabanlı ısı haritası.
- **Ürün Portföy Analizi (Treemap):** Kategori ve ürün bazlı ciro hiyerarşisinin görselleştirilmesi.
- **Finansal KPI Kartları:** Brüt Ciro, Toplam Sipariş ve Sepet Ortalaması (AOV) metriklerinin anlık takibi.
- **Dahili Simülatör:** Dış bir script'e ihtiyaç duymadan, dashboard üzerinden kontrol edilebilen canlı sipariş üretim motoru.

## 📁 Dosya Yapısı
* `dashboard.py`: Kullanıcı arayüzü ve ana uygulama kodu.
* `database.py`: SQLAlchemy modelleri ve veritabanı bağlantı ayarları.
* `requirements.txt`: Gerekli kütüphanelerin listesi.
* `eticaret_canli.db`: Üretilen verilerin saklandığı ilişkisel veritabanı.

## 🛠️ Kurulum ve Çalıştırma
Projeyi yerel bilgisayarınızda çalıştırmak için:

1. Depoyu klonlayın:
   ```bash
   git clone [https://github.com/omerrcann/CanliETicaretDB.git](https://github.com/omerrcann/CanliETicaretDB.git)
   
Gerekli kütüphaneleri kurun:

```bash
pip install -r requirements.txt
```


Uygulamayı başlatın:
```bash
streamlit run dashboard.py
```


---

### Son bir dokunuş: `requirements.txt`
GitHub'da başkalarının projeni tek komutla kurabilmesi için bu dosya şarttır. Proje klasöründe **`requirements.txt`** adında bir dosya daha oluştur ve içine şunları yaz:

```text
streamlit
pandas
plotly
sqlalchemy