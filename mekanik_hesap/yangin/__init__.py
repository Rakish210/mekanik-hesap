"""Yangin tesisati hesaplari (KATALOG.md 7. baslik, 10 hesap).

Dayanak: TS EN 12845 (sprinkler), TS EN 671 (yangin dolabi),
TS EN 14384 (hidrant), TS EN 15004 (gazli sondurme),
BYKHY m.95 (hidrant alani). Hidrolik kayip Hazen-Williams ile
hesaplanir; su tesisatindaki mevcut yaklasimla (colebrook/water)
tutarli olmasi icin C katsayisi ve pratik kabuller ayrica
isaretlidir. Katsayisi bilinmeyen basliga [STANDART-TEYIT]
yazilir, standart uydurulmaz.
"""

import math

# Hazen-Williams puruzluluk katsayisi, celik boru pratik kabul
# (TS EN 12845 hidrolik hesap eki esasli pratik).
C_CELIK = 120.0


def hazen_williams_kayip(uzunluk_m, debi_m3h, cap_mm, c=C_CELIK):
    """Hazen-Williams boru kaybi, mSS.

    hf = 10.67*L*Q^1.852 / (C^1.852*D^4.871); Q m3/s, D m.
    """
    l_m, cap = float(uzunluk_m), float(cap_mm)
    c = float(c)
    if l_m < 0 or float(debi_m3h) < 0 or cap <= 0 or c <= 0:
        raise ValueError("girisler gecerli olmali")
    q = float(debi_m3h) / 3600.0
    d = cap / 1000.0
    return 10.67 * l_m * q ** 1.852 / (c ** 1.852 * d ** 4.871)


def sprinkler_debi(k_faktor, basinc_bar):
    """Tek sprinkler debisi, L/dk. q = K*kok(p) (TS EN 12845).

    K metrik: L/dk/bar^0.5 (or. K80, K115).
    """
    k, p = float(k_faktor), float(basinc_bar)
    if k <= 0 or p <= 0:
        raise ValueError("K ve basinc pozitif olmali")
    return k * math.sqrt(p)


def sprinkler_zon(zon_alani_m2, yogunluk_mm_dk, k_faktor=80.0,
                  basinc_bar=1.0):
    """Islak/kuru boru zon hesabi: (zon_debi_Ldk, sprinkler_sayisi).

    Debi = alan * tasarim yogunlugu; sprinkler sayisi debi / tekil
    debiye yuvarlanir. Yogunluk ve tehlike sinifi secimi projeye
    aittir [STANDART-TEYIT]; TS EN 12845 tablo degerleri teyit edilir.
    """
    alan = float(zon_alani_m2)
    yog = float(yogunluk_mm_dk)
    if alan <= 0 or yog <= 0:
        raise ValueError("alan ve yogunluk pozitif olmali")
    zon_debi = alan * yog
    tekil = sprinkler_debi(k_faktor, basinc_bar)
    return zon_debi, int(math.ceil(zon_debi / tekil))


def dolap_debi(dolap_adet, birim_debi_ldk=100.0, es_zaman=2):
    """Yangin dolabi debisi, L/dk. TS EN 671 esasli pratik.

    Birim debi ve es zamanli dolap sayisi pratik kabul
    [STANDART-TEYIT]; hortum boyu TS EN 671-1 (20/25/30 m) projede
    secilir.
    """
    adet = int(dolap_adet)
    if adet <= 0 or float(birim_debi_ldk) <= 0 or int(es_zaman) <= 0:
        raise ValueError("girisler pozitif olmali")
    aktif = min(adet, int(es_zaman))
    return aktif * float(birim_debi_ldk)


def hidrant_hatti(hidrant_adet, birim_debi_ldk=1900.0 / 12,
                  uzunluk_m=100.0, cap_mm=100.0,
                  statik_mss=10.0, artik_mss=70.0):
    """Hidrant hatti: (toplam_debi_Ldk, pompa_basinci_mSS).

    Birim debi ve artik basinc BYKHY m.95 esasli pratik kabul
    [STANDART-TEYIT]; kayip Hazen-Williams ile bulunur.
    """
    adet = int(hidrant_adet)
    if adet <= 0 or float(birim_debi_ldk) <= 0:
        raise ValueError("hidrant adedi ve birim debi pozitif olmali")
    toplam = adet * float(birim_debi_ldk)
    kayip = hazen_williams_kayip(uzunluk_m, toplam * 0.06, cap_mm)
    basinc = float(statik_mss) + kayip + float(artik_mss)
    return toplam, basinc


