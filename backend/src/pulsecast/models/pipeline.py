from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from xgboost import XGBClassifier


def build_xgb_pipeline(feature_columns: list[str], random_state: int = 42) -> Pipeline:
    prep = ColumnTransformer(
        transformers=[
            (
                "numeric",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="median", add_indicator=True)),
                    ("scaler", RobustScaler(with_centering=True, with_scaling=True)),
                ]),
                feature_columns,
            )
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )
    model = XGBClassifier(
        n_estimators=350,
        max_depth=4,
        learning_rate=0.035,
        subsample=0.85,
        colsample_bytree=0.80,
        min_child_weight=4,
        reg_alpha=0.20,
        reg_lambda=2.0,
        objective="binary:logistic",
        eval_metric="logloss",
        random_state=random_state,
        n_jobs=-1,
    )
    return Pipeline([("prep", prep), ("model", model)])
