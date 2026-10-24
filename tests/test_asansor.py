"""Asansor testleri (2 hesap + tasiyabilirlik)."""

import unittest

from mekanik_hesap.asansor.asansor import (
    tip_secimi,
    sefer_suresi,
    tasiyabilirlik,
)


class TestAsansor(unittest.TestCase):
    def test_tip(self):
        self.assertEqual(tip_secimi(kisi=5), (6.0, 450.0))
        self.assertEqual(tip_secimi(yuk_kg=600), (8.0, 630.0))
        with self.assertRaises(ValueError):
            tip_secimi(kisi=100)

    def test_sefer(self):
        rtt = sefer_suresi(10, 3.0, 1.6, 10.0)
        self.assertAlmostEqual(rtt, 2 * 30 / 1.6 + (2 * 10 / 3) * 10.0)
        with self.assertRaises(ValueError):
            sefer_suresi(1, 3, 1.6)

    def test_tasiyabilirlik(self):
        p_m3h = tasiyabilirlik(8, 100)
        self.assertAlmostEqual(p_m3h, 8 * 0.7 * 300 / 100)
        with self.assertRaises(ValueError):
            tasiyabilirlik(8, 0)


if __name__ == "__main__":
    unittest.main()
