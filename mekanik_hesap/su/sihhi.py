"""Sihhi tesisat hesaplari (KATALOG.md 4. baslik, 13 hesap).

Dayanak: TS EN 806 (bina ici temiz su tesisati), DIN 1988
(boru capi tayini ve hiz sinirlari), TS EN 12056 (pis su ve
yagmur suyu drenaji). Mahal tuketim ve cihaz birim debi
katalog degerleri projeye gore secilir [STANDART-TEYIT];
standart uydurulmaz.
"""

import math
from typing import Union

_STANDART_CAP = (15, 20, 25, 32, 40, 50, 65, 80, 100, 125, 150, 200)

# Pratik cihaz birim debileri, L/s [STANDART-TEYIT]
CIHAZ_DEBI = {
    "lavabo": 0.10, "klozet": 0.15, "dus": 0.15, "banyo": 0.20,
    "eviye": 0.15, "bulasik": 0.15, "camasir": 0.20, "pisuvar": 0.10,
}


def cihaz_toplam_debi(cihazlar: list[tuple[str, Union[int, float]]]) -> float:
    """Cihaz listesi [(ad, adet)] -> toplam kurulu debi, L/s."""
    toplam = 0.0
    for ad, adet in cihazlar:
        if str(ad) not in CIHAZ_DEBI:
            raise ValueError("bilinmeyen cihaz: %r" % (ad,))
        if float(adet) < 0:
            raise ValueError("adet negatif olamaz")
        toplam += CIHAZ_DEBI[str(ad)] * float(adet)
    return toplam


def temiz_su_boru_capi(debi_ls: Union[int, float],
                       hiz_ms: float = 1.5) -> float:
    """Temiz su boru capi, mm; bir ust standart capa yuvarlanir.

    Q = A*v bagintisi. Hiz siniri DIN 1988 esasli pratik
    (dagitimda ~1.0-2.0 m/s); secim projeye aittir [STANDART-TEYIT].
    """
    debi, hiz = float(debi_ls), float(hiz_ms)
    if debi <= 0 or hiz <= 0:
        raise ValueError("debi ve hiz pozitif olmali")
    d_mm = math.sqrt(4.0 * (debi / 1000.0) / math.pi / hiz) * 1000.0
    for cap in _STANDART_CAP:
        if cap >= d_mm:
            return float(cap)
    return float(math.ceil(d_mm))


def hidrofor(debi_m3h: Union[int, float], h_geo_m: Union[int, float],
             kayip_mss: Union[int, float], p_min_bar: float = 2.0
             ) -> tuple[float, float, float]:
    """Hidrofor secimi: (debi_m3h, basinc_mSS, basinc_bar).

    H = Hgeo + kayip + p_min donusumu. TS EN 806 basinc
    gereksinimi esasli; bina kayip katsayisi pratik.
    """
    q, hg, hk = float(debi_m3h), float(h_geo_m), float(kayip_mss)
    pmin = float(p_min_bar)
    if q <= 0 or hg < 0 or hk < 0 or pmin <= 0:
        raise ValueError("girisler gecerli olmali")
    h_mss = hg + hk + pmin * 10.2
    return q, h_mss, h_mss / 10.2


def su_deposu(kisi: Union[int, float], tuketim_l_gun: float = 150.0,
              gun: float = 1.0) -> float:
    """Su deposu hacmi, L. V = n*q*t. Tuketim kabulu pratik."""
    n, q, t = float(kisi), float(tuketim_l_gun), float(gun)
    if n <= 0 or q <= 0 or t <= 0:
        raise ValueError("girisler pozitif olmali")
    return n * q * t


def pis_su_boru_cap(debi_ls: Union[int, float],
                    egim_oran: float = 0.02) -> float:
    """Pis su boru capi, mm. TS EN 12056 esasli pratik secim.

    [STANDART-TEYIT]: parsel ici minimum cap ve egim tablosu
    icin; burada debi araligina gore cap onerilir.
    """
    debi = float(debi_ls)
    egim = float(egim_oran)
    if debi <= 0 or egim <= 0:
        raise ValueError("debi ve egim pozitif olmali")
    if debi <= 2.5:
        return 110.0
    if debi <= 6.0:
        return 125.0
    if debi <= 12.0:
        return 160.0
    return 200.0


def yagmur_suyu(alan_m2: Union[int, float],
                yagis_mm_h: float = 150.0) -> float:
    """Yagmur suyu debisi, L/s. Q = A*i/3600. TS EN 12056.

    Yagis siddeti yerel idare/MGM verisinden secilir
    [STANDART-TEYIT]; varsayilan pratiktir.
    """
    alan, yagis = float(alan_m2), float(yagis_mm_h)
    if alan <= 0 or yagis <= 0:
        raise ValueError("alan ve yagis pozitif olmali")
    return alan * yagis / 3600.0


def yag_tutucu(debi_ls: Union[int, float],
               bekleme_dk: float = 3.0) -> float:
    """Yag tutucu hacmi, L. V = Q*t (bekleme suresi pratik)."""
    debi, bek = float(debi_ls), float(bekleme_dk)
    if debi <= 0 or bek <= 0:
        raise ValueError("girisler pozitif olmali")
    return debi * bek * 60.0


