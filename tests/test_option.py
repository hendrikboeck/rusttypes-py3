# Copyright (c) 2024, Hendrik Böck <hendrikboeck.dev@protonmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

from dataclasses import dataclass
from types import NoneType
from typing import Type, TypeVar

from rusttypes.option import Option, Nil, Some, to_option
from rusttypes.result import Err, Ok
from rusttypes.traits import Default

T = TypeVar("T")


@dataclass
class Foo(Default):
    x: int

    @classmethod
    def default(cls: Type[T]) -> T:
        return cls(42)


def test_eq():
    assert Nil == None
    assert Nil == Nil
    assert Nil is Nil
    assert Nil != Some(1)

    assert Some(1) == Some(1)
    assert Some(1) != Some(2)


def test_repr():
    assert repr(Nil) == "Nil"
    assert repr(Some(1)) == "Some(1)"
    assert repr(Some(Nil)) == "Some(Nil)"


def test_str():
    assert str(Nil) == "Nil"
    assert str(Some(1)) == "Some(1)"
    assert str(Some(Nil)) == "Some(Nil)"


def test_bool():
    assert not Nil
    assert Some(1)
    assert Some(Nil)


def test_as_optional():
    assert Nil.as_optional() is None
    assert Some(1).as_optional() == 1
    assert Some(Nil).as_optional() is Nil


def test_to_option():
    assert to_option(None) is Nil
    assert to_option(1) == Some(1)
    assert to_option(Nil) == Some(Nil)


def test_is_some():
    assert not Nil.is_some()
    assert Some(1).is_some()
    assert Some(Nil).is_some()


def test_is_some_and():
    assert Nil.is_some_and(lambda x: x > 1) == False
    assert Some(2).is_some_and(lambda x: x > 1) == True
    assert Some(0).is_some_and(lambda x: x == 1) == False


def test_is_nil():
    assert Nil.is_nil()
    assert not Some(1).is_nil()
    assert not Some(Nil).is_nil()


def test_expect():
    assert Some(1).expect("error") == 1

    try:
        Nil.expect("error")
        assert False
    except RuntimeError as e:
        assert str(e) == "error"


def test_unwrap():
    assert Some(1).unwrap() == 1

    try:
        Nil.unwrap()
        assert False
    except RuntimeError as e:
        assert str(e) == "Called unwrap on a Nil value"


def test_unwrap_or():
    assert Some(1).unwrap_or(2) == 1
    assert Nil.unwrap_or(2) == 2


def test_unwrap_or_else():
    k = 10

    assert Some(4).unwrap_or_else(lambda: 2 * k) == 4
    assert Nil.unwrap_or_else(lambda: 2 * k) == 20


def test_unwrap_or_default():

    bar = Some(Foo(10))
    baz = Nil

    assert bar.unwrap_or_default(Foo).x == 10
    assert baz.unwrap_or_default(Foo).x == 42


def test_unwrap_unchecked():
    assert Some(1).unwrap_unchecked() == 1

    try:
        Nil.unwrap_unchecked()
        assert False
    except RuntimeError as e:
        assert str(e) == "Called unwrap_unchecked on a Nil value"


def test_map():
    x = Some("Hello, World!")

    assert x.map(lambda v: len(v)) == Some(13)
    assert Nil.map(lambda v: len(v)) == Nil


def test_inspect():
    x = Some(1)

    def f(v):
        assert v == 1

    assert x.inspect(f) == Some(1)
    assert Nil.inspect(f) == Nil


def test_map_or():
    x = Some("foo")

    assert x.map_or(42, lambda v: len(v)) == 3
    assert Nil.map_or(42, lambda v: len(v)) == 42


def test_map_or_else():
    k = 21
    x = Some("foo")

    assert x.map_or_else(lambda: 2 * k, lambda v: len(v)) == 3
    assert Nil.map_or_else(lambda: 2 * k, lambda v: len(v)) == 42


def test_ok_or():
    x = Some("foo")

    assert x.ok_or(0) == Ok("foo")
    assert Nil.ok_or(0) == Err(0)


def test_ok_or_else():
    x = Some("foo")

    assert x.ok_or_else(lambda: 0) == Ok("foo")
    assert Nil.ok_or_else(lambda: 0) == Err(0)


def test_and():
    assert Some(2).and_(Nil) == Nil
    assert Nil.and_(Some("foo")) == Nil
    assert Some(2).and_(Some("foo")) == Some("foo")
    assert Nil.and_(Nil) == Nil


