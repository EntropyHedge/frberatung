from __future__ import annotations

from typing import Dict, Any, Tuple

from .spec import SPEC


def clamp(x: float, lo: float, hi: float) -> float:
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


def interpolate(x: float, x0: float, x1: float, y0: float, y1: float) -> float:
    if x <= x0:
        return y0
    if x >= x1:
        return y1
    t = (x - x0) / (x1 - x0)
    return y0 + t * (y1 - y0)


def score_rt(rt_answers: Dict[str, str]) -> float:
    total = 0.0
    weight_sum = 0.0
    for q in SPEC["rt_questions"]:
        qid = q["id"]
        w = float(q["weight"])
        weight_sum += w
        label = rt_answers.get(qid)
        points = None
        for c in q["choices"]:
            if c["label"] == label:
                points = float(c["points"])
                break
        if points is None:
            raise ValueError(f"Missing or invalid answer for {qid}")
        total += points * w
    if weight_sum == 0:
        return 0.0
    return clamp(total / weight_sum, 0.0, 100.0)


def score_rc(profile: Dict[str, Any], income_stability: str) -> Tuple[float, Dict[str, float]]:
    weights = SPEC["rc_weights"]

    age = float(profile["age"])
    retirement_age = float(profile["retirement_age"])
    H = max(retirement_age - age, 0.0)
    # A) Horizon (piecewise-linear using knots at 3→15, 7→45, 15→70; >15→85)
    if H <= 3.0:
        A = 15.0
    elif H <= 7.0:
        A = interpolate(H, 3.0, 7.0, 15.0, 45.0)
    elif H <= 15.0:
        A = interpolate(H, 7.0, 15.0, 45.0, 70.0)
    else:
        A = 85.0

    # B) Balance-sheet resilience
    nw = max(float(profile["net_worth"]), 0.0)
    spend = max(float(profile["annual_essential_spend"]), 1e-9)
    ratio = nw / spend
    # knots: ≤1→25, 2→40, 4→60, 7→75, 10→90
    if ratio <= 1:
        B = 25.0
    elif ratio <= 2:
        B = interpolate(ratio, 1.0, 2.0, 25.0, 40.0)
    elif ratio <= 4:
        B = interpolate(ratio, 2.0, 4.0, 40.0, 60.0)
    elif ratio <= 7:
        B = interpolate(ratio, 4.0, 7.0, 60.0, 75.0)
    elif ratio <= 10:
        B = interpolate(ratio, 7.0, 10.0, 75.0, 90.0)
    else:
        B = 90.0

    # C) Income stability
    income_map = {
        "contract": 35.0,
        "mixed": 55.0,
        "stable_employee": 70.0,
        "tenured": 85.0,
    }
    C = float(income_map.get(income_stability, 55.0))

    # D) Debt stress
    income = max(float(profile["annual_income_after_tax"]), 1e-9)
    dsr = max(float(profile["annual_debt_service"]), 0.0) / income
    if dsr >= 0.40:
        D = 20.0
    elif dsr >= 0.25:
        D = interpolate(dsr, 0.25, 0.40, 40.0, 20.0)
    elif dsr >= 0.10:
        D = interpolate(dsr, 0.10, 0.25, 60.0, 40.0)
    else:
        D = 80.0
    # bonus/malus
    total_debt = max(float(profile["total_debt"]), 0.0)
    debt_to_nw = total_debt / max(nw, 1e-9)
    if debt_to_nw <= 0.10:
        D += 5.0
    elif debt_to_nw > 0.50:
        D -= 5.0
    D = clamp(D, 0.0, 100.0)

    # E) Emergency fund
    ef = max(float(profile["emergency_fund_months"]), 0.0)
    if ef <= 1.0:
        E = 15.0
    elif ef <= 3.0:
        E = 40.0
    elif ef <= 5.0:
        E = 65.0
    else:
        E = 85.0

    # F) Near-term liabilities coverage
    ntl = profile["near_term_liabilities"]
    years_due = float(ntl.get("years_until_due", 0.0))
    coverage_status = ntl.get("coverage_status", "not_covered")
    if years_due <= 3:
        if coverage_status == "covered_or_far":
            F = 80.0
        elif coverage_status == "partial":
            F = 55.0
        else:
            F = 25.0
    else:
        F = 80.0

    subs = {"A_horizon": A, "B_balance": B, "C_income": C, "D_debt": D, "E_emergency": E, "F_liabilities": F}
    RC = (
        weights["horizon"] * A
        + weights["balance"] * B
        + weights["income"] * C
        + weights["debt"] * D
        + weights["emergency"] * E
        + weights["liabilities"] * F
    )
    return clamp(RC, 0.0, 100.0), subs


