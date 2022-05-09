from flask_login import login_required, login_user
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash, current_app
from app.models.user import User
from app.blueprints.auth import bp


@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")

    # method == post
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.objects.find(username=username)
    if user:
        # check password hash
        # check_password_hash(
        # if user.password_hash == get_hash(password, algorithm, secret)

        #     login_user(user)
        #     return jsonify({'type': 'success', 'message': 'User logged in successfully!'})
        # else:
        #     return jsonify({'type': 'error', 'message': 'Username or password was incorrect'})
        pass

    else:
        return jsonify({'type': 'error', 'message': 'Username or password was incorrect'})
