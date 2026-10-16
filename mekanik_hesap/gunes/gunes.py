"""Gunes enerjisi hesaplari (KATALOG.md 5. baslik, 5 hesap).

Dayanak: TS EN 12975 (gunes kolektorleri), TS EN 12976
(fabrika yapimi sistemler), TS EN 12977 (ozel sistemler).
Isinim ve verim kabulleri yoresel katalog/olcum ile
netlestirilir [STANDART-TEYIT].
"""


def kolektor_alan(gunluk_ihtiyac_kwh, isinim_kwh_m2gun=4.5,
                  sistem_verim=0.45):
    """Gerekli kolektor alani, m2. A = E/(isinim*verim)."""
    e_kwh = float(gunluk_ihtiyac_kwh)
    g_kwh = float(isinim_kwh_m2gun)
    eta = float(sistem_verim)
    if e_kwh <= 0 or g_kwh <= 0 or not (0 < eta <= 1.0):
        raise ValueError("girisler gecerli olmali")
    return e_kwh / (g_kwh * eta)


def gunluk_enerji(kisi, kisi_basi_l=50.0, t_soguk=10.0, t_sicak=60.0):
    """Gunluk sicak su enerji ihtiyaci, kWh. E = V*1.161*dT/1000."""
    hacim = float(kisi) * float(kisi_basi_l)
    dt = float(t_sicak) - float(t_soguk)
    if hacim <= 0 or dt <= 0:
        raise ValueError("girisler gecerli olmali")
    return hacim * 1.161 * dt / 1000.0


def gunes_boyler(gunluk_l, gunes_karsilama=0.6):
    """Gunes destekli boyler hacmi, L. Gunluk tuketimin karsilama
    oranina gore pratik secim [STANDART-TEYIT]."""
    gun, oran = float(gunluk_l), float(gunes_karsilama)
    if gun <= 0 or not (0 < oran <= 1.0):
        raise ValueError("girisler gecerli olmali")
    return gun * oran


def solar_pompa(alan_m2, ozgul_debi_l_h_m2=30.0):
    """Solar cevre pompa debisi, L/h. V_dot = A*q_ozgul. Katalog
    araligi pratik [STANDART-TEYIT]."""
    alan, qoz = float(alan_m2), float(ozgul_debi_l_h_m2)
    if alan <= 0 or qoz <= 0:
        raise ValueError("girisler pozitif olmali")
    return alan * qoz


def solar_genlesme(sistem_hacmi_l, t_soguk=10.0, t_sicak=90.0,
                   p_min_bar=1.5, p_maks_bar=3.0, antifriz_katsayi=1.3):
    """Solar genlesme kabi nominal hacmi, L. Su genlesmesi ve
    antifriz katsayisiyla pratik [STANDART-TEYIT]."""
    v_l = float(sistem_hacmi_l)
    dt = float(t_sicak) - float(t_soguk)
    pmin, pmaks = float(p_min_bar), float(p_maks_bar)
    k = float(antifriz_katsayi)
    if v_l <= 0 or dt <= 0 or pmaks <= pmin or k <= 0:
        raise ValueError("girisler gecerli olmali")
    ve_l = v_l * 0.00043 * dt * k
    return ve_l * (pmaks + 1.0) / (pmaks - pmin)


def geri_odeme(yatirim_tl, yillik_kazanc_kwh, birim_fiyat_tl_kwh):
    """Basit geri odeme suresi, yil. T = yatirim / (kazanc*fiyat)."""
    ytl, kaz, bir = (float(yatirim_tl), float(yillik_kazanc_kwh),
                     float(birim_fiyat_tl_kwh))
    if ytl <= 0 or kaz <= 0 or bir <= 0:
        raise ValueError("girisler pozitif olmali")
    return ytl / (kaz * bir)
