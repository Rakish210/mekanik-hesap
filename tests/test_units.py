"""units testleri."""
import unittest

from mekanik_hesap.units import convert, c_to_k, k_to_c


class TestUnits(unittest.TestCase):
    def test_length(self):
        self.assertAlmostEqual(convert(1000, "mm", "m"), 1.0)
        self.assertAlmostEqual(convert(1, "m", "mm"), 1000.0)
        self.assertAlmostEqual(convert(1, "km", "m"), 1000.0)

    def test_pressure(self):
        self.assertAlmostEqual(convert(1, "bar", "kpa"), 100.0)
        self.assertAlmostEqual(convert(1, "bar", "pa"), 100000.0)
        self.assertAlmostEqual(convert(760, "mmhg", "kpa"), 101.325, places=2)

    def test_flow(self):
        self.assertAlmostEqual(convert(1, "m3h", "ls"), 1.0 / 3.6)
        self.assertAlmostEqual(convert(1, "m3s", "m3h"), 3600.0)

    def test_power_energy(self):
        self.assertAlmostEqual(convert(1, "kw", "w"), 1000.0)
        self.assertAlmostEqual(convert(1, "kwh", "kj"), 3600.0)
        self.assertAlmostEqual(convert(1, "kwh", "kcal"), 860.42, places=1)

    def test_temperature(self):
        self.assertAlmostEqual(c_to_k(0), 273.15)
        self.assertAlmostEqual(k_to_c(273.15), 0.0)

    def test_errors(self):
        with self.assertRaises(ValueError):
            convert(1, "mm", "bar")
        with self.assertRaises(ValueError):
            convert(1, "C", "K")
        with self.assertRaises(ValueError):
            convert(1, "yok", "m")


if __name__ == "__main__":
    unittest.main()
