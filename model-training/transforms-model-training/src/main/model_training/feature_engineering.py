# Feature engineering for fraud detection model training
import pandas as pd
import numpy as np

def engineer_features(df):
    """Engineer features from raw transaction + customer data for model training."""
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['weekday'] = df['timestamp'].dt.dayofweek
    df['is_weekend'] = (df['weekday'] >= 5).astype(int)
    df['is_night_txn'] = df['hour'].isin([0,1,2,3,4,5,22,23]).astype(int)
    df['is_business_hours'] = ((df['hour'] >= 9) & (df['hour'] <= 17)).astype(int)
    df = df.sort_values(['customer_id', 'timestamp'])
    df['prev_timestamp'] = df.groupby('customer_id')['timestamp'].shift(1)
    df['time_diff_from_last_txn'] = (df['timestamp'] - df['prev_timestamp']).dt.total_seconds()
    df['is_rapid_txn'] = (df['time_diff_from_last_txn'] <= 300).astype(int)
    df['customer_txn_count_24h'] = df.groupby('customer_id')['transaction_id'].transform('count')
    df['customer_total_amount_24h'] = df.groupby('customer_id')['amount'].transform('sum')
    df['customer_avg_amount_24h'] = df.groupby('customer_id')['amount'].transform('mean')
    df['is_high_amount'] = (df['amount'] > 500).astype(int)
    df['is_very_high_amount'] = (df['amount'] > 1000).astype(int)
    df['customer_total_amount_1month'] = df['customer_total_amount_24h']
    df['exceeds_monthly_limit'] = (df['customer_total_amount_1month'] > df['customer_monthly_limit']).astype(int)
    df['amount_over_avg24h'] = df['amount'] / (df['customer_avg_amount_24h'] + 1)
    df['is_unusual_spending'] = (df['amount_over_avg24h'] > 3).astype(int)
    df['risk_amount_interaction'] = (df['risk_score'] * df['amount'] / 1000)
    df['is_young_customer'] = (df['customer_age'] < 25).astype(int)
    df['is_senior_customer'] = (df['customer_age'] > 65).astype(int)
    df = df.drop(columns=['prev_timestamp'], errors='ignore')
    df['time_diff_from_last_txn'] = df['time_diff_from_last_txn'].fillna(0)
    return df
