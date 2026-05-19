import palantir_models as pm
from palantir_models.serializers import DillSerializer
import pandas as pd


class FraudDetectionModelAdapter(pm.ModelAdapter):
    @pm.auto_serialize(
        model=DillSerializer(),
        feature_names=DillSerializer(),
        optimal_threshold=DillSerializer(),
    )
    def __init__(self, model, feature_names, optimal_threshold):
        super().__init__()
        self.model = model
        self.feature_names = feature_names
        self.optimal_threshold = optimal_threshold

    @classmethod
    def api(cls):
        inputs = {
            "transactions": pm.Pandas(
                columns=[
                    ("transaction_id", str),
                    ("hour", int), ("weekday", int), ("is_weekend", int),
                    ("is_night_txn", int), ("is_business_hours", int),
                    ("time_diff_from_last_txn", float), ("is_rapid_txn", int),
                    ("customer_txn_count_24h", int), ("customer_total_amount_24h", float),
                    ("customer_avg_amount_24h", float), ("amount", float),
                    ("amount_over_avg24h", float), ("is_high_amount", int),
                    ("is_very_high_amount", int), ("exceeds_monthly_limit", int),
                    ("is_unusual_spending", int), ("risk_amount_interaction", float),
                    ("is_young_customer", int), ("is_senior_customer", int),
                    ("customer_age", int), ("customer_monthly_limit", float),
                    ("risk_score", float),
                ]
            )
        }
        outputs = {
            "predictions": pm.Pandas(
                columns=[
                    ("transaction_id", str),
                    ("fraud_probability", float),
                    ("is_fraud_predicted", int),
                    ("threshold_used", float),
                ]
            )
        }
        return inputs, outputs

    def predict(self, transactions):
        transaction_ids = transactions["transaction_id"]
        X = transactions[self.feature_names]
        fraud_proba = self.model.predict_proba(X)[:, 1]
        is_fraud = (fraud_proba >= self.optimal_threshold).astype(int)
        result = pd.DataFrame({
            "transaction_id": transaction_ids.values,
            "fraud_probability": fraud_proba,
            "is_fraud_predicted": is_fraud,
            "threshold_used": self.optimal_threshold,
        })
        return result
