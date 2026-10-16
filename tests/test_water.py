"""water testleri (IAPWS-IF97 kontrol noktalari)."""
import unittest

from mekanik_hesap.water import (
    density, dyn_viscosity, kin_viscosity, sat_pressure,
)


class TestWater(unittest.TestCase):
    def test_density_points(self):
        self.assertAlmostEqual(density(20), 998.21, delta=1.0)
        self.assertAlmostEqual(density(100), 958.35, delta=2.0)

    def test_density_falls(self):
        self.assertTrue(density(4) > density(60) > density(100))

    def test_viscosity(self):
        self.assertAlmostEqual(dyn_viscosity(20), 1.002e-3, delta=5e-5)
        self.assertTrue(dyn_viscosity(4) > dyn_viscosity(100))
        nu = kin_viscosity(20)
        self.assertAlmostEqual(nu, 1.004e-6, delta=5e-8)

    def test_sat_pressure(self):
        self.assertAlmostEqual(sat_pressure(100), 101.325, delta=2.0)
        self.assertAlmostEqual(sat_pressure(20), 2.339, delta=0.2)
        self.assertTrue(sat_pressure(4) < sat_pressure(60) < sat_pressure(100))

    def test_range_errors(self):
        for fn in (density, dyn_viscosity, kin_viscosity, sat_pressure):
            with self.assertRaises(ValueError):
                fn(3.9)
            with self.assertRaises(ValueError):
                fn(101.0)


if __name__ == "__main__":
    unittest.main()
