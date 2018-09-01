from flask import request
import marketplace.api_folder.api_utils as utils


def get_cache(rest_function):
    def get_cache_wrapper(self, *args, **kwargs):
        path = request.url
        cache = utils.get_cached_json(path)
        return rest_function(self, path=path, cache=cache, **kwargs)

    return get_cache_wrapper
