"""
MIT License

Copyright (c) 2019-present Luc1412

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import pytest

from fortnite_api.enums import Enum, try_enum


class DummyEnum(Enum):
    FOO = "foo"
    BAR = "bar"
    BAZ = "baz"


def test_dummy_enum():
    # Test basic enum functionality
    assert len(DummyEnum) == 3
    assert list(DummyEnum) == [DummyEnum.FOO, DummyEnum.BAR, DummyEnum.BAZ]
    assert list(reversed(DummyEnum)) == [DummyEnum.BAZ, DummyEnum.BAR, DummyEnum.FOO]

    # Test enum member access
    assert DummyEnum.FOO.name == "FOO"
    assert DummyEnum.FOO.value == "foo"
    assert DummyEnum["FOO"] == DummyEnum.FOO
    assert DummyEnum("foo") == DummyEnum.FOO

    # Test immutability
    with pytest.raises(TypeError):
        DummyEnum.FOO = "new"  # type: ignore # This should raise an error
    with pytest.raises(TypeError):
        del DummyEnum.FOO  # type: ignore  # This should raise an error

    # Test try_enum functionality
    valid_value = "foo"
    invalid_value = "invalid"

    valid_instance = try_enum(DummyEnum, valid_value)
    assert valid_instance == DummyEnum.FOO
    assert valid_instance.value == valid_value
    assert isinstance(valid_instance, DummyEnum)

    invalid_instance = try_enum(DummyEnum, invalid_value)
    assert invalid_instance.name == f"UNKNOWN_{invalid_value}"
    assert invalid_instance.value == invalid_value
    assert isinstance(invalid_instance, DummyEnum)

    # Test string representations
    assert str(DummyEnum.FOO) == "DummyEnum.FOO"
    assert repr(DummyEnum.FOO) == "<DummyEnum.FOO: 'foo'>"
    assert repr(DummyEnum) == "<enum DummyEnum>"

    # Test members property
    assert DummyEnum.__members__ == {"FOO": DummyEnum.FOO, "BAR": DummyEnum.BAR, "BAZ": DummyEnum.BAZ}
