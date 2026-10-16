"""Yardimci 3/7: su ozellikleri (water sarmalasi).

Dayanak: IAPWS-IF97 doymus su tablolari (NIST Chemistry WebBook
su verileri) [STANDART-TEYIT]. Bu modul veri uretmez;
mekanik_hesap.water fonksiyonlarini katalog kalemi olarak sarar.
Sicaklik araligi 4-100 C.
"""

from mekanik_hesap.water import (
    density, dyn_viscosity, kin_viscosity, sat_pressure,
)


def su_yogunlugu(t_c):
    """Su yogunlugu, kg/m3. 4-100 C."""
    return density(t_c)


def su_dinamik_viskozite(t_c):
    """Dinamik viskozite, Pa.s. 4-100 C."""
    return dyn_viscosity(t_c)


def su_kinematik_viskozite(t_c):
    """Kinematik viskozite, m2/s. 4-100 C."""
    return kin_viscosity(t_c)


def su_doyma_basinci(t_c):
    """Doyma basinci, kPa. 4-100 C (logaritmik enterpolasyon)."""
    return sat_pressure(t_c)
