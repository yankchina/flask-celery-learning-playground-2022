from flask_login import login_required, current_user
from flask import jsonify, url_for
# from app.models.user import User
from app.blueprints.matchmaking import bp
from app.blueprints.matchmaking.server import get_matchmaking_server
from app.blueprints.matchmaking.tasks import find_match



@bp.route('/join_matchmaking')
@login_required
def join_matchmaking():
    # request_matchmaking()
    # joined_queue = current_user.join_queue()

    # print(current_user)
    # print(joined_queue)

    # if not joined_queue:
    #     return jsonify({'success': False, 'message': 'User failed to join queue'})

    # need to send celery task that updates redis queue and cycles through to find match

    players = find_match.delay((current_user.get_matchmaking_info(),))

    # if players:
        # send_invitation_request(players)
    print('players', flush=True)
    print(players, flush=True)

    return jsonify({
        'success': True,
        # 'location': url_for('matchmaking.taskstatus', task_id=task.id)
    })

    # return jsonify({'type': 'success', 'message': 'User successfully joined queue'})

@bp.route('/status/<task_id>')
def taskstatus(task_id):
    task = find_match.AsyncResult(task_id)
    print(task)
    print(task.state)
    print(task.info)
    print(dir(task))
    return jsonify({'success': True, 'message': 'checked task'})



@bp.route('/leave_matchmaking', methods=["POST"])
@login_required
def leave_matchmaking():

    left_queue = current_user.leave_queue()

    if left_queue:
        return jsonify({'type': 'success', 'message': 'User left queue.'})

    return jsonify({'type': 'error', 'message': 'User was not in a queue to leave.'})