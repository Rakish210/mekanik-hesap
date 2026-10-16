"""gaz (FAZ 4 ekleri) testleri."""
import unittest

from mekanik_hesap import gaz, gas
from mekanik_hesap.gaz import (
    gaz_yogunlugu, basinc_kaybi, boru_capi, sayac_secimi,
    havalandirma_menfezi, baca_kesiti, alarm_zonu,
)


class TestGaz(unittest.TestCase):
    def test_yogunluk(self):
        r21 = gaz_yogunlugu(21.0)
        r300 = gaz_yogunlugu(300.0)
        self.assertTrue(0.7 < r21 < r300 < 1.1, (r21, r300))

    def test_kayip_kademeler(self):
        k21 = basinc_kaybi(20.0, 10.0, 50.0, 21.0)
        k300 = basinc_kaybi(20.0, 10.0, 50.0, 300.0)
        self.assertTrue(0 <= k300 <= k21, (k21, k300))

    def test_boru_capi(self):
        self.assertEqual(boru_capi(10.0, 21.0), 25.0)
        # Secilen cap hiz sinirini saglamali (gas.hbk_hiz ile tutarli)
        from mekanik_hesap.gas import hbk_hiz
        cap = boru_capi(10.0, 21.0)
        p_bar = (1013.25 + 21.0) / 1000.0
        self.assertLessEqual(hbk_hiz(10.0, p_bar, cap), 6.0)

    def test_sayac(self):
        self.assertEqual(sayac_secimi(4.0), "G4")
        self.assertEqual(sayac_secimi(6.0), "G4")
        self.assertEqual(sayac_secimi(6.1), "G6")
        with self.assertRaises(ValueError):
            sayac_secimi(500.0)

    def test_menfez_baca(self):
        self.assertAlmostEqual(havalandirma_menfezi(24.0), 72.0)
        self.assertAlmostEqual(baca_kesiti(24.0), 12.0)

    def test_alarm_zonu(self):
        self.assertEqual(alarm_zonu(5), 2)
        self.assertEqual(alarm_zonu(4), 1)

    def test_gas_reexport(self):
        self.assertEqual(gas.sayac_secimi(4.0), "G4")
        self.assertAlmostEqual(gas.havalandirma_menfezi(24.0), 72.0)

    def test_errors(self):
        for fn in (lambda: gaz_yogunlugu(0),
                   lambda: basinc_kaybi(20.0, 10.0, 0, 21.0),
                   lambda: boru_capi(-1, 21.0),
                   lambda: havalandirma_menfezi(0),
                   lambda: alarm_zonu(0)):
            with self.assertRaises(ValueError):
                fn()


if __name__ == "__main__":
    unittest.main()
