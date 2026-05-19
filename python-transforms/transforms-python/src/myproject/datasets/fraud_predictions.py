from transforms.api import Input, Output, transform
from palantir_models.models import ModelAdapter
from palantir_models.transforms import ModelInput

NUM_CPUS = 1
MEMORY_GB = 8
NUM_GPUS = None

MODEL_FEATURE_COLUMNS = [
    "hour", "weekday", "is_weekend", "is_night_txn", "is_business_hours",
    "time_diff_from_last_txn", "is_rapid_txn", "customer_txn_count_24h",
    "customer_total_amount_24h", "customer_avg_amount_24h", "amount",
    "amount_over_avg24h", "is_high_amount", "is_very_high_amount",
    "exceeds_monthly_limit", "is_unusual_spending", "risk_amount_interaction",
    "is_young_customer", "is_senior_customer", "customer_age",
    "customer_monthly_limit", "risk_score",
]

@transform(
    predictions_output=Output("ri.foundry.main.dataset.0eb1f394-74da-484c-8253-41566be33532"),
    transactions_input=Input("ri.foundry.main.dataset.0f03f979-bbaf-4778-9dfb-b4118e40cd53"),
    model_input=ModelInput(
        "ri.models.main.model.71d98ce7-d254-4069-958a-c9ac7da6ab5c",
        use_sidecar=True,
        sidecar_resources={"cpus": NUM_CPUS, "memory_gb": MEMORY_GB, "gpus": NUM_GPUS},
    ),
)
def compute(predictions_output, transactions_input, model_input):
    """Run fraud detection ML model inference on engineered features."""
    transactions_df = transactions_input.dataframe().toPandas()
    model_columns = ["transaction_id"] + MODEL_FEATURE_COLUMNS
    model_input_df = transactions_df[model_columns].copy()
    model_input_df[MODEL_FEATURE_COLUMNS] = model_input_df[MODEL_FEATURE_COLUMNS].fillna(0)
    predictions = model_input.predict(transactions=model_input_df)
    predictions_output.write_pandas(predictions)
