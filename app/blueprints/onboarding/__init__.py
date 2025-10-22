from flask import Blueprint
from flask_restful import Api

onboarding_bp = Blueprint('onboarding', __name__, url_prefix='/api/onboarding')
api = Api(onboarding_bp)

from . import routes  # noqa: E402,F401


