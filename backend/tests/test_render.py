from fastapi.testclient import TestClient
from pulsecast.service.render_api import app, tools_for, requests_by_ip

def test_missing_key_is_explicit(monkeypatch):
    monkeypatch.delenv('GEMINI_API_KEY',raising=False)
    requests_by_ip.clear()
    client=TestClient(app)
    assert client.get('/health').json()['llm_configured'] is False
    assert client.post('/agent',json={'subject_id':'004','question':'Explain'}).status_code==503

def test_patient_cannot_select_other_demo_subject():
    assert TestClient(app).post('/agent',json={'subject_id':'016','question':'Explain','audience':'patient'}).status_code==403

def test_demo_tools_match_scope_and_flag_fixtures():
    tools=tools_for('004',45,'patient')
    assert 'compare_cohorts' not in tools
    assert tools['get_current_risk'].fn('004')['signal_confidence']==.34
    assert tools['get_subject_summary'].fn('004')['hba1c']==6.4
    assert tools['get_subject_summary'].fn('004')['wearable_data']=='synthetic'
