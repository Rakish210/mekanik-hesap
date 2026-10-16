"""Havuz tesisati hesaplari (KATALOG.md 6. baslik, 4 hesap).

Dayanak: TS EN 15288 (yuzme havuzlari guvenlik),
TS EN 13451 (havuz donanimi). Devir suresi, filtrasyon hizi
ve isitma kabulleri tip secimidir [STANDART-TEYIT]; isletme
sartnamesi ile netlestirilir.
"""


def havuz_hacim(uzunluk_m, genislik_m, derinlik_m):
    """Havuz su hacmi, m3. V = L*B*h_ort."""
    l_m, b_m, h_m = (float(uzunluk_m), float(genislik_m),
                     float(derinlik_m))
    if l_m <= 0 or b_m <= 0 or h_m <= 0:
        raise ValueError("olculer pozitif olmali")
    return l_m * b_m * h_m


def devir_debisi(hacim_m3, devir_saat=6.0):
    """Havuz devir debisi, m3/h. Q = V/T. Devir suresi tip
    secimidir [STANDART-TEYIT] (ozel/kamu havuzu farkli)."""
    v_m3, t_h = float(hacim_m3), float(devir_saat)
    if v_m3 <= 0 or t_h <= 0:
        raise ValueError("hacim ve devir suresi pozitif olmali")
    return v_m3 / t_h


def filtre_pompa(debir_m3h, filtrasyon_hizi=30.0):
    """Filtre alani (m2) ve pompa debisi (m3/h) onerisi.

    A = Q/v_f. Filtrasyon hizi kum filtre pratigi
    [STANDART-TEYIT]; katalog ile dogrulanir.
    """
    q_m3h, vf = float(debir_m3h), float(filtrasyon_hizi)
    if q_m3h <= 0 or vf <= 0:
        raise ValueError("girisler pozitif olmali")
    return q_m3h, q_m3h / vf


def havuz_isitma(hacim_m3, dt_k, isitma_saati=24.0):
    """Havuz suyu ilk isitma yuku, kW. Q = V*1.161*dT/t."""
    v_m3, dt, t_h = float(hacim_m3), float(dt_k), float(isitma_saati)
    if v_m3 <= 0 or dt <= 0 or t_h <= 0:
        raise ValueError("girisler pozitif olmali")
    return v_m3 * 1.161 * dt / t_h


def kapali_havuz_havalandirma(havuz_alani_m2, q_birim_m3h_m2=10.0):
    """Kapali havuz havalandirma/nem alma debisi, m3/h.

    Pratik birim debi ile on secim [STANDART-TEYIT]; nem yuku
    buharlasma hesabiyla netlestirilir.
    """
    alan, qb = float(havuz_alani_m2), float(q_birim_m3h_m2)
    if alan <= 0 or qb <= 0:
        raise ValueError("girisler pozitif olmali")
    return alan * qb
