import pandas as pd
import pytest
from pulsecast.validation.leakage import assert_subject_disjoint, assert_no_cgm_predictors


def test_subject_disjoint_passes():
    assert_subject_disjoint(pd.DataFrame({"subject_id": ["001"]}), pd.DataFrame({"subject_id": ["002"]}))


def test_subject_disjoint_fails():
    with pytest.raises(AssertionError):
        assert_subject_disjoint(pd.DataFrame({"subject_id": ["001"]}), pd.DataFrame({"subject_id": ["001"]}))


def test_no_cgm_predictors():
    assert_no_cgm_predictors(["hr_mean", "bvp_std"])
    with pytest.raises(AssertionError):
        assert_no_cgm_predictors(["hr_mean", "cgm_mean"])