def solve_required_return(W0: float, C: float, H: float, W_target: float) -> float:
    # Handle trivial cases
    if H <= 0:
        return 0.0 if W_target <= W0 else 0.15
    if C == 0 and W_target <= W0:
        return 0.0

    # Bisection on r in [-0.05, 0.15]
    lo, hi = -0.05, 0.15

    def f(r: float) -> float:
        if abs(r) < 1e-9:
            return W0 + C * H - W_target
        growth = (1.0 + r) ** H
        ann = ((growth - 1.0) / r) * C
        return W0 * growth + ann - W_target

    f_lo = f(lo)
    f_hi = f(hi)
    if f_lo > 0 and f_hi > 0:
        return lo  # already above target with low r
    if f_lo < 0 and f_hi < 0:
        return hi  # even high r not enough → cap

    for _ in range(80):
        mid = 0.5 * (lo + hi)
        f_mid = f(mid)
        if f_mid == 0 or abs(hi - lo) < 1e-7:
            return mid
        if (f_lo <= 0 and f_mid >= 0) or (f_lo >= 0 and f_mid <= 0):
            hi = mid
            f_hi = f_mid
        else:
            lo = mid
            f_lo = f_mid
    return 0.5 * (lo + hi)


def rn_points_from_delta(delta_pp: float) -> float:
    for b in SPEC["rn_brackets_pp"]:
        if "up_to" in b and delta_pp <= b["up_to"]:
            return float(b["points"])
    return float(next(b for b in SPEC["rn_brackets_pp"] if "above" in b)["points"])


def score_rn(profile: Dict[str, Any], W_target: float, rf_real: float) -> Tuple[float, float]:
    age = float(profile["age"])
    retirement_age = float(profile["retirement_age"])
    H = max(retirement_age - age, 0.0)
    W0 = max(float(profile["investable_assets"]), 0.0)
    C = float(profile["annual_contribution"])

    r_star = solve_required_return(W0=W0, C=C, H=H, W_target=W_target)
    r_star = clamp(r_star, -0.05, 0.15)
    delta_pp = (r_star - rf_real) * 100.0

    # piecewise with interpolation between brackets
    if delta_pp <= 0:
        rn = 25.0
    elif delta_pp <= 1:
        rn = interpolate(delta_pp, 0.0, 1.0, 25.0, 40.0)
    elif delta_pp <= 2:
        rn = interpolate(delta_pp, 1.0, 2.0, 40.0, 55.0)
    elif delta_pp <= 3:
        rn = interpolate(delta_pp, 2.0, 3.0, 55.0, 70.0)
    elif delta_pp <= 4:
        rn = interpolate(delta_pp, 3.0, 4.0, 70.0, 80.0)
    else:
        rn = 90.0

    return clamp(rn, 0.0, 100.0), delta_pp


def combine_scores(RT: float, RC: float, RN: float, H: float, ef_months: float, need_gap_pp: float) -> Tuple[float, dict]:
    caps = SPEC["caps"]
    w = SPEC["combine_weights"]
    annotations = []

    rs_raw = w["RT"] * RT + w["RC"] * RC + w["RN"] * RN
    rs_cap = caps["capacity_cap_slope"] * RC + caps["capacity_cap_intercept"]
    rs1 = min(rs_raw, rs_cap)
    capacity_capped = rs1 < rs_raw
    if capacity_capped:
        annotations.append("Limited by capacity (RC).")

    if ef_months >= 3.0 and need_gap_pp >= 2.0:
        if rs1 < 55.0:
            rs1 = 55.0
            annotations.append("Higher growth suggested to reach goals.")
        need_floor_applied = True
    else:
        need_floor_applied = False

    if H <= 3.0 and rs1 > caps["short_horizon_max_RS"]:
        rs1 = caps["short_horizon_max_RS"]
        short_horizon_capped = True
    else:
        short_horizon_capped = False

    rs = clamp(rs1, 0.0, 100.0)
    flags = {
        "capacity_capped": capacity_capped,
        "need_floor_applied": need_floor_applied,
        "short_horizon_capped": short_horizon_capped,
    }
    return rs, {"rs_raw": rs_raw, "rs_cap": rs_cap, **flags, "annotations": annotations}


