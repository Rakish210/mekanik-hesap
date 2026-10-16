"""Elektrik tesisat arayuz hesaplari (KATALOG.md 14. baslik, 20 hesap).

Dayanak: IEC 60364 (alcak gerilim tesisleri: 4-41 koruma, 4-43 asiri
akim, 5-52 kablo, 5-54 topraklama), IEC 62305 (paratoner/YKS),
TS EN 12464-1 (ic aydinlatma), EN 54-14 (yangin algilama tasarim),
EN 1838 (acil aydinlatma), EN 50173 (data kablolama), IEC 60831
(kompanzasyon kondansatoru), IEC 61537 (kablo tasiyi sistemi).
Tasima akimi tablolari, eszamanlilik katsayilari, aydinlatma duzey
secimi ve pratik kabuller projeye aittir; degeri bilinmeyen baslik
[STANDART-TEYIT] ile isaretlidir, standart uydurulmaz.
"""

import math

# Bakir iletken tasima akimi, A (PVC, 3 yuklu damar, 30 C havada).
# IEC 60364-5-52 tablo B.52.2 esasli pratik dizi [STANDART-TEYIT];
# doseme sekli/duzeltme katsayisi projede teyit edilir.
_KESIT_AKIM = (
    (1.5, 15.5), (2.5, 21.0), (4.0, 28.0), (6.0, 36.0),
    (10.0, 50.0), (16.0, 66.0), (25.0, 84.0), (35.0, 104.0),
    (50.0, 125.0), (70.0, 160.0), (95.0, 200.0), (120.0, 230.0),
    (150.0, 260.0), (185.0, 300.0), (240.0, 350.0),
)

# Sigorta/salter anma akim dizisi, A (pratik pano dizisi).
_ANMA = (6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160,
         200, 250, 400, 630)

# Trafo standart guc dizisi, kVA.
_TRAFO = (25, 50, 100, 160, 250, 400, 630, 800, 1000, 1250, 1600,
          2000, 2500)

_BAKIR_RHO = 0.0178  # ohm.mm2/m (20 C pratik)


def yuk_akimi(guc_w, gerilim_v=400.0, faz=3, cosfi=0.8):
    """Yuk akimi, A. 1 faz: I=P/(U cos); 3 faz: I=P/(kok3 U cos).

    Guc donusumleri ve akim-sigorta bagintisi IEC 60364 esaslidir.
    """
    p = float(guc_w)
    u = float(gerilim_v)
    cosf = float(cosfi)
    if p < 0 or u <= 0 or not (0 < cosf <= 1.0):
        raise ValueError("guc, gerilim ve cosfi gecerli olmali")
    if int(faz) == 1:
        return p / (u * cosf)
    if int(faz) == 3:
        return p / (math.sqrt(3.0) * u * cosf)
    raise ValueError("faz 1 veya 3 olmali")


def guc_ucgeni(p_kw=None, s_kva=None, q_kvar=None, cosfi=None):
    """Aktif/gorunur/reaktif guc donusumu: (P_kW, S_kVA, Q_kVAr, cosfi).

    Verilen ikiden digerleri bulunur: S=kok(P2+Q2), cos=P/S.
    En az iki girdi verilmelidir.
    """
    vals = [p_kw, s_kva, q_kvar, cosfi]
    if sum(v is not None for v in vals) < 2:
        raise ValueError("en az iki girdi verilmelidir")
    p = float(p_kw) if p_kw is not None else None
    s = float(s_kva) if s_kva is not None else None
    q = float(q_kvar) if q_kvar is not None else None
    c = float(cosfi) if cosfi is not None else None
    if c is not None and not (0 < c <= 1.0):
        raise ValueError("cosfi (0,1] araliginda olmali")
    if p is not None and s is not None:
        if s <= 0 or p < 0 or p > s:
            raise ValueError("0 <= P <= S olmali")
        q = math.sqrt(max(s * s - p * p, 0.0))
        c = p / s if s else 1.0
    elif p is not None and q is not None:
        if p < 0 or q < 0:
            raise ValueError("P ve Q negatif olamaz")
        s = math.sqrt(p * p + q * q)
        c = p / s if s else 1.0
    elif s is not None and q is not None:
        if s <= 0 or q < 0 or q > s:
            raise ValueError("0 <= Q <= S olmali")
        p = math.sqrt(max(s * s - q * q, 0.0))
        c = p / s if s else 1.0
    elif p is not None and c is not None:
        if p < 0:
            raise ValueError("P negatif olamaz")
        s = p / c
        q = math.sqrt(max(s * s - p * p, 0.0))
    elif s is not None and c is not None:
        if s <= 0:
            raise ValueError("S pozitif olmali")
        p = s * c
        q = math.sqrt(max(s * s - p * p, 0.0))
    else:
        raise ValueError("bu girdi cifti desteklenmez")
    return p, s, q, c


