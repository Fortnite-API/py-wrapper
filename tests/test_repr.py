from typing import Tuple
from fortnite_api.utils import simple_repr


@simple_repr
class Foo:
    __slots__: Tuple[str, ...] = ('foo', 'bar', 'baz')

    def __init__(self, foo: int, bar: int, baz: int) -> None:
        self.foo = foo
        self.bar = bar
        self.baz = baz


@simple_repr
class Bar(Foo):
    __slots__: Tuple[str, ...] = ('buz',)

    def __init__(self, foo: int, bar: int, baz: int, buz: int) -> None:
        super().__init__(foo, bar, baz)
        self.buz: int = buz


def test_simple_repr() -> None:
    foo = Foo(1, 2, 3)

    assert getattr(foo, '__repr__')() == '<Foo foo=1, bar=2, baz=3>'


def test_simple_repr_inheritance() -> None:
    bar = Bar(1, 2, 3, 4)

    assert getattr(bar, '__repr__')() == '<Bar buz=4, foo=1, bar=2, baz=3>'
