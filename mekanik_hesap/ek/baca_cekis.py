"""Baca cekisi ve yogusma kontrolu (KATALOG.md Ek, 2. hesap).

Dayanak: TS 13384 (baca tasarimi; cekis ve kesit hesabi).
Cekis: dp = p/R * (1/Tdis - 1/Tbaca) * g * H.
Yogusma esikleri pratik kabul [STANDART-TEYIT: TS 13384, TS 7363]; uretici ve
TS 13384 sartlari esastir.
"""

import math
from typing import Union

_R_HAVA = 287.0  # J/(kg.K)
_G = 9.81


def cekis(h_m: Union[int, float], t_baca_c: Union[int, float],
          t_dis_c: Union[int, float],
          p_pa: float = 101325.0) -> float:
    """Baca cekisi, Pa. Tbaca > Tdis olmalidir."""
    h = float(h_m)
    tb = float(t_baca_c) + 273.15
    td = float(t_dis_c) + 273.15
    p = float(p_pa)
    if h <= 0 or p <= 0:
        raise ValueError("yukseklik ve basinc pozitif olmali")
    if tb <= td:
        raise ValueError("baca gazi dis havadan sicak olmali")
    return p / _R_HAVA * (1.0 / td - 1.0 / tb) * _G * h


def yogusma_kontrol(t_baca_c: Union[int, float],
                    yakit: str = "dogalgaz"
                    ) -> tuple[bool, str]:
    """Yogusma riski -> (risk: bool, aciklama).

    Asit cig noktasi esikleri pratik [STANDART-TEYIT: TS 13384, TS 7363]:
    dogalgaz ~55 C, siviyakit ~130 C.
    """
    t = float(t_baca_c)
    esik = {"dogalgaz": 55.0, "lpg": 55.0, "motorin": 130.0,
            "fueloil": 140.0, "komur": 120.0, "pelet": 60.0}
    if str(yakit) not in esik:
        raise ValueError("bilinmeyen yakit: %r" % (yakit,))
    if t >= esik[str(yakit)]:
        return False, "yogusma riski dusuk"
    return True, "baca gazi esik altinda: yogusmali baca gerekir"


def baca_capi(debi_m3h: Union[int, float],
              hiz_ms: float = 4.0) -> float:
    """Baca ic capi, mm; bir ust 10 mm'ye yuvarlanir.

    Hiz kabulu pratik [STANDART-TEYIT: TS 13384, TS 7363]; TS 13384 basin kaybi
    sarti saglanmalidir.
    """
    debi, hiz = float(debi_m3h), float(hiz_ms)
    if debi <= 0 or hiz <= 0:
        raise ValueError("debi ve hiz pozitif olmali")
    d_mm = math.sqrt(4.0 * (debi / 3600.0) / math.pi / hiz) * 1000.0
    return float(math.ceil(d_mm / 10.0) * 10)