def kablo_kesit(akim_a):
    """Kablo kesit tayini, mm2. Akimi karsilayan ilk standart kesit.

    Tasima akimi dizisi IEC 60364-5-52 esasli pratik
    [STANDART-TEYIT]; duzeltme katsayilari projede teyit edilir.
    """
    i = float(akim_a)
    if i <= 0:
        raise ValueError("akim pozitif olmali")
    for kesit, kapasite in _KESIT_AKIM:
        if i <= kapasite:
            return float(kesit)
    raise ValueError("akim tablo araligini asiyor")


def gerilim_dusumu(akim_a, uzunluk_m, kesit_mm2, gerilim_v=400.0,
                   faz=3, cosfi=0.8):
    """Gerilim dusumu, %. Tek faz: 2 rho L I cos/S; 3 faz: kok3 ...

    IEC 60364-5-52 ek G esasli pratik baginti [STANDART-TEYIT];
    reaktans dusumu ihmal edilmistir (aydinlatma/priz hatti pratigi).
    Sinir deger (%3 aydinlatma, %5 kuvvet) projede teyit edilir.
    """
    i = float(akim_a)
    l_m = float(uzunluk_m)
    s = float(kesit_mm2)
    u = float(gerilim_v)
    cosf = float(cosfi)
    if i < 0 or l_m < 0 or s <= 0 or u <= 0:
        raise ValueError("girisler gecerli olmali")
    if not (0 < cosf <= 1.0):
        raise ValueError("cosfi (0,1] araliginda olmali")
    if int(faz) == 1:
        du = 2.0 * _BAKIR_RHO * l_m * i * cosf / s
    elif int(faz) == 3:
        du = math.sqrt(3.0) * _BAKIR_RHO * l_m * i * cosf / s
    else:
        raise ValueError("faz 1 veya 3 olmali")
    return du / u * 100.0


def sigorta_secimi(yuk_akim_a, tasima_akim_a=None):
    """Sigorta/salter secimi, A. Ib <= In sarti + standart dizi.

    IEC 60364-4-43 (Ib <= In <= Iz) esaslidir; Iz verilirse
    In <= Iz de saglanir, saglanmazsa ValueError verir.
    Trafolu salter acma egrisi (B/C/D) pano notunda secilir
    [STANDART-TEYIT].
    """
    ib = float(yuk_akim_a)
    if ib <= 0:
        raise ValueError("yuk akimi pozitif olmali")
    for anma in _ANMA:
        if anma >= ib:
            if tasima_akim_a is not None and anma > float(tasima_akim_a):
                raise ValueError("In <= Iz saglanmiyor, kesit buyutulur")
            return float(anma)
    raise ValueError("akim salter dizisini asiyor")


def kacak_akim(kullanim="priz"):
    """Kacak akim rolesi kademesi, mA. IEC 60364-4-41 esasli pratik.

    priz/isitici devresi: 30; ana dagitim/yangin koruma: 300.
    Tip (AC/A/F/B) yuk tipine gore secilir [STANDART-TEYIT].
    """
    tablo = {"priz": 30.0, "aydinlatma": 30.0, "ana": 300.0,
             "yangin": 300.0, "santiye": 30.0}
    key = str(kullanim).lower()
    if key not in tablo:
        raise ValueError("kullanim priz/aydinlatma/ana/yangin/santiye olmali")
    return tablo[key]


def topraklama_cubugu(zemin_ohm_m, boy_m=3.0, cap_mm=16.0):
    """Tek topraklama cubugu direnci, ohm. R=rho/(2 pi L) ln(4L/d).

    IEC 60364-5-54 esasli klasik baginti; zemin ozdirenci olcumle
    teyit edilir [STANDART-TEYIT].
    """
    rho = float(zemin_ohm_m)
    l_m = float(boy_m)
    d = float(cap_mm) / 1000.0
    if rho <= 0 or l_m <= 0 or d <= 0:
        raise ValueError("girisler pozitif olmali")
    return rho / (2.0 * math.pi * l_m) * math.log(4.0 * l_m / d)


