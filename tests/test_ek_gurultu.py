"""Ek: gurultu testleri."""

import unittest

from mekanik_hesap.ek.gurultu import (
    fan_guc_duzeyi,
    kanal_degerlendirme,
    nc_karsilastir,
)


class TestGurultu(unittest.TestCase):
    def test_fan(self):
        lw = fan_guc_duzeyi(10000, 500)
        self.assertAlmostEqual(lw, 40.0 + 53.98 - 8.0, places=1)
        self.assertGreater(fan_guc_duzeyi(20000, 500), lw)

    def test_kanal(self):
        self.assertEqual(kanal_degerlendirme(2.5)[0], "sessiz")
        self.assertEqual(kanal_degerlendirme(4.0)[0], "kabul")
        self.assertEqual(kanal_degerlendirme(7.0)[0], "gurultulu")
        with self.assertRaises(ValueError):
            kanal_degerlendirme(0)

    def test_nc(self):
        hedef, uygun, _ = nc_karsilastir(40, "ofis")
        self.assertEqual(hedef, 35)
        self.assertTrue(uygun)
        _, uygun, _ = nc_karsilastir(60, "ofis")
        self.assertFalse(uygun)
        with self.assertRaises(ValueError):
            nc_karsilastir(40, "bilinmez")


if __name__ == "__main__":
    unittest.main()
