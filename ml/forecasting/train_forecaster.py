"""
InsightBI AI — ML Forecasting Module (ml/forecasting/train_forecaster.py)
Time-series sales forecasting using RandomForestRegressor / GradientBoostingRegressor.
Generates 30-day and 90-day future predictions with confidence bounds and metrics.
"""

import os
import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

class SalesForecaster:
    def __init__(self, n_estimators: int = 20, max_depth: int = 6):
        self.model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=42, n_jobs=-1)
        self.model_path = os.path.join(MODEL_DIR, "sales_forecaster.pkl")

    def _create_features(self, df_daily: pd.DataFrame) -> pd.DataFrame:
        df = df_daily.copy()
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)

        df["month"] = df["date"].dt.month
        df["day_of_week"] = df["date"].dt.dayofweek
        df["quarter"] = df["date"].dt.quarter
        df["day_of_month"] = df["date"].dt.day

        # Lag features
        df["lag_1"] = df["revenue"].shift(1)
        df["lag_7"] = df["revenue"].shift(7)
        df["lag_30"] = df["revenue"].shift(30)

        # Rolling statistics
        df["rolling_7_mean"] = df["revenue"].shift(1).rolling(7).mean()
        df["rolling_30_mean"] = df["revenue"].shift(1).rolling(30).mean()

        return df.dropna().reset_index(drop=True)

    def train_and_forecast(self, df_sales: pd.DataFrame, forecast_days: int = 90) -> dict:
        if df_sales.empty:
            return {"forecast": [], "metrics": {}}

        # Aggregate daily sales
        df = df_sales.copy()
        if "date" not in df.columns and "date_id" in df.columns:
            df["date"] = pd.to_datetime(df["date_id"].astype(str), format="%Y%m%d", errors="coerce")

        daily = df.groupby("date")["revenue"].sum().reset_index()

        # Create features
        df_feat = self._create_features(daily)
        if len(df_feat) < 30:
            return {"forecast": [], "metrics": {}}

        features = ["month", "day_of_week", "quarter", "day_of_month", "lag_1", "lag_7", "lag_30", "rolling_7_mean", "rolling_30_mean"]
        X = df_feat[features]
        y = df_feat["revenue"]

        # Train / Test split (last 30 days for evaluation)
        train_size = len(df_feat) - 30
        X_train, X_test = X.iloc[:train_size], X.iloc[train_size:]
        y_train, y_test = y.iloc[:train_size], y.iloc[train_size:]

        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)

        mae = float(mean_absolute_error(y_test, y_pred))
        rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
        mape = float(np.mean(np.abs((y_test - y_pred) / np.maximum(y_test, 1.0))) * 100.0)

        # Re-train on full dataset
        self.model.fit(X, y)
        joblib.dump(self.model, self.model_path)

        # Generate future dates predictions
        last_date = df_feat["date"].max()
        history = list(df_feat["revenue"].values)
        future_forecasts = []

        cur_date = last_date
        for i in range(1, forecast_days + 1):
            cur_date = cur_date + timedelta(days=1)
            
            lag_1 = history[-1]
            lag_7 = history[-7] if len(history) >= 7 else history[-1]
            lag_30 = history[-30] if len(history) >= 30 else history[-1]
            r7_mean = float(np.mean(history[-7:]))
            r30_mean = float(np.mean(history[-30:]))

            row_feat = pd.DataFrame([{
                "month": cur_date.month,
                "day_of_week": cur_date.dayofweek,
                "quarter": cur_date.quarter,
                "day_of_month": cur_date.day,
                "lag_1": lag_1,
                "lag_7": lag_7,
                "lag_30": lag_30,
                "rolling_7_mean": r7_mean,
                "rolling_30_mean": r30_mean
            }])

            pred_rev = float(self.model.predict(row_feat)[0])
            pred_rev = max(0.0, round(pred_rev, 2))
            history.append(pred_rev)

            # 10% lower/upper bounds
            lower_bound = round(pred_rev * 0.90, 2)
            upper_bound = round(pred_rev * 1.10, 2)

            future_forecasts.append({
                "date": cur_date.strftime("%Y-%m-%d"),
                "date_id": int(cur_date.strftime("%Y%m%d")),
                "predicted_revenue": pred_rev,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "model_name": "RandomForest_TimeSeries",
                "model_version": "v1.0"
            })

        return {
            "forecast": future_forecasts,
            "metrics": {"mae": round(mae, 2), "rmse": round(rmse, 2), "mape_percent": round(mape, 2)}
        }

def train_sales_forecaster(df_sales: pd.DataFrame, forecast_days: int = 90) -> dict:
    forecaster = SalesForecaster()
    return forecaster.train_and_forecast(df_sales, forecast_days)
