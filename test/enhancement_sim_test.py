import unittest
from src import enhancement_sim as es
class TestEnhancementSim(unittest.TestCase):
    def test_enhance(self):
        # Test edge cases ( 0% chance of success and 100% chance of success)
        self.assertTrue(es.enhance(1))
        self.assertFalse(es.enhance(0))

        # Test for invalid chances
        with self.assertRaises(ValueError):
            es.enhance(-0.1)
        with self.assertRaises(ValueError):
            es.enhance(1.1)

        # Testing by statistical probability
        trials = 100_000
        success_count = sum(es.enhance(0.2) for _ in range(trials))
        self.assertAlmostEqual(success_count / trials, 0.2, delta=0.01)

        success_count = sum(es.enhance(0.5) for _ in range(trials))
        self.assertAlmostEqual(success_count / trials, 0.5, delta=0.01)
if __name__ == '__main__':
    unittest.main()
