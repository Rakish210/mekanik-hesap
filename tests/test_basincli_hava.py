"""Basincli hava testleri (4 hesap)."""
import unittest

from mekanik_hesap.basincli_hava.basincli_hava import (
    tuketim_toplam, kompresor_secimi, tank_hacmi, boru_capi,
    basinc_kaybi, kurutucu_secimi,
)


class TestBasincliHava(unittest.TestCase):
    def test_tuketim(self):
        self.assertAlmostEqual(
            tuketim_toplam([(10, 2)], 0.7, 0.1), 20 * 0.7 * 1.1)

    def test_kompresor(self):
        self.assertAlmostEqual(kompresor_secimi(100), 110.0)

    def test_tank(self):
        self.assertAlmostEqual(tank_hacmi(2.0, 1.0, 2.0), 4000.0)

    def test_boru(self):
        self.assertGreater(boru_capi(100, 10.0, 8.0), 0)
        with self.assertRaises(ValueError):
            boru_capi(0)

    def test_kayip(self):
        self.assertGreater(basinc_kaybi(50, 40, 200), 0)

    def test_kurutucu(self):
        self.assertAlmostEqual(kurutucu_secimi(100), 115.0)

    def test_hatalar(self):
        for fn in (lambda: tuketim_toplam([(-1, 1)]),
                   lambda: kompresor_secimi(0),
                   lambda: tank_hacmi(1, 0),
                   lambda: kurutucu_secimi(0)):
            with self.assertRaises(ValueError):
                fn()


if __name__ == "__main__":
    unittest.main()
