from flask import jsonify
import random
from app import cache, celery

@celery.task(name="add_to_store")
def add_to_store():
    print(dir(cache))
    players = cache.get('players') or []
    print(players, flush=True)
    players.append(random.randint(0,1000))
    cache.set('players', players)
    print(players, flush=True)
    return jsonify({'success': True})
