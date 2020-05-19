from intercom2.json import DateTimeEncoder, DateTimeDecoder
import json
from datetime import datetime, date
from dateutil.tz import tzutc


def test_encode_datetime():
    obj = {'foo_at': datetime(2020, 1, 1, 12, 0, 0)}
    j = json.dumps(obj, cls=DateTimeEncoder)
    assert j == '{"foo_at": 1577880000.0}'


def test_encode_date():
    obj = {'foo_at': date(2020, 1, 1)}
    j = json.dumps(obj, cls=DateTimeEncoder)
    assert j == '{"foo_at": 1577836800.0}'


def test_decode_datetime():
    j = '{"foo_at": 1577880000.0}'
    obj = json.loads(j, cls=DateTimeDecoder)
    assert obj['foo_at'] == datetime(2020, 1, 1, 12, 0, 0)


def test_decode_datetime_str():
    j = '{"foo_at": "1577880000.0"}'
    obj = json.loads(j, cls=DateTimeDecoder)
    assert obj['foo_at'] == datetime(2020, 1, 1, 12, 0, 0)


def test_decode_datetime_iso():
    j = '{"foo_at": "2020-05-19T10:00:17Z"}'
    obj = json.loads(j, cls=DateTimeDecoder)
    assert obj['foo_at'] == datetime(2020, 5, 19, 10, 0, 17, tzinfo=tzutc())


def test_decode_nested_datetime():
    j = '{"nest": {"foo_at": 1577880000.0}}'
    obj = json.loads(j, cls=DateTimeDecoder)
    assert obj['nest']['foo_at'] == datetime(2020, 1, 1, 12, 0, 0)


def test_dont_decode_number():
    j = '{"foo": 1577880000.0}'
    obj = json.loads(j, cls=DateTimeDecoder)
    assert obj['foo'] == 1577880000.0
