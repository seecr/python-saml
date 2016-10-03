from contextlib import contextmanager
from datetime import datetime as _datetime
from hashlib import sha1
from time import time as _time
from uuid import uuid4

# TS: Hackish way to enable random-id and time-mocking (to test SAMLResponse's).
#
# Set `mocked_time_fn to a truthy-value, a function returning UNIX-Time (time.time()'s format).
#
# Set `mocked_random_id_fn' to a truthy-value, a function returning a `random-id-string' when called.

mocked_time_fn = None
mocked_random_id_fn = None


@contextmanager
def mocked_time(time_fn):
    global mocked_time_fn

    prev_time_fn = mocked_time_fn
    try:
        mocked_time_fn = time_fn
        yield
    finally:
        mocked_time_fn = prev_time_fn

@contextmanager
def mocked_generate_unique_id(random_id_fn):
    global mocked_random_id_fn

    prev_random_id_fn = mocked_random_id_fn
    try:
        mocked_random_id_fn = random_id_fn
        yield
    finally:
        mocked_random_id_fn = prev_random_id_fn

def time():
    if mocked_time_fn:
        return mocked_time_fn()
    return _time()

def _mocked_datetime_utcnow():
    return _datetime.utcfromtimestamp(mocked_time_fn())

class datetime(object):
    def __getattr__(self, attr):
        if mocked_time_fn:
            return self._mocked_getattr(attr)
        return getattr(_datetime, attr)

    def _mocked_getattr(self, attr):
        if attr == 'utcnow':
            return _mocked_datetime_utcnow
        return getattr(_datetime, attr)


datetime = datetime()

def generate_unique_id():
    if mocked_random_id_fn:
        return mocked_random_id_fn()
    return 'ONELOGIN_%s' % sha1(uuid4().hex).hexdigest()  # Weird, but the original implementation.
