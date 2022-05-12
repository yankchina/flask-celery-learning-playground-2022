from app.blueprints.redis import bp
from app.blueprints.redis.tasks import add_to_store


@bp.route('/test_redis')
def test_redis():
    return add_to_store()