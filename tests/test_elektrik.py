"""Elektrik arayuz testleri (KATALOG.md 14. baslik, 20 hesap)."""
import math
import unittest

from mekanik_hesap.elektrik import (
    yuk_akimi, guc_ucgeni, kablo_kesit, gerilim_dusumu, sigorta_secimi,
    kacak_akim, topraklama_cubugu, topraklama_elektrot, paratoner_yaricap,
    aydinlatma_armatur, kompanzasyon, jenerator_gucu, ups_secimi,
    trafo_gucu, salter_ayari, busbar_kesit, bakir_agirlik, tava_doluluk,
    dedektor_sayisi, yangin_zon, acil_aydinlatma, motor_yol_verme,
    es_potansiyel, data_limit, pano_isi, talep_guc, enerji_tuketim,
)


class TestElektrik(unittest.TestCase):
    def test_yuk_akimi(self):
        self.assertAlmostEqual(yuk_akimi(8000, 400, 3, 0.8),
                               8000 / (math.sqrt(3) * 400 * 0.8))
        self.assertAlmostEqual(yuk_akimi(2000, 230, 1, 0.9),
                               2000 / (230 * 0.9))
        with self.assertRaises(ValueError):
            yuk_akimi(1000, 400, 2)

    def test_guc_ucgeni(self):
        p, s, q, c = guc_ucgeni(p_kw=80, s_kva=100)
        self.assertAlmostEqual(q, 60.0)
        self.assertAlmostEqual(c, 0.8)
        p2, s2, q2, c2 = guc_ucgeni(s_kva=100, cosfi=0.8)
        self.assertAlmostEqual(p2, 80.0)
        with self.assertRaises(ValueError):
            guc_ucgeni(p_kw=80)

    def test_kablo_kesit(self):
        self.assertEqual(kablo_kesit(20), 2.5)
        self.assertEqual(kablo_kesit(100), 35.0)
        with self.assertRaises(ValueError):
            kablo_kesit(9999)

    def test_gerilim_dusumu(self):
        du = gerilim_dusumu(20, 50, 2.5, 400, 3, 0.8)
        bek = math.sqrt(3) * 0.0178 * 50 * 20 * 0.8 / 2.5 / 400 * 100
        self.assertAlmostEqual(du, bek)
        with self.assertRaises(ValueError):
            gerilim_dusumu(20, 50, 0)

    def test_sigorta(self):
        self.assertEqual(sigorta_secimi(28), 32.0)
        self.assertEqual(sigorta_secimi(28, 36), 32.0)
        with self.assertRaises(ValueError):
            sigorta_secimi(28, 25)

    def test_kacak(self):
        self.assertEqual(kacak_akim("priz"), 30.0)
        self.assertEqual(kacak_akim("ana"), 300.0)
        with self.assertRaises(ValueError):
            kacak_akim("xyz")

    def test_topraklama(self):
        r = topraklama_cubugu(100, 3.0, 16.0)
        bek = 100 / (2 * math.pi * 3) * math.log(4 * 3 / 0.016)
        self.assertAlmostEqual(r, bek)
        self.assertEqual(topraklama_elektrot(40, 10), 4)
        with self.assertRaises(ValueError):
            topraklama_cubugu(-5)

    def test_paratoner(self):
        self.assertAlmostEqual(paratoner_yaricap(10, 45),
                               math.sqrt(2 * 45 * 10 - 100))
        with self.assertRaises(ValueError):
            paratoner_yaricap(50, 45)

    def test_aydinlatma(self):
        self.assertEqual(aydinlatma_armatur(100, 500, 4000, 0.6, 0.8),
                         math.ceil(500 * 100 / (4000 * 0.48)))
        with self.assertRaises(ValueError):
            aydinlatma_armatur(0, 500, 4000)

    def test_kompanzasyon(self):
        q = kompanzasyon(100, 0.7, 0.95)
        t1 = math.sqrt(1 - 0.49) / 0.7
        t2 = math.sqrt(1 - 0.9025) / 0.95
        self.assertAlmostEqual(q, 100 * (t1 - t2))
        with self.assertRaises(ValueError):
            kompanzasyon(100, 0.95, 0.7)

    def test_jenerator(self):
        self.assertAlmostEqual(jenerator_gucu(200, 0.7, 0.8, 1.25),
                               200 * 0.7 * 1.25 / 0.8)
        with self.assertRaises(ValueError):
            jenerator_gucu(200, 1.5)

    def test_ups(self):
        ups, ah = ups_secimi(10000, 15, 0.9, 12.0, 32.0)
        self.assertAlmostEqual(ups, 12.5)
        self.assertAlmostEqual(ah, 10000 * 0.25 / (12 * 32 * 0.9) * 1000)
        with self.assertRaises(ValueError):
            ups_secimi(0, 15)

    def test_trafo_salter(self):
        self.assertEqual(trafo_gucu(1000, 0.7), 800.0)
        self.assertEqual(salter_ayari(400),
                         630.0)  # 400kVA ~577A -> 630
        with self.assertRaises(ValueError):
            trafo_gucu(100000, 1.0)

    def test_busbar_bakir(self):
        self.assertAlmostEqual(busbar_kesit(300, 1.5), 200.0)
        self.assertAlmostEqual(bakir_agirlik(95, 100, 3),
                               95 * 100 * 3 * 8.96 / 1000)
        with self.assertRaises(ValueError):
            busbar_kesit(-10)

    def test_tava(self):
        oran = tava_doluluk([10, 10, 10], 300, 60)
        bek = 3 * math.pi * 25 / 18000 * 100
        self.assertAlmostEqual(oran, bek)
        with self.assertRaises(ValueError):
            tava_doluluk([])

    def test_dedektor_zon(self):
        self.assertEqual(dedektor_sayisi(120, "duman"), 2)
        self.assertEqual(dedektor_sayisi(120, "isinim"), 4)
        self.assertEqual(yangin_zon(3000), 2)
        with self.assertRaises(ValueError):
            dedektor_sayisi(10, "xyz")

    def test_acil(self):
        adet, sure = acil_aydinlatma(300, 1.0, 300.0, 3.0)
        self.assertEqual((adet, sure), (1, 3.0))
        with self.assertRaises(ValueError):
            acil_aydinlatma(-1, 1.0, 300.0)

    def test_motor(self):
        anma, kalkis = motor_yol_verme(15, 400, 0.85, 0.9, "dogrudan")
        bek = 15000 / (math.sqrt(3) * 400 * 0.85 * 0.9)
        self.assertAlmostEqual(anma, bek)
        self.assertAlmostEqual(kalkis, bek * 7.0)
        with self.assertRaises(ValueError):
            motor_yol_verme(15, 400, 0.85, 0.9, "xyz")

    def test_es_data(self):
        self.assertEqual(es_potansiyel(35), 17.5)
        self.assertEqual(es_potansiyel(6), 6.0)
        self.assertEqual(data_limit("ethernet"), 100.0)
        with self.assertRaises(ValueError):
            data_limit("xyz")

    def test_pano(self):
        kw, debi = pano_isi(1000, None, 10.0)
        self.assertAlmostEqual(kw, 1.0)
        self.assertAlmostEqual(debi, 1000 / (1.2 * 1005 * 10) * 3600)
        with self.assertRaises(ValueError):
            pano_isi(1000, None, 0)

    def test_talep_enerji(self):
        kurulu, talep = talep_guc([100, 50], 0.7)
        self.assertEqual((kurulu, talep), (150.0, 105.0))
        self.assertAlmostEqual(enerji_tuketim(10, 5, 2), 100.0)
        with self.assertRaises(ValueError):
            talep_guc([10], 2.0)


if __name__ == "__main__":
    unittest.main()