def topraklama_elektrot(tek_direnc_ohm, hedef_ohm=10.0):
    """Topraklama elektrot sayisi, adet. n=tavan(Rtek/Rhedef).

    Paralel verim katsayisi ihmal edilmistir (pratik onsecim);
    olcumle teyit edilir [STANDART-TEYIT].
    """
    r = float(tek_direnc_ohm)
    hedef = float(hedef_ohm)
    if r <= 0 or hedef <= 0:
        raise ValueError("direncler pozitif olmali")
    return int(math.ceil(r / hedef))


def paratoner_yaricap(yukseklik_m, kure_m=45.0):
    """Paratoner (yuvarlanan kure) koruma yaricapi, m.

    Rp=kok(2Rh-h2). Kure yaricapi koruma sinifina gore secilir
    (or. 20/30/45/60 m); IEC 62305 esasli pratik [STANDART-TEYIT].
    """
    h = float(yukseklik_m)
    r = float(kure_m)
    if h <= 0 or r <= 0 or h > r:
        raise ValueError("0 < h <= kure yaricapi olmali")
    return math.sqrt(2.0 * r * h - h * h)


def aydinlatma_armatur(alan_m2, lux, lamba_lumen, kullanim=0.6,
                       bakim=0.8):
    """Aydinlatma armatur sayisi, adet. N=E A/(F UF MF).

    Aydinlik duzeyi TS EN 12464-1 tablosundan secilir
    (or. ofis 500 lx); kullanim/bakim katsayisi pratik
    [STANDART-TEYIT].
    """
    a = float(alan_m2)
    e = float(lux)
    f = float(lamba_lumen)
    uf, mf = float(kullanim), float(bakim)
    if a <= 0 or e <= 0 or f <= 0:
        raise ValueError("alan, lux ve lumen pozitif olmali")
    if not (0 < uf <= 1.0) or not (0 < mf <= 1.0):
        raise ValueError("katsayilar (0,1] araliginda olmali")
    return int(math.ceil(e * a / (f * uf * mf)))


def kompanzasyon(p_kw, cos_mevcut, cos_hedef=0.95):
    """Kompanzasyon gucu, kVAr. Qc=P(tan1-tan2). IEC 60831 esasli.

    Hedef guc katsayisi dagitim sirketi sartina gore secilir
    (or. 0.95); kademe sayisi pano projesine aittir.
    """
    p = float(p_kw)
    c1, c2 = float(cos_mevcut), float(cos_hedef)
    if p <= 0:
        raise ValueError("guc pozitif olmali")
    if not (0 < c1 < 1.0) or not (0 < c2 <= 1.0):
        raise ValueError("cos degerleri (0,1] araliginda olmali")
    if c2 <= c1:
        raise ValueError("hedef cos mevcuttan buyuk olmali")
    t1 = math.sqrt(1.0 - c1 * c1) / c1
    t2 = math.sqrt(1.0 - c2 * c2) / c2
    return p * (t1 - t2)


def jenerator_gucu(kurulu_kw, eszaman=0.7, cosfi=0.8, kalkis_payi=1.25):
    """Jenerator gucu, kVA. S=P esz k/cos.

    Eszamanlilik ve motor kalkis payi pratik kabul
    [STANDART-TEYIT]; kritik yuk listesi projede teyit edilir.
    """
    p = float(kurulu_kw)
    esz = float(eszaman)
    cosf = float(cosfi)
    pay = float(kalkis_payi)
    if p <= 0 or not (0 < esz <= 1.0) or pay <= 0:
        raise ValueError("girisler gecerli olmali")
    if not (0 < cosf <= 1.0):
        raise ValueError("cosfi (0,1] araliginda olmali")
    return p * esz * pay / cosf


def ups_secimi(yuk_va, otonomi_dk=15.0, verim=0.9, aku_v=12.0,
               hucre=32.0):
    """UPS ve aku: (ups_kVA, aku_Ah). UPS bir ust %25 payla secilir;
    aku Ah=S t/(V hucre verim)*1000/60 pratik bagintidir
    [STANDART-TEYIT]; aku yaslanma payi projede eklenir.
    """
    s = float(yuk_va)
    t = float(otonomi_dk)
    ver = float(verim)
    v = float(aku_v)
    n = float(hucre)
    if s <= 0 or t <= 0 or v <= 0 or n <= 0:
        raise ValueError("girisler pozitif olmali")
    if not (0 < ver <= 1.0):
        raise ValueError("verim (0,1] araliginda olmali")
    ups = s * 1.25 / 1000.0
    ah = s * (t / 60.0) / (v * n * ver) * 1000.0
    return ups, ah


