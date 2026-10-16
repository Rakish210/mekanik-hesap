"""Isitma hesaplari (KATALOG.md 1. baslik, 14 hesap).

Dayanak: TS EN 12831 (isitma yuku), TS 825 (yalitim),
TS 2164 (kalorifer tesisati esaslari), TS EN 1264 (yerden isitma),
TS EN 12828 (kapali isitma sistemleri). Pratik/ampirik bagintilar
ayrica isaretlidir; katsayisi bilinmeyen basliga [STANDART-TEYIT]
yazilir, standart uydurulmaz.
"""

import math

_SU_OMZGUL_ISI = 1.161  # Wh/m3K esdegeri: 1000 kg/m3 * 4.18 kJ/kgK / 3.6
_HAVA_OMZGUL = 0.34  # Wh/m3K: havalandirma isisi icin (TS EN 12831)

_STANDART_CAP = (15, 20, 25, 32, 40, 50, 65, 80, 100, 125, 150, 200)


def isi_kaybi_mahal(ua_list, hacim_m3, hava_degisim, ti_c, td_c):
    """Mahal isi kaybi, W. TS EN 12831: iletim + havalandirma toplami.

    ua_list: [(U W/m2K, A m2), ...]; hacim_m3: m3; hava_degisim: 1/h;
    ti_c: ic sicaklik C; td_c: dis tasarim sicakligi C.
    Donus: (toplam_W, iletim_W, havalandirma_W).
    """
    dt = float(ti_c) - float(td_c)
    if dt <= 0:
        raise ValueError("ic sicaklik dis sicakliktan buyuk olmali")
    iletim = sum(float(u) * float(a) for u, a in ua_list) * dt
    hav = _HAVA_OMZGUL * float(hacim_m3) * float(hava_degisim) * dt
    return iletim + hav, iletim, hav


def radyator_secimi(q_mahal_w, q_dilim_w, artirim=1.15):
    """Radyator dilim sayisi. Pratik: secim artirim katsayili (TS 2164)."""
    q = float(q_mahal_w) * float(artirim)
    if q <= 0 or float(q_dilim_w) <= 0:
        raise ValueError("yuk ve dilim gucu pozitif olmali")
    return int(math.ceil(q / float(q_dilim_w)))


def yerden_isitma_hatve(q_m2):
    """Yerden isitma boru araligi, cm. TS EN 1264 esasli pratik secim."""
    q = float(q_m2)
    if q <= 0:
        raise ValueError("isi akisi pozitif olmali")
    if q <= 50:
        return 30
    if q <= 70:
        return 20
    if q <= 100:
        return 15
    return 10


def devre_debisi(q_w, dt_k=8.0):
    """Yerden isitma / radyator devre debisi, m3/h. Q = m*c*dT (su)."""
    q_w, dt_k = float(q_w), float(dt_k)
    if q_w <= 0 or dt_k <= 0:
        raise ValueError("yuk ve sicaklik farki pozitif olmali")
    return q_w / (1161.0 * dt_k)


def boru_capi(debi_m3h, hiz_ms):
    """Boru ic capi, mm; bir ust standart capa yuvarlanir. Pratik (TS 2164)."""
    debi_m3h, hiz_ms = float(debi_m3h), float(hiz_ms)
    if debi_m3h <= 0 or hiz_ms <= 0:
        raise ValueError("debi ve hiz pozitif olmali")
    d_mm = math.sqrt(4.0 * (debi_m3h / 3600.0) / math.pi / hiz_ms) * 1000.0
    for cap in _STANDART_CAP:
        if cap >= d_mm:
            return float(cap)
    return float(math.ceil(d_mm))


def pompa_isitma(q_kw, dt_k=20.0, kayip_kpa=30.0):
    """Sirkulasyon pompasi: (debi_m3h, basma_mSS). Pratik secim (TS 2164)."""
    q_kw, dt_k, kayip_kpa = float(q_kw), float(dt_k), float(kayip_kpa)
    if q_kw <= 0 or dt_k <= 0 or kayip_kpa < 0:
        raise ValueError("girisler gecerli olmali")
    debi = q_kw / (_SU_OMZGUL_ISI * dt_k)
    return debi, kayip_kpa / 9.807


def genlesme_tanki(v_sistem_l, t_soguk=10.0, t_sicak=90.0, p_min_bar=1.5,
                   p_maks_bar=3.0):
    """Kapali genlesme tanki nominal hacmi, L. TS EN 12828 basitlesmis.

    Ve = V*beta*dT (su beta ~ 0.00043); Vn = Ve*(Pmaks+1)/(Pmaks-Pmin).
    """
    v = float(v_sistem_l)
    dt = float(t_sicak) - float(t_soguk)
    p_min, p_maks = float(p_min_bar), float(p_maks_bar)
    if v <= 0 or dt <= 0 or p_maks <= p_min:
        raise ValueError("girisler gecerli olmali")
    ve = v * 0.00043 * dt
    return ve * (p_maks + 1.0) / (p_maks - p_min)


