from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MatchOutcome(str, Enum):
    HOME_WIN = "HOME_WIN"
    DRAW = "DRAW"
    AWAY_WIN = "AWAY_WIN"


@dataclass
class Match:
    match_id: str
    home_team: str
    away_team: str
    status: str = "OPEN"
    result: MatchOutcome | None = None


@dataclass
class Prediction:
    match_id: str
    predicted_outcome: MatchOutcome
    stake_points: int
    odds: float
    settled: bool = False


class PredictionError(ValueError):
    pass


class SoccerPredictionService:
    """サッカーの試合予想をポイントで管理するサービス。"""

    def __init__(self, initial_points: int = 0) -> None:
        if initial_points < 0:
            raise PredictionError("initial_points must be >= 0")
        self.points = initial_points
        self.matches: dict[str, Match] = {}
        self.predictions: dict[str, Prediction] = {}

    def add_points(self, amount: int) -> int:
        if amount <= 0:
            raise PredictionError("amount must be > 0")
        self.points += amount
        return self.points

    def register_match(self, match_id: str, home_team: str, away_team: str) -> Match:
        if match_id in self.matches:
            raise PredictionError(f"match {match_id} already exists")
        match = Match(match_id=match_id, home_team=home_team, away_team=away_team)
        self.matches[match_id] = match
        return match

    def place_prediction(
        self,
        match_id: str,
        predicted_outcome: MatchOutcome,
        stake_points: int,
        odds: float,
    ) -> Prediction:
        if match_id not in self.matches:
            raise PredictionError(f"match {match_id} is not registered")
        if match_id in self.predictions:
            raise PredictionError(f"prediction for {match_id} already exists")
        if self.matches[match_id].status != "OPEN":
            raise PredictionError(f"match {match_id} is not open for prediction")
        if stake_points <= 0:
            raise PredictionError("stake_points must be > 0")
        if odds <= 1.0:
            raise PredictionError("odds must be > 1.0")
        if stake_points > self.points:
            raise PredictionError("not enough points")

        self.points -= stake_points
        prediction = Prediction(
            match_id=match_id,
            predicted_outcome=predicted_outcome,
            stake_points=stake_points,
            odds=odds,
        )
        self.predictions[match_id] = prediction
        return prediction

    def settle_match(self, match_id: str, result: MatchOutcome) -> dict[str, int | bool]:
        if match_id not in self.matches:
            raise PredictionError(f"match {match_id} is not registered")

        match = self.matches[match_id]
        if match.status == "FINISHED":
            raise PredictionError(f"match {match_id} is already settled")

        match.status = "FINISHED"
        match.result = result

        prediction = self.predictions.get(match_id)
        if prediction is None:
            return {"has_prediction": False, "won": False, "payout": 0, "balance": self.points}
        if prediction.settled:
            raise PredictionError(f"prediction for {match_id} is already settled")

        prediction.settled = True
        won = prediction.predicted_outcome == result
        payout = int(prediction.stake_points * prediction.odds) if won else 0
        self.points += payout
        return {
            "has_prediction": True,
            "won": won,
            "payout": payout,
            "balance": self.points,
        }
