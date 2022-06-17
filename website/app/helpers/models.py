from flask import current_app



def get_user_from_id(user_id):
    '''
        Parameters:
            user_models (list): User models to choose from, first one found will be chosen
    '''
    from app.models.unregistered_user import UnregisteredUser
    from app.models.user import User
    from app.blueprints.admin.models import Admin

    user_models = [User, UnregisteredUser, Admin]

    for model in user_models:
        user = model.objects(id=user_id).first()
        if user:
            current_app.logger.debug(f'Returning {model.__name__} {user}')
            return user
    return None

def get_user_from_tag(user_tag):
    '''
        Parameters:
            user_models (list): User models to choose from, first one found will be chosen
    '''
    from app.models.unregistered_user import UnregisteredUser
    from app.models.user import User
    from app.blueprints.admin.models import Admin

    user_models = [User, UnregisteredUser, Admin]

    for model in user_models:
        user = model.objects(user_tag=user_tag).first()
        if user:
            current_app.logger.debug(f'Returning {model.__name__} {user}')
            return user
    return None
