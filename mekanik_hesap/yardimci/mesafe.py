"""Yardimci 6/7: sehirlerarasi mesafe onhesabi.

Dayanak: [STANDART-TEYIT]. Kus ucusu Haversine bagintisidir
(R = 6371 km); yol mesafesi = kus_ucusu * yol_katsayi (varsayilan
1.3 pratik); sure = mesafe / hiz. Koordinat tablosu yaklasik
WGS84 pratik degerlerdir [SEHIR-TEYIT], harita/guzergah ile
teyit edilir; sozlesme/guzergah karari icin kullanilmaz.
"""

import math
from typing import Union

_R = 6371.0  # yer yari capi, km.

# sehir -> (enlem_deg, boylam_deg) yaklasik [SEHIR-TEYIT].
SEHIR_KOORD = {
    "istanbul": (41.0, 29.0),
    "ankara": (39.9, 32.8),
    "izmir": (38.4, 27.1),
    "bursa": (40.2, 29.1),
    "antalya": (36.9, 30.7),
    "adana": (37.0, 35.3),
    "konya": (37.9, 32.5),
    "gaziantep": (37.1, 37.4),
    "trabzon": (41.0, 39.7),
    "erzurum": (39.9, 41.3),
}

YOL_KATSAYI = 1.3  # pratik kabul [STANDART-TEYIT].


def sehirler() -> list[str]:
    """Kayitli sehir adlari listesi."""
    return sorted(SEHIR_KOORD)


def kus_ucusu_km(enlem1: Union[int, float], boylam1: Union[int, float],
                 enlem2: Union[int, float],
                 boylam2: Union[int, float]) -> float:
    """Iki koordinat arasi kus ucusu, km (Haversine)."""
    la1, lo1 = math.radians(float(enlem1)), math.radians(float(boylam1))
    la2, lo2 = math.radians(float(enlem2)), math.radians(float(boylam2))
    for v in (la1, lo1, la2, lo2):
        if not math.isfinite(v):
            raise ValueError("koordinatlar sayi olmali")
    dlat, dlon = la2 - la1, lo2 - lo1
    a = (math.sin(dlat / 2.0) ** 2 + math.cos(la1) * math.cos(la2)
         * math.sin(dlon / 2.0) ** 2)
    return 2.0 * _R * math.asin(math.sqrt(max(0.0, min(1.0, a))))


def sehir_mesafesi(sehir1: str, sehir2: str,
                   yol_katsayi: float = YOL_KATSAYI) -> tuple[float, float]:
    """Iki kayitli sehir arasi: (kus_ucusu_km, yol_km).

    Bilinmeyen sehir KeyError verir [SEHIR-TEYIT].
    """
    k = float(yol_katsayi)
    if k <= 0:
        raise ValueError("yol katsayisi pozitif olmali")
    a = str(sehir1).strip().lower()
    b = str(sehir2).strip().lower()
    if a not in SEHIR_KOORD:
        raise KeyError("kayitli sehir degil [SEHIR-TEYIT]: %r" % (sehir1,))
    if b not in SEHIR_KOORD:
        raise KeyError("kayitli sehir degil [SEHIR-TEYIT]: %r" % (sehir2,))
    kus = kus_ucusu_km(*SEHIR_KOORD[a], *SEHIR_KOORD[b])
    return kus, kus * k


def yol_mesafesi(kus_km: Union[int, float],
                 yol_katsayi: float = YOL_KATSAYI) -> float:
    """Kus ucusundan yol mesafesi, km. yol = kus * katsayi."""
    kus, k = float(kus_km), float(yol_katsayi)
    if kus < 0 or k <= 0:
        raise ValueError("girisler gecerli olmali")
    return kus * k


def seyahat_suresi(mesafe_km: Union[int, float],
                   hiz_kmh: float = 90.0) -> float:
    """Seyahat suresi, saat. sure = mesafe / hiz."""
    m, h = float(mesafe_km), float(hiz_kmh)
    if m < 0 or h <= 0:
        raise ValueError("mesafe ve hiz gecerli olmali")
    return m / h