"""Sehir iklim verisi: kis/yaz tasarim sicakliklari (C).

Kaynak notu: degerler TS 825 Ek-A iklim bolgeleri ve MGM genel
iklim verilerine dayanir; projenin bagli oldugu idare/gaz dagitim
sirketi degerleriyle TEYIT EDILMEDEN kullanilmaz. Bu yuzden tum
degerler [SEHIR-TEYIT] isaretlidir. Emin olunmayan sehir
EKlenMEZ; yeni sehir yalnizca dayanak notuyla eklenir.
"""

from typing import Union

# sehir -> (kis_tasarim_C, yaz_tasarim_C, kaynak_not) [SEHIR-TEYIT]
SEHIRLER = {
    "istanbul": (-3.0, 33.0, "TS 825 2. bolge kabulu [SEHIR-TEYIT]"),
    "ankara": (-12.0, 33.0, "TS 825 3. bolge kabulu [SEHIR-TEYIT]"),
    "izmir": (1.0, 36.0, "TS 825 1. bolge kabulu [SEHIR-TEYIT]"),
}


def sehirler() -> list[str]:
    """Kayitli sehir adlari listesi."""
    return sorted(SEHIRLER)


def tasarim_sicakligi(sehir: str
                      ) -> tuple[Union[int, float], Union[int, float], str]:
    """(kis_C, yaz_C, kaynak_not) doner. Bilinmeyen sehir KeyError."""
    ad = str(sehir).strip().lower()
    if ad not in SEHIRLER:
        raise KeyError("kayitli sehir degil [SEHIR-TEYIT]: %r" % (sehir,))
    return SEHIRLER[ad]


def kis_tasarim(sehir: str) -> Union[int, float]:
    """Kis dis tasarim sicakligi, C [SEHIR-TEYIT]."""
    return tasarim_sicakligi(sehir)[0]


def yaz_tasarim(sehir: str) -> Union[int, float]:
    """Yaz dis tasarim sicakligi, C [SEHIR-TEYIT]."""
    return tasarim_sicakligi(sehir)[1]