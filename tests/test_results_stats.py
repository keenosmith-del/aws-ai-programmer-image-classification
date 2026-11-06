"""Pure statistics regressions; no model weights or third-party packages needed."""

from copy import deepcopy
import unittest

from data.calculates_results_stats import calculates_results_stats


class ResultsStatsTests(unittest.TestCase):
    def test_empty_results_have_zero_counts_and_percentages(self):
        self.assertEqual(
            calculates_results_stats({}),
            {
                "n_images": 0,
                "n_dogs_img": 0,
                "n_notdogs_img": 0,
                "n_match": 0,
                "n_correct_dogs": 0,
                "n_correct_notdogs": 0,
                "n_correct_breed": 0,
                "pct_match": 0.0,
                "pct_correct_dogs": 0.0,
                "pct_correct_breed": 0.0,
                "pct_correct_notdogs": 0.0,
            },
        )

    def test_non_dogs_only_keep_real_percentages_and_zero_dog_metrics(self):
        stats = calculates_results_stats({
            "cat.jpg": ["cat", "cat", 1, 0, 0],
            "bear.jpg": ["bear", "retriever", 0, 0, 1],
        })
        self.assertEqual(stats["n_images"], 2)
        self.assertEqual(stats["n_dogs_img"], 0)
        self.assertEqual(stats["n_notdogs_img"], 2)
        self.assertEqual(stats["n_correct_notdogs"], 1)
        self.assertEqual(stats["pct_match"], 50.0)
        self.assertEqual(stats["pct_correct_notdogs"], 50.0)
        self.assertEqual(stats["pct_correct_dogs"], 0.0)
        self.assertEqual(stats["pct_correct_breed"], 0.0)

    def test_dogs_only_distinguish_dog_detection_from_breed_accuracy(self):
        stats = calculates_results_stats({
            "beagle.jpg": ["beagle", "beagle", 1, 1, 1],
            "poodle.jpg": ["poodle", "retriever", 0, 1, 1],
        })
        self.assertEqual(stats["n_dogs_img"], 2)
        self.assertEqual(stats["n_notdogs_img"], 0)
        self.assertEqual(stats["n_correct_dogs"], 2)
        self.assertEqual(stats["n_correct_breed"], 1)
        self.assertEqual(stats["pct_match"], 50.0)
        self.assertEqual(stats["pct_correct_dogs"], 100.0)
        self.assertEqual(stats["pct_correct_breed"], 50.0)
        self.assertEqual(stats["pct_correct_notdogs"], 0.0)

    def test_mixed_results_preserve_counts_percentages_and_input(self):
        results = {
            "beagle.jpg": ["beagle", "beagle", 1, 1, 1],
            "poodle.jpg": ["poodle", "retriever", 0, 1, 1],
            "terrier.jpg": ["terrier", "cat", 0, 1, 0],
            "cat.jpg": ["cat", "cat", 1, 0, 0],
            "bear.jpg": ["bear", "retriever", 0, 0, 1],
        }
        original = deepcopy(results)
        stats = calculates_results_stats(results)
        self.assertEqual(results, original)
        self.assertEqual(stats["n_images"], 5)
        self.assertEqual(stats["n_dogs_img"], 3)
        self.assertEqual(stats["n_notdogs_img"], 2)
        self.assertEqual(stats["n_match"], 2)
        self.assertEqual(stats["n_correct_dogs"], 2)
        self.assertEqual(stats["n_correct_breed"], 1)
        self.assertEqual(stats["n_correct_notdogs"], 1)
        self.assertEqual(stats["pct_match"], 40.0)
        self.assertAlmostEqual(stats["pct_correct_dogs"], 200 / 3)
        self.assertAlmostEqual(stats["pct_correct_breed"], 100 / 3)
        self.assertEqual(stats["pct_correct_notdogs"], 50.0)

    def test_all_incorrect_predictions_have_zero_accuracy(self):
        stats = calculates_results_stats({
            "beagle.jpg": ["beagle", "cat", 0, 1, 0],
            "cat.jpg": ["cat", "beagle", 0, 0, 1],
        })
        for key in (
            "pct_match", "pct_correct_dogs", "pct_correct_breed",
            "pct_correct_notdogs",
        ):
            with self.subTest(metric=key):
                self.assertEqual(stats[key], 0.0)


if __name__ == "__main__":
    unittest.main()
