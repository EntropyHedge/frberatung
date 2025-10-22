from __future__ import annotations

from typing import Dict, Any

from app.extensions import db
from app.blueprints.onboarding.model import RiskAssessment
from .spec import SPEC, SPEC_VERSION
from .scoring import score_rt, score_rc, score_rn, combine_scores, clamp


def compute_assessment(user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    profile = payload["profile"]
    rt_answers = payload["rt_answers"]
    income_stability = payload["income_stability"]

    rf_real = float(profile.get("rf_real") or 0.0)
    country = profile.get("country")

    RT = score_rt(rt_answers)
    RC, rc_subs = score_rc(profile, income_stability)

    target_spend = payload.get("target_spend")
    if target_spend is not None:
        W_target = float(target_spend) / 0.03
    else:
        W_target = float(payload.get("w_target"))

    RN, need_gap_pp = score_rn(profile, W_target=W_target, rf_real=rf_real)

    H = max(float(profile["retirement_age"]) - float(profile["age"]), 0.0)
    ef_months = float(profile["emergency_fund_months"])
    RS, meta = combine_scores(RT=RT, RC=RC, RN=RN, H=H, ef_months=ef_months, need_gap_pp=need_gap_pp)

    carve_out_before_investing = 0.0
    if ef_months < 3.0:
        annual_spend = float(profile["annual_essential_spend"])
        carve_out_before_investing = clamp((3.0 - ef_months) * (annual_spend / 12.0), 0.0, float("inf"))

    breakdown = {
        "rc_subscores": rc_subs,
        "rs_raw": meta["rs_raw"],
        "rs_cap": meta["rs_cap"],
        "capacity_capped": meta["capacity_capped"],
        "need_floor_applied": meta["need_floor_applied"],
        "short_horizon_capped": meta["short_horizon_capped"],
    }

    return {
        "spec_version": SPEC_VERSION,
        "rt": RT,
        "rc": RC,
        "rn": RN,
        "rs": RS,
        "need_gap_pp": need_gap_pp,
        "annotations": meta["annotations"],
        "carve_out_before_investing": carve_out_before_investing,
        "breakdown": breakdown,
        "rf_real": rf_real,
        "country": country,
        "profile": profile,
        "user_id": user_id,
    }


def persist_assessment(result: Dict[str, Any]) -> RiskAssessment:
    ra = RiskAssessment(
        user_id=result["user_id"],
        spec_version=result["spec_version"],
        rt=result["rt"],
        rc=result["rc"],
        rn=result["rn"],
        rs=result["rs"],
        need_gap_pp=result["need_gap_pp"],
        horizon_years=max(float(result["profile"]["retirement_age"]) - float(result["profile"]["age"]), 0.0),
        ef_months=float(result["profile"]["emergency_fund_months"]),
        rf_real=result["rf_real"],
        country=result["country"],
        capacity_capped=bool(result["breakdown"]["capacity_capped"]),
        need_floor_applied=bool(result["breakdown"]["need_floor_applied"]),
        short_horizon_capped=bool(result["breakdown"]["short_horizon_capped"]),
        inputs_json=result["profile"],
        scores_json={
            "rt": result["rt"],
            "rc": result["rc"],
            "rn": result["rn"],
            "rs": result["rs"],
            "annotations": result["annotations"],
            "breakdown": result["breakdown"],
        },
    )
    db.session.add(ra)
    db.session.commit()
    return ra


def to_response(ra: RiskAssessment) -> Dict[str, Any]:
    return {
        "id": str(ra.id),
        "created_at": ra.created_at.isoformat() if ra.created_at else None,
        "spec_version": ra.spec_version,
        "rt": ra.rt,
        "rc": ra.rc,
        "rn": ra.rn,
        "rs": ra.rs,
        "need_gap_pp": ra.need_gap_pp,
        "annotations": ra.scores_json.get("annotations", []) if ra.scores_json else [],
        "carve_out_before_investing": 0.0,
        "breakdown": ra.scores_json.get("breakdown", {}) if ra.scores_json else {},
    }


