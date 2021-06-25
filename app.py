import time
import sys

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    if os.getenv('USE_CACHE') == 'true':
        count = get_hit_count()
    else:
        count = 'unknown'

    return 'Bye WTC! I have been seen {} times.\n'.format(count)
