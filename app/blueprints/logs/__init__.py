from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
import os

logs_bp = Blueprint('logs', __name__, url_prefix='/logs', template_folder='templates')


@logs_bp.route('/')
@login_required
def view_logs():
    if not getattr(current_user, 'is_admin', False):
        abort(403)
    log_path = os.path.abspath('app.log')
    lines = []
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()[-200:]
    return render_template('logs/index.html', log_lines=lines)
