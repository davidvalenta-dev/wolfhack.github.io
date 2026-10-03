from __future__ import annotations

from dataclasses import dataclass
import mlflow
import mlflow.sklearn


@dataclass(frozen=True)
class RegisteredModelRef:
    name: str
    version: str
    uri: str


def log_and_register_model(
    model,
    model_name: str,
    metrics: dict[str, float],
    params: dict[str, object],
    input_example,
) -> RegisteredModelRef:
    mlflow.set_registry_uri("databricks-uc")
    with mlflow.start_run() as run:
        mlflow.log_params({k: str(v) for k, v in params.items()})
        mlflow.log_metrics({k: float(v) for k, v in metrics.items() if v == v})
        info = mlflow.sklearn.log_model(
            sk_model=model,
            name="model",
            input_example=input_example,
        )
        result = mlflow.register_model(f"models:/{info.model_id}", model_name)
        return RegisteredModelRef(
            name=model_name,
            version=str(result.version),
            uri=f"models:/{model_name}/{result.version}",
        )


def load_registered_model(model_uri: str):
    mlflow.set_registry_uri("databricks-uc")
    return mlflow.sklearn.load_model(model_uri)
