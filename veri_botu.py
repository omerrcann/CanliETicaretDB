import time
import random
from database import SessionLocal, Kategori, Urun, Musteri, Siparis, SiparisDetayi, Base, engine

Base.metadata.create_all(bind=engine)

ADLAR = [
    "Ahmet", "Mehmet", "Ayşe", "Fatma", "Mustafa", "Zeynep", "Can", "Deniz", "Emre", "Burak",
    "Cem", "Ali", "Hasan", "Elif", "Esra", "Merve", "Gizem", "Oğuz", "Kaan", "Ceren",
    "Ece", "Selin", "Tolga", "Volkan", "Gökhan", "Yasin", "İbrahim", "Tuğçe", "Büşra", "Kübra",
    "Melis", "Kemal", "Osman", "Ömer", "Faruk", "Serkan", "Derya", "Bahar", "Aslı", "Cansu",
    "Erdem", "Onur", "Umut", "Yusuf", "Sinan", "Barış", "Eren", "Bora", "Arda", "Furkan"
]

SOYADLAR = [
    "Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Yıldız", "Yıldırım", "Öztürk", "Aydın", "Özdemir",
    "Arslan", "Doğan", "Kılıç", "Aslan", "Çetin", "Kara", "Koç", "Kurt", "Özkan", "Şimşek",
    "Polat", "Özcan", "Korkmaz", "Çakır", "Erdoğan", "Yavuz", "Sarı", "Acar", "Şen", "Aktaş",
    "Güler", "Yalçın", "Güneş", "Bozkurt", "Bulut", "Keskin", "Turan", "Özer", "Işık", "Kaplan"
]

ILLER = [
    "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir",
    "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli",
    "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane",
    "Hakkari",
    "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir",
    "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir",
    "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat",
    "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman",
    "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"
]


def dukkani_hazirla(db):
    if db.query(Kategori).count() == 0:
        print("🛒 Hipermarket sıfırdan kuruluyor! Raflar profesyonel verilerle dolduruluyor...")

        kat_elektronik = Kategori(isim="Elektronik", kar_marji=0.15)
        kat_giyim = Kategori(isim="Giyim", kar_marji=0.35)
        kat_kozmetik = Kategori(isim="Kozmetik", kar_marji=0.45)
        db.add_all([kat_elektronik, kat_giyim, kat_kozmetik])
        db.commit()

        elektronik_isimleri = [
            "Akıllı Telefon", "Laptop", "Tablet", "Akıllı Saat", "Bluetooth Kulaklık",
            "Monitör", "Klavye", "Oyuncu Mouse", "Taşınabilir Şarj Aleti", "Oyun Konsolu",
            "4K Televizyon", "Fotoğraf Makinesi", "Kameralı Drone", "Akıllı Ampul", "Robot Süpürge",
            "Sinema Ses Sistemi", "Projeksiyon Cihazı", "E-Kitap Okuyucu", "Akıllı Priz",
            "1TB SSD Disk", "Oyun Anakartı", "Grafik Ekran Kartı", "VR Gözlük"
        ]
        giyim_isimleri = [
            "Kışlık Mont", "Spor Ayakkabı", "Kot Pantolon", "Tişört", "Keten Gömlek",
            "Boğazlı Kazak", "Deri Ceket", "Pileli Etek", "Gece Elbisesi", "Kot Şort",
            "Eşofman Altı", "Kapüşonlu Sweatshirt", "İpek Pijama Takımı", "Spor Çorap",
            "Termal İçlik", "Yün Bere", "Kaşmir Atkı", "Deri Eldiven", "Su Geçirmez Yağmurluk",
            "Şişme Yelek", "Klasik Trençkot", "Yazlık Mayo", "Kumaş Pantolon"
        ]
        kozmetik_isimleri = [
            "Erkek Odunsu Parfüm", "Kadın Çiçeksi Parfüm", "Cilt Yenileyici Serum", "Nemlendirici Yüz Kremi",
            "50 Faktör Güneş Kremi", "Göz Altı Morluk Kremi", "Dökülme Karşıtı Şampuan", "Argan Saç Kremi",
            "Okyanus Ferahlığı Duş Jeli", "Avokadolu Vücut Losyonu", "Sprey Deodorant", "Kırmızı Mat Ruj",
            "Hacim Veren Maskara", "Likit Fondöten", "Toprak Rengi Göz Farı", "Suya Dayanıklı Eyeliner",
            "Şeftali Tonu Allık", "Göz Altı Kapatıcı", "Makyaj Temizleme Suyu", "Yüz Peeling Jel",
            "Hassas Tıraş Köpüğü", "Mat Saç Şekillendirici (Wax)"
        ]

        urun_objeleri = []
        for isim in elektronik_isimleri:
            urun_objeleri.append(
                Urun(kategori_id=kat_elektronik.id, isim=isim, fiyat=round(random.uniform(500, 45000), -1),
                     stok=random.randint(30, 200)))
        for isim in giyim_isimleri:
            urun_objeleri.append(Urun(kategori_id=kat_giyim.id, isim=isim, fiyat=round(random.uniform(150, 3500), -1),
                                      stok=random.randint(100, 500)))
        for isim in kozmetik_isimleri:
            urun_objeleri.append(
                Urun(kategori_id=kat_kozmetik.id, isim=isim, fiyat=round(random.uniform(100, 2500), -1),
                     stok=random.randint(150, 800)))

        db.add_all(urun_objeleri)
        db.commit()
        print(f"✅ Başarılı! Toplam {len(urun_objeleri)} ürün eklendi!\n")


