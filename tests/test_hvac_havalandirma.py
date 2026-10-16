"""Havalandirma modulu testleri: 12 hesap."""

import unittest

from mekanik_hesap.hvac import havalandirma as H

SHELTER_FN = [n for n in ("siginak_debi",) if hasattr(H, n)][0]


class TestHavalandirma(unittest.TestCase):
    def test_taze_hava(self):
        self.assertAlmostEqual(H.taze_hava(10), 300.0)

    def test_hava_degisim(self):
        self.assertAlmostEqual(H.hava_degisim(200.0, 3.0), 600.0)

    def test_kanal_kaybi(self):
        dp = H.kanal_basinc_kaybi(10.0, 0.3, 5.0, 1.2, 0.02, 2.5)
        self.assertAlmostEqual(dp, (0.02 * 10.0 / 0.3 + 2.5) * 15.0)

    def test_fan(self):
        self.assertAlmostEqual(H.fan_gucu(1000.0, 500.0, 0.6),
                               1000.0 / 3600.0 * 500.0 / 0.6 / 1000.0)

    def test_duman(self):
        self.assertAlmostEqual(H.duman_zonu(100.0, 3.0), 1800.0)

    def test_otopark(self):
        self.assertAlmostEqual(H.otopark_debi(20), 6000.0)

    def test_davlumbaz(self):
        self.assertAlmostEqual(H.davlumbaz_debi(3.0), 3000.0)

    def test_siginak(self):
        self.assertAlmostEqual(getattr(H, SHELTER_FN)(50), 500.0)

    def test_merdiven(self):
        self.assertAlmostEqual(H.merdiven_basinc(2), 14400.0)

    def test_tuvalet(self):
        self.assertAlmostEqual(H.tuvalet_egzoz(2, 1), 230.0)

    def test_endustriyel(self):
        self.assertAlmostEqual(H.endustriyel_egzoz(2.0, 0.5), 3600.0)

    def test_susturucu(self):
        self.assertAlmostEqual(H.susturucu_kaybi(50.0, 6.0, 4.0), 112.5)


if __name__ == "__main__":
    unittest.main()
