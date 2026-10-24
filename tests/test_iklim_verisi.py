"""iklim_verisi testleri."""

import unittest

from mekanik_hesap.iklim_verisi import (
    sehirler,
    tasarim_sicakligi,
    kis_tasarim,
    yaz_tasarim,
)


class TestIklimVerisi(unittest.TestCase):
    def test_sehirler(self):
        liste = sehirler()
        self.assertTrue({"istanbul", "ankara", "izmir"} <= set(liste))

    def test_degerler_isaretli(self):
        for sehir in sehirler():
            kis, yaz, not_ = tasarim_sicakligi(sehir)
            self.assertTrue(kis < yaz)
            self.assertIn("SEHIR-TEYIT", not_)

    def test_fonksiyonlar(self):
        self.assertTrue(kis_tasarim("ankara") < kis_tasarim("izmir"))
        self.assertTrue(yaz_tasarim("istanbul") > 0)

    def test_bilinmeyen(self):
        with self.assertRaises(KeyError):
            tasarim_sicakligi("bilinmeyen-sehir")


if __name__ == "__main__":
    unittest.main()
