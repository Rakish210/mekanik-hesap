"""Yakit tuketimi hesabi (KATALOG.md Ek, 1. hesap).

B = P / (eta * Hu). Hu alt isil degerdir; yakit tablosu
pratik katalog degeridir [STANDART-TEYIT], fatura/sartname
Hu degeri esastir.
"""

# Hu: kWh birimi basina (m3 veya kg). [STANDART-TEYIT]
YAKIT_HU = {
    "dogalgaz": {"hu": 9.64, "tuketim_birim": "m3/h"},
    "lpg": {"hu": 12.8, "tuketim_birim": "kg/h"},
    "motorin": {"hu": 11.86, "tuketim_birim": "kg/h"},
    "fueloil": {"hu": 11.2, "tuketim_birim": "kg/h"},
    "komur": {"hu": 7.0, "tuketim_birim": "kg/h"},
    "pelet": {"hu": 4.9, "tuketim_birim": "kg/h"},
}


def saatlik_tuketim(guc_kw, verim, yakit="dogalgaz", hu_kwh=None):
    """Saatlik yakit tuketimi -> (tuketim, birim).

    guc_kw: faydali isi gucu; verim: 0-1; hu_kwh: ozel Hu
    verilirse tablo yerine kullanilir.
    """
    p, eta = float(guc_kw), float(verim)
    if p <= 0 or not (0 < eta <= 1.0):
        raise ValueError("guc pozitif, verim (0,1] olmali")
    if hu_kwh is None:
        if str(yakit) not in YAKIT_HU:
            raise ValueError("bilinmeyen yakit: %r" % (yakit,))
        hu = YAKIT_HU[str(yakit)]["hu"]
        birim = YAKIT_HU[str(yakit)]["tuketim_birim"]
    else:
        hu = float(hu_kwh)
        birim = "m3/h" if str(yakit) == "dogalgaz" else "kg/h"
        if hu <= 0:
            raise ValueError("Hu pozitif olmali")
    return p / eta / hu, birim


def gunluk_tuketim(saatlik, calisma_saat):
    """Gunluk tuketim = saatlik * calisma saati."""
    b, t = float(saatlik), float(calisma_saat)
    if b < 0 or t <= 0:
        raise ValueError("girisler gecerli olmali")
    return b * t


def sezonluk_tuketim(gunluk, gun, es_zaman=1.0):
    """Sezonluk tuketim = gunluk * gun * es_zamanlilik."""
    g, n, e = float(gunluk), float(gun), float(es_zaman)
    if g < 0 or n <= 0 or not (0 < e <= 1.0):
        raise ValueError("girisler gecerli olmali")
    return g * n * e
