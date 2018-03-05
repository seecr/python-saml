from time import time as _time
from datetime import datetime as _datetime

# TS: Hackish way to enable time-mocking (to test SAMLResponse's).
#
# Set `mocked_time_value to a truthy-value to enable time-bending powers; like so:
# sys.modules['onelogin.saml2.time_indirect'].mocked_time_fn = <function returning UNIX-Time (time.time()'s format) when called>.

mocked_time_fn = None

def time():
    if mocked_time_fn:
        return mocked_time_fn()
    return _time()

def _mocked_datetime_utcnow():
    return _datetime.utcfromtimestamp(mock_time_fn())

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
