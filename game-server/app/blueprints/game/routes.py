from flask import render_template, jsonify
from app.blueprints.game import bp




@bp.route('/')
def index():
    return render_template('index.html')