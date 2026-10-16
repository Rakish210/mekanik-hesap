"""Yardimci 1/7: birim cevirici (units sarmalasi).

Dayanak: SI birim sistemi [STANDART-TEYIT]. Bu modul formul
uretmez; mekanik_hesap.units fonksiyonlarini katalog kalemi
olarak sarar.
"""

from mekanik_hesap.units import convert, c_to_k, k_to_c


def birim_cevir(deger, kaynak_birim, hedef_birim):
    """Birim cevirir. Ornek: birim_cevir(1000, "mm", "m") -> 1.0.

    Gecerli birimler: mm/cm/m/km, pa/kpa/bar/mbar/mmhg/mss,
    m3s/m3h/ls/lmin, w/kw/mw, j/kj/kwh/kcal. Sicaklik burada
    yoktur; c_to_k / k_to_c kullanilir.
    """
    return convert(deger, kaynak_birim, hedef_birim)


def santigrat_to_kelvin(t_c):
    """Santigradi kelvine cevirir."""
    return c_to_k(t_c)


def kelvin_to_santigrat(t_k):
    """Kelvini santigrada cevirir."""
    return k_to_c(t_k)
