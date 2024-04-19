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

from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Callable, Generic, Type, TypeVar

from . import option as o
from .traits import Default
from .misc import panic, stringify

T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")
F = TypeVar("F")


class ResultException(Exception, Generic[E]):

    inner: E

    def __init__(self, inner: E):
        self.inner = inner

    def __str__(self):
        return f"ResultException({self.inner})"


class Result(ABC, Generic[T, E]):

    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError

    @abstractmethod
    def __str__(self):
        raise NotImplementedError

    @abstractmethod
    def is_ok(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_ok_and(self, f: Callable[[T], bool]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_err(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_err_and(self, f: Callable[[E], bool]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def ok(self) -> o.Option[T]:
        raise NotImplementedError

    @abstractmethod
    def err(self) -> o.Option[E]:
        raise NotImplementedError

    @abstractmethod
    def map(self, op: Callable[[T], U]) -> Result[U, E]:
        raise NotImplementedError

    @abstractmethod
    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        raise NotImplementedError

    @abstractmethod
    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        raise NotImplementedError

    @abstractmethod
    def map_err(self, op: Callable[[E], F]) -> Result[T, F]:
        raise NotImplementedError

    @abstractmethod
    def inspect(self, op: Callable[[T], None]) -> Result[T, E]:
        raise NotImplementedError

    @abstractmethod
    def inspect_err(self, op: Callable[[E], None]) -> Result[T, E]:
        raise NotImplementedError

    @abstractmethod
    def expect(self, msg: str) -> T:
        raise NotImplementedError

    @abstractmethod
    def unwrap(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def unwrap_or_default(self, t: Type[T]) -> T:
        raise NotImplementedError

    @abstractmethod
    def expect_err(self, msg: str) -> E:
        raise NotImplementedError

    @abstractmethod
    def unwrap_err(self) -> E:
        raise NotImplementedError

    @abstractmethod
    def and_(self, res: Result[U, E]) -> Result[U, E]:
        raise NotImplementedError

    @abstractmethod
    def and_then(self, op: Callable[[T], Result[U, E]]) -> Result[U, E]:
        raise NotImplementedError

    @abstractmethod
    def or_(self, res: Result[T, F]) -> Result[T, F]:
        raise NotImplementedError

    @abstractmethod
    def or_else(self, op: Callable[[E], Result[T, F]]) -> Result[T, F]:
        raise NotImplementedError

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        raise NotImplementedError

    @abstractmethod
    def unwrap_unchecked(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def unwrap_err_unchecked(self) -> E:
        raise NotImplementedError

    @abstractmethod
    def try_(self) -> T:
        raise NotImplementedError


class Ok(Result, Generic[T, E]):

    inner: T

    def __init__(self, inner: T = None):
        self.inner = inner

    def __eq__(self, other):
        return isinstance(other, Ok) and self.inner == other.inner

    def __repr__(self):
        return f"Ok({self.inner})"

    def __str__(self):
        return f"Ok({self.inner})"

    def is_ok(self) -> bool:
        return True

    def is_ok_and(self, f: Callable[[T], bool]) -> bool:
        return f(self.inner)

    def is_err(self) -> bool:
        return False

    def is_err_and(self, f: Callable[[E], bool]) -> bool:
        return False

    def ok(self) -> o.Option[T]:
        return o.Some(self.inner)

    def err(self) -> o.Option[E]:
        return o.Nil

    def map(self, op: Callable[[T], U]) -> Result[U, E]:
        return Ok[U, E](op(self.inner))

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return f(self.inner)

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        return f(self.inner)

    def map_err(self, op: Callable[[E], F]) -> Result[T, F]:
        return Ok[T, F](self.inner)

    def inspect(self, op: Callable[[T], None]) -> Result[T, E]:
        op(self.inner)
        return self

    def inspect_err(self, op: Callable[[E], None]) -> Result[T, E]:
        return self

    def expect(self, msg: str) -> T:
        return self.inner

    def unwrap(self) -> T:
        return self.inner

    def unwrap_or_default(self, t: Type[T]) -> T:
        return self.inner

    def expect_err(self, msg: str) -> E:
        panic(msg)

    def unwrap_err(self) -> E:
        panic("Called unwrap_err on Ok")

    def and_(self, res: Result[U, E]) -> Result[U, E]:
        return res

    def and_then(self, op: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return op(self.inner)

    def or_(self, res: Result[T, F]) -> Result[T, F]:
        return Ok[T, F](self.inner)

    def or_else(self, op: Callable[[E], Result[T, F]]) -> Result[T, F]:
        return Ok[T, F](self.inner)

    def unwrap_or(self, default: T) -> T:
        return self.inner

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        return self.inner

    def unwrap_unchecked(self) -> T:
        return self.inner

    def unwrap_err_unchecked(self) -> E:
        panic("Called unwrap_err_unchecked on Ok")

    def try_(self) -> T:
        return self.inner


class Err(Result, Generic[T, E]):

    inner: E

    def __init__(self, inner: E):
        self.inner = inner

    def __eq__(self, other):
        return isinstance(other, Err) and self.inner == other.inner

    def __repr__(self):
        return f"Err({self.inner})"

    def __str__(self):
        return f"Err({self.inner})"

    def is_ok(self) -> bool:
        return False

    def is_ok_and(self, f: Callable[[T], bool]) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def is_err_and(self, f: Callable[[E], bool]) -> bool:
        return f(self.inner)

    def ok(self) -> o.Option[T]:
        return o.Nil

    def err(self) -> o.Option[E]:
        return o.Some(self.inner)

    def map(self, op: Callable[[T], U]) -> Result[U, E]:
        return Err[U, E](self.inner)

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return default

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        return default(self.inner)

    def map_err(self, op: Callable[[E], F]) -> Result[T, F]:
        return Err[T, F](op(self.inner))

    def inspect(self, op: Callable[[T], None]) -> Result[T, E]:
        return self

    def inspect_err(self, op: Callable[[E], None]) -> Result[T, E]:
        op(self.inner)
        return self

    def expect(self, msg: str) -> T:
        panic(msg)

    def unwrap(self) -> T:
        panic("Called unwrap on Err")

    def unwrap_or_default(self, t: Type[T]) -> T:
        if issubclass(t, Default):
            return t.default()
        panic("Called unwrap_or_default on Err without Default bound")

    def expect_err(self, msg: str) -> E:
        return self.inner

    def unwrap_err(self) -> E:
        return self.inner

    def and_(self, res: Result[U, E]) -> Result[U, E]:
        return Err[U, E](self.inner)

    def and_then(self, op: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return Err[U, E](self.inner)

    def or_(self, res: Result[T, F]) -> Result[T, F]:
        return res

    def or_else(self, op: Callable[[E], Result[T, F]]) -> Result[T, F]:
        return op(self.inner)

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        return op(self.inner)

    def unwrap_unchecked(self) -> T:
        panic("Called unwrap_unchecked on Err")

    def unwrap_err_unchecked(self) -> E:
        return self.inner

    def try_(self) -> T:
        raise ResultException(self.inner)


#
#  --- DECORATORS ---
#

Fn = Callable[..., Result[T, E]]


def catch(*exceptions: Type[BaseException], map_err: Callable[[BaseException], E] = stringify) -> Callable[[Fn], Fn]:
    if len(exceptions) <= 0:
        exceptions = (BaseException,)

    def decorator(fn: Fn) -> Fn:

        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Result[T, E]:
            try:
                return fn(*args, **kwargs)
            except exceptions as e:
                return Err(map_err(e))

        return wrapper

    return decorator


def try_guard(fn: Fn) -> Fn:

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Result[T, E]:
        try:
            return fn(*args, **kwargs)
        except ResultException as e:
            return Err(e.inner)

    return wrapper
