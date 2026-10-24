"""Boru surtunme faktoru: Colebrook-White + Haaland acik formu.

Kaynak: Colebrook (1939) deneysel baginti; Haaland (1983) acik yaklasim.
p: puruzluluk (m), D: ic cap (m), Re: Reynolds sayisi.
"""

import math
from typing import Union


def reynolds(rho: Union[int, float], V: Union[int, float],
             D: Union[int, float], mu: Union[int, float]) -> float:
    """Reynolds sayisi: rho (kg/m3), V (m/s), D (m), mu (Pa.s)."""
    rho, V, D, mu = float(rho), float(V), float(D), float(mu)
    if D <= 0 or mu <= 0:
        raise ValueError("D ve mu pozitif olmali")
    return rho * V * D / mu


def haaland(Re: Union[int, float], eps: Union[int, float],
            D: Union[int, float]) -> float:
    """Haaland acik formu. Turbulansli akis (Re >= 2300) ister."""
    Re, eps, D = float(Re), float(eps), float(D)
    if Re < 2300 or D <= 0 or eps < 0:
        raise ValueError("Re >= 2300, D > 0, eps >= 0 olmali")
    term = ((eps / D) / 3.7) ** 1.11 + 6.9 / Re
    return (1.0 / (-1.8 * math.log10(term))) ** 2


def colebrook(Re: Union[int, float], eps: Union[int, float],
              D: Union[int, float], tol: float = 1e-8,
              max_iter: int = 50) -> float:
    """Colebrook-White cozumu (Haaland baslangicli iterasyon).

    Re < 2300 icin laminer baginti (64/Re) doner.
    """
    Re = float(Re)
    if Re < 2300:
        if Re <= 0:
            raise ValueError("Re pozitif olmali")
        return 64.0 / Re
    f = haaland(Re, eps, D)
    for _ in range(max_iter):
        rhs = -2.0 * math.log10((eps / D) / 3.7 + 2.51 / (Re * math.sqrt(f)))
        f_new = (1.0 / rhs) ** 2
        if abs(f_new - f) < tol:
            return f_new
        f = f_new
    return f