def test_and_then():

    def sq_then_to_str(x: int) -> Option[str]:
        if x >= 1_000_000 or x <= -1_000_000:
            return Nil
        return Some(x**2).map(str)

    assert Some(2).and_then(sq_then_to_str) == Some("4")
    assert Some(1_000_000).and_then(sq_then_to_str) == Nil
    assert Nil.and_then(sq_then_to_str) == Nil


def test_filter():

    def is_even(x: int) -> bool:
        return x % 2 == 0

    assert Some(4).filter(is_even) == Some(4)
    assert Some(3).filter(is_even) == Nil
    assert Nil.filter(is_even) == Nil


def test_or():
    assert Some(2).or_(Nil) == Some(2)
    assert Nil.or_(Some(100)) == Some(100)
    assert Some(2).or_(Some(100)) == Some(2)
    assert Nil.or_(Nil) == Nil


def test_or_else():

    def nobody() -> Option[str]:
        return Nil

    def vikings() -> Option[str]:
        return Some("vikings")

    assert Some("barbarians").or_else(vikings) == Some("barbarians")
    assert Nil.or_else(vikings) == Some("vikings")
    assert Nil.or_else(nobody) == Nil


def test_xor():
    assert Some(2).xor(Nil) == Some(2)
    assert Nil.xor(Some(2)) == Some(2)
    assert Some(2).xor(Some(2)) == Nil
    assert Nil.xor(Nil) == Nil


def test_insert():
    x = Nil
    x = x.insert(1)

    assert x == Some(1)

    x = x.insert(2)
    assert x == Some(2)


def test_get_or_insert():
    x = Nil
    x = x.get_or_insert(1)
    assert x.unwrap() == 1

    x = x.get_or_insert(2)
    assert x.unwrap() == 1


def get_or_insert_default():
    x = Nil
    x = x.get_or_insert_default(Foo)
    assert x.unwrap().x == 42

    x = x.get_or_insert_default(Foo)
    assert x.unwrap().x == 42


def test_get_or_insert_with():
    x = Nil
    x = x.get_or_insert_with(lambda: 1)
    assert x.unwrap() == 1

    x = x.get_or_insert_with(lambda: 2)
    assert x.unwrap() == 1


def test_take():
    x = Some(1)
    x, y = x.take()
    assert x == Nil
    assert y == Some(1)

    x = Nil
    x, y = x.take()
    assert x == Nil
    assert y == Nil


def test_replace():
    x = Some(2)
    x, old = x.replace(3)
    assert x == Some(3)
    assert old == Some(2)

    x = Nil
    x, old = x.replace(3)
    assert x == Some(3)
    assert old == Nil


def test_zip():
    x = Some(42)
    y = Some("foo")
    z = Nil

    assert x.zip(y) == Some((42, "foo"))
    assert x.zip(z) == Nil
    assert z.zip(x) == Nil
    assert z.zip(y) == Nil
    assert z.zip(z) == Nil


def test_zip_with():

    @dataclass
    class Foo:
        x: float
        y: float

    x = Some(3.14)
    y = Some(42.0)

    assert x.zip_with(y, Foo) == Some(Foo(3.14, 42.0))
    assert x.zip_with(Nil, Foo) == Nil


def test_unzip():
    x = Some((42, "foo"))
    y = Nil

    assert x.unzip() == (Some(42), Some("foo"))
    assert y.unzip() == (Nil, Nil)

    x = Some(42)
    try:
        x.unzip()
        assert False
    except ValueError as e:
        assert str(e) == "Can not unzip non-tuple type"

    x = Some((42, "foo", "bar"))
    try:
        x.unzip()
        assert False
    except ValueError as e:
        assert str(e) == "Can not unzip tuple with more/less than 2 elements"

    x = Some((42,))
    try:
        x.unzip()
        assert False
    except ValueError as e:
        assert str(e) == "Can not unzip tuple with more/less than 2 elements"


def test_transpose():
    assert Nil.transpose() == Ok(Nil)
    assert Some(Ok(42)).transpose() == Ok(Some(42))
    assert Some(Err(42)).transpose() == Err(42)


def test_flatten():
    assert Nil.flatten() == Nil
    assert Some(Some(42)).flatten() == Some(42)
    assert Some(Nil).flatten() == Nil
