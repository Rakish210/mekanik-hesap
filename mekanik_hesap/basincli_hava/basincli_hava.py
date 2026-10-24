"""Basincli hava hesaplari (KATALOG.md 10. baslik, 4 hesap).

Dayanak: ISO 1217 (kompresor hacimsel debi deneyi),
TS EN 1012 (kompresor guvenligi). Tuketim toplama, tank ve
boru bagintilari genel muhendislik esaslidir; eszamanlilik ve
kayip kabulleri pratik [STANDART-TEYIT].
"""

import math
from typing import Optional, Union

def tuketim_toplam(kalemler: list[tuple[Union[int, float], Union[int, float]]],
                   eszamanlilik: float = 0.7,
                   kacak_pay: float = 0.1) -> float:
    """Toplam hava ihtiyaci, Nm3/h.

    kalemler: [(tuketim_Nm3h, adet), ...]; sonuc =
    toplam*eszamanlilik*(1+kacak).
    """
    top = 0.0
    for tuk, adet in kalemler:
        if float(tuk) < 0 or float(adet) < 0:
            raise ValueError("tuketim ve adet negatif olamaz")
        top += float(tuk) * float(adet)
    esz = float(eszamanlilik)
    kac = float(kacak_pay)
    if not (0 < esz <= 1.0) or kac < 0:
        raise ValueError("katsayilar gecerli olmali")
    return top * esz * (1.0 + kac)


def kompresor_secimi(ihtiyac_nm3h: float, yedek_pay: float = 0.1) -> float:
    """Kompresor kapasitesi, Nm3/h. Kapasite = ihtiyac*(1+yedek)."""
    iht, yed = float(ihtiyac_nm3h), float(yedek_pay)
    if iht <= 0 or yed < 0:
        raise ValueError("girisler gecerli olmali")
    return iht * (1.0 + yed)


def tank_hacmi(debi_m3min: float, dp_bar: float = 1.0,
               bos_sure_dk: float = 2.0,
               p_atm_bar: float = 1.0) -> float:
    """Hava tanki hacmi, L. V = Q*t*Patm/dp pratik bagintisi
    [STANDART-TEYIT]."""
    q_m3m, dp = float(debi_m3min), float(dp_bar)
    t_dk = float(bos_sure_dk)
    if q_m3m <= 0 or dp <= 0 or t_dk <= 0:
        raise ValueError("girisler pozitif olmali")
    return q_m3m * 1000.0 * t_dk * float(p_atm_bar) / dp


def boru_capi(debi_m3h: float, hiz_ms: float = 10.0,
              p_mutlak_bar: float = 8.0) -> float:
    """Basincli hava boru ic capi, mm. Gercek hacimsel debi
    Q_gercek = Q_normal/p_mutlak; d = kok(4Q/pi v).

    Hiz ve basinc kabulleri pratik [STANDART-TEYIT].
    """
    debi, hiz = float(debi_m3h), float(hiz_ms)
    pmut = float(p_mutlak_bar)
    if debi <= 0 or hiz <= 0 or pmut <= 0:
        raise ValueError("girisler pozitif olmali")
    q_ger = (debi / 3600.0) / pmut
    return math.sqrt(4.0 * q_ger / math.pi / hiz) * 1000.0


def basinc_kaybi(uzunluk_m: float, cap_mm: float, debi_m3h: float,
                 p_mutlak_bar: float = 8.0,
                 katsayi: float = 0.02) -> float:
    """Boru basinc kaybi gostergesi, bar. Olcek bagintisi:
    dp ~ k*L*Qn^2/(p*D^5) [STANDART-TEYIT]; karsi lastirmali
    on secim icindir, katalog ile dogrulanir."""
    l_m, d_mm = float(uzunluk_m), float(cap_mm)
    qn, pm = float(debi_m3h), float(p_mutlak_bar)
    k = float(katsayi)
    if l_m < 0 or d_mm <= 0 or qn <= 0 or pm <= 0 or k <= 0:
        raise ValueError("girisler gecerli olmali")
    return k * l_m * qn ** 2 / (pm * d_mm ** 5)


def kurutucu_secimi(debi_nm3h: float, artirim: float = 0.15) -> float:
    """Kurutucu/filtre kapasitesi, Nm3/h. Kapasite =
    debi*(1+artirim). Ciy noktasi sinifi projeye gore
    secilir [STANDART-TEYIT]."""
    debi = float(debi_nm3h)
    if debi <= 0:
        raise ValueError("debi pozitif olmali")
    return debi * (1.0 + float(artirim))