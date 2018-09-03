from flask import request
from marketplace.api_folder.utils.caching_utils import get_cached_json


def get_cache(rest_function):
    def get_cache_wrapper(self, *args, **kwargs):
        path = request.url
        cache = get_cached_json(path)
        return rest_function(self, path=path, cache=cache, **kwargs)

    return get_cache_wrapper
