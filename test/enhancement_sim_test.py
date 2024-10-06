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
    def test_fs_to_rate(self):
        self.assertAlmostEqual(es.fs_to_rate(18, 0), 0.7, delta=0.01)
        self.assertAlmostEqual(es.fs_to_rate(40, 1), 0.5, delta=0.01)
        self.assertAlmostEqual(es.fs_to_rate(44, 2), 0.405, delta=0.01)
        self.assertAlmostEqual(es.fs_to_rate(110, 3), 0.3, delta=0.01)
        self.assertAlmostEqual(es.fs_to_rate(490, 4), 0.25, delta=0.01)
        
        self.assertAlmostEqual(es.fs_to_rate(19, 0), 0.705, delta=0.01)
        self.assertAlmostEqual(es.fs_to_rate(41, 1), 0.502, delta=0.01)
        self.assertAlmostEqual(es.fs_to_rate(45, 2), 0.4065, delta=0.01)
        self.assertAlmostEqual(es.fs_to_rate(111, 3), 0.3005, delta=0.01)
        self.assertAlmostEqual(es.fs_to_rate(491, 4), 0.2501, delta=0.01)
        
        with self.assertRaises(ValueError):
            es.fs_to_rate(-1, 0)
        with self.assertRaises(ValueError):
            es.fs_to_rate(18, 5)
if __name__ == '__main__':
    unittest.main()
