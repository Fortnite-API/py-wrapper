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

import dataclasses
from typing import Dict, List

from fortnite_api.proxies import TransformerListProxy


@dataclasses.dataclass(frozen=True, eq=True)
class PlaceholderPerson:
    name: str


def test_proxy():
    # A random list of people
    people_raw_data: List[Dict[str, str]] = [
        dict(name="Daniel Maxwell"),
        dict(name="Francis Andrews"),
        dict(name="Stella Norton"),
        dict(name="Nathaniel Reeves"),
    ]

    people: List[PlaceholderPerson] = [PlaceholderPerson(**person) for person in people_raw_data]

    proxy = TransformerListProxy(people_raw_data, transform_data=lambda data: PlaceholderPerson(**data))

    assert len(proxy) == len(people)

    first = people[0]
    assert first in people

    for i, person in enumerate(proxy):
        assert isinstance(person, PlaceholderPerson)
        assert isinstance(proxy[i], PlaceholderPerson)
        assert person == proxy[i]

        assert proxy[i] == person
        assert proxy[i] == people[i]

    # Ensure slicing is right
    assert people[1:3] == proxy[1:3]
    assert people[1:] == proxy[1:]

    # Slicing with step
    assert people[::2] == proxy[::2]

    # Adding
    assert people + people == proxy + proxy

    # Check that the proxy is reversible
    reversed_people = list(reversed(people))
    for i, person in enumerate(reversed(proxy)):
        assert isinstance(person, PlaceholderPerson)
        assert isinstance(proxy[-i - 1], PlaceholderPerson)
        assert person == proxy[-i - 1]

        assert proxy[-i - 1] == person
        assert proxy[-i - 1] == reversed_people[i]
