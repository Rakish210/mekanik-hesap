"""Yardimci 5/7: MMO proje bedeli onhesabi.

Dayanak: [STANDART-TEYIT]. Baginti basit ve seffaftir:
bedel = alan_m2 * birim_fiyat_TL_m2 * sinif_katsayi.
Sinif katsayilari ve birim fiyat pratik kabuldur; MMO guncel
tarife ve sartnamesi ile TEYIT EDILMEDEN sozlesmede
kullanilmaz. Standart uydurulmaz.
"""

from typing import Optional, Union

# Yapi sinifi -> katsayi, pratik onhesap [STANDART-TEYIT].
SINIF_KATSAYI = {
    "konut": 1.0,
    "ofis": 1.1,
    "otel": 1.2,
    "hastane": 1.35,
    "avm": 1.25,
    "endustriyel": 1.3,
    "egitim": 1.1,
}

KDV_ORAN = 0.20  # pratik kabul [STANDART-TEYIT], guncel oran teyit edilir.


def siniflar() -> list[str]:
    """Kayitli yapi sinif adlari listesi."""
    return sorted(SINIF_KATSAYI)


def proje_bedeli(
    alan_m2: Union[int, float],
    birim_fiyat_tl_m2: Union[int, float],
    sinif: str = "konut",
    katsayi: Optional[Union[int, float]] = None,
) -> float:
    """Proje bedeli, TL. bedel = alan * birim_fiyat * katsayi.

    katsayi verilirse tablo yerine kullanilir; verilmezse sinif
    tablosundan alinir. Bilinmeyen sinif ValueError verir.
    """
    alan = float(alan_m2)
    fiyat = float(birim_fiyat_tl_m2)
    if alan <= 0 or fiyat <= 0:
        raise ValueError("alan ve birim fiyat pozitif olmali")
    if katsayi is None:
        key = str(sinif).strip().lower()
        if key not in SINIF_KATSAYI:
            raise ValueError("bilinmeyen sinif: %r" % (sinif,))
        k = SINIF_KATSAYI[key]
    else:
        k = float(katsayi)
        if k <= 0:
            raise ValueError("katsayi pozitif olmali")
    return alan * fiyat * k


def kdv_dahil(bedel_tl: Union[int, float], kdv_oran: float = KDV_ORAN) -> float:
    """KDV dahil bedel, TL. dahil = bedel * (1 + oran)."""
    b = float(bedel_tl)
    oran = float(kdv_oran)
    if b < 0 or not (0 <= oran <= 1.0):
        raise ValueError("bedel ve oran gecerli olmali")
    return b * (1.0 + oran)


def birim_alana_bedel(bedel_tl: Union[int, float], alan_m2: Union[int, float]) -> float:
    """m2 basina bedel, TL/m2. bedel / alan."""
    b, a = float(bedel_tl), float(alan_m2)
    if b < 0 or a <= 0:
        raise ValueError("bedel ve alan gecerli olmali")
    return b / a
