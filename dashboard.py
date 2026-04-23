import streamlit as st
import pandas as pd
import sqlite3
import time
import random
import plotly.express as px
from database import SessionLocal, Musteri, Siparis, SiparisDetayi, Urun, Kategori

st.set_page_config(page_title="E-Ticaret Operasyon Merkezi", page_icon="🌐", layout="wide",
                   initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .kpi-kutu {
        background-color: #161B22;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00F2FF;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
        border: 1px solid #30363D;
    }
    .kpi-baslik { color: #8B949E; font-size: 16px; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px; }
    .kpi-deger { color: #00F2FF; font-size: 28px; font-weight: bold; text-shadow: 0 0 10px rgba(0,242,255,0.5); }
    .stApp { background-color: #0D1117; }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    "<h2 style='text-align: center; color: #00F2FF; text-shadow: 0 0 15px rgba(0,242,255,0.4);'>⚡  E-TİCARET OPERASYON MERKEZİ ⚡</h2><hr style='border: 0.5px solid #30363D;'>",
    unsafe_allow_html=True)

KOORDINATLAR = {
    "Adana": (37.0, 35.3213), "Adıyaman": (37.7648, 38.2786), "Afyonkarahisar": (38.7507, 30.5567),
    "Ağrı": (39.7191, 43.0503),
    "Amasya": (40.6499, 35.8353), "Ankara": (39.9334, 32.8597), "Antalya": (36.8969, 30.7133),
    "Artvin": (41.1828, 41.8183),
    "Aydın": (37.838, 27.8456), "Balıkesir": (39.6484, 27.8826), "Bilecik": (40.1451, 29.9798),
    "Bingöl": (38.8847, 40.4939),
    "Bitlis": (38.4006, 42.1095), "Bolu": (40.7392, 31.6111), "Burdur": (37.7204, 30.2908), "Bursa": (40.1826, 29.0669),
    "Çanakkale": (40.1553, 26.4086), "Çankırı": (40.6013, 33.6134), "Çorum": (40.5489, 34.9533),
    "Denizli": (37.7765, 29.0864),
    "Diyarbakır": (37.9144, 40.2306), "Edirne": (41.6771, 26.5557), "Elazığ": (38.6748, 39.2225),
    "Erzincan": (39.75, 39.5),
    "Erzurum": (39.9043, 41.2679), "Eskişehir": (39.7667, 30.5256), "Gaziantep": (37.0662, 37.3833),
    "Giresun": (40.9128, 38.3895),
    "Gümüşhane": (40.4608, 39.4814), "Hakkari": (37.5744, 43.7408), "Hatay": (36.2066, 36.1572),
    "Isparta": (37.7648, 30.5566),
    "Mersin": (36.8, 34.6167), "İstanbul": (41.0082, 28.9784), "İzmir": (38.4237, 27.1428), "Kars": (40.6013, 43.0975),
    "Kastamonu": (41.3781, 33.7753), "Kayseri": (38.7205, 35.4826), "Kırklareli": (41.7333, 27.2167),
    "Kırşehir": (39.1425, 34.1709),
    "Kocaeli": (40.8533, 29.8815), "Konya": (37.8746, 32.4932), "Kütahya": (39.4167, 29.9833),
    "Malatya": (38.3552, 38.3095),
    "Manisa": (38.6191, 27.4289), "Kahramanmaraş": (37.5858, 36.9371), "Mardin": (37.3122, 40.7339),
    "Muğla": (37.2153, 28.3636),
    "Muş": (38.7304, 41.491), "Nevşehir": (38.6244, 34.7144), "Niğde": (37.9667, 34.6833), "Ordu": (40.9862, 37.8797),
    "Rize": (41.0201, 40.5234), "Sakarya": (40.7569, 30.3783), "Samsun": (41.2867, 36.33), "Siirt": (37.9333, 41.95),
    "Sinop": (42.0231, 35.1531), "Sivas": (39.7477, 37.0179), "Tekirdağ": (40.9833, 27.5167), "Tokat": (40.3167, 36.55),
    "Trabzon": (41.0015, 39.7178), "Tunceli": (39.1061, 39.5481), "Şanlıurfa": (37.1674, 38.7939),
    "Uşak": (38.6823, 29.4082),
    "Van": (38.4891, 43.3889), "Yozgat": (39.8181, 34.8147), "Zonguldak": (41.4564, 31.7987),
    "Aksaray": (38.3687, 34.037),
    "Bayburt": (40.2552, 40.2249), "Karaman": (37.1811, 33.2222), "Kırıkkale": (39.8468, 33.5153),
    "Batman": (37.8812, 41.1351),
    "Şırnak": (37.5164, 42.4611), "Bartın": (41.6344, 32.3375), "Ardahan": (41.1105, 42.7022),
    "Iğdır": (39.9237, 44.045),
    "Yalova": (40.65, 29.2667), "Karabük": (41.2061, 32.6228), "Kilis": (36.7184, 37.1212),
    "Osmaniye": (37.0742, 36.2473),
    "Düzce": (40.8438, 31.1565)
}


def hayalet_bot():
    db = SessionLocal()
    try:
        if db.query(Urun).count() == 0:
            try:
                from veri_botu import dukkani_hazirla
                dukkani_hazirla(db)
                st.toast("🛒 Sunucuda dükkan sıfırdan kuruldu, raflar dolduruldu!", icon="✅")
            except Exception as e:
                st.error(f"Dükkan kurulurken hata: {e}")
            return

        ADLAR = [
            "Ahmet", "Mehmet", "Mustafa", "Ali", "Hüseyin", "Hasan", "İbrahim", "Yusuf", "Murat", "Ömer",
            "Fatih", "Süleyman", "Abdullah", "Mahmut", "İsmail", "Salih", "Recep", "Emre", "Hakan", "Deniz",
            "Burak", "Cem", "Can", "Eren", "Furkan", "Gökhan", "Kaan", "Mert", "Onur", "Serkan",
            "Tolga", "Umut", "Volkan", "Yasin", "Yiğit", "Barış", "Sinan", "Erdem", "Oğuz", "Bora",
            "Ayşe", "Fatma", "Zeynep", "Emine", "Hatice", "Elif", "Merve", "Büşra", "Esra", "Kübra",
            "Özlem", "Derya", "Selin", "Ece", "Aslı", "Pınar", "Gizem", "İrem", "Gamze", "Tuğçe",
            "Ceren", "Melis", "Damla", "Dilan", "Bahar", "Sibel", "Filiz", "Gözde", "Hande", "Nur",
            "Arda", "Batuhan", "Berkay", "Çağatay", "Doruk", "Ege", "Görkem", "Kerem", "Mete", "Sarp",
            "Alperen", "Bedirhan", "Cihan", "Doğan", "Enes", "Hamza", "Kadir", "Levent", "Metin", "Nedim",
            "Pelin", "Rüya", "Simge", "Şevval", "Talha", "Utku", "Vildan", "Yağmur", "Yeliz", "Zehra"
        ]

        SOYADLAR = [
            "Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Yıldız", "Yıldırım", "Öztürk", "Aydın", "Özdemir",
            "Arslan", "Doğan", "Kılıç", "Aslan", "Çetin", "Kara", "Koç", "Kurt", "Özkan", "Şimşek",
            "Polat", "Özcan", "Korkmaz", "Çakır", "Erdoğan", "Yavuz", "Sarı", "Acar", "Şen", "Aktaş",
            "Güler", "Yalçın", "Güneş", "Bozkurt", "Bulut", "Keskin", "Turan", "Özer", "Işık", "Kaplan",
            "Avcı", "Sönmez", "Can", "Alkan", "Gül", "Şentürk", "Uysal", "Yücel", "Günay", "Aksoy",
            "Köse", "Eren", "Yavaş", "Akan", "Uğur", "Taş", "Tekin", "Gündüz", "Akyol", "Erdem",
            "Duman", "Yarar", "Ünal", "Toprak", "Soylu", "Başar", "Umut", "Varol", "Yörük", "Akgün",
            "Boran", " Yaman", "Okur", "Aras", "Baran", "Ateş", "Ekinci", "Uzun", "Bilgin", "Yurt",
            "Savaş", "Sert", "Koca", "Çelikten", "Soydan", "Öz", "Gök", "Ak", "Ay", "Gencer",
            "Kutlu", "Altan", "Erbil", "Tüzün", "Sezer", "Kandemir", "Ulucan", "Sancak", "Tunç", "Öge"
        ]

        for _ in range(random.randint(1, 2)):
            isim = f"{random.choice(ADLAR)} {random.choice(SOYADLAR)}"
            sehir = random.choice(list(KOORDINATLAR.keys()))
            musteri = Musteri(ad_soyad=isim, sehir=sehir, segment=random.choice(["Standart", "Premium"]))
            db.add(musteri)
            db.commit()
            db.refresh(musteri)
            siparis = Siparis(musteri_id=musteri.id, toplam_tutar=0.0)
            db.add(siparis)
            db.commit()
            db.refresh(siparis)
            urunler = db.query(Urun).all()
            alinan_urunler = random.sample(urunler, random.randint(1, 3))
            toplam = 0
            for u in alinan_urunler:
                adet = random.randint(1, 2)
                detay = SiparisDetayi(siparis_id=siparis.id, urun_id=u.id, adet=adet, satilan_fiyat=u.fiyat)
                db.add(detay)
                toplam += (u.fiyat * adet)
            siparis.toplam_tutar = toplam
            db.commit()
    finally:
        db.close()


def verileri_cek():
    conn = sqlite3.connect("eticaret_canli.db")

    df_genel = pd.read_sql(
        "SELECT COUNT(id) as ToplamSiparis, SUM(toplam_tutar) as ToplamCiro, AVG(toplam_tutar) as SepetOrtalamasi FROM siparisler",
        conn)

    df_hiyerarsi = pd.read_sql("""
                               SELECT k.isim as Kategori, u.isim as Urun, SUM(sd.adet * sd.satilan_fiyat) as Ciro
                               FROM siparis_detaylari sd
                                        JOIN urunler u ON sd.urun_id = u.id
                                        JOIN kategoriler k ON u.kategori_id = k.id
                               GROUP BY k.isim, u.isim
                               """, conn)

    df_sehir = pd.read_sql("""
                           SELECT m.sehir as Sehir, SUM(s.toplam_tutar) as Ciro, COUNT(s.id) as SiparisSayisi
                           FROM siparisler s
                                    JOIN musteriler m ON s.musteri_id = m.id
                           GROUP BY m.sehir
                           """, conn)

    df_zaman = pd.read_sql("""
                           SELECT strftime('%H:%M:%S', zaman) as Saat, SUM(toplam_tutar) as Ciro
                           FROM siparisler
                           GROUP BY Saat
                           ORDER BY MAX(id) DESC LIMIT 20
                           """, conn)
    df_zaman = df_zaman.sort_values('Saat')
    conn.close()
    return df_genel, df_hiyerarsi, df_sehir, df_zaman


df_genel, df_hiyerarsi, df_sehir, df_zaman = verileri_cek()

try:
    ciro = df_genel['ToplamCiro'].iloc[0] or 0
    siparis = df_genel['ToplamSiparis'].iloc[0] or 0
    sepet_ort = df_genel['SepetOrtalamasi'].iloc[0] or 0
    aktif_sehir = len(df_sehir)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"<div class='kpi-kutu'><div class='kpi-baslik'>💰 Toplam Brüt Ciro</div><div class='kpi-deger'>₺ {ciro:,.0f}</div></div>",
            unsafe_allow_html=True)
    with c2:
        st.markdown(
            f"<div class='kpi-kutu'><div class='kpi-baslik'>🛒 Toplam Sipariş</div><div class='kpi-deger'>{siparis} Fiş</div></div>",
            unsafe_allow_html=True)
    with c3:
        st.markdown(
            f"<div class='kpi-kutu'><div class='kpi-baslik'>🛍️ Sepet Ortalaması</div><div class='kpi-deger'>₺ {sepet_ort:,.0f}</div></div>",
            unsafe_allow_html=True)
    with c4:
        st.markdown(
            f"<div class='kpi-kutu'><div class='kpi-baslik'>🌍 Aktif Şehir Sayısı</div><div class='kpi-deger'>{aktif_sehir} Şehir</div></div>",
            unsafe_allow_html=True)
except:
    st.warning("Veritabanı okunuyor...")

st.markdown("<br>", unsafe_allow_html=True)

if not df_hiyerarsi.empty:
    satir1_sol, satir1_sag = st.columns([2, 1])

    with satir1_sol:
        fig_trend = px.area(df_zaman, x='Saat', y='Ciro', title="📈 Canlı Satış Trendi (Son 20 İşlem)",
                            color_discrete_sequence=["#00F2FF"], template="plotly_dark")
        fig_trend.update_layout(margin=dict(l=0, r=0, t=40, b=0), height=300)
        st.plotly_chart(fig_trend, use_container_width=True)

    with satir1_sag:
        fig_tree = px.treemap(df_hiyerarsi, path=['Kategori', 'Urun'], values='Ciro',
                              title="🗂️ Kategori & Ürün Hacimleri", template="plotly_dark", color='Ciro',
                              color_continuous_scale='Blues')
        fig_tree.update_layout(margin=dict(l=0, r=0, t=40, b=0), height=300)
        st.plotly_chart(fig_tree, use_container_width=True)

    satir2_sol, satir2_sag = st.columns([1.5, 1])

    with satir2_sol:
        df_sehir['lat'] = df_sehir['Sehir'].apply(lambda x: KOORDINATLAR.get(x, (39.0, 35.0))[0])
        df_sehir['lon'] = df_sehir['Sehir'].apply(lambda x: KOORDINATLAR.get(x, (39.0, 35.0))[1])

        fig_map = px.scatter_mapbox(df_sehir, lat="lat", lon="lon", size="Ciro", color="Ciro", hover_name="Sehir",
                                    hover_data=["SiparisSayisi"], color_continuous_scale="Purp", size_max=40,
                                    zoom=4.5,
                                    center={"lat": 39.0, "lon": 35.0}, title="📍 Şehir Bazında Sipariş Yoğunluğu",
                                    mapbox_style="carto-darkmatter", template="plotly_dark")
        fig_map.update_layout(margin=dict(l=0, r=0, t=40, b=0), height=400)
        st.plotly_chart(fig_map, use_container_width=True)

    with satir2_sag:
        df_top_sehir = df_sehir.sort_values('Ciro', ascending=True).tail(7)
        fig_bar = px.bar(df_top_sehir, x='Ciro', y='Sehir', orientation='h', title="🏆 En Çok Ciro Yapan Şehirler",
                         text_auto='.2s', color='Ciro', color_continuous_scale='Bluered_r', template="plotly_dark")
        fig_bar.update_layout(margin=dict(l=0, r=0, t=40, b=0), height=400, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")
canli = st.checkbox("🔴 Canlı Veri Akışını Başlat", value=False)
if canli:
    hayalet_bot()
    time.sleep(5)
    st.rerun()