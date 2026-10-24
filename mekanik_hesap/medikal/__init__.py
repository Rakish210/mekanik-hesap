"""Medikal gaz hesaplari (KATALOG.md 11. baslik, 5 hesap).

Dayanak: HTM 02-01 (medikal gaz boru sistemleri tasarim ve
isletme), ISO 7396-1 (Tibbi gaz boru sistemleri).
Priz birim debileri, eszamanlilik katsayilari, boru hiz sinirlari
ve manifold otonomi sureleri hastane tipine gore degisir; deger
secimi projeye aittir, pratik kabuller [STANDART-TEYIT: HTM 02-01, ISO 7396-1] ile
isaretlidir. Teyit edilmeden imalata esas alinmaz.
"""

import math
from typing import Union


def oksijen_debi(kalemler: list[tuple[Union[int, float],
                                        Union[int, float]]],
                  eszamanlilik: float = 0.3) -> float:
    """Oksijen toplami, L/dk.

    kalemler: [(birim_debi_Ldk, adet), ...]; sonuc =
    toplam*eszamanlilik. Birim debi (or. servis 10 L/dk,
    yogun bakim 20 L/dk) ve eszamanlilik pratik kabul
    [STANDART-TEYIT: HTM 02-01, ISO 7396-1]; HTM 02-01 bolumune gore teyit edilir.
    """
    top = 0.0
    for birim, adet in kalemler:
        if float(birim) < 0 or float(adet) < 0:
            raise ValueError("birim debi ve adet negatif olamaz")
        top += float(birim) * float(adet)
    esz = float(eszamanlilik)
    if not (0 < esz <= 1.0):
        raise ValueError("eszamanlilik (0,1] araliginda olmali")
    return top * esz


def manifold_ihtiyaci(gunluk_m3: Union[int, float],
                      otonomi_gun: float = 7.0,
                      tup_su_hacmi_l: float = 50.0,
                      dolum_bar: float = 200.0
                      ) -> tuple[float, int]:
    """Manifold: (toplam_m3, tup_adet).

    toplam = gunluk*otonomi; tek tup gaz m3 = su_hacmi_L/1000*bar.
    Otonomi suresi ve tup verisi projedir [STANDART-TEYIT: HTM 02-01, ISO 7396-1];
    HTM 02-01 manifold yedekliligine gore teyit edilir.
    """
    gun = float(gunluk_m3)
    oto = float(otonomi_gun)
    su_l, bar = float(tup_su_hacmi_l), float(dolum_bar)
    if gun <= 0 or oto <= 0 or su_l <= 0 or bar <= 0:
        raise ValueError("girisler pozitif olmali")
    toplam = gun * oto
    tek = su_l / 1000.0 * bar
    return toplam, int(math.ceil(toplam / tek))


def vakum_kapasitesi(priz_adet: int, birim_l_dk: float = 40.0,
                     eszaman: float = 0.3) -> float:
    """Vakum pompasi kapasitesi, L/dk (m3/h icin *0.06).

    Birim cekis ve eszaman pratik kabul [STANDART-TEYIT: HTM 02-01, ISO 7396-1];
    HTM 02-01 / ISO 7396-1 vakum zon degerlerine gore teyit edilir.
    """
    adet = int(priz_adet)
    birim, esz = float(birim_l_dk), float(eszaman)
    if adet <= 0 or birim <= 0 or not (0 < esz <= 1.0):
        raise ValueError("girisler gecerli olmali")
    return adet * birim * esz


def medikal_hava_debisi(priz_adet: int, birim_l_dk: float = 50.0,
                        eszaman: float = 0.3) -> float:
    """Medikal basincli hava debisi, L/dk.

    Birim debi ve eszaman pratik kabul [STANDART-TEYIT: HTM 02-01, ISO 7396-1];
    HTM 02-01 / ISO 7396-1 hava zon degerlerine gore teyit edilir.
    Kompresor seciminde %10-20 yedek pay ayrica eklenir.
    """
    adet = int(priz_adet)
    birim, esz = float(birim_l_dk), float(eszaman)
    if adet <= 0 or birim <= 0 or not (0 < esz <= 1.0):
        raise ValueError("girisler gecerli olmali")
    return adet * birim * esz


def medikal_boru_capi(debi_l_dk: Union[int, float],
                      hiz_ms: float = 8.0) -> float:
    """Medikal gaz boru ic capi, mm. d = kok(4Q/pi v).

    Gaz hizi siniri HTM 02-01 esasli pratik kabul
    [STANDART-TEYIT: HTM 02-01, ISO 7396-1]; hat basinci ve gaz tipine gore teyit edilir.
    """
    debi, hiz = float(debi_l_dk), float(hiz_ms)
    if debi <= 0 or hiz <= 0:
        raise ValueError("debi ve hiz pozitif olmali")
    q = debi / 1000.0 / 60.0
    return math.sqrt(4.0 * q / math.pi / hiz) * 1000.0


def zon_vana(priz_adet: int, zon_max_priz: int = 20
             ) -> tuple[int, int]:
    """Priz ve zon vana yerlesimi: (priz_adet, zon_vana_adet).

    Zon basina azami priz pratik kabul [STANDART-TEYIT: HTM 02-01, ISO 7396-1];
    HTM 02-01 zon vana/alan alarm yerlesimine gore teyit edilir.
    """
    adet = int(priz_adet)
    zmax = int(zon_max_priz)
    if adet <= 0 or zmax <= 0:
        raise ValueError("adetler pozitif olmali")
    return adet, int(math.ceil(adet / zmax))