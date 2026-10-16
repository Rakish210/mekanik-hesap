"""Dogalgaz hesap motoru: TTT, HBK-hiz, isil genlesme, konsol.

Kaynak modul: Mekanik/App/modules/calc_gas.py (ayni formul ve davranis).
Dayanak: KATALOG.md Dogalgaz basligi (TS 7363, TS 13384).
Formuller:
- Hiz: V = 378 * Q / (P * D^2), Q m3/h, P bar, D mm, V m/s
- Isil genlesme: dL = Lo * a * dT, metre
- Konsol: Pmax = 885 * A * D / (L * EF), A cm2, D cm, L m, EF -, Pmax kg
"""


def ttt_toplam(kalemler):
    """kalemler: [(birim_tuketim, adet), ...] -> (toplam, detay_list)"""
    detay = []
    toplam = 0.0
    for birim, adet in kalemler:
        satir = float(birim) * float(adet)
        detay.append(satir)
        toplam += satir
    return toplam, detay


def hbk_hiz(Q, P, Dmm):
    """Hat ici gaz hizi, m/s."""
    Q = float(Q); P = float(P); Dmm = float(Dmm)
    if P <= 0 or Dmm <= 0:
        raise ValueError("P ve D pozitif olmali")
    return 378.0 * Q / (P * Dmm * Dmm)


def isil_genlesme(Lo, a, dT):
    """Isil uzama, metre."""
    return float(Lo) * float(a) * float(dT)


def konsol_pmax(A_cm2, D_cm, L_m, EF):
    """Konsol tasiyici yuk, kg."""
    A_cm2 = float(A_cm2); D_cm = float(D_cm); L_m = float(L_m); EF = float(EF)
    if L_m <= 0 or EF <= 0:
        raise ValueError("L ve EF pozitif olmali")
    return 885.0 * A_cm2 * D_cm / (L_m * EF)


def konsol_guvenli_mi(F, Pmax):
    """Tasiyici yuk guvenlik kontrolu."""
    return float(Pmax) > float(F)


# FAZ 4 ekleri: basin kaybi/sayac/baca/menfez/alarm hesaplari tek
# kaynak olarak `mekanik_hesap.gaz` modundedir; mevcut `gas`
# importlari bozulmamasi icin burada yeniden disari acilir.
from mekanik_hesap.gaz import (  # noqa: E402,F401
    alarm_zonu,
    baca_kesiti,
    basinc_kaybi,
    boru_capi,
    gaz_yogunlugu,
    havalandirma_menfezi,
    sayac_secimi,
)
