"""colebrook testleri."""

import unittest

from mekanik_hesap.colebrook import reynolds, haaland, colebrook


class TestColebrook(unittest.TestCase):
    def test_reynolds(self):
        Re = reynolds(1000.0, 1.0, 0.1, 0.001)
        self.assertAlmostEqual(Re, 100000.0)

    def test_haaland_range(self):
        f = haaland(100000.0, 0.000045, 0.1)
        self.assertTrue(0.018 < f < 0.022, f)

    def test_colebrook_matches_haaland(self):
        # Haaland, Colebrook'un acik yaklasigidir; 3 basamak uyum yeter.
        f_h = haaland(100000.0, 0.000045, 0.1)
        f_c = colebrook(100000.0, 0.000045, 0.1)
        self.assertAlmostEqual(f_c, f_h, places=3)

    def test_laminar(self):
        self.assertAlmostEqual(colebrook(1000.0, 0.000045, 0.1), 0.064)

    def test_errors(self):
        with self.assertRaises(ValueError):
            haaland(1000.0, 0.000045, 0.1)
        with self.assertRaises(ValueError):
            colebrook(0, 0.000045, 0.1)
        with self.assertRaises(ValueError):
            reynolds(1000.0, 1.0, 0.0, 0.001)


if __name__ == "__main__":
    unittest.main()
