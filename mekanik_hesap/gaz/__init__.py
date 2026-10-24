"""Dogalgaz hesap motoru: TTT, HBK-hiz, isil genlesme, konsol,
basin kaybi, boru capi, sayac, baca ve havalandirma menfezi,
alarm/selenoid zonu (KATALOG.md 8. baslik).

Dayanak: TS 7363 (ic tesisat), TS 13384 (baca). Basin kaybi
Darcy-Weisbach ile gaz yogunlugu uzerinden bulunur (fizik tabanli;
colebrook modulu kullanilir). TTT/HBK-hiz/isil-genlesme/konsol
formulleri kaynak modulden alinmistir.
"""

import math
from typing import Union

from mekanik_hesap import colebrook


def ttt_toplam(kalemler: list[tuple[Union[int, float], Union[int, float]]]
               ) -> tuple[float, list[float]]:
    """kalemler: [(birim_tuketim, adet), ...] -> (toplam, detay_list)"""
    detay = []
    toplam = 0.0
    for birim, adet in kalemler:
        satir = float(birim) * float(adet)
        detay.append(satir)
        toplam += satir
    return toplam, detay


def hbk_hiz(Q: Union[int, float], P: Union[int, float],
            Dmm: Union[int, float]) -> float:
    """Hat ici gaz hizi, m/s."""
    Q = float(Q); P = float(P); Dmm = float(Dmm)
    if P <= 0 or Dmm <= 0:
        raise ValueError("P ve D pozitif olmali")
    return 378.0 * Q / (P * Dmm * Dmm)


def isil_genlesme(Lo: Union[int, float], a: Union[int, float],
                  dT: Union[int, float]) -> float:
    """Isil uzama, metre."""
    return float(Lo) * float(a) * float(dT)


def konsol_pmax(A_cm2: Union[int, float], D_cm: Union[int, float],
                L_m: Union[int, float], EF: Union[int, float]) -> float:
    """Konsol tasiyici yuk, kg."""
    A_cm2 = float(A_cm2); D_cm = float(D_cm); L_m = float(L_m); EF = float(EF)
    if L_m <= 0 or EF <= 0:
        raise ValueError("L ve EF pozitif olmali")
    return 885.0 * A_cm2 * D_cm / (L_m * EF)


def konsol_guvenli_mi(F: Union[int, float], Pmax: Union[int, float]) -> bool:
    """Tasiyici yuk guvenlik kontrolu."""
    return float(Pmax) > float(F)


# FAZ 4 ekleri: basin kaybi/sayac/baca/menfez/alarm hesaplari tek
# kaynak olarak `mekanik_hesap.gaz` modundedir; mevcut `gas`
# importlari bozulmamasi icin burada yeniden disari acilir.

from mekanik_hesap import colebrook

# Kuru hava yogunlugu, kg/m3 (0 C, 101.325 kPa); dogalgaz bagil
# yogunlugu ~0.6 pratik kabul [STANDART-TEYIT].
_RHO_HAVA = 1.293
_GAZ_BAGIL = 0.6
_G = 9.81


def gaz_yogunlugu(basinc_mbar: Union[int, float]) -> float:
    """Isletme basincinda gaz yogunlugu, kg/m3 (izotermal ideal gaz)."""
    p = float(basinc_mbar)
    if p <= 0:
        raise ValueError("basinc pozitif olmali")
    return _RHO_HAVA * _GAZ_BAGIL * (1013.25 + p) / 1013.25


