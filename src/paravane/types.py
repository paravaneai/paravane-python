#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2023–2026 Paravane Labs
# SPDX-License-Identifier: MIT
"""
Typed response helpers returned by the SDK.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Mapping, Optional

AnalysisProfile = Literal["quick", "standard", "adaptive", "deep", "catch_all"]


def _optional_bool(value: Any) -> Optional[bool]:
    return value if isinstance(value, bool) else None


def _first_present(data: Mapping[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in data:
            return data[key]
    return None


@dataclass(frozen=True)
class CompanyValidityBeta:
    """
    Beta metadata returned when company-validity support is available.
    """

    feature: Optional[str] = None
    status: Optional[str] = None
    requested: bool = False
    enabled: bool = False
    availability: Optional[str] = None
    additional_credit_cost: Optional[int] = None
    notes: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "CompanyValidityBeta":
        data = dict(payload)
        notes = data.get("notes") if isinstance(data.get("notes"), list) else []
        return cls(
            feature=data.get("feature"),
            status=data.get("status"),
            requested=bool(data.get("requested")),
            enabled=bool(data.get("enabled")),
            availability=data.get("availability"),
            additional_credit_cost=data.get("additional_credit_cost"),
            notes=[str(note) for note in notes],
            raw=data,
        )


@dataclass(frozen=True)
class DocumentaryAssociation:
    """Time-aware documentary evidence connecting a domain to an organization."""

    status: Optional[str] = None
    confidence: Optional[str] = None
    first_seen_at: Optional[str] = None
    last_seen_at: Optional[str] = None
    evidence_count: Optional[int] = None
    routes: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "DocumentaryAssociation":
        data = dict(payload)
        routes = data.get("routes") if isinstance(data.get("routes"), list) else []
        return cls(
            status=data.get("status"),
            confidence=data.get("confidence"),
            first_seen_at=data.get("first_seen_at"),
            last_seen_at=data.get("last_seen_at"),
            evidence_count=data.get("evidence_count"),
            routes=[str(route) for route in routes],
            raw=data,
        )


@dataclass(frozen=True)
class OrganizationLogo:
    """Optional organization logo metadata intended for presentation clients."""

    url: Optional[str] = None
    status: Optional[str] = None
    confidence: Optional[str] = None
    source: Optional[str] = None
    sha256: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "OrganizationLogo":
        data = dict(payload)
        return cls(
            url=data.get("url"),
            status=data.get("status"),
            confidence=data.get("confidence"),
            source=data.get("source"),
            sha256=data.get("sha256"),
            raw=data,
        )


@dataclass(frozen=True)
class OrganizationPresentation:
    """Resolved organization metadata returned with company-validity results."""

    registry_key: Optional[str] = None
    canonical_name: Optional[str] = None
    legal_name: Optional[str] = None
    organization_type: Optional[str] = None
    association_status: Optional[str] = None
    relationship_type: Optional[str] = None
    confidence: Optional[str] = None
    production_verified: Optional[bool] = None
    documentary_evidence: Optional[DocumentaryAssociation] = None
    logo: Optional[OrganizationLogo] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "OrganizationPresentation":
        data = dict(payload)
        documentary_data = data.get("documentary_evidence")
        logo_data = data.get("logo")
        return cls(
            registry_key=data.get("registry_key"),
            canonical_name=data.get("canonical_name"),
            legal_name=data.get("legal_name"),
            organization_type=data.get("organization_type"),
            association_status=data.get("association_status"),
            relationship_type=data.get("relationship_type"),
            confidence=data.get("confidence"),
            production_verified=_optional_bool(data.get("production_verified")),
            documentary_evidence=(
                DocumentaryAssociation.from_dict(documentary_data)
                if isinstance(documentary_data, Mapping)
                else None
            ),
            logo=(
                OrganizationLogo.from_dict(logo_data) if isinstance(logo_data, Mapping) else None
            ),
            raw=data,
        )


@dataclass(frozen=True)
class DomainSignal:
    """
    Normalized public facts about an email domain and its mail posture.
    """

    contract_version: Optional[str] = None
    domain: Optional[str] = None
    registrable_domain: Optional[str] = None
    domain_status: Optional[str] = None
    domain_exists: Optional[bool] = None
    mail_status: Optional[str] = None
    mail_capable: Optional[bool] = None
    mail_usage: Optional[str] = None
    spf_present: Optional[bool] = None
    dmarc_present: Optional[bool] = None
    organization_status: Optional[str] = None
    organization_backed: Optional[bool] = None
    organization_known: Optional[bool] = None
    organization_verified: Optional[bool] = None
    organization_confidence: Optional[str] = None
    company_valid: Optional[bool] = None
    company_confidence: Optional[str] = None
    company_checked_at: Optional[str] = None
    company_evidence_routes: List[str] = field(default_factory=list)
    documentary_association: Optional[DocumentaryAssociation] = None
    association_ambiguous: Optional[bool] = None
    association_claim_count: Optional[int] = None
    evaluated_at: Optional[str] = None
    organization_checked_at: Optional[str] = None
    organization: Optional[OrganizationPresentation] = None
    reason_codes: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "DomainSignal":
        data = dict(payload)
        reason_codes = (
            data.get("reason_codes") if isinstance(data.get("reason_codes"), list) else []
        )
        evidence_routes = (
            data.get("company_evidence_routes")
            if isinstance(data.get("company_evidence_routes"), list)
            else []
        )
        documentary_data = data.get("documentary_association")
        organization_data = data.get("organization")
        return cls(
            contract_version=data.get("contract_version"),
            domain=data.get("domain"),
            registrable_domain=data.get("registrable_domain"),
            domain_status=data.get("domain_status"),
            domain_exists=_optional_bool(data.get("domain_exists")),
            mail_status=data.get("mail_status"),
            mail_capable=_optional_bool(data.get("mail_capable")),
            mail_usage=data.get("mail_usage"),
            spf_present=_optional_bool(data.get("spf_present")),
            dmarc_present=_optional_bool(data.get("dmarc_present")),
            organization_status=data.get("organization_status"),
            organization_backed=_optional_bool(data.get("organization_backed")),
            organization_known=_optional_bool(data.get("organization_known")),
            organization_verified=_optional_bool(data.get("organization_verified")),
            organization_confidence=data.get("organization_confidence"),
            company_valid=_optional_bool(data.get("company_valid")),
            company_confidence=data.get("company_confidence"),
            company_checked_at=data.get("company_checked_at"),
            company_evidence_routes=[str(route) for route in evidence_routes],
            documentary_association=(
                DocumentaryAssociation.from_dict(documentary_data)
                if isinstance(documentary_data, Mapping)
                else None
            ),
            association_ambiguous=_optional_bool(data.get("association_ambiguous")),
            association_claim_count=data.get("association_claim_count"),
            evaluated_at=data.get("evaluated_at"),
            organization_checked_at=data.get("organization_checked_at"),
            organization=(
                OrganizationPresentation.from_dict(organization_data)
                if isinstance(organization_data, Mapping)
                else None
            ),
            reason_codes=[str(code) for code in reason_codes],
            raw=data,
        )


@dataclass(frozen=True)
class SmtpRsAnalysis:
    """
    A normalized smtpRS analyse response with the raw payload preserved.
    """

    email: Optional[str] = None
    decision: Optional[str] = None
    overall_risk: Optional[float] = None
    tier: Optional[str] = None
    analysis_profile: Optional[str] = None
    response_profile: Optional[str] = None
    credit_cost: Optional[int] = None
    credits_charged: Optional[int] = None
    reasons: List[str] = field(default_factory=list)
    usage: Dict[str, Any] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)
    # Appended to preserve the positional field order of the 0.1.0 dataclass.
    company_validity_beta: Optional[CompanyValidityBeta] = None
    raw_risk: Optional[float] = None
    raw_decision: Optional[str] = None
    organization_validity_enabled: Optional[bool] = None
    organization_adjustment: Optional[float] = None
    domain_signal: Optional[DomainSignal] = None
    usage_event_id: Optional[int] = None
    idempotency_replayed: Optional[bool] = None
    layers: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "SmtpRsAnalysis":
        data = dict(payload)
        usage = data.get("usage") if isinstance(data.get("usage"), dict) else {}
        reasons = data.get("reasons") if isinstance(data.get("reasons"), list) else []
        company_validity_data = data.get("company_validity_beta")
        company_validity_beta = (
            CompanyValidityBeta.from_dict(company_validity_data)
            if isinstance(company_validity_data, Mapping)
            else None
        )
        domain_signal_data = data.get("domain_signal")
        domain_signal = (
            DomainSignal.from_dict(domain_signal_data)
            if isinstance(domain_signal_data, Mapping)
            else None
        )
        layers = data.get("layers") if isinstance(data.get("layers"), dict) else {}
        return cls(
            email=data.get("email") or data.get("input"),
            decision=data.get("decision"),
            overall_risk=_first_present(data, "overall_risk", "risk_score"),
            tier=data.get("tier"),
            analysis_profile=data.get("analysis_profile"),
            response_profile=data.get("response_profile"),
            credit_cost=data.get("credit_cost"),
            credits_charged=data.get("credits_charged"),
            company_validity_beta=company_validity_beta,
            raw_risk=data.get("raw_risk"),
            raw_decision=data.get("raw_decision"),
            organization_validity_enabled=_optional_bool(data.get("organization_validity_enabled")),
            organization_adjustment=data.get("organization_adjustment"),
            domain_signal=domain_signal,
            usage_event_id=data.get("usage_event_id"),
            idempotency_replayed=_optional_bool(data.get("idempotency_replayed")),
            layers=dict(layers),
            reasons=[str(reason) for reason in reasons],
            usage=dict(usage),
            raw=data,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Return the original API response payload."""
        return dict(self.raw)
