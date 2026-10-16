"""Yagmur suyu boru agi hesabi (KATALOG.md Ek, 6. hesap).

Dayanak: TS EN 12056-3 (yagmur suyu drenaji).
Q = A*i/3600 (L/s). Yagis siddeti MGM/yerel idareden secilir
[STANDART-TEYIT]. Cap tablosu pratik [STANDART-TEYIT].
"""

# Debi araligi -> onerilen cap, mm [STANDART-TEYIT]
CAP_TABLOSU = ((2.0, 75.0), (5.0, 110.0), (9.0, 125.0),
               (14.0, 160.0), (25.0, 200.0))


def cati_debisi(alan_m2, yagis_mm_h=150.0):
    """Cati debisi, L/s. Q = A*i/3600."""
    alan, yagis = float(alan_m2), float(yagis_mm_h)
    if alan <= 0 or yagis <= 0:
        raise ValueError("alan ve yagis pozitif olmali")
    return alan * yagis / 3600.0


def suzgec_dagilimi(alanlar_m2, yagis_mm_h=150.0):
    """Suzgec basina dusen alan listesi -> [(alan, debi_Ls)].

    Her suzgec kendi toplama alanini drene eder; esit dagilim
    kabulu yapilmaz.
    """
    dag = []
    for alan in alanlar_m2:
        dag.append((float(alan), cati_debisi(alan, yagis_mm_h)))
    if not dag:
        raise ValueError("suzgec listesi bos olamaz")
    return dag


def yagmur_boru_capi(debi_ls):
    """Debiye gore yagmur boru capi, mm [STANDART-TEYIT]."""
    debi = float(debi_ls)
    if debi <= 0:
        raise ValueError("debi pozitif olmali")
    for sinir, cap in CAP_TABLOSU:
        if debi <= sinir:
            return cap
    return 250.0


def ag_hesabi(alanlar_m2, yagis_mm_h=150.0):
    """Boru agi -> {'branslar': [...], 'toplam_Ls': x, 'ana_cap': DN}.

    Branslar suzgec debileridir; ana kol toplam debiyi tasir.
    """
    dag = suzgec_dagilimi(alanlar_m2, yagis_mm_h)
    toplam = sum(debi for _, debi in dag)
    return {"branslar": [{"alan_m2": a, "debi_Ls": q,
                          "cap": yagmur_boru_capi(q)} for a, q in dag],
            "toplam_Ls": toplam,
            "ana_cap": yagmur_boru_capi(toplam)}
