"""Havalandirma hesaplari (KATALOG.md 3. baslik, 12 hesap).

Dayanak: TS EN 13779 (bina havalandirmasi), ASHRAE 62.1 (kabul
edilebilir ic hava kalitesi), VDI 2052 (mutfak), EN 12101 (duman
kontrolu). Kisi basi debi ve pratik katsayilar [STANDART-TEYIT]
ile isaretlidir; standart uydurulmaz.
"""

import math


def taze_hava(kisi, qp_m3h=30.0):
    """Taze hava debisi, m3/h. V = n*qp. TS EN 13779 / ASHRAE 62.1.

    qp varsayilani pratiktir [STANDART-TEYIT]; mahale gore secilir.
    """
    if float(kisi) <= 0 or float(qp_m3h) <= 0:
        raise ValueError("kisi ve birim debi pozitif olmali")
    return float(kisi) * float(qp_m3h)


def hava_degisim(hacim_m3, ach):
    """Hava degisim debisi, m3/h. V = hacim*ACH."""
    if float(hacim_m3) <= 0 or float(ach) <= 0:
        raise ValueError("hacim ve ACH pozitif olmali")
    return float(hacim_m3) * float(ach)


def kanal_basinc_kaybi(uzunluk_m, cap_m, hiz_ms, rho=1.2, lamda=0.02,
                       zeta=0.0):
    """Kanal basinc kaybi, Pa. Darcy-Weisbach: (lamda*L/D + zeta)*rho*V2/2."""
    l_m, d_m, v = float(uzunluk_m), float(cap_m), float(hiz_ms)
    if l_m < 0 or d_m <= 0 or v <= 0:
        raise ValueError("girisler gecerli olmali")
    return (float(lamda) * l_m / d_m + float(zeta)) * float(rho) * v * v / 2.0


def fan_gucu(debi_m3h, dp_pa, verim=0.6):
    """Fan mil gucu, kW. P = V*dP/eta."""
    debi, dp = float(debi_m3h), float(dp_pa)
    if debi <= 0 or dp < 0 or not (0 < float(verim) <= 1.0):
        raise ValueError("girisler gecerli olmali")
    return debi / 3600.0 * dp / float(verim) / 1000.0


def duman_zonu(alan_m2, yukseklik_m, ach=6.0):
    """Duman kontrol zon egzoz debisi, m3/h. Pratik ACH [STANDART-TEYIT]."""
    if float(alan_m2) <= 0 or float(yukseklik_m) <= 0 or float(ach) <= 0:
        raise ValueError("girisler pozitif olmali")
    return float(alan_m2) * float(yukseklik_m) * float(ach)


def otopark_debi(arac_sayisi, q_arac_m3h=300.0):
    """Otopark havalandirma debisi, m3/h. Pratik birim debi [STANDART-TEYIT]."""
    if float(arac_sayisi) <= 0 or float(q_arac_m3h) <= 0:
        raise ValueError("girisler pozitif olmali")
    return float(arac_sayisi) * float(q_arac_m3h)


def davlumbaz_debi(uzunluk_m, q_birim=1000.0):
    """Mutfak davlumbaz egzoz debisi, m3/h. VDI 2052 esasli pratik."""
    if float(uzunluk_m) <= 0 or float(q_birim) <= 0:
        raise ValueError("girisler pozitif olmali")
    return float(uzunluk_m) * float(q_birim)


def siginak_debi(kisi, qp_m3h=10.0):
    """Siginak havalandirma debisi, m3/h. Pratik birim debi [STANDART-TEYIT]."""
    if float(kisi) <= 0 or float(qp_m3h) <= 0:
        raise ValueError("girisler pozitif olmali")
    return float(kisi) * float(qp_m3h)


def merdiven_basinc(kapi_adet, kapi_alan_m2=2.0, hiz_ms=1.0):
    """Merdiven basinclandirma debisi, m3/h. V = n*A*v. EN 12101 ailesi.

    Hiz ve kapi kabulleri pratiktir [STANDART-TEYIT].
    """
    if float(kapi_adet) <= 0 or float(kapi_alan_m2) <= 0 \
            or float(hiz_ms) <= 0:
        raise ValueError("girisler pozitif olmali")
    return float(kapi_adet) * float(kapi_alan_m2) * float(hiz_ms) * 3600.0


def tuvalet_egzoz(klozet=1, pisuvar=0, q_klozet=90.0, q_pisuvar=50.0):
    """Tuvalet/banyo egzoz debisi, m3/h. Pratik birim debi [STANDART-TEYIT]."""
    if int(klozet) < 0 or int(pisuvar) < 0:
        raise ValueError("adetler negatif olamaz")
    return int(klozet) * float(q_klozet) + int(pisuvar) * float(q_pisuvar)


def endustriyel_egzoz(alan_m2, v_capture_ms):
    """Endustriyel egzoz debisi, m3/h. V = A*v_yakalama."""
    if float(alan_m2) <= 0 or float(v_capture_ms) <= 0:
        raise ValueError("girisler pozitif olmali")
    return float(alan_m2) * float(v_capture_ms) * 3600.0


def susturucu_kaybi(dp_katalog_pa, v_tasarim_ms, v_katalog_ms):
    """Susturucu basinc kaybi, Pa. dP ~ v2 olcekleme (dinamik basinc)."""
    dp, v_t, v_k = (float(dp_katalog_pa), float(v_tasarim_ms),
                    float(v_katalog_ms))
    if dp < 0 or v_t <= 0 or v_k <= 0:
        raise ValueError("girisler gecerli olmali")
    return dp * (v_t / v_k) ** 2
