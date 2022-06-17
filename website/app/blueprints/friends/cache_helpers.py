from app import cache

def update_cache_object(cache_key, key, data={}, **kwargs):
    '''
    pass in data to be updated
    '''
    try:
        cache_obj = cache.get(cache_key) or {}
        current_obj = cache_obj.get(key, {})

        current_obj.update(data)
        cache_obj[key] = current_obj
        cache.set(cache_key, cache_obj, **kwargs)

        return True
    except:
        return False

def get_sid_from_user_id(user_id):
    id_map = cache.get('id_map') or {}
    return id_map.get(user_id, {}).get('sid')

def get_key_from_id_map_cache(user_id, key):
    id_map = cache.get('id_map') or {}
    return id_map.get(user_id, {}).get(key)

def clear_cache_key(key):
    cache.delete(key)