from marshmallow import Schema, fields, validates_schema, ValidationError


class NearTermLiabilitiesSchema(Schema):
    amount = fields.Float(required=True)
    years_until_due = fields.Float(required=True)
    coverage_status = fields.String(required=True)  # not_covered, partial, covered_or_far


class ProfileSchema(Schema):
    age = fields.Float(required=True)
    retirement_age = fields.Float(required=True)
    investable_assets = fields.Float(required=True)
    net_worth = fields.Float(required=True)
    annual_income_after_tax = fields.Float(required=True)
    annual_essential_spend = fields.Float(required=True)
    annual_contribution = fields.Float(required=True)
    total_debt = fields.Float(required=True)
    annual_debt_service = fields.Float(required=True)
    emergency_fund_months = fields.Float(required=True)
    near_term_liabilities = fields.Nested(NearTermLiabilitiesSchema, required=True)
    country = fields.String(required=True)
    rf_real = fields.Float(required=False, allow_none=True)


class AssessmentInSchema(Schema):
    profile = fields.Nested(ProfileSchema, required=True)
    # rt answers as dict of {QRTx: label}
    rt_answers = fields.Dict(keys=fields.String(), values=fields.String(), required=True)
    # income stability: contract, mixed, stable_employee, tenured
    income_stability = fields.String(required=True)
    # Either provide w_target or target_spend
    w_target = fields.Float(required=False, allow_none=True)
    target_spend = fields.Float(required=False, allow_none=True)

    @validates_schema
    def validate_targets(self, data, **kwargs):
        w = data.get('w_target')
        s = data.get('target_spend')
        if (w is None) == (s is None):
            raise ValidationError('Provide exactly one of w_target or target_spend')
        p = data['profile']
        for key in ['age','retirement_age','investable_assets','net_worth','annual_income_after_tax','annual_essential_spend','annual_contribution','total_debt','annual_debt_service','emergency_fund_months']:
            if p[key] < 0:
                raise ValidationError(f'{key} must be non-negative')


class AssessmentOutSchema(Schema):
    id = fields.String()
    created_at = fields.DateTime()
    spec_version = fields.String()
    rt = fields.Float()
    rc = fields.Float()
    rn = fields.Float()
    rs = fields.Float()
    need_gap_pp = fields.Float()
    annotations = fields.List(fields.String())
    carve_out_before_investing = fields.Float()
    breakdown = fields.Dict()