def pompa_secimi(debi_m3h, basinc_mss, jokey_oran=0.01):
    """Yangin pompasi: (ana_debi_m3h, ana_basinc_mSS, jokey_debi_m3h).

    Ana pompa debi+basinci aynen; jokey pompa ~%1 debi, ayni basinc
    pratik kabul [STANDART-TEYIT]. Elektrik/dizel/jokey secimi
    projeye aittir.
    """
    debi, basinc = float(debi_m3h), float(basinc_mss)
    oran = float(jokey_oran)
    if debi <= 0 or basinc <= 0 or not (0 < oran < 1.0):
        raise ValueError("girisler gecerli olmali")
    return debi, basinc, debi * oran


def su_deposu(debi_m3h, sure_dk=60.0):
    """Yangin su deposu (rezerv) hacmi, m3. V = Q*t.

    Sure kabulu projeye/BYKHY'a gore secilir [STANDART-TEYIT].
    """
    debi, sure = float(debi_m3h), float(sure_dk)
    if debi <= 0 or sure <= 0:
        raise ValueError("debi ve sure pozitif olmali")
    return debi * sure / 60.0


def _gazli_miktar(hacim_m3, konsantrasyon, ozgul_hacim):
    """Genel toplam basma gazli sondurme bagintisi, kg.

    W = V*C / (S*(100-C)). Konsantrasyon ve ozgul hacim
    gaz tipine gore TS EN 15004 ilgili bolumunden secilir
    [STANDART-TEYIT].
    """
    v = float(hacim_m3)
    c = float(konsantrasyon)
    s = float(ozgul_hacim)
    if v <= 0 or not (0 < c < 100) or s <= 0:
        raise ValueError("girisler gecerli olmali")
    return v * c / (s * (100.0 - c))


def fm200(hacim_m3, konsantrasyon=8.7, ozgul_hacim=0.1373,
          nozul_kapsama_m2=30.0, alan_m2=0.0):
    """FM200 (HFC-227ea) miktari: (kg, nozul_adet). TS EN 15004-5.

    Konsantrasyon ve nozul kapsama alani proje/CPD degeridir
    [STANDART-TEYIT]; alan verilmezse nozul 1 doner.
    """
    miktar = _gazli_miktar(hacim_m3, konsantrasyon, ozgul_hacim)
    alan = float(alan_m2)
    if alan <= 0:
        return miktar, 1
    if float(nozul_kapsama_m2) <= 0:
        raise ValueError("nozul kapsama alani pozitif olmali")
    return miktar, int(math.ceil(alan / float(nozul_kapsama_m2)))


def co2_miktar(hacim_m3, faktor_kg_m3=1.2):
    """CO2 sondurme miktari, kg. Toplam basma pratik faktor
    [STANDART-TEYIT]; yuksek/alcak basinc secimi projeye aittir."""
    v, f = float(hacim_m3), float(faktor_kg_m3)
    if v <= 0 or f <= 0:
        raise ValueError("hacim ve faktor pozitif olmali")
    return v * f


def novec1230(hacim_m3, konsantrasyon=5.6, ozgul_hacim=0.0733):
    """Novec 1230 (FK-5-1-12) miktari, kg. TS EN 15004-2.

    Konsantrasyon proje/CPD degeridir [STANDART-TEYIT].
    """
    return _gazli_miktar(hacim_m3, konsantrasyon, ozgul_hacim)


def kopuk_konsantresi(alan_m2, uygulama_ldk_m2=6.5, sure_dk=15.0,
                      oran=0.03):
    """Kopuk konsantresi miktari, L. V = A*q*t*oran.

    Uygulama yogunlugu, sure ve karisim orani tehlike sinifina gore
    secilir [STANDART-TEYIT].
    """
    alan = float(alan_m2)
    q = float(uygulama_ldk_m2)
    sure, oran = float(sure_dk), float(oran)
    if alan <= 0 or q <= 0 or sure <= 0 or not (0 < oran < 1.0):
        raise ValueError("girisler gecerli olmali")
    return alan * q * sure * oran
