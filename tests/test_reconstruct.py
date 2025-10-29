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

from typing import TypedDict

import fortnite_api
from fortnite_api.abc import ReconstructAble
from fortnite_api.http import HTTPClient


class DummyData(TypedDict):
    id: str


class DummyReconstruct(ReconstructAble[DummyData, HTTPClient]):
    def __init__(self, *, data: DummyData, http: HTTPClient) -> None:
        super().__init__(data=data, http=http)
        self.id: str = data['id']

    def __eq__(self, value: object) -> bool:
        return isinstance(value, DummyReconstruct) and self.id == value.id

    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)


def test_dummy_reconstruction() -> None:
    data: DummyData = {'id': '1'}

    client = fortnite_api.Client()
    http: HTTPClient = client.http
    dummy = DummyReconstruct(data=data, http=http)

    deconstructed = dummy.to_dict()
    reconstructed = DummyReconstruct.from_dict(deconstructed, client=client)

    assert dummy == reconstructed
    assert dummy.to_dict() == reconstructed.to_dict()
    assert dummy.to_dict() == deconstructed
    assert type(dummy) is type(reconstructed)
    assert isinstance(reconstructed, DummyReconstruct)
