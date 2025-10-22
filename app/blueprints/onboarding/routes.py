from flask import request, jsonify, current_app
from flask_restful import Resource
from flask_login import login_required, current_user

from . import api
from .schemas import AssessmentInSchema, AssessmentOutSchema
from .source.services import compute_assessment, persist_assessment, to_response
from .source.spec import SPEC, SPEC_VERSION
from .model import RiskAssessment


class SpecResource(Resource):
    def get(self):
        return jsonify({"spec_version": SPEC_VERSION, **SPEC})


def _resolve_user_id():
    if current_user.is_authenticated:
        return str(current_user.get_id())
    if bool(current_app.config.get("LOGIN_DISABLED")) and current_app.config.get("ENV") == "development":
        return current_app.config.get("DEV_USER_ID")
    return None


class AssessmentResource(Resource):
    method_decorators = [login_required]

    def post(self):
        payload = AssessmentInSchema().load(request.get_json())
        user_id = _resolve_user_id()
        if not user_id:
            return {"error": "Authentication required"}, 401
        result = compute_assessment(user_id=user_id, payload=payload)
        ra = persist_assessment(result)
        return AssessmentOutSchema().dump(to_response(ra)), 201


class AssessmentLatestResource(Resource):
    method_decorators = [login_required]

    def get(self):
        user_id = _resolve_user_id()
        if not user_id:
            return {"error": "Authentication required"}, 401
        ra = RiskAssessment.query.filter_by(user_id=user_id).order_by(RiskAssessment.created_at.desc()).first()
        if not ra:
            return {"message": "no assessment"}, 404
        return AssessmentOutSchema().dump(to_response(ra)), 200


api.add_resource(SpecResource, '/spec')
api.add_resource(AssessmentResource, '/assessment')
api.add_resource(AssessmentLatestResource, '/assessment/latest')


