from .conf import conf
from .exceptions import AppError

if conf["CACHE_TYPE"] == "simple":
    from werkzeug.contrib.cache import SimpleCache

    cache = SimpleCache(default_timeout=conf['CACHE_TIMEOUT'])
elif conf["CACHE_TYPE"] == "fs":
    from werkzeug.contrib.cache import FileSystemCache

    cache = FileSystemCache(cache_dir=conf["CACHE_DIR"], default_timeout=conf['CACHE_TIMEOUT'])
elif conf["CACHE_TYPE"] == "redis":
    from werkzeug.contrib.cache import RedisCache

    cache = RedisCache(host=conf['CACHE_HOST'], port=conf['CACHE_PORT'],
                       password=conf['CACHE_PASSWORD'] or None, db=conf['CACHE_DB'],
                       default_timeout=conf['CACHE_TIMEOUT'], key_prefix=conf['CACHE_PREFIX'])
else:
    raise AppError("Cannot recognize the cache type")
