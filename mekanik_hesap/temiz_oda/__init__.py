"""Temiz oda hesaplari (KATALOG.md 12. baslik, 4 hesap).

Dayanak: ISO 14644-1 (siniflandirma), ISO 14644-2 (izleme),
ISO 14644-4 (tasarim). ACH tablosu, basinc kademesi, HEPA birim
debisi ve ic yuk kabulleri pratik olup [STANDART-TEYIT: ISO 14644-1/2/4] ile
isaretlidir; GMP/urun sinifi gereksinimi projede teyit edilir.
MACO (izin verilen azami tasima) temizlik validasyonu bagintisidir;
guvenlik faktoru urune gore secilir [STANDART-TEYIT: ISO 14644-1/2/4].
"""

import math
from typing import Optional, Union

# Sinifa gore tipik hava degisim sayisi, 1/h.
# Pratik aralik [STANDART-TEYIT: ISO 14644-1/2/4]; ISO 14644 sinif + geri kazanim
# suresine gore teyit edilir.
ACH_TABLOSU = {
    "ISO5": 300.0,
    "ISO6": 150.0,
    "ISO7": 60.0,
    "ISO8": 20.0,
}

RHO_HAVA = 1.2
CP_HAVA = 1.005


def ach_debi(hacim_m3: Union[int, float], ach: Union[int, float]) -> float:
    """Besleme debisi, m3/h. Q = V*ACH."""
    v, n = float(hacim_m3), float(ach)
    if v <= 0 or n <= 0:
        raise ValueError("hacim ve ACH pozitif olmali")
    return v * n


def sinif_debisi(hacim_m3: Union[int, float], iso_sinif: str = "ISO7") -> float:
    """Sinifa gore besleme debisi, m3/h. ACH tablosu pratik
    [STANDART-TEYIT: ISO 14644-1/2/4]."""
    if iso_sinif not in ACH_TABLOSU:
        raise ValueError("iso_sinif ISO5/ISO6/ISO7/ISO8 olmali")
    return ach_debi(hacim_m3, ACH_TABLOSU[iso_sinif])


def iso_ust_limit(sinif_n: Union[int, float], partikul_um: float = 0.5) -> float:
    """ISO 14644-1 ust limit konsantrasyonu, parcacik/m3.

    Cn = 10^N * (0.1/D)^2.08; D mikrometre, 0.1<=D<=5.
    """
    n = float(sinif_n)
    d = float(partikul_um)
    if not (1 <= n <= 9) or not (0.1 <= d <= 5.0):
        raise ValueError("sinif 1-9, cap 0.1-5 um olmali")
    return (10.0**n) * ((0.1 / d) ** 2.08)


def ornek_nokta(alan_m2: Union[int, float]) -> int:
    """Kalifikasyon en az ornekleme nokta sayisi, adet.

    ISO 14644-1: NL = kok(A), yukari yuvarlanir (A m2).
    """
    a = float(alan_m2)
    if a <= 0:
        raise ValueError("alan pozitif olmali")
    return int(math.ceil(math.sqrt(a)))


def basinc_kacak_debi(
    aciklik_m2: Union[int, float],
    dp_pa: float = 12.5,
    rho: float = RHO_HAVA,
    cd: float = 0.65,
) -> float:
    """Fark basincta kacis debisi, m3/h. Q = Cd*A*kok(2 dp/rho).

    Basinc kademesi (or. 10-15 Pa) ve Cd pratik kabul
    [STANDART-TEYIT: ISO 14644-1/2/4]; kapi/derz sizdirmazligina gore teyit edilir.
    """
    a, dp = float(aciklik_m2), float(dp_pa)
    if a <= 0 or dp <= 0 or float(rho) <= 0:
        raise ValueError("girisler pozitif olmali")
    q = float(cd) * a * math.sqrt(2.0 * dp / float(rho))
    return q * 3600.0


def hepa_sayisi(debi_m3h: Union[int, float], birim_m3h: float = 1000.0) -> int:
    """HEPA filtre adedi. Adet = tavan(debi/birim).

    Birim kapasite katalog degeridir [STANDART-TEYIT: ISO 14644-1/2/4].
    """
    debi, birim = float(debi_m3h), float(birim_m3h)
    if debi <= 0 or birim <= 0:
        raise ValueError("debi ve birim kapasite pozitif olmali")
    return int(math.ceil(debi / birim))


def isi_nem_yuku(
    debi_m3h: Union[int, float], dt_k: float = 5.0, dn_g_kg: float = 2.0
) -> tuple[float, float]:
    """Sicaklik ve nem kontrol yuku: (duyulur_kW, gizli_kW).

    Duyulur = rho*cp*Q*dT/3600; gizli = rho*Q*dn*h_fg/3600,
    h_fg = 2500 kJ/kg. dT ve nem farki proje kabuludur
    [STANDART-TEYIT: ISO 14644-1/2/4].
    """
    debi = float(debi_m3h)
    dt, dn = float(dt_k), float(dn_g_kg)
    if debi <= 0 or dt < 0 or dn < 0:
        raise ValueError("girisler gecerli olmali")
    duy = RHO_HAVA * CP_HAVA * (debi / 3600.0) * dt
    giz = RHO_HAVA * (debi / 3600.0) * (dn / 1000.0) * 2500.0
    return duy, giz


def maco(
    onceki_gunluk_doz_mg: Union[int, float],
    sonraki_gunluk_doz_mg: Union[int, float],
    parti_buyuklugu_kg: Union[int, float],
    paylasilan_alan_m2: Optional[Union[int, float]] = None,
    guvenlik: float = 1000.0,
    sonraki_parti_kg: Optional[Union[int, float]] = None,
) -> float:
    """MACO, mg. MACO = TDDa*MBS / (SF*TDDb).

    TDD: gunluk terapotik doz; MBS: sonraki parti buyuklugu (kg);
    SF: guvenlik faktoru (oral 1000 pratik). Doz ve SF urune gore
    secilir [STANDART-TEYIT: ISO 14644-1/2/4]; validasyon protokolunde teyit edilir.
    """
    tdda = float(onceki_gunluk_doz_mg)
    tddb = float(sonraki_gunluk_doz_mg)
    mbs = float(parti_buyuklugu_kg if sonraki_parti_kg is None else sonraki_parti_kg)
    sf = float(guvenlik)
    if tdda <= 0 or tddb <= 0 or mbs <= 0 or sf <= 0:
        raise ValueError("girisler pozitif olmali")
    _ = paylasilan_alan_m2
    return tdda * (mbs * 1000000.0) / (sf * tddb)
