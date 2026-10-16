"""Ek: sismik aski testleri."""
import math
import unittest

from mekanik_hesap.ek.sismik_aski import (
    sismik_kuvvet, aski_tasarim_yuku, max_aski_mesafe,
)


class TestSismik(unittest.TestCase):
    def test_kuvvet(self):
        f = sismik_kuvvet(100, 1.0)
        self.assertAlmostEqual(f, 100 * 9.81 / 2.5)

    def test_tasarim_yuku(self):
        d, y, b = aski_tasarim_yuku(100, 1.0)
        self.assertAlmostEqual(d, 981.0)
        self.assertAlmostEqual(b, math.sqrt(d ** 2 + y ** 2))

    def test_mesafe(self):
        self.assertEqual(max_aski_mesafe(100), 4.0)
        with self.assertRaises(ValueError):
            max_aski_mesafe(999)

    def test_hatalar(self):
        for fn in (lambda: sismik_kuvvet(0, 1.0),
                   lambda: sismik_kuvvet(10, -1.0)):
            with self.assertRaises(ValueError):
                fn()


if __name__ == "__main__":
    unittest.main()
