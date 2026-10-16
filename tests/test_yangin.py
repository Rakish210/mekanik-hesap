"""yangin testleri."""
import unittest

from mekanik_hesap import yangin
from mekanik_hesap.yangin import (
    hazen_williams_kayip, sprinkler_debi, sprinkler_zon, dolap_debi,
    hidrant_hatti, pompa_secimi, su_deposu, fm200, co2_miktar,
    novec1230, kopuk_konsantresi,
)


class TestYangin(unittest.TestCase):
    def test_hazen_williams(self):
        hf = hazen_williams_kayip(100.0, 60.0, 100.0)
        self.assertTrue(0 < hf < 20.0, hf)

    def test_sprinkler(self):
        self.assertAlmostEqual(sprinkler_debi(80.0, 1.0), 80.0)
        self.assertAlmostEqual(sprinkler_debi(80.0, 4.0), 160.0)

    def test_zon(self):
        debi, adet = sprinkler_zon(100.0, 5.0)
        self.assertAlmostEqual(debi, 500.0)
        self.assertEqual(adet, 7)  # 500/80 -> 6.25 -> 7

    def test_dolap(self):
        self.assertAlmostEqual(dolap_debi(5), 200.0)
        self.assertAlmostEqual(dolap_debi(1), 100.0)

    def test_hidrant(self):
        debi, basinc = hidrant_hatti(2)
        self.assertTrue(debi > 0 and basinc > 70.0)

    def test_pompa_depo(self):
        debi, basinc, jokey = pompa_secimi(60.0, 80.0)
        self.assertAlmostEqual(jokey, 0.6)
        self.assertAlmostEqual(su_deposu(60.0, 60.0), 60.0)

    def test_gazli(self):
        m, n = fm200(100.0, alan_m2=60.0)
        self.assertTrue(m > 0 and n == 2)
        self.assertTrue(co2_miktar(100.0) == 120.0)
        self.assertTrue(novec1230(100.0) > 0)

    def test_kopuk(self):
        v = kopuk_konsantresi(100.0)
        self.assertAlmostEqual(v, 100.0 * 6.5 * 15.0 * 0.03)

    def test_errors(self):
        for fn in (lambda: sprinkler_debi(0, 1.0),
                   lambda: su_deposu(-5, 60.0),
                   lambda: hidrant_hatti(0),
                   lambda: co2_miktar(0)):
            with self.assertRaises((ValueError, KeyError)):
                fn()


if __name__ == "__main__":
    unittest.main()
