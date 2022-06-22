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
        user = model.objects(user_tag=user_tag)
        if user:
            if len(user) > 1: # conflicting tag
                current_app.logger.error(f'Conflicting user tag found: {user_tag}')
                return {'success': False, 'message': 'More than one user found with that tag. This issue has been reported to administrators. An immediate fix is to either have your friend send you a request or ask them to change their username if they are an unregistered user.'}

            current_app.logger.debug(f'Returning {model.__name__} {user}')
            return user.first()
    return None
