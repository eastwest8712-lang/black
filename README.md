# サッカー試合予想ポイント管理

このリポジトリは、以下を満たすシンプルな実装です。

- サッカーの試合結果を予想する
- 独自ポイントを使って予想する
- 試合終了後に結果を反映する

## 使い方（Python）

```python
from soccer_predictor import SoccerPredictionService, MatchOutcome

service = SoccerPredictionService(initial_points=100)
service.register_match("M1", "Japan", "Korea")

# 20ptでホーム勝ち予想（オッズ2.5）
service.place_prediction("M1", MatchOutcome.HOME_WIN, stake_points=20, odds=2.5)

# 試合結果を反映
result = service.settle_match("M1", MatchOutcome.HOME_WIN)
print(result)
# {'has_prediction': True, 'won': True, 'payout': 50, 'balance': 130}
```

## テスト

```bash
python -m unittest discover -s tests -p 'test_*.py'
```
