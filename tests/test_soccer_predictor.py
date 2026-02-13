import unittest

from soccer_predictor import MatchOutcome, PredictionError, SoccerPredictionService


class SoccerPredictionServiceTest(unittest.TestCase):
    def test_predict_and_win(self) -> None:
        service = SoccerPredictionService(initial_points=100)
        service.register_match("M1", "Japan", "Korea")

        service.place_prediction(
            match_id="M1",
            predicted_outcome=MatchOutcome.HOME_WIN,
            stake_points=20,
            odds=2.5,
        )

        self.assertEqual(service.points, 80)

        settlement = service.settle_match("M1", MatchOutcome.HOME_WIN)

        self.assertTrue(settlement["won"])
        self.assertEqual(settlement["payout"], 50)
        self.assertEqual(service.points, 130)

    def test_predict_and_lose(self) -> None:
        service = SoccerPredictionService(initial_points=100)
        service.register_match("M2", "Spain", "Brazil")
        service.place_prediction("M2", MatchOutcome.DRAW, 30, 3.0)

        settlement = service.settle_match("M2", MatchOutcome.AWAY_WIN)

        self.assertFalse(settlement["won"])
        self.assertEqual(settlement["payout"], 0)
        self.assertEqual(service.points, 70)

    def test_cannot_use_more_points_than_balance(self) -> None:
        service = SoccerPredictionService(initial_points=10)
        service.register_match("M3", "A", "B")

        with self.assertRaises(PredictionError):
            service.place_prediction("M3", MatchOutcome.DRAW, 20, 2.1)

    def test_settle_without_prediction(self) -> None:
        service = SoccerPredictionService(initial_points=10)
        service.register_match("M4", "A", "B")

        settlement = service.settle_match("M4", MatchOutcome.DRAW)

        self.assertFalse(settlement["has_prediction"])
        self.assertEqual(settlement["balance"], 10)


if __name__ == "__main__":
    unittest.main()
