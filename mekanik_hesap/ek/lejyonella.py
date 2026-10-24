"""Lejyonella risk skoru ve onlemler (KATALOG.md Ek, 5. hesap).

Dayanak: HTM 04-01 (sicak/soguk su guvenligi prensipleri).
Skor agirliklari pratik [STANDART-TEYIT]; sahada su guvenlik
plani esastir.
"""

from typing import Union

# Skor -> seviye esikleri [STANDART-TEYIT]
SEVIYE = ((34, "dusuk"), (66, "orta"), (100, "yuksek"))


def risk_skoru(
    sicaklik_c: Union[int, float],
    bekleme_gun: Union[int, float],
    dead_leg_m: Union[int, float],
) -> tuple[float, str]:
    """Risk skoru -> (skor 0-100, seviye).

    Sicaklik: 25-45 C yuksek risk; <20 veya >60 dusuk.
    Bekleme >7 gun ve dead-leg >2 m skoru artirir.
    """
    t, bek, dl = (float(sicaklik_c), float(bekleme_gun), float(dead_leg_m))
    if bek < 0 or dl < 0:
        raise ValueError("bekleme ve dead-leg negatif olamaz")
    if 25.0 <= t <= 45.0:
        skor = 40.0
    elif (20.0 <= t < 25.0) or (45.0 < t <= 50.0):
        skor = 20.0
    elif 50.0 < t <= 60.0:
        skor = 10.0
    else:
        skor = 0.0
    if bek > 7.0:
        skor += 30.0
    elif bek >= 3.0:
        skor += 15.0
    if dl > 2.0:
        skor += 30.0
    elif dl > 1.0:
        skor += 15.0
    skor = min(100.0, skor)
    for esik, ad in SEVIYE:
        if skor <= esik:
            return skor, ad
    return skor, "yuksek"


def onlem_listesi(seviye: str) -> list[str]:
    """Seviyeye gore onlem listesi (HTM 04-01 prensipleri)."""
    if str(seviye) not in ("dusuk", "orta", "yuksek"):
        raise ValueError("bilinmeyen seviye: %r" % (seviye,))
    onlem = ["sicak su >=60 C, dagitim >=55 C tut", "dead-legleri kaldir veya kisalt"]
    if seviye in ("orta", "yuksek"):
        onlem += [
            "haftalik dusuk kullanimli uclari purge et",
            "soguk su <20 C tut, izolasyonu kontrol et",
        ]
    if seviye == "yuksek":
        onlem += [
            "termal dezenfeksiyon uygula ve numune al",
            "su guvenlik planini gozden gecir",
        ]
    return onlem
