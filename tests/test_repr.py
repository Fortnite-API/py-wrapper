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

from __future__ import annotations

from fortnite_api.utils import simple_repr


@simple_repr
class Foo:
    __slots__: tuple[str, ...] = ('foo', 'bar', 'baz')

    def __init__(self, foo: int, bar: int, baz: int) -> None:
        self.foo = foo
        self.bar = bar
        self.baz = baz


@simple_repr
class Bar(Foo):
    __slots__: tuple[str, ...] = ('buz',)

    def __init__(self, foo: int, bar: int, baz: int, buz: int) -> None:
        super().__init__(foo, bar, baz)
        self.buz: int = buz


def test_simple_repr() -> None:
    foo = Foo(1, 2, 3)

    assert getattr(foo, '__repr__')() == '<Foo foo=1, bar=2, baz=3>'


def test_simple_repr_inheritance() -> None:
    bar = Bar(1, 2, 3, 4)

    assert getattr(bar, '__repr__')() == '<Bar buz=4, foo=1, bar=2, baz=3>'
