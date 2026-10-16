"""Ek: lejyonella testleri."""
import unittest

from mekanik_hesap.ek.lejyonella import risk_skoru, onlem_listesi


class TestLejyonella(unittest.TestCase):
    def test_yuksek(self):
        skor, seviye = risk_skoru(35, 10, 3)
        self.assertEqual((skor, seviye), (100.0, "yuksek"))

    def test_dusuk(self):
        skor, seviye = risk_skoru(65, 1, 0.5)
        self.assertEqual(seviye, "dusuk")

    def test_orta(self):
        _, seviye = risk_skoru(35, 1, 0.5)
        self.assertEqual(seviye, "orta")

    def test_onlem(self):
        self.assertGreater(len(onlem_listesi("yuksek")),
                          len(onlem_listesi("dusuk")))
        with self.assertRaises(ValueError):
            onlem_listesi("bilinmez")
        with self.assertRaises(ValueError):
            risk_skoru(35, -1, 0)


if __name__ == "__main__":
    unittest.main()
