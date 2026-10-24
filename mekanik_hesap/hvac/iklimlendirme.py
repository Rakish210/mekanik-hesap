"""Iklimlendirme hesaplari (KATALOG.md 2. baslik, 12 hesap).

Dayanak: ASHRAE Handbook Fundamentals (sogutma yuku bilesen toplami),
TS EN 13779 (hava debileri). Katalog karsilastirmalari ve dagitim
katsayilari pratik/ampiriktir, [STANDART-TEYIT: TS EN 13779, ASHRAE Handbook] ile isaretlidir.
"""

import math
from typing import Union

_HAVA_HACIMSEL = 1.2 * 1.005 / 3600.0  # kW per (m3/h*K): ~0.000335
_SU_KATSAYI = 1.161  # kW per (m3/h*K), su


def sogutma_yuku(bilesenler_w: list[Union[int, float]],
                 emniyet: float = 0.10) -> float:
    """Sogutma yuku, W. ASHRAE bilesen toplami + emniyet.

    bilesenler_w: [iletim, ic kazanc, aydinlatma, insan, havalandirma...].
    """
    if not bilesenler_w or any(float(b) < 0 for b in bilesenler_w):
        raise ValueError("bilesen yukleri gecerli olmali")
    toplam = sum(float(b) for b in bilesenler_w)
    return toplam * (1.0 + float(emniyet))


def fancoil_secimi(q_oda_w: Union[int, float],
                   katalog_w: list[Union[int, float]],
                   emniyet: float = 1.1) -> float:
    """Fancoil secimi: yuku karsilayan ilk katalog cihazi, W.

    [STANDART-TEYIT: TS EN 13779, ASHRAE Handbook]: uretici katalog eslestirmesi pratiktir.
    """
    hedef = float(q_oda_w) * float(emniyet)
    if hedef <= 0 or not katalog_w:
        raise ValueError("yuk ve katalog gecerli olmali")
    for kap in sorted(float(k) for k in katalog_w):
        if kap >= hedef:
            return kap
    raise ValueError("katalogda yeterli cihaz yok")


def santral_debi(q_kw: Union[int, float], dt_k: float = 8.0) -> float:
    """Klima santrali hava debisi, m3/h. V = Q/(rho*cp*dT)."""
    q_kw, dt_k = float(q_kw), float(dt_k)
    if q_kw <= 0 or dt_k <= 0:
        raise ValueError("yuk ve sicaklik farki pozitif olmali")
    return q_kw / (_HAVA_HACIMSEL * dt_k)


def vrf_dagilimi(ic_kapasiteler_kw: list[Union[int, float]],
                 diversity: float = 0.9) -> float:
    """VRF dis unite kapasitesi, kW. Pratik cesitlilik katsayili."""
    if not ic_kapasiteler_kw:
        raise ValueError("ic unite listesi bos olamaz")
    toplam = sum(float(k) for k in ic_kapasiteler_kw)
    if toplam <= 0 or not (0 < float(diversity) <= 1.0):
        raise ValueError("girisler gecerli olmali")
    return toplam * float(diversity)


def chiller_kapasite(q_toplam_kw: Union[int, float],
                     emniyet: float = 0.10) -> float:
    """Chiller kapasitesi, kW. Toplam + emniyet (pratik secim)."""
    if float(q_toplam_kw) <= 0:
        raise ValueError("toplam yuk pozitif olmali")
    return float(q_toplam_kw) * (1.0 + float(emniyet))


def kule_kapasite(q_chiller_kw: Union[int, float],
                  p_komp_kw: Union[int, float],
                  dt_k: float = 5.0) -> tuple[float, float]:
    """Sogutma kulesi: (rejeksiyon_kW, su_debisi_m3h). Qrej = Q + P."""
    q_ch, p_k = float(q_chiller_kw), float(p_komp_kw)
    dt_k = float(dt_k)
    if q_ch <= 0 or p_k < 0 or dt_k <= 0:
        raise ValueError("girisler gecerli olmali")
    qrej = q_ch + p_k
    return qrej, qrej / (_SU_KATSAYI * dt_k)


def nem_miktari(debi_m3h: Union[int, float],
                dx_grkg: Union[int, float],
                rho: float = 1.2) -> float:
    """Nemlendirme/nem alma kapasitesi, kg/h. m = V*rho*dx."""
    debi, dx = float(debi_m3h), float(dx_grkg)
    if debi <= 0 or dx < 0:
        raise ValueError("girisler gecerli olmali")
    return debi * float(rho) * dx / 1000.0


def soguk_su_boru(debi_m3h: Union[int, float],
                  hiz_ms: float = 1.0) -> float:
    """Soguk su boru capi, mm; bir ust standart capa yuvarlanir."""
    debi_m3h, hiz_ms = float(debi_m3h), float(hiz_ms)
    if debi_m3h <= 0 or hiz_ms <= 0:
        raise ValueError("debi ve hiz pozitif olmali")
    d_mm = math.sqrt(4.0 * (debi_m3h / 3600.0) / math.pi / hiz_ms) * 1000.0
    for cap in (15, 20, 25, 32, 40, 50, 65, 80, 100, 125, 150, 200):
        if cap >= d_mm:
            return float(cap)
    return float(math.ceil(d_mm))


def kondens_drenaj(q_kw: Union[int, float]) -> int:
    """Kondens drenaj capi, mm. Pratik tablo [STANDART-TEYIT: TS EN 13779, ASHRAE Handbook]."""
    q = float(q_kw)
    if q <= 0:
        raise ValueError("kapasite pozitif olmali")
    if q <= 7:
        return 20
    if q <= 20:
        return 25
    if q <= 60:
        return 32
    return 40


def kanal_kesiti(debi_m3h: Union[int, float],
                 hiz_ms: float = 5.0) -> tuple[float, float]:
    """Hava kanali kesiti, m2 ve esdeger dairesel cap, mm."""
    debi_m3h, hiz_ms = float(debi_m3h), float(hiz_ms)
    if debi_m3h <= 0 or hiz_ms <= 0:
        raise ValueError("debi ve hiz pozitif olmali")
    alan = (debi_m3h / 3600.0) / hiz_ms
    cap_mm = math.sqrt(4.0 * alan / math.pi) * 1000.0
    return alan, cap_mm


def menfez_adet(debi_m3h: Union[int, float],
                menfez_m3h: Union[int, float]) -> int:
    """Menfez/difuzor adedi. Pratik katalog eslestirme [STANDART-TEYIT: TS EN 13779, ASHRAE Handbook]."""
    debi, kap = float(debi_m3h), float(menfez_m3h)
    if debi <= 0 or kap <= 0:
        raise ValueError("debiler pozitif olmali")
    return int(math.ceil(debi / kap))


def taze_hava_orani(v_taze_m3h: Union[int, float],
                    v_toplam_m3h: Union[int, float]) -> float:
    """Taze hava orani, %. TS EN 13779 debi orani."""
    v_taze, v_top = float(v_taze_m3h), float(v_toplam_m3h)
    if v_taze < 0 or v_top <= 0 or v_taze > v_top:
        raise ValueError("debiler gecerli olmali")
    return 100.0 * v_taze / v_top