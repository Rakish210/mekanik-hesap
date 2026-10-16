"""Isitma modulu testleri: 14 hesap + hata yollari."""

import unittest

from mekanik_hesap.hvac import isitma as I


class TestIsitma(unittest.TestCase):
    def test_isi_kaybi(self):
        top, ilet, hav = I.isi_kaybi_mahal([(0.5, 40.0), (2.5, 6.0)],
                                            100.0, 0.5, 22.0, -3.0)
        self.assertAlmostEqual(ilet, 875.0)
        self.assertAlmostEqual(hav, 425.0)
        self.assertAlmostEqual(top, 1300.0)

    def test_isi_kaybi_hata(self):
        with self.assertRaises(ValueError):
            I.isi_kaybi_mahal([(0.5, 1.0)], 10.0, 0.5, -3.0, 22.0)

    def test_radyator(self):
        self.assertEqual(I.radyator_secimi(1300.0, 150.0), 10)

    def test_hatve(self):
        self.assertEqual(I.yerden_isitma_hatve(40.0), 30)
        self.assertEqual(I.yerden_isitma_hatve(80.0), 15)
        self.assertEqual(I.yerden_isitma_hatve(120.0), 10)

    def test_devre_debisi(self):
        self.assertAlmostEqual(I.devre_debisi(1161.0, 8.0), 0.125)

    def test_boru_capi(self):
        self.assertEqual(I.boru_capi(1.0, 0.8), 25.0)

    def test_pompa(self):
        debi, h = I.pompa_isitma(50.0, 20.0, 30.0)
        self.assertAlmostEqual(debi, 50.0 / (1.161 * 20.0), places=4)
        self.assertAlmostEqual(h, 30.0 / 9.807, places=4)

    def test_genlesme(self):
        vn = I.genlesme_tanki(1000.0, 10.0, 90.0, 1.5, 3.0)
        ve = 1000.0 * 0.00043 * 80.0
        self.assertAlmostEqual(vn, ve * 4.0 / 1.5)

    def test_kazan(self):
        self.assertAlmostEqual(I.kazan_kapasitesi(100.0, 0.15, 20.0), 135.0)

    def test_baca_cekisi(self):
        dp = I.baca_cekisi(10.0, 0.0, 150.0)
        bek = 9.81 * 10.0 * (353.0 / 273.15 - 353.0 / 423.15)
        self.assertAlmostEqual(dp, bek)

    def test_balans_kv(self):
        self.assertAlmostEqual(I.balans_kv(2.0, 0.1), 2.0 / 0.1 ** 0.5)

    def test_uc_yollu(self):
        kvs, ok = I.uc_yollu_kvs(2.0, 0.1)
        self.assertAlmostEqual(kvs, 2.0 / 0.1 ** 0.5)
        self.assertTrue(ok)

    def test_esanjor(self):
        self.assertAlmostEqual(I.esanjor_kapasite(10.0, 80.0, 60.0),
                               10.0 * 1.161 * 20.0)

    def test_lmtd(self):
        self.assertAlmostEqual(I.lmtd(80.0, 60.0, 50.0, 40.0),
                               10.0 / __import__("math").log(2.0))

    def test_yakit(self):
        self.assertAlmostEqual(I.yakit_tuketimi(100.0, 34500.0, 0.9),
                               100.0 * 3600.0 / (34500.0 * 0.9))

    def test_yalitim(self):
        self.assertAlmostEqual(I.yalitim_kalinligi(0.4, 0.04),
                               0.04 * (2.5 - 0.17))

    def test_zon_dagilim(self):
        top, oran, debi_oran = I.zon_debi_dagilimi([30.0, 70.0])
        self.assertAlmostEqual(top, 100.0)
        self.assertAlmostEqual(sum(oran), 1.0)
        self.assertAlmostEqual(oran[1], 0.7)


if __name__ == "__main__":
    unittest.main()