def fosseptik(kisi: Union[int, float], gun: float = 1.0,
              kisi_basi_l: float = 120.0) -> float:
    """Fosseptik hacmi, L. V = n*q*t. [STANDART-TEYIT]: sizdirmazlik ve
    bolme sartlari yerel idare onayina tabidir."""
    n, t, q = float(kisi), float(gun), float(kisi_basi_l)
    if n <= 0 or t <= 0 or q <= 0:
        raise ValueError("girisler pozitif olmali")
    return n * q * t


def dalgic_pompa(debi_m3h: Union[int, float],
                 yukseklik_m: Union[int, float],
                 verim: float = 0.6) -> float:
    """Pis su dalgic pompa mil gucu, kW. P = rho*g*Q*H/eta."""
    q, h = float(debi_m3h), float(yukseklik_m)
    eta = float(verim)
    if q <= 0 or h <= 0 or not (0 < eta <= 1.0):
        raise ValueError("girisler gecerli olmali")
    return 1000.0 * 9.81 * (q / 3600.0) * h / eta / 1000.0


def sicak_su_sirkulasyon(q_kayip_kw: Union[int, float],
                         dt_k: float = 5.0) -> float:
    """Sicak su sirkulasyon debisi, m3/h. Q = P/(1.161*dT)."""
    p, dt = float(q_kayip_kw), float(dt_k)
    if p <= 0 or dt <= 0:
        raise ValueError("kayip ve dT pozitif olmali")
    return p / (1.161 * dt)


def boyler(kisi: Union[int, float], kisi_basi_l: float = 50.0,
           t_soguk: float = 10.0, t_sicak: float = 60.0,
           isitma_saati: float = 2.0) -> tuple[float, float]:
    """Boyler: (hacim_L, isitici_kW). Hacim kisi basina pratik;
    guc Q = m*c*dT/t. [STANDART-TEYIT]: kisi basi tuketim icin."""
    n = float(kisi)
    dt = float(t_sicak) - float(t_soguk)
    t_h = float(isitma_saati)
    if n <= 0 or dt <= 0 or t_h <= 0 or float(kisi_basi_l) <= 0:
        raise ValueError("girisler gecerli olmali")
    hacim = n * float(kisi_basi_l)
    guc = hacim * 1.161 * dt / 1000.0 / t_h
    return hacim, guc


def yumusatma(debi_m3h: Union[int, float],
              sertlik_giris_fr: float = 30.0,
              sertlik_cikis_fr: float = 5.0,
              calisma_saat: float = 8.0,
              recine_kapasite_m3fr: float = 50.0) -> float:
    """Su yumusatma: gunluk tuz yukune gore recine hacmi, L.

    Yuzeyel hesap: tutulan sertlik = Q*t*(gin-gout); recine_L =
    tutulan / kapasite * 1000. Katalog degerleri pratik
    [STANDART-TEYIT].
    """
    q = float(debi_m3h)
    dsert = float(sertlik_giris_fr) - float(sertlik_cikis_fr)
    t_h = float(calisma_saat)
    kap = float(recine_kapasite_m3fr)
    if q <= 0 or dsert <= 0 or t_h <= 0 or kap <= 0:
        raise ValueError("girisler gecerli olmali")
    tutulan = q * t_h * dsert
    return tutulan / kap * 1000.0


def basinc_dusurucu_kademe(p_giris_bar: Union[int, float],
                           p_cikis_bar: Union[int, float],
                           kademe_oran: float = 2.5) -> int:
    """Basinc dusurucu kademe sayisi. Tek kademe orani sinirli
    pratik kabul [STANDART-TEYIT]; donus int kademe."""
    pg, pc = float(p_giris_bar), float(p_cikis_bar)
    oran = float(kademe_oran)
    if pg <= 0 or pc <= 0 or oran <= 1.0:
        raise ValueError("girisler gecerli olmali")
    if pc >= pg:
        return 1
    import math as _m
    return int(_m.ceil(_m.log(pg / pc) / _m.log(oran)))


def bahce_sulama(alan_m2: Union[int, float],
                 sulama_mm_gun: float = 5.0,
                 sulama_saat: float = 2.0,
                 zon_sayisi: int = 1
                 ) -> tuple[float, float, float]:
    """Bahce sulama: (gunluk_m3, debi_m3h, zon_debi_m3h).

    Gunluk su = alan * sulama yuksekligi; debi sulama suresine
    bolunur. Sulama normu iklimsel pratik [STANDART-TEYIT].
    """
    alan = float(alan_m2)
    sul = float(sulama_mm_gun)
    saat = float(sulama_saat)
    zon = int(zon_sayisi)
    if alan <= 0 or sul <= 0 or saat <= 0 or zon <= 0:
        raise ValueError("girisler pozitif olmali")
    gunluk = alan * sul / 1000.0
    debi = gunluk / saat
    return gunluk, debi, debi / zon