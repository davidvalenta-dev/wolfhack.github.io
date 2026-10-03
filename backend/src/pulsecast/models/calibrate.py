from __future__ import annotations

import numpy as np
from scipy.special import expit, logit
from scipy.optimize import minimize


class PlattCalibrator:
    def __init__(self):
        self.a = 1.0
        self.b = 0.0

    def fit(self, probabilities, y):
        p = np.clip(np.asarray(probabilities, dtype=float), 1e-6, 1 - 1e-6)
        y = np.asarray(y, dtype=float)
        z = logit(p)

        def loss(theta):
            q = expit(theta[0] * z + theta[1])
            q = np.clip(q, 1e-8, 1 - 1e-8)
            return -np.mean(y * np.log(q) + (1 - y) * np.log(1 - q))

        result = minimize(loss, x0=np.array([1.0, 0.0]), method="BFGS")
        self.a, self.b = map(float, result.x)
        return self

    def predict(self, probabilities):
        p = np.clip(np.asarray(probabilities, dtype=float), 1e-6, 1 - 1e-6)
        return expit(self.a * logit(p) + self.b)
