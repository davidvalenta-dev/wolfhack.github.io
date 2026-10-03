from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go


def risk_chart(frame: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=frame["window_end"],
        y=100 * frame["smoothed_probability"],
        mode="lines",
        name="Rolling risk",
    ))
    fig.add_trace(go.Scatter(
        x=frame["window_end"],
        y=100 * frame["signal_confidence"],
        mode="lines",
        name="Signal confidence",
    ))
    fig.update_layout(
        height=360,
        yaxis=dict(range=[0, 100], title="Percent"),
        xaxis_title="Time",
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h"),
    )
    return fig


def cohort_bar(frame: pd.DataFrame, top_k: int = 8) -> go.Figure:
    data = frame.head(top_k).sort_values("abs_standardized_delta")
    fig = go.Figure(go.Bar(
        x=data["standardized_delta"],
        y=data["feature"],
        orientation="h",
    ))
    fig.update_layout(height=420, xaxis_title="Standardized median difference", margin=dict(l=20, r=20, t=30, b=20))
    return fig
