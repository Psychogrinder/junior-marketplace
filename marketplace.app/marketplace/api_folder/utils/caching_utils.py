import json
import redis
from flask import request
from marketplace import cache, REDIS_STORAGE_TIME, error_reports


# Decorators

def get_cache(rest_function):
    def get_cache_wrapper(self, *args, **kwargs):
        path = request.url
        cache = get_cached_json(path=path)
        kwargs['meta'] = get_cached_json(path='{}/meta'.format(path))
        return rest_function(self, path=path, cache=cache, **kwargs)

    return get_cache_wrapper


def check_redis_connection(cache_function):
    def check_connection_wrapper(*args, **kwargs):
        try:
            cache.ping()
            kwargs['is_connected'] = True
        except redis.exceptions.ConnectionError:
            kwargs['is_connected'] = False
            error_reports.send_report('No connect to redis', 'app', reporter='cache')
        return cache_function(**kwargs)

    return check_connection_wrapper


# Functions

@check_redis_connection
def cache_json_and_get(**kwargs):
    if kwargs['is_connected']:
        cache.execute_command('JSON.SET', kwargs['path'], '.', json.dumps(kwargs['response']))
        cache.expire(kwargs['path'], REDIS_STORAGE_TIME)
    return kwargs['response']


@check_redis_connection
def get_cached_json(**kwargs):
    if kwargs['is_connected']:
        res = cache.execute_command('JSON.GET', kwargs['path'], 'NOESCAPE')
        return json.loads(res) if res is not None else None
    else:
        return None
