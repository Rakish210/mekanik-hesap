"""Ek: baca cekisi testleri."""
import unittest

from mekanik_hesap.ek.baca_cekis import cekis, yogusma_kontrol, baca_capi


class TestBaca(unittest.TestCase):
    def test_cekis(self):
        dp = cekis(10, 180, 0)
        self.assertGreater(dp, 20.0)
        self.assertLess(dp, 120.0)
        self.assertGreater(cekis(20, 180, 0), dp)

    def test_yogusma(self):
        risk, _ = yogusma_kontrol(40)
        self.assertTrue(risk)
        risk, _ = yogusma_kontrol(180)
        self.assertFalse(risk)
        with self.assertRaises(ValueError):
            yogusma_kontrol(100, yakit="bilinmez")

    def test_cap(self):
        self.assertEqual(baca_capi(3600, 4.0), 570.0)
        with self.assertRaises(ValueError):
            baca_capi(-1)

    def test_hatalar(self):
        for fn in (lambda: cekis(0, 180, 0),
                   lambda: cekis(10, 10, 20)):
            with self.assertRaises(ValueError):
                fn()


if __name__ == "__main__":
    unittest.main()
