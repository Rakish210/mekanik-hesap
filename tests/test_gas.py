"""gas testleri (KLV degerleriyle karsilastirma)."""

import unittest

from mekanik_hesap.gas import (
    ttt_toplam,
    hbk_hiz,
    isil_genlesme,
    konsol_pmax,
    konsol_guvenli_mi,
)


class TestGas(unittest.TestCase):
    def test_ttt_single(self):
        t, _ = ttt_toplam([(1710.0, 1)])
        self.assertAlmostEqual(t, 1710.0)

    def test_ttt_multi(self):
        t, _ = ttt_toplam([(271.56, 1), (737.08, 2)])
        self.assertAlmostEqual(t, 271.56 + 1474.16, places=4)

    def test_hbk_hiz(self):
        v = hbk_hiz(1710.0, 3.0, 102.3)
        self.assertTrue(20.0 < v < 21.5, v)

    def test_isil_genlesme(self):
        dl = isil_genlesme(13.0, 1.18e-5, 45.0)
        self.assertAlmostEqual(dl, 0.006903, places=9)

    def test_konsol(self):
        p = konsol_pmax(4.75, 20.0, 5.5, 8.0)
        self.assertAlmostEqual(p, 1910.7954545, places=3)
        self.assertTrue(konsol_guvenli_mi(101.42, p))
        self.assertFalse(konsol_guvenli_mi(5000.0, p))

    def test_errors(self):
        with self.assertRaises(ValueError):
            hbk_hiz(1710.0, 0, 102.3)
        with self.assertRaises(ValueError):
            konsol_pmax(4.75, 20.0, 0, 8.0)


if __name__ == "__main__":
    unittest.main()
