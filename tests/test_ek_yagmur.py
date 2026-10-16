"""Ek: yagmur agi testleri."""
import unittest

from mekanik_hesap.ek.yagmur_3d import (
    cati_debisi, suzgec_dagilimi, yagmur_boru_capi, ag_hesabi,
)


class TestYagmur(unittest.TestCase):
    def test_debi(self):
        self.assertAlmostEqual(cati_debisi(360, 150), 15.0)

    def test_dagilim(self):
        dag = suzgec_dagilimi([100, 200])
        self.assertEqual(len(dag), 2)
        self.assertAlmostEqual(dag[0][1] * 2, dag[1][1])
        with self.assertRaises(ValueError):
            suzgec_dagilimi([])

    def test_cap(self):
        self.assertEqual(yagmur_boru_capi(1.5), 75.0)
        self.assertEqual(yagmur_boru_capi(15.0), 200.0)
        self.assertEqual(yagmur_boru_capi(100.0), 250.0)
        with self.assertRaises(ValueError):
            yagmur_boru_capi(0)

    def test_ag(self):
        ag = ag_hesabi([100, 200], 150)
        self.assertAlmostEqual(ag["toplam_Ls"], 12.5)
        self.assertEqual(len(ag["branslar"]), 2)
        self.assertEqual(ag["ana_cap"], yagmur_boru_capi(12.5))


if __name__ == "__main__":
    unittest.main()
