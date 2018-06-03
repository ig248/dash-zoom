import logging as log
import os
from flask import Flask
from flask_caching import Cache


log.basicConfig(level=log.DEBUG)
server = Flask(__name__)
cache = Cache(server, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'localhost:6379'),
    'CACHE_DEFAULT_TIMEOUT': 0,
})


def flat_key(*keys):
    """Generate one key from a sequence of identifiers"""
    return ':'.join([str(k) for k in keys])