def basinc_kaybi(uzunluk_m: Union[int, float],
                 debi_m3h: Union[int, float],
                 cap_mm: Union[int, float],
                 basinc_mbar: Union[int, float],
                 puruzluluk_mm: Union[int, float] = 0.05,
                 zeta: Union[int, float] = 2.0) -> float:
    """Boru basin kaybi, mbar. Darcy-Weisbach + colebrook surtunmesi.

    Kademe (21/50/300 mbar) yogunluk uzerinden dikkate alinir.
    Puruzluluk ve yerel kayip katsayisi pratik [STANDART-TEYIT].
    """
    l_m = float(uzunluk_m)
    cap = float(cap_mm)
    if l_m < 0 or float(debi_m3h) < 0 or cap <= 0:
        raise ValueError("girisler gecerli olmali")
    rho = gaz_yogunlugu(basinc_mbar)
    d = cap / 1000.0
    # Debi normal m3/h -> isletme sartlarinda hiz
    q_isletme = float(debi_m3h) / 3600.0 * 1013.25 / (1013.25
                                                      + float(basinc_mbar))
    v = q_isletme / (math.pi * d * d / 4.0)
    if v <= 0:
        return 0.0
    mu = 1.1e-5  # dogalgaz dinamik viskozite, Pa.s (pratik)
    re = colebrook.reynolds(rho, v, d, mu)
    f = colebrook.colebrook(re, float(puruzluluk_mm) / 1000.0, d)
    dp_pa = (f * l_m / d + float(zeta)) * rho * v * v / 2.0
    return dp_pa / 100.0


def boru_capi(debi_m3h: Union[int, float],
              basinc_mbar: Union[int, float],
              hiz_sinir_ms: float = 6.0) -> float:
    """HBK boru capi, mm; bir ust standart capa yuvarlanir.

    V = 378*Q/(P*D2) bagintisindan hiz sinirini saglayan cap.
    Hiz siniri TS 7363 esasli pratik [STANDART-TEYIT].
    """
    q = float(debi_m3h)
    p_bar = (1013.25 + float(basinc_mbar)) / 1000.0
    v_lim = float(hiz_sinir_ms)
    if q <= 0 or p_bar <= 0 or v_lim <= 0:
        raise ValueError("girisler pozitif olmali")
    d_mm = math.sqrt(378.0 * q / (p_bar * v_lim))
    for cap in (15, 20, 25, 32, 40, 50, 65, 80, 100, 150, 200):
        if cap >= d_mm:
            return float(cap)
    return float(math.ceil(d_mm))


# Anma debisine gore sayac sinifi (m3/h), pratik secim
# [STANDART-TEYIT]; G serisi EN 1359 esaslidir.
_SAYAC = (("G4", 6.0), ("G6", 10.0), ("G10", 16.0), ("G16", 25.0),
          ("G25", 40.0), ("G40", 65.0), ("G65", 100.0),
          ("G100", 160.0))


def sayac_secimi(debi_m3h: Union[int, float]) -> str:
    """Sayac sinifi secimi. Debiyi karsilayan ilk G sinifi doner."""
    q = float(debi_m3h)
    if q <= 0:
        raise ValueError("debi pozitif olmali")
    for sinif, qmaks in _SAYAC:
        if q <= qmaks:
            return sinif
    raise ValueError("debi sayac araligini asiyor")


def havalandirma_menfezi(guc_kw: Union[int, float],
                         katsayi_cm2_kw: float = 3.0) -> float:
    """Havalandirma menfez alani, cm2. A = P*k.

    Katsayi TS 7363 esasli pratik kabul [STANDART-TEYIT]; alt/ust
    menfez dagilimi ve yerlesim sarti dagitim sirketi onayina tabidir.
    """
    p, k = float(guc_kw), float(katsayi_cm2_kw)
    if p <= 0 or k <= 0:
        raise ValueError("guc ve katsayi pozitif olmali")
    return p * k


def baca_kesiti(guc_kw: Union[int, float],
                katsayi_cm2_kw: float = 0.5) -> float:
    """Baca kesit alani, cm2. A = P*k (TS 13384 esasli pratik).

    Katsayi ve cekis sarti proje/baca raporuna gore teyit edilir
    [STANDART-TEYIT].
    """
    p, k = float(guc_kw), float(katsayi_cm2_kw)
    if p <= 0 or k <= 0:
        raise ValueError("guc ve katsayi pozitif olmali")
    return p * k


def alarm_zonu(cihaz_adet: int, zon_kapasite: int = 4) -> int:
    """Gaz alarm/selenoid vana zon sayisi. Pratik zon kapasitesi
    [STANDART-TEYIT]; yerlesim ve vana tipi projeye aittir."""
    adet = int(cihaz_adet)
    kap = int(zon_kapasite)
    if adet <= 0 or kap <= 0:
        raise ValueError("girisler pozitif olmali")
    return int(math.ceil(adet / kap))