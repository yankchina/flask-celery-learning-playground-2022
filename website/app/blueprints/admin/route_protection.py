from flask import url_for, render_template, current_app, abort, redirect
from flask_login import current_user
# from app.models import Permission

# def admin_required(func):
#     from app.blueprints.admin.models import Admin
#     def protect_route(*args, **kwargs):
#         if current_user._cls == "Admin":
#             return func(*args, **kwargs)
#         else:
#             return render_template(url_for('admin.not_authorized'))
#     return protect_route

from functools import wraps

def admin_required(func):
    '''Redirects users who are not admin to their current page
        to restrict access to admin only pages'''
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user._cls != 'Admin':
            return redirect(url_for('admin.not_authorized'))
        return func(*args, **kwargs)
    return decorated_view

# def permission_required(permission):
#     """Restrict a view to users with the given permission."""

#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             if not current_user.can(permission):
#                 abort(403)
#             return f(*args, **kwargs)

#         return decorated_function

#     return decorator


# def admin_required(f):
#     return permission_required(Permission.ADMINISTER)(f)