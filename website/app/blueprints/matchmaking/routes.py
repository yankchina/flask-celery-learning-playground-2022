from flask_login import login_required, current_user
from flask import jsonify, url_for, render_template, request, current_app
# from app.models.user import User
from app import socketio, cache
from app.blueprints.matchmaking import bp
from app.blueprints.matchmaking.tasks import find_match


@bp.route('/join_matchmaking')
@login_required
def join_matchmaking_route():
    joined_queue = current_user.join_queue()
    if not joined_queue:
        return jsonify({'success': False, 'message': 'Failed to join queue'})
    task = find_match.apply_async(args=[current_user.get_matchmaking_info()], priority=0)
    return jsonify({
        'success': True,
        'location': url_for('matchmaking.find_match_task_status', task_id=task.id),
        'message': 'Joined queue.'
    })


@bp.route('/leave_matchmaking', methods=["POST"])
@login_required
def leave_matchmaking_route():
    players = cache.get('queued-players') or []
    user_id = str(current_user.id)
    players = [p for p in players if p['id'] != user_id]
    cache.set('queued-players', players)

    left_queue = current_user.leave_queue()
    if left_queue:
        return jsonify({'type': 'success', 'message': 'User left queue.'})

    return jsonify({'type': 'error', 'message': 'User was not in a queue to leave.'})
