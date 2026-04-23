from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import datetime

DATABASE_URL = "sqlite:///./eticaret_canli.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Kategori(Base):
    __tablename__ = "kategoriler"
    id = Column(Integer, primary_key=True, index=True)
    isim = Column(String, unique=True, index=True)
    kar_marji = Column(Float)
    urunler = relationship("Urun", back_populates="kategori")

class Urun(Base):
    __tablename__ = "urunler"
    id = Column(Integer, primary_key=True, index=True)
    kategori_id = Column(Integer, ForeignKey("kategoriler.id"))
    isim = Column(String, index=True)
    fiyat = Column(Float)
    stok = Column(Integer)
    kategori = relationship("Kategori", back_populates="urunler")
    siparis_detaylari = relationship("SiparisDetayi", back_populates="urun")

class Musteri(Base):
    __tablename__ = "musteriler"
    id = Column(Integer, primary_key=True, index=True)
    ad_soyad = Column(String)
    sehir = Column(String)
    segment = Column(String)

    siparisler = relationship("Siparis", back_populates="musteri")

class Siparis(Base):
    __tablename__ = "siparisler"
    id = Column(Integer, primary_key=True, index=True)
    musteri_id = Column(Integer, ForeignKey("musteriler.id"))
    zaman = Column(DateTime, default=datetime.datetime.utcnow)
    toplam_tutar = Column(Float, default=0.0)

    musteri = relationship("Musteri", back_populates="siparisler")
    detaylar = relationship("SiparisDetayi", back_populates="siparis")

class SiparisDetayi(Base):
    __tablename__ = "siparis_detaylari"
    id = Column(Integer, primary_key=True, index=True)
    siparis_id = Column(Integer, ForeignKey("siparisler.id"))
    urun_id = Column(Integer, ForeignKey("urunler.id"))
    adet = Column(Integer)
    satilan_fiyat = Column(Float)

    siparis = relationship("Siparis", back_populates="detaylar")
    urun = relationship("Urun", back_populates="siparis_detaylari")

print("Veritabanı ve tablolar oluşturuluyor...")
Base.metadata.create_all(bind=engine)
print("İşlem başarılı! Mimari kuruldu.")