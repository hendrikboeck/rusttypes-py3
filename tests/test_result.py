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

import math
from dataclasses import dataclass

from rusttypes.option import Nil, Some
from rusttypes.result import Result, Ok, Err, catch, try_guard


@dataclass
class Foo:
    x: int

    @staticmethod
    def default() -> Foo:
        return Foo(42)


def test_is_ok():
    x = Ok(-3)
    assert x.is_ok() is True

    x = Err("Some error message")
    assert x.is_ok() is False


def test_is_ok_and():
    x = Ok(2)
    assert x.is_ok_and(lambda x: x > 1) is True

    x = Ok(0)
    assert x.is_ok_and(lambda x: x > 1) is False

    x = Err("Some error message")
    assert x.is_ok_and(lambda x: x > 1) is False


def test_is_err():
    x = Ok(-3)
    assert x.is_err() is False

    x = Err("Some error message")
    assert x.is_err() is True


def test_is_err_and():
    x = Err("Some error message")
    assert x.is_err_and(lambda x: x == "Some error message") is True

    x = Err("Some error message")
    assert x.is_err_and(lambda x: x == "Some other message") is False

    x = Ok(123)
    assert x.is_err_and(lambda x: x == "Some error message") is False


def test_ok():
    x = Ok(2)
    assert x.ok() == Some(2)

    x = Err("Some error message")
    assert x.ok() == Nil


def test_err():
    x = Ok(2)
    assert x.err() == Nil

    x = Err("Some error message")
    assert x.err() == Some("Some error message")


def test_map():
    x = Ok(2)
    assert x.map(lambda x: x + 1) == Ok(3)

    x = Err("Some error message")
    assert x.map(lambda x: x + 1) == Err("Some error message")


def test_map_or():
    x = Ok("foo")
    assert x.map_or(42, lambda v: len(v)) == 3

    x = Err("bar")
    assert x.map_or(42, lambda v: len(v)) == 42


def test_map_or_else():
    k = 21

    x = Ok("foo")
    assert x.map_or_else(lambda _: k * 2, lambda v: len(v)) == 3

    x = Err("bar")
    assert x.map_or_else(lambda _: k * 2, lambda v: len(v)) == 42


def test_map_err():
    def stringify(x: int) -> str:
        return f"error code {x}"

    x = Ok(2)
    assert x.map_err(stringify) == Ok(2)

    x = Err(13)
    assert x.map_err(stringify) == Err("error code 13")


def test_inspect():
    def is_two(x: int) -> None:
        assert x == 2

    x = Ok(2)
    assert x.inspect(is_two) == Ok(2)

    x = Err("Some error message")
    assert x.inspect(is_two) == Err("Some error message")


def test_inspect_err():
    def is_err(x: str) -> None:
        assert x == "Some error message"

    x = Err("Some error message")
    assert x.inspect_err(is_err) == Err("Some error message")

    x = Ok()
    assert x.inspect_err(is_err) == Ok()


def test_expect():
    x = Ok(2)
    assert x.expect("Should not panic") == 2

    x = Err("Some error message")
    try:
        x.expect("Should panic")
    except RuntimeError as e:
        assert str(e) == "Should panic"


def test_unwrap():
    x = Ok(2)
    assert x.unwrap() == 2

    x = Err("Some error message")
    try:
        x.unwrap()
    except RuntimeError as e:
        assert str(e) == "Called unwrap on Err"


def test_unwrap_or_default():
    x = Ok(Foo(2))
    assert x.unwrap_or_default(Foo).x == 2

    x = Err[Foo, str]("Some error message")
    assert x.unwrap_or_default(Foo).x == 42


def test_expect_err():
    x = Err("Some error message")
    assert x.expect_err("Should not panic") == "Some error message"

    x = Ok()
    try:
        x.expect_err("Should panic")
    except RuntimeError as e:
        assert str(e) == "Should panic"


def test_unwrap_err():
    x = Err("Some error message")
    assert x.unwrap_err() == "Some error message"

    x = Ok()
    try:
        x.unwrap_err()
    except RuntimeError as e:
        assert str(e) == "Called unwrap_err on Ok"


