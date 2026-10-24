"""Sismik aski hesabi (KATALOG.md Ek, 3. hesap).

Dayanak: TBDY (bina disi/mekanik donanim esdeger sismik yuk).
Formul sadelestirilmis pratik: F_yatay = W * SDS * I / Rp.
Katsayi kabulleri proje ve TBDY Bolum 6'ya gore secilir
[STANDART-TEYIT: TS 498, Eurocode 8]; nihai tahkik statik projeye aittir.
"""

from typing import Union

# DN'ye gore pratik max aski araligi, m [STANDART-TEYIT: TS 498, Eurocode 8]
ASKI_MESAFE = {
    15: 2.0,
    20: 2.0,
    25: 2.5,
    32: 2.5,
    40: 3.0,
    50: 3.0,
    65: 3.5,
    80: 3.5,
    100: 4.0,
    125: 4.0,
    150: 4.5,
    200: 5.0,
}


def sismik_kuvvet(
    agirlik_kg: Union[int, float],
    sds: Union[int, float],
    onem: Union[int, float] = 1.0,
    rp: Union[int, float] = 2.5,
) -> float:
    """Yatay esdeger sismik kuvvet, N.

    agirlik_kg: askiya gelen toplam agirlik (boru+su+izolasyon);
    sds: kisa periyot tasarim katsayisi; onem: bina onem katsayisi.
    """
    w, s, i, r = (float(agirlik_kg), float(sds), float(onem), float(rp))
    if w <= 0 or s <= 0 or i <= 0 or r <= 0:
        raise ValueError("girisler pozitif olmali")
    return w * 9.81 * s * i / r


def aski_tasarim_yuku(
    agirlik_kg: Union[int, float],
    sds: Union[int, float],
    onem: Union[int, float] = 1.0,
    rp: Union[int, float] = 2.5,
) -> tuple[float, float, float]:
    """Aski tasarim yuku -> (dusey_N, yatay_N, bileske_N).

    Dusey = agirlik; yatay = sismik kuvvet; bileske vektorel.
    """
    import math as _m

    w = float(agirlik_kg)
    dusey = w * 9.81
    yatay = sismik_kuvvet(w, sds, onem, rp)
    return dusey, yatay, _m.sqrt(dusey**2 + yatay**2)


def max_aski_mesafe(dn: int) -> float:
    """DN'ye gore max aski araligi, m [STANDART-TEYIT: TS 498, Eurocode 8]."""
    d = int(dn)
    if d not in ASKI_MESAFE:
        raise ValueError("tabloda yok DN: %r" % (dn,))
    return ASKI_MESAFE[d]
