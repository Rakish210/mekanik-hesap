"""Gurultu ve NC karsilastirmasi (KATALOG.md Ek, 4. hesap).

Fan ses gucu ampirik kestirimdir [STANDART-TEYIT]; uretici
oktaiv bant verisi esastir. NC hedefleri pratik [STANDART-TEYIT].
"""

import math
from typing import Union

# Mahal turu -> hedef NC [STANDART-TEYIT]
NC_HEDEF = {
    "yatak_odasi": 30, "hastane": 30, "konut": 30, "ofis": 35,
    "sinif": 35, "toplanti": 35, "lokanta": 40, "avm": 40,
    "spor": 45, "atolye": 50,
}


def fan_guc_duzeyi(debi_m3h: Union[int, float],
                   basinc_pa: Union[int, float]) -> float:
    """Fan ses guc duzeyi kestirimi, dBA.

    LwA = 10*log10(Q) + 20*log10(P) - 8 (Q: m3/h, P: Pa).
    Ampirik [STANDART-TEYIT]; ayni sinif fanlar icin kiyaslama.
    """
    q, p = float(debi_m3h), float(basinc_pa)
    if q <= 0 or p <= 0:
        raise ValueError("debi ve basinc pozitif olmali")
    return 10.0 * math.log10(q) + 20.0 * math.log10(p) - 8.0


def kanal_degerlendirme(hiz_ms: Union[int, float]) -> tuple[str, str]:
    """Kanal hizina gore gurultu degerlendirmesi [STANDART-TEYIT].

    -> (durum, aciklama). Sinir: 3 m/s sessiz, 5 m/s kabul.
    """
    hiz = float(hiz_ms)
    if hiz <= 0:
        raise ValueError("hiz pozitif olmali")
    if hiz <= 3.0:
        return "sessiz", "dusuk hiz: gurultu riski dusuk"
    if hiz <= 5.0:
        return "kabul", "normal hiz: menfez secimine dikkat"
    return "gurultulu", "yuksek hiz: kesit buyut veya susturucu"


def nc_karsilastir(olculen_dba: Union[int, float],
                   mahal: str = "ofis") -> tuple[int, bool, str]:
    """Olculen dBA'yi mahal NC hedefine karsilastir.

    Yaklasik cevrim NC ~ dBA - 7 [STANDART-TEYIT].
    -> (hedef_NC, uygun: bool, aciklama).
    """
    dba = float(olculen_dba)
    if dba <= 0:
        raise ValueError("dBA pozitif olmali")
    if str(mahal) not in NC_HEDEF:
        raise ValueError("bilinmeyen mahal: %r" % (mahal,))
    hedef = NC_HEDEF[str(mahal)]
    nc = dba - 7.0
    if nc <= hedef:
        return hedef, True, "saglaniyor"
    return hedef, False, "asiliyor: susturucu/hiz dusurme gerekir"