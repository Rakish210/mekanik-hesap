"""Birim ceviriciler: uzunluk, basinc, debi, guc, enerji, sicaklik.

Dayanak: SI birim sistemi. Sicaklik donusumu ayri fonksiyondadir
(fark ve mutlak deger karisikligini onlemek icin convert disinda).
"""

from typing import Union

_LENGTH = {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0}
_PRESSURE = {
    "pa": 1.0,
    "kpa": 1000.0,
    "bar": 100000.0,
    "mbar": 100.0,
    "mmhg": 133.322,
    "mss": 9806.65,  # metre su sutunu
}
_FLOW = {"m3s": 1.0, "m3h": 1.0 / 3600.0, "ls": 0.001, "lmin": 0.001 / 60.0}
_POWER = {"w": 1.0, "kw": 1000.0, "mw": 1.0e6}
_ENERGY = {"j": 1.0, "kj": 1000.0, "kwh": 3.6e6, "kcal": 4184.0}

_TABLES = (_LENGTH, _PRESSURE, _FLOW, _POWER, _ENERGY)


def convert(value: Union[int, float], from_unit: str, to_unit: str) -> float:
    """Degeri from_unit biriminden to_unit birimine cevirir.

    Ornek: convert(1000, "mm", "m") -> 1.0
    Sicaklik birimleri burada yoktur; c_to_k / k_to_c kullanin.
    Bilinmeyen veya farkli tablolardan birimler ValueError verir.
    """
    fu = str(from_unit).lower()
    tu = str(to_unit).lower()
    for tab in _TABLES:
        if fu in tab and tu in tab:
            return float(value) * tab[fu] / tab[tu]
    raise ValueError("cevrim yok: %r -> %r" % (from_unit, to_unit))


def c_to_k(t_c: Union[int, float]) -> float:
    """Santigradi kelvine cevirir."""
    return float(t_c) + 273.15


def k_to_c(t_k: Union[int, float]) -> float:
    """Kelvini santigrada cevirir."""
    return float(t_k) - 273.15
