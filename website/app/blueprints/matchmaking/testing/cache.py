from app import cache
from app.helpers.print import prnt



def test_uid_object():
    id_map = cache.get('id_map') or {}
    prnt(id_map)
