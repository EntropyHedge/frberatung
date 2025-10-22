SPEC_VERSION = "2025-10-22.v1"

SPEC = {
    "rt_questions": [
        {"id":"QRT1","weight":0.25,"choices":[{"label":"<=5%","points":10},{"label":"10%","points":25},{"label":"15%","points":40},{"label":"20%","points":55},{"label":"30%","points":70},{"label":"40%","points":85},{"label":">=50%","points":95}]},
        {"id":"QRT2","weight":0.25,"choices":[{"label":"sell all","points":10},{"label":"sell some","points":35},{"label":"hold","points":65},{"label":"buy more","points":90}]},
        {"id":"QRT3","weight":0.15,"choices":[{"label":"new","points":30},{"label":"1-3y","points":50},{"label":"3-7y","points":65},{"label":"7-15y","points":80},{"label":">15y","points":90}]},
        {"id":"QRT4","weight":0.15,"choices":[{"label":"strongly agree","points":20},{"label":"agree","points":40},{"label":"neutral","points":60},{"label":"disagree","points":80},{"label":"strongly disagree","points":90}]},
        {"id":"QRT5","weight":0.20,"choices":[{"label":"sold near lows","points":20},{"label":"paused contributions","points":40},{"label":"held","points":70},{"label":"rebalanced/bought","points":90}]}
    ],
    "rc_weights": {"horizon":0.25,"balance":0.20,"income":0.15,"debt":0.15,"emergency":0.15,"liabilities":0.10},
    "rn_brackets_pp": [
        {"up_to":0,"points":25},
        {"up_to":1,"points":40},
        {"up_to":2,"points":55},
        {"up_to":3,"points":70},
        {"up_to":4,"points":80},
        {"above":4,"points":90}
    ],
    "combine_weights": {"RT":0.35,"RC":0.45,"RN":0.20},
    "caps": {"capacity_cap_slope":0.85,"capacity_cap_intercept":15,"need_floor_band_min":55,"short_horizon_max_RS":40},
}


