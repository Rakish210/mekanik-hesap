"""Yardimci hesaplar (7 hesap) testleri."""

import math
import unittest

from mekanik_hesap.yardimci import (
    birim,
    surtunme,
    su_ozellik,
    hesap_makinesi,
    mmo_bedel,
    mesafe,
    bep_karbon,
)
from mekanik_hesap import units, colebrook, water


class TestBirim(unittest.TestCase):
    def test_sarmalama(self):
        self.assertAlmostEqual(birim.birim_cevir(1000, "mm", "m"), 1.0)
        self.assertAlmostEqual(
            birim.birim_cevir(1, "bar", "kpa"),
            units.convert(1, "bar", "kpa"),
        )
        self.assertAlmostEqual(birim.santigrat_to_kelvin(0), 273.15)
        self.assertAlmostEqual(birim.kelvin_to_santigrat(273.15), 0.0)

    def test_hatalar(self):
        with self.assertRaises(ValueError):
            birim.birim_cevir(1, "mm", "bar")


class TestSurtunme(unittest.TestCase):
    def test_sarmalama(self):
        self.assertAlmostEqual(
            surtunme.reynolds_sayisi(1000.0, 1.0, 0.1, 0.001), 100000.0
        )
        f_h = colebrook.haaland(100000.0, 0.000045, 0.1)
        self.assertAlmostEqual(surtunme.haaland_faktoru(100000.0, 0.000045, 0.1), f_h)
        self.assertAlmostEqual(
            surtunme.surtunme_faktoru(100000.0, 0.000045, 0.1), f_h, places=3
        )
        self.assertAlmostEqual(surtunme.surtunme_faktoru(1000.0, 0.0, 0.1), 0.064)

    def test_darcy(self):
        dp = surtunme.darcy_kayip(0.02, 100.0, 0.1, 1000.0, 1.0)
        self.assertAlmostEqual(dp, 0.02 * (100.0 / 0.1) * 1000.0 * 0.5)
        with self.assertRaises(ValueError):
            surtunme.darcy_kayip(0.02, 100.0, 0.0, 1000.0, 1.0)
        with self.assertRaises(ValueError):
            surtunme.haaland_faktoru(1000.0, 0.000045, 0.1)


class TestSuOzellik(unittest.TestCase):
    def test_sarmalama(self):
        self.assertAlmostEqual(su_ozellik.su_yogunlugu(20), water.density(20))
        self.assertAlmostEqual(
            su_ozellik.su_dinamik_viskozite(20), water.dyn_viscosity(20)
        )
        self.assertAlmostEqual(
            su_ozellik.su_kinematik_viskozite(20), water.kin_viscosity(20)
        )
        self.assertAlmostEqual(
            su_ozellik.su_doyma_basinci(100), water.sat_pressure(100), places=1
        )

    def test_hatalar(self):
        with self.assertRaises(ValueError):
            su_ozellik.su_yogunlugu(200)


class TestHesapMakinesi(unittest.TestCase):
    def test_fonksiyonlar(self):
        m = hesap_makinesi
        self.assertAlmostEqual(m.us_al(2, 10), 1024.0)
        self.assertAlmostEqual(m.kok(9), 3.0)
        self.assertAlmostEqual(m.kok(27, 3), 3.0)
        self.assertAlmostEqual(m.log10(1000), 3.0)
        self.assertAlmostEqual(m.ln(math.e), 1.0)
        self.assertAlmostEqual(m.exp(0), 1.0)
        self.assertAlmostEqual(m.sin_deg(30), 0.5, places=6)
        self.assertAlmostEqual(m.cos_deg(60), 0.5, places=6)
        self.assertAlmostEqual(m.tan_deg(45), 1.0, places=6)
        self.assertAlmostEqual(m.faktoriyel(5), 120.0)
        self.assertAlmostEqual(m.yuzde(25, 200), 12.5)
        self.assertAlmostEqual(m.hipotenus(3, 4), 5.0)
        self.assertAlmostEqual(m.deg_to_rad(180), math.pi)
        self.assertAlmostEqual(m.rad_to_deg(math.pi), 180.0)

    def test_hatalar(self):
        m = hesap_makinesi
        for fn in (
            lambda: m.kok(-1),
            lambda: m.log10(0),
            lambda: m.ln(-2),
            lambda: m.faktoriyel(-1),
            lambda: m.faktoriyel(2.5),
            lambda: m.yuzde(1, 0),
        ):
            with self.assertRaises(ValueError):
                fn()