def trafo_gucu(kurulu_kva, talep=0.7):
    """Trafo gucu, kVA. Ihtiyac=kurulu*talep; bir ust standart secilir.

    Talep katsayisi yuk etudune aittir [STANDART-TEYIT].
    """
    k = float(kurulu_kva)
    t = float(talep)
    if k <= 0 or not (0 < t <= 1.0):
        raise ValueError("girisler gecerli olmali")
    ihtiyac = k * t
    for guc in _TRAFO:
        if guc >= ihtiyac:
            return float(guc)
    raise ValueError("guc trafo dizisini asiyor")


def salter_ayari(trafo_kva, gerilim_v=400.0):
    """Trafo AG ana salter akimi, A. In=tavan(S/(kok3 U)) standart dizi.

    IEC 60364-4-43 esasli pratik onsecim; ayarlanabilir acma egrisi
    selektivite etudunde teyit edilir [STANDART-TEYIT].
    """
    s = float(trafo_kva)
    u = float(gerilim_v)
    if s <= 0 or u <= 0:
        raise ValueError("girisler pozitif olmali")
    ib = s * 1000.0 / (math.sqrt(3.0) * u)
    for anma in _ANMA:
        if anma >= ib:
            return float(anma)
    raise ValueError("akim salter dizisini asiyor")


def busbar_kesit(akim_a, yogunluk_a_mm2=1.5):
    """Busbar kesiti, mm2. S=I/J. Bakir bara akim yogunlugu pratik
    kabul [STANDART-TEYIT]; kisa devre dayanimi projede teyit edilir.
    """
    i = float(akim_a)
    j = float(yogunluk_a_mm2)
    if i <= 0 or j <= 0:
        raise ValueError("girisler pozitif olmali")
    return i / j


def bakir_agirlik(kesit_mm2, uzunluk_m, damar=3):
    """Kablo bakir agirligi, kg. m=kesit L damar 8.96/1000.

    Kesif/metraj pratigidir [STANDART-TEYIT].
    """
    s = float(kesit_mm2)
    l_m = float(uzunluk_m)
    n = int(damar)
    if s <= 0 or l_m < 0 or n <= 0:
        raise ValueError("girisler gecerli olmali")
    return s * l_m * n * 8.96 / 1000.0


def tava_doluluk(kablo_caplar_mm, tava_mm=300.0, yukseklik_mm=60.0,
                 sinir=0.4):
    """Kablo tavasi doluluk orani, %. Doluluk=kablo alani/tava alani.

    %40 sinir IEC 61537 esasli pratik kabul [STANDART-TEYIT].
    """
    caps = [float(c) for c in kablo_caplar_mm]
    if not caps or any(c <= 0 for c in caps):
        raise ValueError("cap listesi gecerli olmali")
    w = float(tava_mm)
    h = float(yukseklik_mm)
    lim = float(sinir)
    if w <= 0 or h <= 0 or not (0 < lim <= 1.0):
        raise ValueError("tava olculeri gecerli olmali")
    kablo_alan = sum(math.pi * (c / 2.0) ** 2 for c in caps)
    return kablo_alan / (w * h) * 100.0


def dedektor_sayisi(alan_m2, tip="duman"):
    """Yangin dedektor sayisi, adet. Duman: 60 m2, isinim: 30 m2
    kapsama pratik kabul [STANDART-TEYIT]; EN 54-14 yerlesim
    kurallarina gore teyit edilir."""
    a = float(alan_m2)
    if a <= 0:
        raise ValueError("alan pozitif olmali")
    tablo = {"duman": 60.0, "isinim": 30.0, "kombine": 60.0}
    key = str(tip).lower()
    if key not in tablo:
        raise ValueError("tip duman/isinim/kombine olmali")
    return int(math.ceil(a / tablo[key]))


def yangin_zon(alan_m2, zon_max_m2=2000.0):
    """Yangin alarm zon sayisi, adet. Zon alani EN 54-14 esasli
    pratik (2000 m2) [STANDART-TEYIT]."""
    a = float(alan_m2)
    z = float(zon_max_m2)
    if a <= 0 or z <= 0:
        raise ValueError("girisler pozitif olmali")
    return int(math.ceil(a / z))


