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
    """Exception that is thrown when calling ``Result::try_`` on an ``Err``. The inner value is the error that caused the
    exception. This exception is caught by the ``try_guard`` decorator. This type is not meant to be used by the user.

    Attributes:
        inner (E): The error that caused the exception.

    Examples:

        This exception is thrown when calling ``Result::try_`` on an ``Err``::

            >>> Err("error").try_()
            Traceback (most recent call last):
                ...
    """

    inner: E

    def __init__(self, inner: E):
        self.inner = inner

    def __str__(self):
        return f"ResultException({self.inner})"


class Result(ABC, Generic[T, E]):
    """Result type that represents either a successful value or an error. The ``Result`` type is a sum type that can be
    either an ``Ok`` or an ``Err``. The ``Ok`` variant holds the successful value, while the ``Err`` variant holds the
    error value. The ``Result`` type is used to handle errors in a functional way. The ``Result`` type is inspired by
    Rust's ``Result`` type.

    Variants:

    - ``Ok(T)``: Represents a successful value ``T``.
    - ``Err(E)``: Represents an error value of type ``E``.
    """

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
        """Returns ``True`` if the ``Result`` is ``Ok``.

        Returns:
            bool: ``True`` if the ``Result`` is ``Ok``, otherwise ``False``.

        Examples::

            >>> Ok(42).is_ok()
            True

            >>> Err("Some error message").is_ok()
            False
        """
        raise NotImplementedError

    @abstractmethod
    def is_ok_and(self, f: Callable[[T], bool]) -> bool:
        """Returns ``True`` if the result is ``Ok`` and the value inside of it matches a predicate.

        Args:
            f (Callable[[T], bool]): The predicate to match against.

        Returns:
            bool: ``True`` if the result is ``Ok`` and the value inside of it matches the predicate, otherwise
            ``False``.

        Examples::

            >>> Ok(42).is_ok_and(lambda x: x > 0)
            True

            >>> Ok(-42).is_ok_and(lambda x: x > 0)
            False

            >>> Err("Some error message").is_ok_and(lambda x: x > 0)
            False
        """
        raise NotImplementedError

    @abstractmethod
    def is_err(self) -> bool:
        """Returns ``True`` if the result is ``Err``. Is the inverse of ``Result::is_ok``.

        Returns:
            bool: ``True`` if the result is ``Err``, otherwise ``False``.

        Examples::

            >>> Ok(42).is_err()
            False

            >>> Err("Some error message").is_err()
            True
        """
        raise NotImplementedError

    @abstractmethod
    def is_err_and(self, f: Callable[[E], bool]) -> bool:
        """Returns ``True`` if the result is ``Err`` and the value inside of it matches a predicate.

        Args:
            f (Callable[[E], bool]): The predicate to match against.

        Returns:
            bool: ``True`` if the result is ``Err`` and the value inside of it matches the predicate, otherwise
            ``False``.

        Examples::

            >>> Ok(42).is_err_and(lambda x: isinstance(x, str))
            False

            >>> Err("Some error message").is_err_and(lambda x: isinstance(x, str))
            True
        """
        raise NotImplementedError

    @abstractmethod
    def ok(self) -> o.Option[T]:
        """Converts from ``Result[T, E]`` to ``Option[T]``.

        Converts ``self`` into an ``Option[T]`` and discarding the error, if any.

        Returns:
            Option[T]: ``Some(T)`` if the result is ``Ok``, otherwise ``Nil``.

        Examples::

            >>> Ok(42).ok()
            Some(42)

            >>> Err("Some error message").ok()
            Nil
        """
        raise NotImplementedError

    @abstractmethod
    def err(self) -> o.Option[E]:
        """Converts from ``Result[T, E]`` to ``Option[E]``.

        Converts ``self`` into an ``Option[E]`` and discarding the success value, if any.

        Returns:
            Option[E]: ``Some(E)`` if the result is ``Err``, otherwise ``Nil``.

        Examples::

            >>> Ok(42).err()
            Nil

            >>> Err("Some error message").err()
            Some("Some error message")
        """
        raise NotImplementedError

    @abstractmethod
    def map(self, op: Callable[[T], U]) -> Result[U, E]:
        """Maps a ``Result[T, E]`` to ``Result[U, E]`` by applying a function to a contained ``Ok`` value,
        leaving an ``Err`` value untouched.

        This function can be used to compose the results of two functions.

        Args:
            op (Callable[[T], U]): The function to apply to the contained value.

        Returns:
            Result[U, E]: ``Ok(U)`` if the result is ``Ok``, otherwise ``Err(E)``.

        Examples::

            >>> Ok(21).map(lambda x: x * 2)
            Ok(42)

            >>> Err("Some error message").map(lambda x: x * 2)
            Err("Some error message")
        """
        raise NotImplementedError

    @abstractmethod
    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        """Returns the provided default (if ``Err``), or applies a function to the contained value (if ``Ok``).

        Arguments passed to ``map_or`` are eagerly evaluated; if you are passing the result of a function call,
        it is recommended to use ``map_or_else``, which is lazily evaluated.

        Args:
            default (U): The value to return if the result is ``Err``.
            f (Callable[[T], U]): The function to apply to the contained value if the result is ``Ok``.

        Returns:
            U: The result of the function if the result is ``Ok``, otherwise the default value.

        Examples::

            >>> Ok(21).map_or(0, lambda x: x * 2)
            42

            >>> Err("Some error message").map_or(0, lambda x: x * 2)
            0
        """
        raise NotImplementedError

    @abstractmethod
    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        """Maps a ``Result[T, E]`` to ``U`` by applying fallback function ``default`` to a contained ``Err`` value,
        or function ``f`` to a contained ``Ok`` value.

        This function can be used to unpack a successful result while handling an error.

        Args:
            default (Callable[[E], U]): The function to apply to the contained value if the result is ``Err``.
            f (Callable[[T], U]): The function to apply to the contained value if the result is ``Ok``.

        Returns:
            U: The result of the function if the result is ``Ok``, otherwise the default value.

        Examples::

            >>> Ok(21).map_or_else(lambda e: 0, lambda x: x * 2)
            42

            >>> Err("Some error message").map_or_else(lambda e: 0, lambda x: x * 2)
            0
        """
        raise NotImplementedError

    @abstractmethod
    def map_err(self, op: Callable[[E], F]) -> Result[T, F]:
        """Maps a ``Result[T, E]`` to ``Result[T, F]`` by applying a function to a contained ``Err`` value,
        leaving an ``Ok`` value untouched.

        This function can be used to pass through a successful result while handling an error.

        Args:
            op (Callable[[E], F]): The function to apply to the contained value.

        Returns:
            Result[T, F]: ``Ok(T)`` if the result is ``Ok``, otherwise ``Err(F)``.

        Examples::

            >>> Ok(42).map_err(lambda e: f"Error: {e}"))
            Ok(42)

            >>> Err(42).map_err(lambda e: f"Error: {e}")
            Err("Error: 42")
        """
        raise NotImplementedError

    @abstractmethod
    def inspect(self, op: Callable[[T], None]) -> Result[T, E]:
        """Calls the provided closure with a copy of the contained value (if ``Ok``).

        Args:
            op (Callable[[T], None]): The closure to call with the contained value.

        Returns:
            Result[T, E]: The result itself.

        Examples::

            >>> Ok(42).inspect(print)
            42
            Ok(42)

            >>> Err("Some error message").inspect(print)
            Err("Some error message")
        """
        raise NotImplementedError

    @abstractmethod
    def inspect_err(self, op: Callable[[E], None]) -> Result[T, E]:
        """Calls the provided closure with a copy of the contained error (if ``Err``).

        Args:
            op (Callable[[E], None]): The closure to call with the contained error.

        Returns:
            Result[T, E]: The result itself.

        Examples::

            >>> Ok(42).inspect_err(print)
            Ok(42)

            >>> Err("Some error message").inspect_err(print)
            Some error message
            Err("Some error message")
        """
        raise NotImplementedError

    @abstractmethod
    def expect(self, msg: str) -> T:
        """Returns the contained ``Ok`` value..

        Because this function may panic, its use is generally discouraged. Instead, prefer to use pattern matching and
        handle the ``Err`` case explicitly, or call ``unwrap_or``, ``unwrap_or_else``, or ``unwrap_or_default``.

        Args:
            msg (str): The message to display in case of a panic.

        Returns:
            T: The contained value if the result is ``Ok``.

        Raises:
            RuntimeError: If the result is ``Err``.

        Examples::

            >>> Ok(42).expect("This should not panic")
            42

            >>> Err("Some error message").expect("This should panic")
            RuntimeError: This should panic
        """
        raise NotImplementedError

    @abstractmethod
    def unwrap(self) -> T:
        """Returns the contained ``Ok`` value.

        Because this function may panic, its use is generally discouraged. Instead, prefer to use pattern matching and
        handle the ``Err`` case explicitly, or call ``unwrap_or``, ``unwrap_or_else``, or ``unwrap_or_default``.

        Returns:
            T: The contained value if the result is ``Ok``.

        Raises:
            RuntimeError: If the result is ``Err``.

        Examples::

            >>> Ok(42).unwrap()
            42

            >>> Err("Some error message").unwrap()
            RuntimeError: Called unwrap on Err
        """
        raise NotImplementedError

    @abstractmethod
    def unwrap_or_default(self, t: Type[T]) -> T:
        """Returns the contained ``Ok`` value or a default. ``t`` has to be a type that implements the ``Default``
        trait.

        If ``Ok``, returns the contained value, otherwise if ``Err``, returns the default value for that type.

        Args:
            t (Type[T]): The type that implements the ``Default`` trait.

        Returns:
            T: The contained value if the result is ``Ok``, otherwise the default value of the type.

        Examples:

            Lets assume we have a type that implements the ``Default`` trait::

                from __future__ import annotations
                from dataclasses import dataclass
                from rustlike.traits import Default

                T = TypeVar("T")

                @dataclass
                class Foo(Default):
                    x: int

                    @staticmethod
                    def default() -> Foo:
                        return Foo(42)

            Now we can use the ``unwrap_or_default`` method::

                >>> Ok(Foo(21)).unwrap_or_default(Foo)
                Foo(21)

                >>> Err("Some error message").unwrap_or_default(Foo)
                Foo(42)
        """
        raise NotImplementedError

    @abstractmethod
    def expect_err(self, msg: str) -> E:
        """Returns the contained ``Err`` value.

        Args:
            msg (str): The message to display in case of a panic.

        Returns:
            E: The contained value if the result is ``Err``.

        Raises:
            RuntimeError: If the result is ``Ok``.

        Examples::

            >>> Ok(42).expect_err("This should panic")
            RuntimeError: This should panic

            >>> Err("Some error message").expect_err("This should not panic")
            Some error message
        """
        raise NotImplementedError

    @abstractmethod
    def unwrap_err(self) -> E:
        """Returns the contained ``Err`` value.

        Returns:
            E: The contained value if the result is ``Err``.

        Raises:
            RuntimeError: If the result is ``Ok``.

        Examples::

            >>> Ok(42).unwrap_err()
            RuntimeError: Called unwrap_err on Ok

            >>> Err("Some error message").unwrap_err()
            "Some error message"
        """
        raise NotImplementedError

    @abstractmethod
    def and_(self, res: Result[U, E]) -> Result[U, E]:
        """Returns ``res`` if the result is ``Ok``, otherwise returns the ``Err`` value of ``self``.

        Arguments passed to ``and_`` are eagerly evaluated; if you are passing the result of a function call,
        it is recommended to use ``and_then``, which is lazily evaluated.

        Args:
            res (Result[U, E]): The result to return if the result is ``Ok``.

        Returns:
            Result[U, E]: ``res`` if the result is ``Ok``, otherwise the ``Err`` value of ``self``.

        Examples::

            >>> Ok(42).and_(Ok(21))
            Ok(21)

            >>> Ok(42).and_(Err("Some error message"))
            Err("Some error message")

            >>> Err("Some error message").and_(Ok(21))
            Err("Some error message")

            >>> Err("Some error message").and_(Err("Another error message"))
            Err("Some error message")
        """
        raise NotImplementedError

    @abstractmethod
    def and_then(self, op: Callable[[T], Result[U, E]]) -> Result[U, E]:
        """Calls ``op`` if the result is ``Ok``, otherwise returns the ``Err`` value of ``self``.

        This function can be used for control flow based on Result values.

        Args:
            op (Callable[[T], Result[U, E]]): The function to call if the result is ``Ok``.

        Returns:
            Result[U, E]: The result of the function if the result is ``Ok``, otherwise the ``Err`` value of ``self``.

        Examples:
            Lets assume we have a function that squares and then stringifies an ``float``, that can fail if the
            ``float`` is greater than ``1_000_000``::

                import math

                def sq_and_stringify(x: int) -> Result[str, str]:
                    if math.abs(x) >= 1_000_000:
                        return Err("Number too large")
                    return Ok(str(x * x))

            Now we can use the ``and_then`` method to chain the function calls::

                >>> Ok(42).and_then(sq_and_stringify)
                Ok("1764")

                >>> Ok(1_000_000).and_then(sq_and_stringify)
                Err("Number too large")

        """
        raise NotImplementedError

    @abstractmethod
    def or_(self, res: Result[T, F]) -> Result[T, F]:
        """Returns ``res`` if the result is ``Err``, otherwise returns the ``Ok`` value of ``self``.

        Arguments passed to ``or_`` are eagerly evaluated; if you are passing the result of a function call, it is
        recommended to use ``or_else``, which is lazily evaluated.

        Args:
            res (Result[T, F]): The result to return if the result is ``Err``.

        Returns:
            Result[T, F]: ``res`` if the result is ``Err``, otherwise the ``Ok`` value of ``self``.

        Examples::

            >>> Ok(42).or_(Ok(21))
            Ok(42)

            >>> Ok(42).or_(Err("Some error message"))
            Ok(42)

            >>> Err("Some error message").or_(Ok(21))
            Ok(21)

            >>> Err("Some error message").or_(Err("Another error message"))
            Err("Another error message")
        """
        raise NotImplementedError

    @abstractmethod
    def or_else(self, op: Callable[[E], Result[T, F]]) -> Result[T, F]:
        """Calls ``op`` if the result is ``Err``, otherwise returns the ``Ok`` value of ``self``.

        This function can be used for control flow based on result values.

        Args:
            op (Callable[[E], Result[T, F]]): The function to call if the result is ``Err``.

        Returns:
            Result[T, F]: The result of the function if the result is ``Err``, otherwise the ``Ok`` value of ``self``.

        Examples:

            Lets assume we have function that squares an int and a function that returns the int as an error::

                def sq(x: int) -> Result[int, int]:
                    return Ok(x * x)

                def err(x: int) -> Result[int, int]:
                    return Err(x)

            Now we can use the ``or_else`` method to chain the function calls::

                >> Ok(2).or_else(sq).or_else(sq)
                Ok(2)

                >>> Ok(2).or_else(err).or_else(sq)
                Ok(2)

                >>> Err(3).or_else(sq).or_else(err)
                Ok(9)

                >>> Err(3).or_else(err).or_else(err)
                Err(3)
        """
        raise NotImplementedError

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        """Returns the contained ``Ok`` value or a provided default.

        Arguments passed to ``unwrap_or`` are eagerly evaluated; if you are passing the result of a function call,
        it is recommended to use ``unwrap_or_else``, which is lazily evaluated.

        Args:
            default (T): The value to return if the result is ``Err``.

        Returns:
            T: The contained value if the result is ``Ok``, otherwise the default value.

        Examples::

            >>> Ok(42).unwrap_or(0)
            42

            >>> Err("Some error message").unwrap_or(0)
            0
        """
        raise NotImplementedError

    @abstractmethod
    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        """Returns the contained ``Ok`` value or computes it from a closure.

        Args:
            op (Callable[[E], T]): The closure to call if the result is ``Err``.

        Returns:
            T: The contained value if the result is ``Ok``, otherwise the result of the closure.

        Examples::

            >>> Ok(42).unwrap_or_else(lambda e: len(e))
            42

            >>> Err("foo").unwrap_or_else(lambda e: len(e))
            3
        """
        raise NotImplementedError

    @abstractmethod
    def unwrap_unchecked(self) -> T:
        """Returns the contained ``Ok`` value.

        Returns:
            T: The contained value if the result is ``Ok``.

        Raises:
            RuntimeError: If the result is ``Err``.

        Examples::

            >>> Ok(42).unwrap_unchecked()
            42

            >>> Err("Some error message").unwrap_unchecked()
            RuntimeError: Called unwrap_unchecked on Err
        """
        raise NotImplementedError

    @abstractmethod
    def unwrap_err_unchecked(self) -> E:
        """Retruns the contained ``Err`` value.

        Returns:
            E: The contained value if the result is ``Err``.

        Raises:
            RuntimeError: If the result is ``Ok``.

        Examples::

            >>> Ok(42).unwrap_err_unchecked()
            RuntimeError: Called unwrap_err_unchecked on Ok

            >>> Err("Some error message").unwrap_err_unchecked()
            "Some error message"
        """
        raise NotImplementedError

    @abstractmethod
    def try_(self) -> T:
        """Returns the contained ``Ok``, else raises the contained ``Err`` value as ``ResultException``. Should only
        be used in combination with the ``@try_guard`` decorator.

        Works in conjunction with the ``@try_guard`` decorator similar to the ``?`` operator in Rust.

        Returns:
            T: The contained value if the result is ``Ok``.

        Raises:
            ResultException: If the result is ``Err``.

        Examples:

            Lets say we have a function that parses a string to an integer. If the string is not a valid integer,
            we want to return an error instead of raising a ``ValueError``. Now we want to parse an array of integers
            and return an error if one of the integers is invalid::

                @catch(ValueError)
                def parse_int(s: str) -> Result[int, str]:
                    return Ok(int(s))

                @try_guard
                def parse_int_array(arr: str) -> Result[List[int], str]:
                    return Ok([parse_int(s).try_() for s in arr.split()])

            You can now use the function and handle the error case::

                >>> parse_int_array("42 21 1337")
                Ok([42, 21, 1337])

                >>> parse_int_array("42 foo 1337")
                Err("invalid literal for int() with base 10: 'foo'")
        """
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
    """Catch specified exceptions and return them as ``Err``. If no exceptions are specified, catch all exceptions. Use
    the ``map_err`` function to map the caught exception to the error type of the ``Result``.

    Args:
        *exceptions (Type[BaseException]): The exceptions to catch.
        map_err (Callable[[BaseException], E]): The function to map the caught exception to the error type of the
            ``Result``. Defaults to ``rustlike.misc.stringify``.

    Returns:
        Callable[[Callable[..., Result[T, E]]], Callable[..., Result[T, E]]]: Decorator that catches the specified exceptions and returns them as ``Err``.

    Examples:

        Lets say we have a function that parses a string to an integer. If the string is not a valid integer, we want to
        return an error instead of raising a ``ValueError``::

            @catch(ValueError)
            def parse_int(s: str) -> Result[int, str]:
                return Ok(int(s))

        You can now use the function and handle the error case::

            >>> parse_int("42")
            Ok(42)

            >>> parse_int("foo")
            Err("invalid literal for int() with base 10: 'foo'")
    """

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
    """Bubble up ``Err`` that are thrown inside the function. If an ``Err`` is thrown, it is returned as is. This
    is useful in combination with the ``Result::try_`` method.

    Works in conjunction with the ``Result::try_`` function similar to the ``?`` operator in Rust.

    Args:
        fn (Callable[..., Result[T, E]]): The function to wrap.

    Returns:
        Callable[..., Result[T, E]]: Wrapped function that bubbles up ``Err``.

    Examples:

            Lets say we have a function that parses a string to an integer. If the string is not a valid integer, we want to
            return an error instead of raising a ``ValueError``. Now we want to parse an array of integers and return an
            error if one of the integers is invalid::

                @catch(ValueError)
                def parse_int(s: str) -> Result[int, str]:
                    return Ok(int(s))

                @try_guard
                def parse_int_array(arr: str) -> Result[List[int], str]:
                    return Ok([parse_int(s).try_() for s in arr.split()])

            You can now use the function and handle the error case::

                >>> parse_int_array("42 21 1337")
                Ok([42, 21, 1337])

                >>> parse_int_array("42 foo 1337")
                Err("invalid literal for int() with base 10: 'foo'")

    """

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Result[T, E]:
        try:
            return fn(*args, **kwargs)
        except ResultException as e:
            return Err(e.inner)

    return wrapper
