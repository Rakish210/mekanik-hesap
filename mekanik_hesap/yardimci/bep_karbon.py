"""Yardimci 7/7: BEP birincil enerji ve karbon onhesabi.

Dayanak: [STANDART-TEYIT]. Bagintilar basit ve seffaftir:
birincil_enerji = tuketim_kWh * cevrim_katsayi;
emisyon_kgCO2 = tuketim_kWh * emisyon_faktoru.
Katsayi ve faktorler pratik kabuldur; BEP hesabi ve ulusal
katsayilar ile TEYIT EDILMEDEN belgelendirmede kullanilmaz.
Standart uydurulmaz.
"""

from typing import Optional, Union

# yakit -> (cevrim_katsayi, kgCO2/kWh) pratik [STANDART-TEYIT].
YAKIT_KATSAYI = {
    "elektrik": (2.36, 0.44),
    "dogalgaz": (1.0, 0.202),
    "lpg": (1.0, 0.227),
    "motorin": (1.0, 0.267),
    "fueloil": (1.0, 0.279),
    "komur": (1.0, 0.341),
    "pelet": (1.0, 0.016),
}


def yakitlar() -> list[str]:
    """Kayitli yakit adlari listesi."""
    return sorted(YAKIT_KATSAYI)


def birincil_enerji(tuketim_kwh: Union[int, float],
                    yakit: str = "dogalgaz",
                    cevrim: Optional[Union[int, float]] = None) -> float:
    """Birincil enerji, kWh. tuketim * cevrim_katsayi.

    cevrim verilirse tablo yerine kullanilir.
    """
    t = float(tuketim_kwh)
    if t < 0:
        raise ValueError("tuketim negatif olamaz")
    key = str(yakit).strip().lower()
    if cevrim is None:
        if key not in YAKIT_KATSAYI:
            raise ValueError("bilinmeyen yakit: %r" % (yakit,))
        k = YAKIT_KATSAYI[key][0]
    else:
        k = float(cevrim)
        if k <= 0:
            raise ValueError("cevrim katsayisi pozitif olmali")
    return t * k


def karbon_emisyon(tuketim_kwh: Union[int, float],
                   yakit: str = "dogalgaz",
                   faktor: Optional[Union[int, float]] = None) -> float:
    """Karbon emisyonu, kgCO2. tuketim_kWh * faktor."""
    t = float(tuketim_kwh)
    if t < 0:
        raise ValueError("tuketim negatif olamaz")
    key = str(yakit).strip().lower()
    if faktor is None:
        if key not in YAKIT_KATSAYI:
            raise ValueError("bilinmeyen yakit: %r" % (yakit,))
        f = YAKIT_KATSAYI[key][1]
    else:
        f = float(faktor)
        if f < 0:
            raise ValueError("faktor negatif olamaz")
    return t * f


def toplam_emisyon(kalemler_kwh: list[tuple[str, Union[int, float]]]) -> float:
    """Yakit kalemleri [(yakit, kwh)] -> toplam kgCO2."""
    toplam = 0.0
    for yakit, kwh in kalemler_kwh:
        toplam += karbon_emisyon(kwh, yakit)
    return toplam


def birim_alan_gosterge(deger: Union[int, float],
                        alan_m2: Union[int, float]) -> float:
    """m2 basina gosterge: deger / alan (kWh/m2 veya kgCO2/m2)."""
    d, a = float(deger), float(alan_m2)
    if d < 0 or a <= 0:
        raise ValueError("girisler gecerli olmali")
    return d / a