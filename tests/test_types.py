import pytest
from zigpy_zigate import types as t
from zigpy_zigate.api import RESPONSES, COMMANDS


def test_deserialize():
    extra = b'\xBE\xEF'
    data = b'\x00\x01\x00\x02'
    schema = RESPONSES[0x8000]
    result, rest = t.deserialize(data + extra, schema)
    assert rest == b''
    assert result[0] == 0x00
    assert result[1] == 0x01
    assert result[2] == 0x0002
    assert result[3] == extra

    extra = b'\xBE\xEF'
    data = b'\x00\x00\x01\x00\x01\x01\x01\x02\x12\x34\x02\xab\xcd\x02\x01\x00'
    schema = RESPONSES[0x8002]
    result, rest = t.deserialize(data + extra, schema)
    assert result[0] == 0x00
    assert result[1] == 0x0001
    assert result[2] == 0x0001
    assert result[3] == 0x01
    assert result[4] == 0x01
    assert result[5] == 0x02
    assert result[6] == 0x1234
    assert result[7] == 0x02
    assert result[8] == 0xabcd
    assert result[9] == b'\x01\x00'
    assert rest == extra

    data = b'\x00\x01\x01\x02\x12\x34\xff'
    schema = RESPONSES[0x8702]
    result, rest = t.deserialize(data + extra, schema)
    addr = t.Address()
    addr.address_mode = t.ADDRESS_MODE.NWK
    addr.address = 0x1234
    assert result[0] == 0x00
    assert result[1] == 0x01
    assert result[2] == 0x01
    assert result[3] == addr
    assert result[4] == 0xff

    data = b'\x00\x01\x01\x03\x12\x34\x56\x78\x9a\xbc\xde\xf0\xff'
    schema = RESPONSES[0x8702]
    result, rest = t.deserialize(data + extra, schema)
    addr = t.Address()
    addr.address_mode = t.ADDRESS_MODE.IEEE
    addr.address = 0x123456789abcdef0
    assert result[0] == 0x00
    assert result[1] == 0x01
    assert result[2] == 0x01
    assert result[3] == addr
    assert result[4] == 0xff


def test_serialize():
    data = [True]
    schema = COMMANDS[0x0002]
    result = t.serialize(data, schema)
    assert result == b'\x01'

    data = [b'\x12\x34']
    schema = (t.LBytes,)
    result = t.serialize(data, schema)
    assert result == b'\x02\x124'
