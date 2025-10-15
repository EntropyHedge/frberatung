from . import main_bp
from flask import render_template, redirect, url_for, abort
from flask_login import current_user, login_required
from datetime import datetime
from app.extensions import cache
import os
@main_bp.route('/')
def index():
    return render_template('home.html', current_user=current_user, year=datetime.now().year)
    
@main_bp.route('/charts')
@login_required
#@cache.cached(timeout=1000)
def charts():
    return render_template('charts.html',current_user = current_user, year=datetime.now().year)

@main_bp.route('/bitcoin')
@login_required
def bitcoin():
    return render_template('bitcoin.html',current_user = current_user, year=datetime.now().year)

@main_bp.route('/commodities')
@login_required
def commodities():
    return render_template('commodities.html',current_user = current_user, year=datetime.now().year)

@main_bp.route('/chat')
@login_required
@cache.cached(timeout=1000)
def chat():
    return render_template('chat.html',current_user = current_user, year=datetime.now().year)

@main_bp.route('/historic')
@login_required
def historic():
    return render_template('historic.html',current_user = current_user, year=datetime.now().year)

@main_bp.route('/global-liquidity')
@login_required
def global_liquidity():
    return render_template('global_liquidity.html',current_user = current_user, year=datetime.now().year)

@main_bp.route('/cot-analytics')
@login_required  
def cot_analytics():
    return render_template('cot_analytics.html')

def get_name_of_templates(folder_name):
    files = []
    for file in os.listdir(folder_name):
        if file.endswith('.html'):
            files.append(file)
    return files


@main_bp.route('/testing/<filename>')
@login_required
def testing(filename):
    # Validate filename to prevent directory traversal
    if filename not in get_name_of_templates('app/templates/testing'):
        abort(404)
    return render_template(f'testing/{filename}', current_user=current_user, year=datetime.now().year)
