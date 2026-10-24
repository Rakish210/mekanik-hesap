"""Ek: yakit tuketimi testleri."""

import unittest

from mekanik_hesap.ek.yakit_tuketim import (
    YAKIT_HU,
    saatlik_tuketim,
    gunluk_tuketim,
    sezonluk_tuketim,
)


class TestYakit(unittest.TestCase):
    def test_saatlik(self):
        b, birim = saatlik_tuketim(100, 0.9)
        self.assertAlmostEqual(b, 100 / 0.9 / YAKIT_HU["dogalgaz"]["hu"])
        self.assertEqual(birim, "m3/h")

    def test_ozel_hu(self):
        b, _ = saatlik_tuketim(100, 1.0, hu_kwh=10.0)
        self.assertAlmostEqual(b, 10.0)

    def test_gun_sezon(self):
        self.assertAlmostEqual(gunluk_tuketim(10, 8), 80.0)
        self.assertAlmostEqual(sezonluk_tuketim(80, 150), 12000.0)
        self.assertAlmostEqual(sezonluk_tuketim(80, 150, 0.8), 9600.0)

    def test_hatalar(self):
        for fn in (
            lambda: saatlik_tuketim(0, 0.9),
            lambda: saatlik_tuketim(10, 1.5),
            lambda: saatlik_tuketim(10, 0.9, yakit="bilinmez"),
            lambda: gunluk_tuketim(10, 0),
            lambda: sezonluk_tuketim(10, -5),
        ):
            with self.assertRaises(ValueError):
                fn()


if __name__ == "__main__":
    unittest.main()
