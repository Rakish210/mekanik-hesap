"""Iklimlendirme modulu testleri: 12 hesap."""

import unittest

from mekanik_hesap.hvac import iklimlendirme as C


class TestIklimlendirme(unittest.TestCase):
    def test_sogutma_yuku(self):
        self.assertAlmostEqual(C.sogutma_yuku([1000.0, 2000.0], 0.10), 3300.0)

    def test_fancoil(self):
        self.assertAlmostEqual(
            C.fancoil_secimi(3000.0, [2000.0, 3500.0, 5000.0]), 3500.0
        )

    def test_fancoil_yetersiz(self):
        with self.assertRaises(ValueError):
            C.fancoil_secimi(9000.0, [2000.0])

    def test_santral_debi(self):
        self.assertAlmostEqual(
            C.santral_debi(10.0, 8.0), 10.0 / (1.2 * 1.005 / 3600.0 * 8.0)
        )

    def test_vrf(self):
        self.assertAlmostEqual(C.vrf_dagilimi([10.0, 12.0], 0.9), 19.8)

    def test_chiller(self):
        self.assertAlmostEqual(C.chiller_kapasite(100.0), 110.0)

    def test_kule(self):
        qrej, debi = C.kule_kapasite(100.0, 25.0, 5.0)
        self.assertAlmostEqual(qrej, 125.0)
        self.assertAlmostEqual(debi, 125.0 / (1.161 * 5.0))

    def test_nem(self):
        self.assertAlmostEqual(C.nem_miktari(1000.0, 5.0), 6.0)

    def test_soguk_su_boru(self):
        self.assertEqual(C.soguk_su_boru(5.0, 1.0), 50.0)

    def test_kondens(self):
        self.assertEqual(C.kondens_drenaj(5.0), 20)
        self.assertEqual(C.kondens_drenaj(50.0), 32)

    def test_kanal(self):
        alan, cap = C.kanal_kesiti(3600.0, 5.0)
        self.assertAlmostEqual(alan, 0.2)
        self.assertAlmostEqual(cap, (4.0 * 0.2 / 3.14159265) ** 0.5 * 1000.0, places=1)

    def test_menfez(self):
        self.assertEqual(C.menfez_adet(1000.0, 300.0), 4)

    def test_taze_oran(self):
        self.assertAlmostEqual(C.taze_hava_orani(300.0, 1000.0), 30.0)


if __name__ == "__main__":
    unittest.main()