def test_and():
    x = Ok(2)
    y = Err("late error")
    assert x.and_(y) == Err("late error")

    x = Err("early error")
    y = Ok("foo")
    assert x.and_(y) == Err("early error")

    x = Err("not a 2")
    y = Err("late error")
    assert x.and_(y) == Err("not a 2")

    x = Ok(2)
    y = Ok("different result type")
    assert x.and_(y) == Ok("different result type")


def test_and_then():
    def sq_then_to_string(x: int) -> Result[str, str]:
        if x < 1_000_000 and x > -1_000_000:
            return Ok(str(x * x))
        return Err("overflow")

    assert Ok(2).and_then(sq_then_to_string) == Ok("4")
    assert Ok(1_000_000).and_then(sq_then_to_string) == Err("overflow")
    assert Err("not a number").and_then(sq_then_to_string) == Err("not a number")


def test_or():
    x = Ok(2)
    y = Err("late error")
    assert x.or_(y) == Ok(2)

    x = Err("early error")
    y = Ok(2)
    assert x.or_(y) == Ok(2)

    x = Ok(2)
    y = Ok(100)
    assert x.or_(y) == Ok(2)

    x = Err("early error")
    y = Err("late error")
    assert x.or_(y) == Err("late error")


def test_or_else():
    def sq(x: int) -> Result[int, int]:
        return Ok(x * x)

    def err(x: int) -> Result[int, int]:
        return Err(x)

    assert Ok(2).or_else(sq).or_else(sq) == Ok(2)
    assert Ok(2).or_else(err).or_else(sq) == Ok(2)
    assert Err(3).or_else(sq).or_else(err) == Ok(9)
    assert Err(3).or_else(err).or_else(err) == Err(3)


def test_unwrap_or():
    default = 2

    x = Ok(9)
    assert x.unwrap_or(default) == 9

    x = Err("error")
    assert x.unwrap_or(default) == default


def test_unwrap_or_else():
    def count(x: str) -> int:
        return len(x)

    assert Ok(2).unwrap_or_else(count) == 2
    assert Err("foo").unwrap_or_else(count) == 3


def test_unwrap_unchecked():
    x = Ok(2)
    assert x.unwrap_unchecked() == 2

    x = Err("Some error message")
    try:
        x.unwrap_unchecked()
    except RuntimeError as e:
        assert str(e) == "Called unwrap_unchecked on Err"


def test_unwrap_err_unchecked():
    x = Err("Some error message")
    assert x.unwrap_err_unchecked() == "Some error message"

    x = Ok(2)
    try:
        x.unwrap_err_unchecked()
    except RuntimeError as e:
        assert str(e) == "Called unwrap_err_unchecked on Ok"


def test_catch():
    @catch()
    def raise_runtime_error(x: int) -> Result[int, str]:
        if x < 0:
            raise ValueError("x must be positive")
        raise RuntimeError("Some error message")

    assert raise_runtime_error(0) == Err("Some error message")
    assert raise_runtime_error(-1) == Err("x must be positive")

    @catch(RuntimeError, ValueError)
    def raise_runtime_error_2(x: int) -> Result[int, str]:
        if x < 0:
            raise ValueError("x must be positive")
        raise RuntimeError("Some error message")

    assert raise_runtime_error_2(0) == Err("Some error message")
    assert raise_runtime_error_2(-1) == Err("x must be positive")

    @catch(RuntimeError, map_err=lambda _: "runtime error")
    def raise_runtime_error_3() -> Result[int, str]:
        raise RuntimeError("Some error message")

    assert raise_runtime_error_3() == Err("runtime error")

    @catch(RuntimeError)
    def raise_value_error() -> Result[int, str]:
        raise ValueError("Some error message")

    try:
        raise_value_error()
    except ValueError as e:
        assert str(e) == "Some error message"


def test_try_guard():
    def pos(x: float) -> Result[float, str]:
        return Ok(x) if x >= 0 else Err("x must be positive")

    @try_guard
    def sqrt(x: float) -> Result[float, str]:
        x = pos(x).try_()
        return Ok(math.sqrt(x))

    assert sqrt(4.0) == Ok(2.0)
    assert sqrt(-1.0) == Err("x must be positive")

    @try_guard
    def sqrt_map_err(x: float) -> Result[float, float]:
        x = pos(x).map_err(lambda _: x).try_()
        return Ok(math.sqrt(x))

    assert sqrt_map_err(4.0) == Ok(2.0)
    assert sqrt_map_err(-1.0) == Err(-1.0)
