"""Havuz tesisati testleri (4 hesap)."""
import unittest

from mekanik_hesap.su.havuz import (
    havuz_hacim, devir_debisi, filtre_pompa, havuz_isitma,
    kapali_havuz_havalandirma,
)


class TestHavuz(unittest.TestCase):
    def test_hacim(self):
        self.assertAlmostEqual(havuz_hacim(25, 10, 1.5), 375.0)

    def test_devir(self):
        self.assertAlmostEqual(devir_debisi(375, 6), 62.5)

    def test_filtre(self):
        q_m3h, alan = filtre_pompa(60, 30)
        self.assertEqual(q_m3h, 60.0)
        self.assertAlmostEqual(alan, 2.0)

    def test_isitma(self):
        self.assertAlmostEqual(havuz_isitma(100, 20, 24),
                               100 * 1.161 * 20 / 24)

    def test_havalandirma(self):
        self.assertEqual(kapali_havuz_havalandirma(200), 2000.0)

    def test_hatalar(self):
        for fn in (lambda: havuz_hacim(0, 1, 1),
                   lambda: devir_debisi(10, 0),
                   lambda: filtre_pompa(-1),
                   lambda: havuz_isitma(10, 0),
                   lambda: kapali_havuz_havalandirma(-5)):
            with self.assertRaises(ValueError):
                fn()


if __name__ == "__main__":
    unittest.main()
