# Enterprise Fraud Detection - Python Transforms

Python data transformation pipelines for the EFD project.

## Transforms

- **transform.py** - Processes streaming transaction data incrementally, joins with customer data, and engineers features
- **fraud_predictions.py** - Runs ML model inference for fraud detection
- **avro_to_parquet.py** - Converts Kafka AVRO data to Parquet format