class TestMmoBedel(unittest.TestCase):
    def test_bedel(self):
        b = mmo_bedel.proje_bedeli(1000, 50, sinif="konut")
        self.assertAlmostEqual(b, 50000.0)
        b2 = mmo_bedel.proje_bedeli(1000, 50, katsayi=1.2)
        self.assertAlmostEqual(b2, 60000.0)
        self.assertAlmostEqual(mmo_bedel.kdv_dahil(1000), 1200.0)
        self.assertAlmostEqual(mmo_bedel.birim_alana_bedel(50000, 1000), 50.0)

    def test_hatalar(self):
        for fn in (
            lambda: mmo_bedel.proje_bedeli(0, 50),
            lambda: mmo_bedel.proje_bedeli(100, 50, sinif="bilinmez"),
            lambda: mmo_bedel.proje_bedeli(100, 50, katsayi=0),
            lambda: mmo_bedel.kdv_dahil(-5),
            lambda: mmo_bedel.birim_alana_bedel(100, 0),
        ):
            with self.assertRaises(ValueError):
                fn()


class TestMesafe(unittest.TestCase):
    def test_kus_ucusu(self):
        d = mesafe.kus_ucusu_km(41.0, 29.0, 39.9, 32.8)
        self.assertTrue(300 < d < 450, d)  # istanbul-ankara olcegi
        self.assertAlmostEqual(mesafe.kus_ucusu_km(41.0, 29.0, 41.0, 29.0), 0.0)

    def test_sehir_yol_sure(self):
        kus, yol = mesafe.sehir_mesafesi("istanbul", "ankara")
        self.assertAlmostEqual(yol, kus * mesafe.YOL_KATSAYI)
        self.assertAlmostEqual(mesafe.yol_mesafesi(100), 130.0)
        self.assertAlmostEqual(mesafe.seyahat_suresi(180, 90), 2.0)

    def test_hatalar(self):
        with self.assertRaises(KeyError):
            mesafe.sehir_mesafesi("istanbul", "bilinmez")
        for fn in (
            lambda: mesafe.yol_mesafesi(-1),
            lambda: mesafe.seyahat_suresi(100, 0),
            lambda: mesafe.sehir_mesafesi("istanbul", "ankara", yol_katsayi=0),
        ):
            with self.assertRaises(ValueError):
                fn()


class TestBepKarbon(unittest.TestCase):
    def test_emisyon(self):
        self.assertAlmostEqual(bep_karbon.karbon_emisyon(1000, "dogalgaz"), 202.0)
        self.assertAlmostEqual(bep_karbon.birincil_enerji(1000, "elektrik"), 2360.0)
        self.assertAlmostEqual(
            bep_karbon.toplam_emisyon([("dogalgaz", 1000), ("elektrik", 1000)]),
            202.0 + 440.0,
        )
        self.assertAlmostEqual(bep_karbon.birim_alan_gosterge(202.0, 100), 2.02)

    def test_hatalar(self):
        for fn in (
            lambda: bep_karbon.karbon_emisyon(-5),
            lambda: bep_karbon.karbon_emisyon(10, yakit="bilinmez"),
            lambda: bep_karbon.birincil_enerji(10, yakit="bilinmez"),
            lambda: bep_karbon.birincil_enerji(10, cevrim=0),
            lambda: bep_karbon.karbon_emisyon(10, faktor=-1),
            lambda: bep_karbon.birim_alan_gosterge(10, 0),
        ):
            with self.assertRaises(ValueError):
                fn()


if __name__ == "__main__":
    unittest.main()
