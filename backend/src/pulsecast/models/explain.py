from __future__ import annotations

import numpy as np
import pandas as pd


def transformed_feature_names(pipeline) -> list[str]:
    prep = pipeline.named_steps["prep"]
    return [str(x) for x in prep.get_feature_names_out()]


def global_feature_importance(pipeline, top_k: int = 30) -> pd.DataFrame:
    model = pipeline.named_steps["model"]
    names = transformed_feature_names(pipeline)
    imp = np.asarray(model.feature_importances_, dtype=float)
    n = min(len(names), len(imp))
    frame = pd.DataFrame({"feature": names[:n], "importance": imp[:n]})
    return frame.sort_values("importance", ascending=False).head(top_k).reset_index(drop=True)


def local_contributions_approx(pipeline, row: pd.DataFrame, top_k: int = 8) -> pd.DataFrame:
    prep = pipeline.named_steps["prep"]
    model = pipeline.named_steps["model"]
    X = prep.transform(row)
    names = list(prep.get_feature_names_out())
    booster = model.get_booster()
    dmatrix = __import__("xgboost").DMatrix(X, feature_names=names)
    contrib = booster.predict(dmatrix, pred_contribs=True)[0]
    values = contrib[:-1]
    frame = pd.DataFrame({"feature": names[: len(values)], "contribution": values})
    frame["abs_contribution"] = frame["contribution"].abs()
    return frame.sort_values("abs_contribution", ascending=False).head(top_k).reset_index(drop=True)
