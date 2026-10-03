from __future__ import annotations

import os
import pandas as pd
import streamlit as st

from pulsecast.agent.client import DatabricksChatClient
from pulsecast.agent.orchestrator import WearableAgent
from pulsecast.agent.schemas import AgentRequest
from pulsecast.agent.tools import DataTools
from pulsecast.app.charts import risk_chart, cohort_bar
from pulsecast.app.state import initialize_state
from pulsecast.config import get_settings

settings = get_settings()
st.set_page_config(page_title="PulseCast", layout="wide")
initialize_state()

@st.cache_data(ttl=30)
def load_artifacts():
    risk = pd.read_parquet(f"{settings.artifact_root}/risk.parquet")
    summary = pd.read_parquet(f"{settings.artifact_root}/subject_summary.parquet")
    comparison = pd.read_parquet(f"{settings.artifact_root}/feature_comparison.parquet")
    return risk, summary, comparison

risk, summary, comparison = load_artifacts()
subjects = sorted(summary["subject_id"].astype(str).unique())
subject_id = st.sidebar.selectbox("Subject", subjects, index=0)
st.session_state.subject_id = subject_id

current_summary = summary[summary["subject_id"].astype(str) == subject_id].iloc[0]
current_risk = risk[risk["subject_id"].astype(str) == subject_id].sort_values("window_end")
latest = current_risk.iloc[-1]

st.title("PulseCast")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rolling risk", f"{latest['smoothed_probability'] * 100:.0f}%")
c2.metric("Signal confidence", f"{latest['signal_confidence'] * 100:.0f}%")
c3.metric("HbA1c", f"{current_summary['hba1c']:.1f}")
c4.metric("Risk trend", str(latest.get("trend", "stable")).replace("_", " ").title())
st.plotly_chart(risk_chart(current_risk), use_container_width=True)

left, right = st.columns([1, 1])
with left:
    st.subheader("Cohort feature differences")
    st.plotly_chart(cohort_bar(comparison), use_container_width=True)
with right:
    st.subheader("Agent")
    question = st.text_input("Question", value="Why is this subject's current risk elevated?")
    if st.button("Analyze", type="primary"):
        tools = DataTools(risk, summary, comparison).registry()
        agent = WearableAgent(DatabricksChatClient(settings.llm_endpoint), tools)
        result = agent.run(AgentRequest(subject_id=subject_id, question=question))
        st.write(result.answer)
        if st.session_state.show_debug:
            st.json(result.tool_trace)

st.sidebar.checkbox("Show agent trace", key="show_debug")
st.caption("Research prototype only; not a diagnostic device.")
