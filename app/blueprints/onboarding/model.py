from app.extensions import db
from datetime import datetime


class RiskAssessment(db.Model):
    __tablename__ = 'risk_assessments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    spec_version = db.Column(db.String(32), nullable=False)
    country = db.Column(db.String(2))
    rf_real = db.Column(db.Float)

    rt = db.Column(db.Float)
    rc = db.Column(db.Float)
    rn = db.Column(db.Float)
    rs = db.Column(db.Float)
    need_gap_pp = db.Column(db.Float)
    horizon_years = db.Column(db.Float)
    ef_months = db.Column(db.Float)

    capacity_capped = db.Column(db.Boolean, default=False)
    need_floor_applied = db.Column(db.Boolean, default=False)
    short_horizon_capped = db.Column(db.Boolean, default=False)

    inputs_json = db.Column(db.JSON)
    scores_json = db.Column(db.JSON)


