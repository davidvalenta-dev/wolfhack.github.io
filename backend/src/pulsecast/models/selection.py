from __future__ import annotations

from dataclasses import dataclass
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import roc_auc_score

from pulsecast.models.pipeline import build_xgb_pipeline


@dataclass
class CandidateModelResult:
    name: str
    auc: float
    estimator: object


def candidate_estimators(feature_columns: list[str], random_state: int = 42) -> dict[str, object]:
    linear = Pipeline([
        ("impute", SimpleImputer(strategy="median", add_indicator=True)),
        ("scale", StandardScaler()),
        ("model", LogisticRegression(C=0.25, class_weight="balanced", max_iter=4000, random_state=random_state)),
    ])
    rf = Pipeline([
        ("impute", SimpleImputer(strategy="median", add_indicator=True)),
        ("model", RandomForestClassifier(n_estimators=500, max_depth=5, min_samples_leaf=8, class_weight="balanced", random_state=random_state, n_jobs=-1)),
    ])
    hist = Pipeline([
        ("impute", SimpleImputer(strategy="median", add_indicator=True)),
        ("model", HistGradientBoostingClassifier(max_iter=250, learning_rate=0.05, max_leaf_nodes=15, l2_regularization=2.0, random_state=random_state)),
    ])
    return {"logistic": linear, "random_forest": rf, "hist_gb": hist, "xgboost": build_xgb_pipeline(feature_columns, random_state)}


def compare_models(windows: pd.DataFrame, feature_columns: list[str]) -> pd.DataFrame:
    from sklearn.base import clone
    rows = []
    X = windows[feature_columns]
    y = windows["target"].astype(int).to_numpy()
    groups = windows["subject_id"].astype(str).to_numpy()
    logo = LeaveOneGroupOut()
    for name, base in candidate_estimators(feature_columns).items():
        oof = pd.Series(index=windows.index, dtype=float)
        for train_idx, test_idx in logo.split(X, y, groups):
            model = clone(base)
            model.fit(X.iloc[train_idx], y[train_idx])
            oof.iloc[test_idx] = model.predict_proba(X.iloc[test_idx])[:, 1]
        temp = pd.DataFrame({"subject_id": groups, "target": y, "p": oof.to_numpy()})
        agg = temp.groupby("subject_id", as_index=False).agg(target=("target", "first"), p=("p", "median"))
        auc = roc_auc_score(agg["target"], agg["p"]) if agg["target"].nunique() == 2 else float("nan")
        rows.append({"model": name, "subject_auc": auc})
    return pd.DataFrame(rows).sort_values("subject_auc", ascending=False)
