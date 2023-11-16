# Intercom encodes timestamps as UTC Unix timestamps
# So we always encode/decode python datetime or date objects as this
import json
from datetime import datetime, date
from dateutil.parser import parse
from dateutil.tz import UTC
from decimal import Decimal


class IntercomFormatEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.timestamp()
        if isinstance(obj, date):
            return datetime(obj.year, obj.month, obj.day).timestamp()
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


class IntercomFormatDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        kwargs.pop('encoding', None)
        json.JSONDecoder.__init__(
            self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        for k, v in dct.items():
            if k.endswith("_at") and v is not None:
                try:
                    dct[k] = datetime.fromtimestamp(float(v), tz=UTC)
                except ValueError:
                    dct[k] = parse(v)
                except OverflowError:
                    pass
        return dct
