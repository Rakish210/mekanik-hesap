"""Yardimci 2/7: surtunme faktoru (colebrook sarmalasi).

Dayanak: Colebrook (1939) deneysel baginti, Haaland (1983) acik
yaklasim [STANDART-TEYIT]. Bu modul formul uretmez;
mekanik_hesap.colebrook fonksiyonlarini katalog kalemi olarak
sarar ve Darcy-Weisbach basin kaybini ekler.
"""

from mekanik_hesap.colebrook import reynolds, haaland, colebrook


def reynolds_sayisi(rho, hiz_ms, cap_m, mu):
    """Reynolds sayisi: rho (kg/m3), hiz (m/s), cap (m), mu (Pa.s)."""
    return reynolds(rho, hiz_ms, cap_m, mu)


def surtunme_faktoru(Re, puruzluluk_m, cap_m):
    """Surtunme faktoru. Re < 2300 laminer (64/Re), aksi halde
    Colebrook-White cozumudur."""
    return colebrook(Re, puruzluluk_m, cap_m)


def haaland_faktoru(Re, puruzluluk_m, cap_m):
    """Haaland acik formu. Turbulansli akis (Re >= 2300) ister."""
    return haaland(Re, puruzluluk_m, cap_m)


def darcy_kayip(f, uzunluk_m, cap_m, rho, hiz_ms):
    """Darcy-Weisbach basin kaybi, Pa. dp = f*(L/D)*rho*V^2/2."""
    ff, l_m, d = float(f), float(uzunluk_m), float(cap_m)
    r, v = float(rho), float(hiz_ms)
    if ff <= 0 or l_m < 0 or d <= 0 or r <= 0 or v < 0:
        raise ValueError("f, L, D, rho gecerli; hiz negatif olamaz")
    return ff * (l_m / d) * r * v * v / 2.0
