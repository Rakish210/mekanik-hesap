"""Temiz oda testleri (4 hesap + sinif/MACO)."""
import math
import unittest

from mekanik_hesap.temiz_oda import (
    ach_debi, sinif_debisi, iso_ust_limit, ornek_nokta,
    basinc_kacak_debi, hepa_sayisi, isi_nem_yuku, maco,
)


class TestTemizOda(unittest.TestCase):
    def test_ach(self):
        self.assertAlmostEqual(ach_debi(100.0, 60.0), 6000.0)

    def test_sinif(self):
        self.assertAlmostEqual(sinif_debisi(100.0, "ISO7"), 6000.0)
        with self.assertRaises(ValueError):
            sinif_debisi(100.0, "ISO9X")

    def test_iso_limit(self):
        # ISO5, 0.5 um: formul ~3517, tablo 3520 (yuvarlanmis)
        self.assertAlmostEqual(iso_ust_limit(5, 0.5), 3520.0, delta=5.0)

    def test_nokta(self):
        self.assertEqual(ornek_nokta(100.0), 10)
        self.assertEqual(ornek_nokta(50.0), 8)

    def test_kacak(self):
        self.assertGreater(basinc_kacak_debi(0.02, 12.5), 0)

    def test_hepa(self):
        self.assertEqual(hepa_sayisi(6000.0, 1000.0), 6)
        self.assertEqual(hepa_sayisi(6100.0, 1000.0), 7)

    def test_yuk(self):
        duy, giz = isi_nem_yuku(3600.0, 5.0, 2.0)
        self.assertAlmostEqual(duy, 1.2 * 1.005 * 5.0, places=3)
        self.assertAlmostEqual(giz, 1.2 * 2.0 / 1000.0 * 2500.0,
                               places=3)

    def test_maco(self):
        # TDDa=10mg, MBS=100kg, SF=1000, TDDb=20mg -> 50 000 mg
        self.assertAlmostEqual(maco(10.0, 20.0, 100.0), 50000.0)

    def test_hatalar(self):
        for fn in (lambda: ach_debi(0, 20),
                   lambda: iso_ust_limit(10),
                   lambda: ornek_nokta(0),
                   lambda: basinc_kacak_debi(0, 12.5),
                   lambda: hepa_sayisi(0),
                   lambda: isi_nem_yuku(0),
                   lambda: maco(0, 1, 1)):
            with self.assertRaises(ValueError):
                fn()


if __name__ == "__main__":
    unittest.main()
