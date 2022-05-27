from flask_login import current_user
# from Database.mongo.models import User, UnregisteredUser


def get_username():
    if '_cls' in dir(current_user):
        if current_user._cls == 'UnregisteredUser' or current_user._cls == 'User':
            return current_user.username
        else:
            return ''
    else:
        return ''

def get_user_class(user):
    if user.is_anonymous:
        return 'Anonymous'
    else:
        return user._cls

def random_print_string():
    print('\n\n\n yes this works \n\n\n')