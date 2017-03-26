from flask import Blueprint
from .. models import Permission

import pydevd

# pydevd.settrace('192.168.56.1', port=22, stdoutToServer=True, stderrToServer=True)

main = Blueprint('main', __name__)

from . import views, errors


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
