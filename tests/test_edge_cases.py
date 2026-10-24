"""Edge case testleri: negatif giris, sifir, buyuk degerler.

Her fonksiyon icin ValueError/KeyError gibi beklenen hatalar
ve sinir degerler test edilir.
"""

import unittest

from mekanik_hesap.asansor import asansor
from mekanik_hesap.su import sihhi
from mekanik_hesap.hvac import isitma
from mekanik_hesap import gaz


class TestEdgeCases(unittest.TestCase):
    def test_asansor_tip_secimi_no_args(self):
        with self.assertRaises(ValueError):
            asansor.tip_secimi()

    def test_asansor_tip_secimi_too_large(self):
        with self.assertRaises(ValueError):
            asansor.tip_secimi(kisi=100)

    def test_isi_kaybi_negative_dt(self):
        with self.assertRaises(ValueError):
            isitma.isi_kaybi_mahal([(1.0, 10.0)], 50.0, 1.0, 10.0, 20.0)

    def test_devre_debisi_zero(self):
        with self.assertRaises(ValueError):
            isitma.devre_debisi(0, 8.0)

    def test_temiz_su_boru_capi_zero(self):
        with self.assertRaises(ValueError):
            sihhi.temiz_su_boru_capi(0, 1.5)

    def test_hidrofor_zero_debi(self):
        with self.assertRaises(ValueError):
            sihhi.hidrofor(0, 10.0, 5.0)

    def test_gaz_hbk_hiz_zero_p(self):
        with self.assertRaises(ValueError):
            gaz.hbk_hiz(1.0, 0, 25.0)

    def test_gaz_sayac_secimi_zero(self):
        with self.assertRaises(ValueError):
            gaz.sayac_secimi(0)

    def test_gaz_alarm_zonu_zero(self):
        with self.assertRaises(ValueError):
            gaz.alarm_zonu(0)


if __name__ == "__main__":
    unittest.main()