def canli_siparis_simulasyonu():
    db = SessionLocal()
    dukkani_hazirla(db)

    print("🚀 CANLI YAYIN BAŞLADI: Temiz ve profesyonel veriler akıyor... (Durdurmak için CTRL+C)")

    try:
        while True:
            mantikli_isim = f"{random.choice(ADLAR)} {random.choice(SOYADLAR)}"

            yeni_musteri = Musteri(
                ad_soyad=mantikli_isim,
                sehir=random.choice(ILLER),
                segment=random.choice(["Standart", "Standart", "Premium"])
            )
            db.add(yeni_musteri)
            db.commit()
            db.refresh(yeni_musteri)

            yeni_siparis = Siparis(musteri_id=yeni_musteri.id, toplam_tutar=0.0)
            db.add(yeni_siparis)
            db.commit()
            db.refresh(yeni_siparis)

            alinacak_urun_sayisi = random.randint(1, 5)
            tum_urunler = db.query(Urun).all()
            sepetteki_urunler = random.sample(tum_urunler, alinacak_urun_sayisi)

            siparis_toplami = 0.0

            for urun in sepetteki_urunler:
                satin_alinan_adet = random.randint(1, 3)
                if urun.stok >= satin_alinan_adet:
                    detay = SiparisDetayi(
                        siparis_id=yeni_siparis.id,
                        urun_id=urun.id,
                        adet=satin_alinan_adet,
                        satilan_fiyat=urun.fiyat
                    )
                    db.add(detay)
                    urun.stok -= satin_alinan_adet
                    siparis_toplami += (urun.fiyat * satin_alinan_adet)

            if siparis_toplami > 0:
                yeni_siparis.toplam_tutar = siparis_toplami
                db.commit()
                print(
                    f"[{yeni_siparis.zaman.strftime('%H:%M:%S')}] 🛍️ {yeni_musteri.ad_soyad} ({yeni_musteri.sehir}) -> Toplam: {siparis_toplami:,.0f} TL")
            else:
                db.delete(yeni_siparis)
                db.commit()

            time.sleep(random.uniform(0.1, 1.5))

    except KeyboardInterrupt:
        print("\n🛑 Simülasyon durduruldu.")
    finally:
        db.close()


if __name__ == "__main__":
    canli_siparis_simulasyonu()