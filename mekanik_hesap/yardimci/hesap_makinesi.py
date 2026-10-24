"""Yardimci 4/7: bilimsel hesap makinesi fonksiyonlari.

Dayanak: temel matematik tanimlari [STANDART-TEYIT]. Bagintilar
seffaf ve birimsizdir; aci fonksiyonlari derece alir. Dis
kaynak ve site icerigi yoktur.
"""

import math
from typing import Union


def us_al(taban: Union[int, float], us: Union[int, float]) -> float:
    """Ust alma: taban**us."""
    return float(taban) ** float(us)


def kok(deger: Union[int, float], derece: Union[int, float] = 2.0) -> float:
    """n. dereceden kok. deger >= 0, derece > 0 olmali."""
    x, n = float(deger), float(derece)
    if x < 0 or n <= 0:
        raise ValueError("deger >= 0, derece > 0 olmali")
    return x ** (1.0 / n)


def log10(deger: Union[int, float]) -> float:
    """10 tabaninda logaritma. deger > 0 olmali."""
    x = float(deger)
    if x <= 0:
        raise ValueError("deger pozitif olmali")
    return math.log10(x)


def ln(deger: Union[int, float]) -> float:
    """Dogal logaritma. deger > 0 olmali."""
    x = float(deger)
    if x <= 0:
        raise ValueError("deger pozitif olmali")
    return math.log(x)


def exp(deger: Union[int, float]) -> float:
    """Ustel fonksiyon: e**deger."""
    return math.exp(float(deger))


def sin_deg(aci_deg: Union[int, float]) -> float:
    """Sinus, aci derece."""
    return math.sin(math.radians(float(aci_deg)))


def cos_deg(aci_deg: Union[int, float]) -> float:
    """Kosinus, aci derece."""
    return math.cos(math.radians(float(aci_deg)))


def tan_deg(aci_deg: Union[int, float]) -> float:
    """Tanjant, aci derece."""
    return math.tan(math.radians(float(aci_deg)))


def faktoriyel(n: Union[int, float]) -> float:
    """Faktoriyel. n negatif olmayan tamsayi olmali."""
    k = int(n)
    if k != float(n) or k < 0:
        raise ValueError("n negatif olmayan tamsayi olmali")
    return float(math.factorial(k))


def yuzde(parca: Union[int, float], butun: Union[int, float]) -> float:
    """Yuzde: parca/butun*100. butun sifir olamaz."""
    p, b = float(parca), float(butun)
    if b == 0:
        raise ValueError("butun sifir olamaz")
    return p / b * 100.0


def hipotenus(a: Union[int, float], b: Union[int, float]) -> float:
    """Dik kenarlardan hipotenus: kok(a2+b2)."""
    return math.hypot(float(a), float(b))


def deg_to_rad(aci_deg: Union[int, float]) -> float:
    """Dereceyi radyana cevirir."""
    return math.radians(float(aci_deg))


def rad_to_deg(aci_rad: Union[int, float]) -> float:
    """Radyani dereceye cevirir."""
    return math.degrees(float(aci_rad))
