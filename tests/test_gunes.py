"""Gunes enerjisi testleri (5 hesap)."""

import unittest

from mekanik_hesap.gunes.gunes import (
    kolektor_alan,
    gunluk_enerji,
    gunes_boyler,
    solar_pompa,
    solar_genlesme,
    geri_odeme,
)


class TestGunes(unittest.TestCase):
    def test_alan(self):
        self.assertAlmostEqual(kolektor_alan(10, 5, 0.5), 4.0)

    def test_gunluk(self):
        self.assertAlmostEqual(gunluk_enerji(4, 50, 10, 60), 200 * 1.161 * 50 / 1000.0)

    def test_boyler(self):
        self.assertEqual(gunes_boyler(200, 0.6), 120.0)

    def test_pompa(self):
        self.assertEqual(solar_pompa(10), 300.0)

    def test_genlesme(self):
        self.assertGreater(solar_genlesme(100), 0)

    def test_odeme(self):
        self.assertAlmostEqual(geri_odeme(10000, 2000, 2.5), 2.0)

    def test_hatalar(self):
        for fn in (
            lambda: kolektor_alan(0, 5, 0.5),
            lambda: gunluk_enerji(0, 50, 10, 60),
            lambda: solar_pompa(-1),
            lambda: geri_odeme(1, 0, 1),
        ):
            with self.assertRaises(ValueError):
                fn()


if __name__ == "__main__":
    unittest.main()
