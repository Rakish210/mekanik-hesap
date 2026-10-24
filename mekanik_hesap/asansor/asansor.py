"""Asansor hesaplari (KATALOG.md 9. baslik, 2 hesap).

Dayanak: TS EN 81-20/50 (asansor yapim guvenligi),
TS EN ISO 4190 (kabin/kuyu olculeri dizisi). Trafik
hesabinda sefer suresi klasik RTT bagintisidir; doluluk ve
kapi suresi kabulleri pratik [STANDART-TEYIT].
"""

from typing import Optional, Union

# EN ISO 4190 esasli yaygin tip dizisi [STANDART-TEYIT]: (kisi, yuk_kg)
_TIP: list[tuple[int, int]] = [(4, 320), (6, 450), (8, 630), (10, 800), (13, 1000)]


def tip_secimi(kisi: Optional[Union[int, float]] = None,
               yuk_kg: Optional[Union[int, float]] = None) -> tuple[float, float]:
    """Kabin tipi: (kisi, yuk_kg). Kisi veya yukten bir ust tipe
    yuvarlanir. Olcu detaylari katalogdan secilir."""
    if kisi is None and yuk_kg is None:
        raise ValueError("kisi veya yuk verilmelidir")
    for kisi_t, yuk_t in _TIP:
        if kisi is not None and float(kisi) <= kisi_t:
            return float(kisi_t), float(yuk_t)
        if kisi is None and yuk_kg is not None and float(yuk_kg) <= yuk_t:
            return float(kisi_t), float(yuk_t)
    raise ValueError("kapasite tip dizisini asiyor")


def sefer_suresi(kat: int, kat_arasi_m: float, hiz_ms: float,
                 kapi_sure_s: float = 10.0,
                 durak_sayisi: Optional[Union[int, float]] = None) -> float:
    """Tek sefer suresi (RTT), s. RTT = 2*H/v + durak*kapi.

    H: toplam seyir yuksekligi; durak verilmezse 2*kat/3 pratik
    kabul [STANDART-TEYIT].
    """
    kat_n = int(kat)
    h_m = kat_n * float(kat_arasi_m)
    v_ms = float(hiz_ms)
    tkapi = float(kapi_sure_s)
    if kat_n < 2 or h_m <= 0 or v_ms <= 0 or tkapi < 0:
        raise ValueError("girisler gecerli olmali")
    durak = float(durak_sayisi) if durak_sayisi else (2.0 * kat_n / 3.0)
    return 2.0 * h_m / v_ms + durak * tkapi


def tasiyabilirlik(kabin_kisi: float, sefer_sure_s: float,
                   doluluk: float = 0.7) -> float:
    """5 dk tasiyabilirlik, kisi. P = kabin*doluluk*300/RTT.
    Pratik doluluk kabulu [STANDART-TEYIT]."""
    kab = float(kabin_kisi)
    rtt = float(sefer_sure_s)
    dol = float(doluluk)
    if kab <= 0 or rtt <= 0 or not (0 < dol <= 1.0):
        raise ValueError("girisler gecerli olmali")
    return kab * dol * 300.0 / rtt