def acil_aydinlatma(alan_m2, lux=1.0, armatur_lumen=300.0, sure_h=3.0):
    """Acil aydinlatma: (armatur_adet, aku_sure_h).

    Aydinlik EN 1838 esasli pratik (kacis hatti 1 lx)
    [STANDART-TEYIT]; sure sinifi (1/3 h) projede secilir.
    """
    a = float(alan_m2)
    e = float(lux)
    f = float(armatur_lumen)
    sure = float(sure_h)
    if a <= 0 or e <= 0 or f <= 0 or sure <= 0:
        raise ValueError("girisler pozitif olmali")
    return int(math.ceil(e * a / f)), sure


def motor_yol_verme(guc_kw, gerilim_v=400.0, cosfi=0.85, verim=0.9,
                    tip="dogrudan"):
    """Motor yol verme: (anma_A, kalkis_A). Kalkis katsayisi: dogrudan
    7, yildiz-ucgen 2.5, soft-starter 3.5, surucu 1.5 pratik kabul
    [STANDART-TEYIT]; IEC 60947-4-1 kontaktor secimi projede teyit edilir.
    """
    p = float(guc_kw)
    u = float(gerilim_v)
    if p <= 0 or u <= 0:
        raise ValueError("guc ve gerilim pozitif olmali")
    if not (0 < float(cosfi) <= 1.0) or not (0 < float(verim) <= 1.0):
        raise ValueError("cosfi ve verim (0,1] araliginda olmali")
    katsayi = {"dogrudan": 7.0, "yildiz-ucgen": 2.5, "soft": 3.5,
               "surucu": 1.5}
    key = str(tip).lower()
    if key not in katsayi:
        raise ValueError("tip dogrudan/yildiz-ucgen/soft/surucu olmali")
    anma = p * 1000.0 / (math.sqrt(3.0) * u * float(cosfi) * float(verim))
    return anma, anma * katsayi[key]


def es_potansiyel(ana_kesit_mm2):
    """Es potansiyel baglanti kesiti, mm2. S/2, en az 6 mm2.

    IEC 60364-5-54 esasli pratik; ana topraklama barasi projede
    teyit edilir [STANDART-TEYIT].
    """
    s = float(ana_kesit_mm2)
    if s <= 0:
        raise ValueError("kesit pozitif olmali")
    return max(6.0, s / 2.0)


def data_limit(protokol="ethernet"):
    """Data hatti uzunluk siniri, m. EN 50173 esasli pratik tablo
    [STANDART-TEYIT]; kablo sinifi projede teyit edilir."""
    tablo = {"ethernet": 100.0, "rs485": 1200.0, "usb2": 5.0,
             "hdmi": 15.0, "fiber": 2000.0, "knx": 1000.0}
    key = str(protokol).lower()
    if key not in tablo:
        raise ValueError("protokol ethernet/rs485/usb2/hdmi/fiber/knx olmali")
    return tablo[key]


def pano_isi(kayip_w, debi_m3h=None, dt_k=10.0):
    """Pano isi yuku ve fan: (kW, gerekli_debi_m3h).

    Q=P/(rho cp dT)*3600; rho=1.2, cp=1.005. dT pratik kabul
    [STANDART-TEYIT]; filtre/klima secimi pano projesine aittir.
    """
    p = float(kayip_w)
    dt = float(dt_k)
    if p < 0 or dt <= 0:
        raise ValueError("girisler gecerli olmali")
    debi = p / (1.2 * 1.005 * 1000.0 * dt) * 3600.0
    if debi_m3h is not None and float(debi_m3h) < 0:
        raise ValueError("debi negatif olamaz")
    return p / 1000.0, debi


def talep_guc(kalemler_kw, eszaman=0.7):
    """Talep guc, kW. Talep=kurulu*eszaman.

    Eszamanlilik katsayisi yuk tipine gore secilir, pratik kabul
    [STANDART-TEYIT]; dagitim sirketi sarti projede teyit edilir.
    """
    if isinstance(kalemler_kw, (int, float)):
        kalemler = [float(kalemler_kw)]
    else:
        kalemler = [float(x) for x in kalemler_kw]
    if not kalemler or any(x < 0 for x in kalemler):
        raise ValueError("kalemler gecerli olmali")
    esz = float(eszaman)
    if not (0 < esz <= 1.0):
        raise ValueError("eszaman (0,1] araliginda olmali")
    kurulu = sum(kalemler)
    return kurulu, kurulu * esz


def enerji_tuketim(guc_kw, sure_h, adet=1):
    """Enerji tuketimi, kWh. E=P t n (kesif/fatura onhesabi)."""
    p = float(guc_kw)
    t = float(sure_h)
    n = float(adet)
    if p < 0 or t < 0 or n <= 0:
        raise ValueError("girisler gecerli olmali")
    return p * t * n
