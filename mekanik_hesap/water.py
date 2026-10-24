"""4-100 C arasi su ozellikleri: yogunluk, viskozite, doyma basinci.

Kaynak: IAPWS-IF97 doymus su tablolari (NIST Chemistry WebBook su
verileri). Ara sicakliklar tablodan enterpolasyonla bulunur
(doyma basincinda logaritmik enterpolasyon).
"""

from typing import Union

_T = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
_RHO = [  # kg/m3, doymus sivi yogunlugu
    999.84,
    999.70,
    998.21,
    995.65,
    992.22,
    988.03,
    983.20,
    977.76,
    971.80,
    965.32,
    958.35,
]
_MU = [  # mPa.s, dinamik viskozite
    1.787,
    1.307,
    1.002,
    0.797,
    0.653,
    0.547,
    0.467,
    0.404,
    0.355,
    0.315,
    0.282,
]
_PSAT = [  # kPa, doyma basinci
    0.611,
    1.228,
    2.339,
    4.247,
    7.385,
    12.35,
    19.95,
    31.20,
    47.41,
    70.14,
    101.42,
]

_TMIN, _TMAX = 4.0, 100.0


def _check(t_c: Union[int, float]) -> float:
    t = float(t_c)
    if not (_TMIN <= t <= _TMAX):
        raise ValueError("sicaklik 4-100 C araliginda olmali")
    return t


def _lin(t: float, ys: list[float]) -> float:
    for i in range(len(_T) - 1):
        if _T[i] <= t <= _T[i + 1]:
            w = (t - _T[i]) / (_T[i + 1] - _T[i])
            return ys[i] + w * (ys[i + 1] - ys[i])
    return ys[-1]


def density(t_c: Union[int, float]) -> float:
    """Su yogunlugu, kg/m3."""
    return _lin(_check(t_c), _RHO)


def dyn_viscosity(t_c: Union[int, float]) -> float:
    """Dinamik viskozite, Pa.s."""
    return _lin(_check(t_c), _MU) / 1000.0


def kin_viscosity(t_c: Union[int, float]) -> float:
    """Kinematik viskozite, m2/s."""
    t = _check(t_c)
    return dyn_viscosity(t) / density(t)


def sat_pressure(t_c: Union[int, float]) -> float:
    """Doyma basinci, kPa (logaritmik enterpolasyon)."""
    t = _check(t_c)
    for i in range(len(_T) - 1):
        if _T[i] <= t <= _T[i + 1]:
            w = (t - _T[i]) / (_T[i + 1] - _T[i])
            lo, hi = _PSAT[i], _PSAT[i + 1]
            if lo <= 0:
                return hi * w
            return lo * (hi / lo) ** w
    return _PSAT[-1]
