from flask import jsonify, current_app, request
from app.blueprints.game_two import bp

@bp.route('/delete_game')
def delete_game():
    data = request.args.to_dict(flat=False)
    game_id = data.get('game_id')[0]

    if data.get('key')[0] != current_app.config.get('GAME_SERVER_AUTHENTICATION_KEY'):
        current_app.logger.exception(f"No key was supplied. Returning...")
    try:
        success = current_app.game_manager.delete_game(game_id)
        if success:
            return jsonify({'success': False})
    except:
        current_app.logger.exception(f"Failed to delete game.")
        return jsonify({'success': False})