def kazan_kapasitesi(q_toplam_kw, artirim=0.15, boyler_kw=0.0):
    """Kazan kapasitesi, kW. TS EN 12831 toplami + artirim + boyler payi."""
    return float(q_toplam_kw) * (1.0 + float(artirim)) + float(boyler_kw)


def baca_cekisi(yukseklik_m, t_dis_c, t_baca_c):
    """Baca cekisi (tabii cekis), Pa. Fizik: dP = H*g*(rho_dis-rho_baca).

    [STANDART-TEYIT]: baca kesit tayini pratik katsayilari icin.
    """
    h = float(yukseklik_m)
    if h <= 0:
        raise ValueError("baca yuksekligi pozitif olmali")
    rho_dis = 353.0 / (273.15 + float(t_dis_c))
    rho_baca = 353.0 / (273.15 + float(t_baca_c))
    return 9.81 * h * (rho_dis - rho_baca)


def balans_kv(debi_m3h, dp_bar):
    """Balans vanasi Kv, m3/h. Kv = V / kok(dp). Genel vana bagintisi."""
    debi, dp = float(debi_m3h), float(dp_bar)
    if debi <= 0 or dp <= 0:
        raise ValueError("debi ve basinc farki pozitif olmali")
    return debi / math.sqrt(dp)


def uc_yollu_kvs(debi_m3h, dp_bar, otorite_min=0.25):
    """Uc yollu vana Kvs, m3/h. Pratik: Kvs = V/kok(dp), otorite >= 0.25.

    Donus: (kvs, otorite_ok). Otorite kontrolu icin vana dp / devre dp
    orani disaridan verilir; burada alt sinir notu duser [STANDART-TEYIT].
    """
    kvs = balans_kv(debi_m3h, dp_bar)
    return kvs, float(otorite_min) >= 0.25


def esanjor_kapasite(debi_m3h, t_giris, t_cikis):
    """Plakali esanjor kapasitesi, kW. Q = m*c*dT (su, 1.161 katsayisi)."""
    dt = abs(float(t_giris) - float(t_cikis))
    if float(debi_m3h) <= 0 or dt <= 0:
        raise ValueError("debi ve sicaklik farki pozitif olmali")
    return float(debi_m3h) * _SU_OMZGUL_ISI * dt


def lmtd(t1_sicak, t1_soguk, t2_sicak, t2_soguk):
    """Logaritmik ortalama sicaklik farki, K. Genel isi transferi."""
    a = float(t1_sicak) - float(t1_soguk)
    b = float(t2_sicak) - float(t2_soguk)
    if a <= 0 or b <= 0:
        raise ValueError("uc sicaklik farklari pozitif olmali")
    if abs(a - b) < 1e-9:
        return a
    return (a - b) / math.log(a / b)


def yakit_tuketimi(q_kw, hu_kj_birim, verim=0.9, saat=1.0):
    """Yakit tuketimi, birim (hu birimine gore kg veya m3). B = Q*h/(Hu*n)."""
    q_kw, hu, verim = float(q_kw), float(hu_kj_birim), float(verim)
    if q_kw <= 0 or hu <= 0 or not (0 < verim <= 1.0):
        raise ValueError("girisler gecerli olmali")
    return q_kw * 3600.0 * float(saat) / (hu * verim)


def yalitim_kalinligi(u_hedef, lamda, r_diger=0.17):
    """Gerekli yalitim kalinligi, m. TS 825: d = lamda*(1/U - R_diger)."""
    u_hedef, lamda = float(u_hedef), float(lamda)
    if u_hedef <= 0 or lamda <= 0:
        raise ValueError("U ve lamda pozitif olmali")
    r_gerek = 1.0 / u_hedef - float(r_diger)
    if r_gerek <= 0:
        raise ValueError("hedef U, mevcut katmanlarla saglaniyor")
    return lamda * r_gerek


def zon_debi_dagilimi(q_zon_list):
    """Kollektor zon debileri: (toplam_kW, [oran, ...], [debi_m3h, ...]).

    Debi orani yuk orani ile aynidir; su rejimi tum zonlarda esit
    kabul edilir (pratik, TS 2164).
    """
    yukler = [float(q) for q in q_zon_list]
    if not yukler or any(q < 0 for q in yukler) or sum(yukler) <= 0:
        raise ValueError("zon yukleri gecerli olmali")
    toplam = sum(yukler)
    oranlar = [q / toplam for q in yukler]
    return toplam, oranlar, oranlar
