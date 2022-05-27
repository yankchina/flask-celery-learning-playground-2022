import datetime
from app import cache
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_babel import _
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash, current_app
from app.models.user import User
from app.blueprints.admin import bp
from app.blueprints.admin.models import Admin
from app.blueprints.admin.route_protection import admin_required
from app.blueprints.admin.forms import LoginForm
from app.blueprints.admin.sockets import emit_admin_notification
from app.blueprints.matchmaking.resets import reset_all


@bp.route('/control_panel')
@login_required
@admin_required
def index():
    id_map = cache.get('id_map') or {}
    return render_template('admin/index.html', id_map=id_map)

@bp.route('/test')
@login_required
@admin_required
def test():
    return render_template('admin/test.html')

@bp.route('/not_authorized')
def not_authorized():
    return render_template('admin/not_authorized.html')
    # return render_template('not_authorized.html')

# @bp.route('/login', methods=["GET", "POST"])
# def login():
#     if request.method == "GET":
#         return render_template("login.html")

#     # method == post
#     username = request.form.get('username')
#     password = request.form.get('password')

#     user = User.objects.find(username=username)
#     if user:
#         # check password hash
#         # check_password_hash(
#         # if user.password_hash == get_hash(password, algorithm, secret)

#         #     login_user(user)
#         #     return jsonify({'type': 'success', 'message': 'User logged in successfully!'})
#         # else:
#         #     return jsonify({'type': 'error', 'message': 'Username or password was incorrect'})
#         pass
#     else:
#         return jsonify({'type': 'error', 'message': 'Username or password was incorrect'})


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user._cls == "Admin":
        return redirect(url_for('admin.index'))

    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.objects(username=form.username.data).first()
        if admin is None or not check_password_hash(admin.password_hash, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('admin.login'))
        print('\n\n')
        print(current_user, flush=True)
        logout_user() # we have to call this here because we are logged in by default as an unregistered user
        print(current_user, flush=True)
        login_user(admin, remember=True, duration=datetime.timedelta(days=30))
        print(current_user, flush=True)
        print('\n\n')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin.index')
        return redirect(next_page)
    return render_template('admin/login.html', title=_('Sign In'), form=form)


@bp.route('/send_notification_to_sid')
@login_required
@admin_required
def send_notification_to_sid():
    msg = request.args.get('message')
    sid = request.args.get('sid')
    emit_admin_notification(sid, msg)
    return jsonify({'success': True})

@bp.route('/clear_id_map_cache')
@login_required
@admin_required
def clear_id_map_cache():
    cache.set('id_map', None)
    return jsonify({'success': True})

@bp.route('/reset_all_matchmaking_user_id')
@login_required
@admin_required
def reset_all_matchmaking_user_id():
    user_id = request.args.get('user_id')
    reset_all(user_id)
    return jsonify({'success': True})

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
