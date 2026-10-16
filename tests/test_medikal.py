"""Medikal gaz testleri (5 hesap)."""
import unittest

from mekanik_hesap.medikal import (
    oksijen_debi, manifold_ihtiyaci, vakum_kapasitesi,
    medikal_hava_debisi, medikal_boru_capi, zon_vana,
)


class TestMedikal(unittest.TestCase):
    def test_oksijen(self):
        self.assertAlmostEqual(
            oksijen_debi([(10, 10)], 0.3), 100 * 0.3)

    def test_manifold(self):
        top, adet = manifold_ihtiyaci(10.0, 7.0, 50.0, 200.0)
        self.assertAlmostEqual(top, 70.0)
        self.assertEqual(adet, 7)

    def test_vakum(self):
        self.assertAlmostEqual(vakum_kapasitesi(10, 40.0, 0.3), 120.0)

    def test_hava(self):
        self.assertAlmostEqual(medikal_hava_debisi(10, 50.0, 0.3), 150.0)

    def test_boru(self):
        self.assertGreater(medikal_boru_capi(100.0, 8.0), 0)
        with self.assertRaises(ValueError):
            medikal_boru_capi(0)

    def test_zon(self):
        priz, vana = zon_vana(45, 20)
        self.assertEqual((priz, vana), (45, 3))

    def test_hatalar(self):
        for fn in (lambda: oksijen_debi([(-1, 1)]),
                   lambda: manifold_ihtiyaci(0),
                   lambda: vakum_kapasitesi(0),
                   lambda: medikal_hava_debisi(0),
                   lambda: zon_vana(0)):
            with self.assertRaises(ValueError):
                fn()


if __name__ == "__main__":
    unittest.main()
