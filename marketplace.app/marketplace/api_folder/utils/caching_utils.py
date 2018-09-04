import json

from marketplace import cache, REDIS_STORAGE_TIME


def cache_json_and_get(path, response):
    cache.execute_command('JSON.SET', path, '.', json.dumps(response))
    cache.expire(path, REDIS_STORAGE_TIME)
    return response


def get_cached_json(path):
    res = cache.execute_command('JSON.GET', path, 'NOESCAPE')
    return json.loads(res) if res is not None else None
