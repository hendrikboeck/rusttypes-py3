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
from typing import Any, Callable, Generic, List, Optional, Tuple, Type, TypeVar, final, Final

from . import result as r
from .traits import Default

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")
R = TypeVar("R")


class Option(ABC, Generic[T]):

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
    def __bool__(self):
        raise NotImplementedError

    @abstractmethod
    def as_optional(self) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def is_some(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_some_and(self, f: Callable[[T], bool]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_none(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def expect(self, msg: str) -> T:
        raise NotImplementedError

    @abstractmethod
    def unwrap(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        raise NotImplementedError

    @abstractmethod
    def unwrap_or_default(self, t: Type[T]) -> T:
        raise NotImplementedError

    @abstractmethod
    def unwrap_unchecked(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def map(self, f: Callable[[T], U]) -> Option[U]:
        raise NotImplementedError

    @abstractmethod
    def inspect(self, f: Callable[[T], None]) -> Option[T]:
        raise NotImplementedError

    @abstractmethod
    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        raise NotImplementedError

    @abstractmethod
    def map_or_else(self, default: Callable[[], U], f: Callable[[T], U]) -> U:
        raise NotImplementedError

    @abstractmethod
    def ok_or(self, err: E) -> r.Result[T, E]:
        raise NotImplementedError

    @abstractmethod
    def ok_or_else(self, f: Callable[[], E]) -> r.Result[T, E]:
        raise NotImplementedError

    @abstractmethod
    def and_(self, optb: Option[U]) -> Option[U]:
        raise NotImplementedError

    @abstractmethod
    def and_then(self, f: Callable[[T], Option[U]]) -> Option[U]:
        raise NotImplementedError

    @abstractmethod
    def filter(self, f: Callable[[T], bool]) -> Option[T]:
        raise NotImplementedError

    @abstractmethod
    def or_(self, optb: Option[T]) -> Option[T]:
        raise NotImplementedError

    @abstractmethod
    def or_else(self, f: Callable[[], Option[T]]) -> Option[T]:
        raise NotImplementedError

    @abstractmethod
    def xor(self, optb: Option[T]) -> Option[T]:
        raise NotImplementedError

    @abstractmethod
    def insert(self, value: T) -> Some[T]:
        raise NotImplementedError

    @abstractmethod
    def get_or_insert(self, value: T) -> Some[T]:
        raise NotImplementedError

    @abstractmethod
    def get_or_insert_default(self, t: Type[T]) -> Some[T]:
        raise NotImplementedError

    @abstractmethod
    def get_or_insert_with(self, f: Callable[[], T]) -> Some[T]:
        raise NotImplementedError

    @abstractmethod
    def take(self) -> Tuple[NilType, Option[T]]:
        raise NotImplementedError

    @abstractmethod
    def replace(self, value: T) -> Tuple[Option[T], Option[T]]:
        raise NotImplementedError

    @abstractmethod
    def zip(self, other: Option[U]) -> Option[Tuple[T, U]]:
        raise NotImplementedError

    @abstractmethod
    def zip_with(self, other: Option[U], f: Callable[[ T, U ], R]) -> Option[R]:
        raise NotImplementedError

    @abstractmethod
    def unzip(self) -> Tuple[Option[Any], Option[Any]]:
        raise NotImplementedError

    @abstractmethod
    def transpose(self) -> r.Result[Option[T], Any]:
        raise NotImplementedError

    @abstractmethod
    def flatten(self) -> Option[T]:
        raise NotImplementedError


class Some(Option, Generic[T]):

    inner: T

    def __init__(self, inner: T) -> None:
        self.inner = inner

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Some) and self.inner == other.inner

    def __repr__(self) -> str:
        return f"Some({self.inner})"

    def __str__(self) -> str:
        return f"Some({self.inner})"

    def __bool__(self) -> bool:
        return True

    def as_optional(self) -> Optional[T]:
        return self.inner

    def is_some(self) -> bool:
        return True

    def is_some_and(self, f: Callable[[T], bool]) -> bool:
        return f(self.inner)

    def is_none(self) -> bool:
        return False

    def expect(self, msg: str) -> T:
        return self.inner

    def unwrap(self) -> T:
        return self.inner

    def unwrap_or(self, default: T) -> T:
        return self.inner

    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        return self.inner

    def unwrap_or_default(self, t: Type[T]) -> T:
        return self.inner

    def unwrap_unchecked(self) -> T:
        return self.inner

    def map(self, f: Callable[[T], U]) -> Option[U]:
        return Some(f(self.inner))

    def inspect(self, f: Callable[[T], None]) -> Option[T]:
        f(self.inner)
        return self

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return f(self.inner)

    def map_or_else(self, default: Callable[[], U], f: Callable[[T], U]) -> U:
        return f(self.inner)

    def ok_or(self, err: E) -> r.Result[T, E]:
        return r.Ok(self.inner)

    def ok_or_else(self, f: Callable[[], E]) -> r.Result[T, E]:
        return r.Ok(self.inner)

    def and_(self, optb: Option[U]) -> Option[U]:
        return optb

    def and_then(self, f: Callable[[T], Option[U]]) -> Option[U]:
        return f(self.inner)

    def filter(self, f: Callable[[T], bool]) -> Option[T]:
        return self if f(self.inner) else Nil

    def or_(self, optb: Option[T]) -> Option[T]:
        return self

    def or_else(self, f: Callable[[], Option[T]]) -> Option[T]:
        return self

    def xor(self, optb: Option[T]) -> Option[T]:
        return Nil if optb.is_some() else self

    def insert(self, value: T) -> Some[T]:
        self.inner = value
        return self

    def get_or_insert(self, value: T) -> Some[T]:
        return self

    def get_or_insert_default(self, t: Type[T]) -> Some[T]:
        return self

    def get_or_insert_with(self, f: Callable[[], T]) -> Some[T]:
        return self

    def take(self) -> Tuple[NilType, Option[T]]:
        return Nil, Some(self.inner)

    def replace(self, value: T) -> Tuple[Option[T], Option[T]]:
        ret = self.inner
        self.inner = value
        return self, Some(ret)

    def zip(self, other: Option[U]) -> Option[Tuple[T, U]]:
        return other.map(lambda v: (self.inner, v))

    def zip_with(self, other: Option[U], f: Callable[[ T, U ], R]) -> Option[R]:
        return other.map(lambda v: f(self.inner, v))

    def unzip(self) -> Tuple[Option[Any], Option[Any]]:
        if not isinstance(self.inner, (Tuple, List)):
            raise ValueError("Can not unzip non-tuple type")
        if len(self.inner) != 2:
            raise ValueError("Can not unzip tuple with more/less than 2 elements")

        return Some(self.inner[0]), Some(self.inner[1])

    def transpose(self) -> r.Result[Option[T], Any]:
        if not isinstance(self.inner, r.Result):
            raise ValueError("Can not transpose if .inner is non-result type")

        if self.inner.is_ok():
            return r.Ok(Some(self.inner.unwrap()))

        return r.Err(self.inner.unwrap_err())

    def flatten(self) -> Option[T]:
        if not isinstance(self.inner, Option):
            raise ValueError("Can not flatten if .inner is non-option type")

        return self.inner


@final
class NilType(Option, Generic[T]):

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, NilType) or other is None

    def __repr__(self) -> str:
        return "Nil"

    def __str__(self) -> str:
        return "Nil"

    def __bool__(self):
        return False

    def as_optional(self) -> Optional[T]:
        return None

    def is_some(self) -> bool:
        return False

    def is_some_and(self, f: Callable[[T], bool]) -> bool:
        return False

    def is_none(self) -> bool:
        return True

    def expect(self, msg: str) -> T:
        raise RuntimeError(msg)

    def unwrap(self) -> T:
        raise RuntimeError("Called unwrap on a Nil value")

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        return f()

    def unwrap_or_default(self, t: Type[T]) -> T:
        if not issubclass(t, Default):
            raise ValueError("Can not unwrap_or_default on non-Default type")

        return t.default()

    def unwrap_unchecked(self) -> T:
        raise RuntimeError("Called unwrap_unchecked on a Nil value")

    def map(self, f: Callable[[T], U]) -> Option[U]:
        return Nil

    def inspect(self, f: Callable[[T], None]) -> Option[T]:
        return Nil

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return default

    def map_or_else(self, default: Callable[[], U], f: Callable[[T], U]) -> U:
        return default()

    def ok_or(self, err: E) -> r.Result[T, E]:
        return r.Err(err)

    def ok_or_else(self, f: Callable[[], E]) -> r.Result[T, E]:
        return r.Err(f())

    def and_(self, optb: Option[U]) -> Option[U]:
        return Nil

    def and_then(self, f: Callable[[T], Option[U]]) -> Option[U]:
        return Nil

    def filter(self, f: Callable[[T], bool]) -> Option[T]:
        return Nil

    def or_(self, optb: Option[T]) -> Option[T]:
        return optb

    def or_else(self, f: Callable[[], Option[T]]) -> Option[T]:
        return f()

    def xor(self, optb: Option[T]) -> Option[T]:
        return optb

    def insert(self, value: T) -> Some[T]:
        return Some(value)

    def get_or_insert(self, value: T) -> Some[T]:
        return Some(value)

    def get_or_insert_default(self, t: Type[T]) -> Some[T]:
        if not issubclass(t, Default):
            raise ValueError("Can not get_or_insert_default on non-Default type")

        return Some(t.default())

    def get_or_insert_with(self, f: Callable[[], T]) -> Some[T]:
        return Some(f())

    def take(self) -> Tuple[NilType, Option[T]]:
        return Nil, Nil

    def replace(self, value: T) -> Tuple[Option[T], Option[T]]:
        return Some(value), Nil

    def zip(self, other: Option[U]) -> Option[Tuple[T, U]]:
        return Nil

    def zip_with(self, other: Option[U], f: Callable[[ T, U ], R]) -> Option[R]:
        raise NotImplementedError

    def unzip(self) -> Tuple[Option[Any], Option[Any]]:
        return (Nil, Nil)

    def transpose(self) -> r.Result[Option[T], Any]:
        return r.Ok(Nil)

    def flatten(self) -> Option[T]:
        return Nil


Nil: Final = NilType()


def to_option(opt: Optional[T]) -> Option[T]:
    return Nil if opt is None else Some(opt)
