"""Havalandirma hesaplari (KATALOG.md 3. baslik, 12 hesap).

Dayanak: TS EN 13779 (bina havalandirmasi), ASHRAE 62.1 (kabul
edilebilir ic hava kalitesi), VDI 2052 (mutfak), EN 12101 (duman
kontrolu). Kisi basi debi ve pratik katsayilar [STANDART-TEYIT: TS EN 13779, ASHRAE 62.1]
ile isaretlidir; standart uydurulmaz.
"""

from typing import Union

def taze_hava(kisi: Union[int, float],
              qp_m3h: float = 30.0) -> float:
    """Taze hava debisi, m3/h. V = n*qp. TS EN 13779 / ASHRAE 62.1.

    qp varsayilani pratiktir [STANDART-TEYIT: TS EN 13779, ASHRAE 62.1]; mahale gore secilir.
    """
    if float(kisi) <= 0 or float(qp_m3h) <= 0:
        raise ValueError("kisi ve birim debi pozitif olmali")
    return float(kisi) * float(qp_m3h)


def hava_degisim(hacim_m3: Union[int, float],
                 ach: Union[int, float]) -> float:
    """Hava degisim debisi, m3/h. V = hacim*ACH."""
    if float(hacim_m3) <= 0 or float(ach) <= 0:
        raise ValueError("hacim ve ACH pozitif olmali")
    return float(hacim_m3) * float(ach)


def kanal_basinc_kaybi(uzunluk_m: Union[int, float],
                       cap_m: Union[int, float],
                       hiz_ms: Union[int, float],
                       rho: float = 1.2, lamda: float = 0.02,
                       zeta: float = 0.0) -> float:
    """Kanal basinc kaybi, Pa. Darcy-Weisbach: (lamda*L/D + zeta)*rho*V2/2."""
    l_m, d_m, v = float(uzunluk_m), float(cap_m), float(hiz_ms)
    if l_m < 0 or d_m <= 0 or v <= 0:
        raise ValueError("girisler gecerli olmali")
    return (float(lamda) * l_m / d_m + float(zeta)) * float(rho) * v * v / 2.0


def fan_gucu(debi_m3h: Union[int, float], dp_pa: Union[int, float],
             verim: float = 0.6) -> float:
    """Fan mil gucu, kW. P = V*dP/eta."""
    debi, dp = float(debi_m3h), float(dp_pa)
    if debi <= 0 or dp < 0 or not (0 < float(verim) <= 1.0):
        raise ValueError("girisler gecerli olmali")
    return debi / 3600.0 * dp / float(verim) / 1000.0


def duman_zonu(alan_m2: Union[int, float],
               yukseklik_m: Union[int, float],
               ach: float = 6.0) -> float:
    """Duman kontrol zon egzoz debisi, m3/h. Pratik ACH [STANDART-TEYIT: TS EN 13779, ASHRAE 62.1]."""
    if float(alan_m2) <= 0 or float(yukseklik_m) <= 0 or float(ach) <= 0:
        raise ValueError("girisler pozitif olmali")
    return float(alan_m2) * float(yukseklik_m) * float(ach)


def otopark_debi(arac_sayisi: Union[int, float],
                 q_arac_m3h: float = 300.0) -> float:
    """Otopark havalandirma debisi, m3/h. Pratik birim debi [STANDART-TEYIT: TS EN 13779, ASHRAE 62.1]."""
    if float(arac_sayisi) <= 0 or float(q_arac_m3h) <= 0:
        raise ValueError("girisler pozitif olmali")
    return float(arac_sayisi) * float(q_arac_m3h)


def davlumbaz_debi(uzunluk_m: Union[int, float],
                   q_birim: float = 1000.0) -> float:
    """Mutfak davlumbaz egzoz debisi, m3/h. VDI 2052 esasli pratik."""
    if float(uzunluk_m) <= 0 or float(q_birim) <= 0:
        raise ValueError("girisler pozitif olmali")
    return float(uzunluk_m) * float(q_birim)


def siginak_debi(kisi: Union[int, float],
                 qp_m3h: float = 10.0) -> float:
    """Siginak havalandirma debisi, m3/h. Pratik birim debi [STANDART-TEYIT: TS EN 13779, ASHRAE 62.1]."""
    if float(kisi) <= 0 or float(qp_m3h) <= 0:
        raise ValueError("girisler pozitif olmali")
    return float(kisi) * float(qp_m3h)


def merdiven_basinc(kapi_adet: Union[int, float],
                    kapi_alan_m2: float = 2.0,
                    hiz_ms: float = 1.0) -> float:
    """Merdiven basinclandirma debisi, m3/h. V = n*A*v. EN 12101 ailesi.

    Hiz ve kapi kabulleri pratiktir [STANDART-TEYIT: TS EN 13779, ASHRAE 62.1].
    """
    if float(kapi_adet) <= 0 or float(kapi_alan_m2) <= 0 \
            or float(hiz_ms) <= 0:
        raise ValueError("girisler pozitif olmali")
    return float(kapi_adet) * float(kapi_alan_m2) * float(hiz_ms) * 3600.0


def tuvalet_egzoz(klozet: int = 1, pisuvar: int = 0,
                  q_klozet: float = 90.0,
                  q_pisuvar: float = 50.0) -> float:
    """Tuvalet/banyo egzoz debisi, m3/h. Pratik birim debi [STANDART-TEYIT: TS EN 13779, ASHRAE 62.1]."""
    if int(klozet) < 0 or int(pisuvar) < 0:
        raise ValueError("adetler negatif olamaz")
    return int(klozet) * float(q_klozet) + int(pisuvar) * float(q_pisuvar)


def endustriyel_egzoz(alan_m2: Union[int, float],
                      v_capture_ms: Union[int, float]) -> float:
    """Endustriyel egzoz debisi, m3/h. V = A*v_yakalama."""
    if float(alan_m2) <= 0 or float(v_capture_ms) <= 0:
        raise ValueError("girisler pozitif olmali")
    return float(alan_m2) * float(v_capture_ms) * 3600.0


def susturucu_kaybi(dp_katalog_pa: Union[int, float],
                    v_tasarim_ms: Union[int, float],
                    v_katalog_ms: Union[int, float]) -> float:
    """Susturucu basinc kaybi, Pa. dP ~ v2 olcekleme (dinamik basinc)."""
    dp, v_t, v_k = (float(dp_katalog_pa), float(v_tasarim_ms),
                    float(v_katalog_ms))
    if dp < 0 or v_t <= 0 or v_k <= 0:
        raise ValueError("girisler gecerli olmali")
    return dp * (v_t / v_k) ** 2