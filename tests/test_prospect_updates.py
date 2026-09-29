from gtm_agent import data_service


def test_update_prospect_info_persists_and_invalidates_profile(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("LANGSMITH_TRACING", "false")
    from gtm_agent.gtm_agent import build_prospect_profile

    prospect_id = "LEAD-39002"
    record = data_service.get_prospect_record(prospect_id)
    original_tech_stack = list(record["tech_stack"])
    data_service.invalidate_profile(prospect_id)

    try:
        build_prospect_profile.invoke(prospect_id)
        result = data_service.update_prospect_info(prospect_id, "Terraform")

        assert result["updated"] is True
        assert "Terraform" in data_service.fetch_tech_stack(prospect_id)
        profile = build_prospect_profile.invoke(prospect_id)["prospect_profile"]
        assert "Terraform" in profile["tech_stack"]
    finally:
        record["tech_stack"] = original_tech_stack
        data_service.invalidate_profile(prospect_id)
