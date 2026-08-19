#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2023–2026 Paravane Labs
# SPDX-License-Identifier: MIT
from paravane import ParavaneClient, SmtpRsAnalysis


class FakeResponse:
    def __init__(self, status_code=200, payload=None, headers=None):
        self.status_code = status_code
        self._payload = payload or {}
        self.headers = headers or {}
        self.content = b"{}"
        self.text = "{}"

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self):
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        return FakeResponse(
            payload={
                "email": "person@example.com",
                "decision": "allow",
                "overall_risk": 0.11,
                "raw_risk": 1.11,
                "raw_decision": "review",
                "organization_validity_enabled": True,
                "organization_adjustment": -1,
                "analysis_profile": "deep",
                "credit_cost": 5,
                "credits_charged": 1,
                "usage_event_id": 42,
                "idempotency_replayed": False,
                "layers": {"Layer1": {"is_valid": True}},
                "reasons": ["example"],
                "domain_signal": {
                    "contract_version": "domain-organization-signal/v4",
                    "domain": "example.com",
                    "registrable_domain": "example.com",
                    "domain_status": "active",
                    "domain_exists": True,
                    "mail_status": "capable",
                    "mail_capable": True,
                    "mail_usage": "configured",
                    "spf_present": True,
                    "dmarc_present": False,
                    "organization_status": "verified",
                    "organization_backed": True,
                    "organization_known": True,
                    "organization_verified": True,
                    "organization_confidence": "high",
                    "company_valid": True,
                    "company_confidence": "high",
                    "company_checked_at": "2026-07-31T12:00:00Z",
                    "company_evidence_routes": ["sec_edgar", "wikidata"],
                    "documentary_association": {
                        "status": "current",
                        "confidence": "high",
                        "first_seen_at": "2025-01-01T00:00:00Z",
                        "last_seen_at": "2026-07-31T12:00:00Z",
                        "evidence_count": 3,
                        "routes": ["sec_edgar"],
                    },
                    "association_ambiguous": False,
                    "association_claim_count": 1,
                    "evaluated_at": "2026-07-31T12:00:01Z",
                    "organization_checked_at": "2026-07-31T12:00:00Z",
                    "organization": {
                        "registry_key": "org_example",
                        "canonical_name": "Example, Inc.",
                        "production_verified": True,
                        "logo": {
                            "url": "https://api.example.test/logos/org_example.png",
                            "status": "verified",
                            "confidence": "high",
                        },
                    },
                    "reason_codes": ["mail_capable", "company_valid"],
                    "future_field": "preserved",
                },
                "company_validity_beta": {
                    "feature": "company_validity",
                    "status": "beta",
                    "requested": True,
                    "enabled": True,
                    "availability": "paid_smtprs_only",
                    "additional_credit_cost": 0,
                    "notes": ["Beta contract."],
                },
            }
        )


def test_analyze_calls_expected_endpoint_and_headers():
    session = FakeSession()
    client = ParavaneClient(
        api_key="pvn_test_key",
        base_url="https://api.example.test",
        session=session,
    )
    result = client.smtprs.analyze(
        "person@example.com",
        profile="deep",
        company_validity_beta=True,
        idempotency_key="idem_123",
    )
    method, url, kwargs = session.calls[0]
    assert method == "POST"
    assert url == "https://api.example.test/v1/analyse"
    assert kwargs["json"] == {"email": "person@example.com"}
    assert kwargs["params"] == {
        "profile": "deep",
        "company_validity_beta": True,
    }
    assert kwargs["headers"]["X-API-Key"] == "pvn_test_key"
    assert kwargs["headers"]["Idempotency-Key"] == "idem_123"
    assert result.decision == "allow"
    assert result.overall_risk == 0.11
    assert result.credits_charged == 1
    assert result.company_validity_beta is not None
    assert result.company_validity_beta.status == "beta"
    assert result.company_validity_beta.requested is True
    assert result.company_validity_beta.enabled is True
    assert result.company_validity_beta.additional_credit_cost == 0
    assert result.company_validity_beta.notes == ["Beta contract."]
    assert result.raw_risk == 1.11
    assert result.raw_decision == "review"
    assert result.organization_validity_enabled is True
    assert result.organization_adjustment == -1
    assert result.analysis_profile == "deep"
    assert result.credit_cost == 5
    assert result.domain_signal is not None
    assert result.domain_signal.domain == "example.com"
    assert result.domain_signal.mail_capable is True
    assert result.domain_signal.company_valid is True
    assert result.domain_signal.company_evidence_routes == ["sec_edgar", "wikidata"]
    assert result.domain_signal.documentary_association is not None
    assert result.domain_signal.documentary_association.evidence_count == 3
    assert result.domain_signal.association_ambiguous is False
    assert result.domain_signal.organization is not None
    assert result.domain_signal.organization.canonical_name == "Example, Inc."
    assert result.domain_signal.organization.logo is not None
    assert result.domain_signal.organization.logo.status == "verified"
    assert result.domain_signal.raw["future_field"] == "preserved"
    assert result.usage_event_id == 42
    assert result.idempotency_replayed is False
    assert result.layers["Layer1"]["is_valid"] is True
    assert result.to_dict()["email"] == "person@example.com"


def test_analyze_can_include_extra_params():
    session = FakeSession()
    client = ParavaneClient(
        api_key="pvn_test_key",
        base_url="https://api.example.test",
        session=session,
    )
    client.smtprs.analyze(
        "person@example.com",
        fast=True,
        extra_params={"experimental": "yes"},
    )
    _, _, kwargs = session.calls[0]
    assert kwargs["json"] == {"email": "person@example.com"}
    assert kwargs["params"] == {"fast": True, "experimental": "yes"}


def test_analyze_omits_company_validity_beta_when_not_requested():
    session = FakeSession()
    client = ParavaneClient(
        api_key="pvn_test_key",
        base_url="https://api.example.test",
        session=session,
    )
    client.smtprs.analyze("person@example.com")
    _, _, kwargs = session.calls[0]
    assert "company_validity_beta" not in kwargs["params"]


def test_legacy_mode_flags_remain_available_for_compatibility():
    session = FakeSession()
    client = ParavaneClient(
        api_key="pvn_test_key",
        base_url="https://api.example.test",
        session=session,
    )
    client.smtprs.analyze("person@example.com", disposable_only=True)
    _, _, kwargs = session.calls[0]
    assert kwargs["params"] == {"disposable_only": True}


def test_zero_overall_risk_does_not_fall_back_to_legacy_score():
    result = SmtpRsAnalysis.from_dict({"overall_risk": 0, "risk_score": 9})

    assert result.overall_risk == 0
