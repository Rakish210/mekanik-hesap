"""Sihhi tesisat testleri (13 hesap)."""

import unittest

from mekanik_hesap.su.sihhi import (
    cihaz_toplam_debi,
    temiz_su_boru_capi,
    hidrofor,
    su_deposu,
    pis_su_boru_cap,
    yagmur_suyu,
    yag_tutucu,
    fosseptik,
    dalgic_pompa,
    sicak_su_sirkulasyon,
    boyler,
    yumusatma,
    basinc_dusurucu_kademe,
    bahce_sulama,
)


class TestSihhi(unittest.TestCase):
    def test_cihaz(self):
        self.assertAlmostEqual(cihaz_toplam_debi([("lavabo", 2), ("klozet", 1)]), 0.35)
        with self.assertRaises(ValueError):
            cihaz_toplam_debi([("bilinmez", 1)])

    def test_boru(self):
        self.assertEqual(temiz_su_boru_capi(0.5, 1.5), 25.0)
        with self.assertRaises(ValueError):
            temiz_su_boru_capi(0, 1.5)

    def test_hidrofor(self):
        q, h, b = hidrofor(5, 20, 10, 2.0)
        self.assertAlmostEqual(h, 20 + 10 + 2.0 * 10.2)
        self.assertAlmostEqual(b, h / 10.2)

    def test_depo(self):
        self.assertEqual(su_deposu(10, 150, 1), 1500.0)

    def test_pis_su(self):
        self.assertEqual(pis_su_boru_cap(2.0), 110.0)
        self.assertEqual(pis_su_boru_cap(8.0), 160.0)

    def test_yagmur(self):
        self.assertAlmostEqual(yagmur_suyu(100, 150), 100 * 150 / 3600.0)

    def test_yag_fos(self):
        self.assertAlmostEqual(yag_tutucu(1.0, 3.0), 180.0)
        self.assertAlmostEqual(fosseptik(10), 1200.0)

    def test_pompa_sirk(self):
        self.assertGreater(dalgic_pompa(10, 8), 0)
        self.assertAlmostEqual(sicak_su_sirkulasyon(5, 5), 5 / (1.161 * 5))

    def test_boyler(self):
        hac, guc = boyler(4, 50, 10, 60, 2.0)
        self.assertEqual(hac, 200.0)
        self.assertGreater(guc, 0)

    def test_yumusatma(self):
        self.assertGreater(yumusatma(2, 30, 5, 8), 0)
        with self.assertRaises(ValueError):
            yumusatma(2, 5, 5, 8)

    def test_kademe(self):
        self.assertEqual(basinc_dusurucu_kademe(10, 3), 2)
        self.assertEqual(basinc_dusurucu_kademe(3, 4), 1)

    def test_sulama(self):
        gun, deb, zon = bahce_sulama(1000, 5, 2, 2)
        self.assertAlmostEqual(gun, 5.0)
        self.assertAlmostEqual(deb, 2.5)
        self.assertAlmostEqual(zon, 1.25)

    def test_hatalar(self):
        for fn in (
            lambda: su_deposu(0),
            lambda: yagmur_suyu(-1),
            lambda: fosseptik(-2),
        ):
            with self.assertRaises(ValueError):
                fn()


if __name__ == "__main__":
    unittest.main()
