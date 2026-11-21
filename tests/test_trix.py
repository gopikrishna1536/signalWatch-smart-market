import unittest
from signalwatch.trix_indicator import TRIXIndicator

class TestTRIXIndicator(unittest.TestCase):
    def test_trix(self):
        closes = [100.0 + i * 0.5 for i in range(50)]
        res = TRIXIndicator.calculate(closes, period=10)
        self.assertGreater(len(res), 0)

if __name__ == "__main__":
    unittest.main()
