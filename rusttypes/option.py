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
    """Option type that represents an optional value.

    Variants:

    - ``Some(T)``: Some value of type ``T``.
    - ``Nil``: No value.
    """

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        """Compares an ``Option`` with any other object and returns ``True`` if they are equal, ``False`` otherwise.

        Args:
            other (Any): The object to compare with.

        Returns:
            bool: ``True`` if the objects are equal, ``False`` otherwise.

        Examples::

            >>> Some(1) == Some(1)
            True

            >>> Some(1) == Some(2)
            False

            >>> Some(1) == Nil
            False

            >>> Nil == Nil
            True
        """
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        """Representation of the ``Option`` as a ``str``

        Returns:
            str: The representation of the ``Option``.

        Examples::

            >>> Some(1)
            "Some(1)"

            >>> Nil
            "Nil"
        """
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        """Representation of the ``Option`` as a ``str``

        Returns:
            str: The representation of the ``Option``.

        Examples::

            >>> Some(1)
            "Some(1)"

            >>> Nil
            "Nil"
        """
        raise NotImplementedError

    @abstractmethod
    def __bool__(self) -> bool:
        """Returns ``True`` if the ``Option`` is ``Some``, ``False`` if it is ``Nil``

        Returns:
            bool: ``True`` if the ``Option`` is ``Some``, ``False`` if it is ``Nil``

        Examples::

            >>> bool(Some(1))
            True

            >>> bool(Nil)
            False
        """
        raise NotImplementedError

    @abstractmethod
    def as_optional(self) -> Optional[T]:
        """Converts the ``Option`` to an Python ``Optional``

        Returns:
            Optional[T]: The contained value or ``None`` if the ``Option`` is ``Nil``.

        Examples::

            >>> Some(1).as_optional()
            1

            >>> Nil.as_optional()
            None
        """
        raise NotImplementedError

    @abstractmethod
    def is_some(self) -> bool:
        """Returns ``true`` if the option is a ``Some`` value. Equal in function to boolean cast ``bool(...)``.

        Returns:
            bool: ``True`` if the option is a ``Some`` value, ``False`` otherwise.

        Examples::

            >>> Some(1).is_some()
            True

            >>> Nil.is_some()
            False
        """
        raise NotImplementedError

    @abstractmethod
    def is_some_and(self, f: Callable[[T], bool]) -> bool:
        """Checks if the option is a ``Some`` and the value inside of it matches a predicate.

        Args:
            f (Callable[[T], bool]): The predicate to match the value against.

        Returns:
            bool: ``True`` if the option is a ``Some`` and the value matches the predicate, ``False`` otherwise.

        Examples::

            >>> Some(1).is_some_and(lambda x: x > 0)
            True

            >>> Some(0).is_some_and(lambda x: x > 0)
            False

            >>> Nil.is_some_and(lambda x: x > 0)
            False
        """
        raise NotImplementedError

    @abstractmethod
    def is_nil(self) -> bool:
        """Returns ``true`` if the option is a ``Nil`` value. Equal in function to boolean cast ``not bool(...)``.

        Returns:
            bool: ``True`` if the option is a ``Nil`` value, ``False`` otherwise.

        Examples::

            >>> Some(1).is_nil()
            False

            >>> Nil.is_nil()
            True
        """
        raise NotImplementedError

    @abstractmethod
    def expect(self, msg: str) -> T:
        """Returns the contained ``Some`` value.

        Arguments:
            msg: The error message to display if the value is a ``Nil``.

        Raises:
            RuntimeError: with the given message if the value is a ``Nil``.

        Returns:
            T: The contained value.

        Examples::

            >>> Some(1).expect("Value is None")
            1

            >>> Nil.expect("Value is None")
            RuntimeError: Value is None
        """
        raise NotImplementedError

    @abstractmethod
    def unwrap(self) -> T:
        """Returns the contained ``Some`` value.

        Because this function may throw a RuntimeError, its use is generally discouraged. Instead, prefer to
        handle the ``Nil`` case explicitly, or call ``unwrap_or``, ``unwrap_or_else``, or ``unwrap_or_default``.

        Returns:
            T: The contained value.

        Raises:
            RuntimeError: if the value is a ``None``.

        Examples::

            >>> Some(1).unwrap()
            1

            >>> Nil.unwrap()
            RuntimeError: Called unwrap on a Nil value
        """
        raise NotImplementedError

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        """Returns the contained ``Some`` value or a provided default.

        Arguments passed to ``unwrap_or`` are eagerly evaluated; if you are passing the result of a function call,
        it is recommended to use ``unwrap_or_else``, which is lazily evaluated.

        Returns:
            T: The contained value or the default value.

        Examples::

            >>> Some(1).unwrap_or(2)
            1

            >>> Nil.unwrap_or(2)
            2
        """
        raise NotImplementedError

    @abstractmethod
    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        """Returns the contained ``Some`` value or computes it from a closure.

        Args:
            f (Callable[[], T]): The closure to compute the default value.

        Returns:
            T: The contained value or the default value.

        Examples::

            >>> Some(1).unwrap_or_else(lambda: 2)
            1

            >>> Nil.unwrap_or_else(lambda: 2)
            2
        """
        raise NotImplementedError

    @abstractmethod
    def unwrap_or_default(self, t: Type[T]) -> T:
        """Returns the contained Some value or a default.

        Consumes the self argument then, if Some, returns the contained value, otherwise if ``Nil``, returns the
        default value for that type ``t``, which must implement the ``Default`` trait.

        Args:
            t (Type[T]): The type to get the default value from.

        Returns:
            T: The contained value or the default value.

        Examples:
            Lets assume the following dataclass that implements the ``Default`` trait::

                from __future__ import annotations
                from dataclasses import dataclass
                from rusttypes.traits import Default

                T = TypeVar("T")

                @dataclass
                class MyType(Default):
                    value: int

                    @staticmethod
                    def default() -> MyType:
                        return MyType(42)

            You can now use ``unwrap_or_default`` like this::

                >>> x = Some(MyType(1))
                >>> x.unwrap_or_default(MyType).value
                1

                >>> Nil.unwrap_or_default(MyType).value
                42

        """
        raise NotImplementedError

    @abstractmethod
    def unwrap_unchecked(self) -> T:
        """Returns the contained ``Some`` value.

        Returns:
            T: The contained value.

        Raises:
            RuntimeError: if the value is a ``Nil``.

        Examples::

            >>> Some(1).unwrap_unchecked()
            1

            >>> Nil.unwrap_unchecked()
            RuntimeError: Called unwrap_unchecked on a Nil value
        """
        raise NotImplementedError

    @abstractmethod
    def map(self, f: Callable[[T], U]) -> Option[U]:
        """Maps an ``Option[T]`` to ``Option[U]`` by applying a function to a contained value (if ``Some``) or returns
        ``Nil`` (if ``Nil``).

        Args:
            f (Callable[[T], U]): The function to apply to the contained value.

        Returns:
            Option[U]: The mapped ``Option[U]``.

        Examples::

            >>> Some(1).map(lambda x: x + 1)
            Some(2)

            >>> Nil.map(lambda x: x + 1)
            Nil
        """
        raise NotImplementedError

    @abstractmethod
    def inspect(self, f: Callable[[T], None]) -> Option[T]:
        """Calls the provided closure with the contained value (if ``Some``).

        Args:
            f (Callable[[T], None]): The closure to call with the value.

        Returns:
            Option[T]: The ``Option`` itself.

        Examples::

            >>> Some(1).inspect(print)
            1
            Some(1)

            >>> Nil.inspect(print)
            Nil
        """
        raise NotImplementedError

    @abstractmethod
    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        """Returns the provided default result (if ``Nil``), or applies a function to the contained value
        (if ``Some``).

        Arguments passed to ``map_or`` are eagerly evaluated; if you are passing the result of a function call, it is
        recommended to use ``map_or_else``, which is lazily evaluated.

        Args:
            default (U): The default value to return if the ``Option`` is ``Nil``.
            f (Callable[[T], U]): The function to apply to the contained value.

        Returns:
            U: The mapped value or the default value.

        Examples::

            >>> Some("foo").map_or(42, lambda v: len(v))
            3

            >>> Nil.map_or(42, lambda v: len(v))
            42
        """
        raise NotImplementedError

    @abstractmethod
    def map_or_else(self, default: Callable[[], U], f: Callable[[T], U]) -> U:
        """Computes a default function result (if ``Nil``), or applies a different function to the contained value
        (if ``Some``).

        Args:
            default (Callable[[], U]): The closure to compute the default value.
            f (Callable[[T], U]): The function to apply to the contained value.

        Returns:
            U: The mapped value or the default value.

        Examples::

            >>> Some("foo").map_or_else(lambda: 42, lambda v: len(v))
            3

            >>> Nil.map_or_else(lambda: 42, lambda v: len(v))
            42
        """
        raise NotImplementedError

    @abstractmethod
    def ok_or(self, err: E) -> r.Result[T, E]:
        """Transforms the ``Option[T]`` into a ``Result[T, E]``, mapping ``Some(v)`` to ``Ok(v)`` and ``Nil`` to
        ``Err(err)``.

        Arguments passed to ``ok_or`` are eagerly evaluated; if you are passing the result of a function call, it
        is recommended to use ``ok_or_else``, which is lazily evaluated.

        Args:
            err (E): The error value to use if the ``Option`` is ``Nil``.

        Returns:
            Result[T, E]: The transformed ``Result``.

        Examples::

            >>> Some(1).ok_or("Error")
            Ok(1)

            >>> Nil.ok_or("Error")
            Err("Error")
        """
        raise NotImplementedError

    @abstractmethod
    def ok_or_else(self, f: Callable[[], E]) -> r.Result[T, E]:
        """Transforms the ``Option[T]`` into a ``Result[T, E]``, mapping ``Some(v)`` to ``Ok(v)`` and ``Nil`` to
        ``Err(f())``.

        Args:
            f (Callable[[], E]): The closure to compute the error value if the ``Option`` is ``Nil``.

        Returns:
            Result[T, E]: The transformed ``Result``.

        Examples::

            >>> Some(1).ok_or_else(lambda: "Error")
            Ok(1)

            >>> Nil.ok_or_else(lambda: "Error")
            Err("Error")
        """
        raise NotImplementedError

    @abstractmethod
    def and_(self, optb: Option[U]) -> Option[U]:
        """Returns ``Nil`` if the option is ``Nil``, otherwise returns ``optb``.

        Arguments passed to ``and_`` are eagerly evaluated; if you are passing the result of a function call, it is
        recommended to use ``and_then``, which is lazily evaluated.

        Args:
            optb (Option[U]): The other option to return if the current option is ``Some``.

        Returns:
            Option[U]: The other option if the current option is ``Some``, ``Nil`` otherwise.

        Examples::

            >>> Some(1).and_(Some("foo"))
            Some("foo")

            >>> Some(1).and_(Nil)
            Nil

            >>> Nil.and_(Some(2))
            Nil
        """
        raise NotImplementedError

    @abstractmethod
    def and_then(self, f: Callable[[T], Option[U]]) -> Option[U]:
        """Returns ``Nil`` if the option is ``Nil``, otherwise calls ``f`` with the wrapped value and returns the
        result.

        Some languages call this operation flatmap.

        Args:
            f (Callable[[T], Option[U]]): The function to call with the value if the option is ``Some``.

        Returns:
            Option[U]: The result of the function call or ``Nil``.

        Examples:
            Lets assume the following function ``is_positive``::

                import math

                def sqrt(x: float) -> Option[float]:
                    if x < 0:
                        return Nil
                    return Some(math.sqrt(x))

            You can now use ``and_then`` like this::

                >>> Some(4).and_then(sqrt)
                Some(2)

                >>> Some(-1).and_then(sqrt)
                Nil

                >>> Nil.and_then(sqrt)
                Nil
        """
        raise NotImplementedError

    @abstractmethod
    def filter(self, predicate: Callable[[T], bool]) -> Option[T]:
        """Returns ``Nil`` if the option is ``Nil``, otherwise calls ``predicate`` with the wrapped value and returns:

        - ``Some(val)`` if ``predicate`` returns ``True`` (where ``val`` is the wrapped value), and
        - ``Nil`` if ``predicate`` returns ``False``.

        You can imagine the ``Option[T]`` being an iterator over one or zero elements. ``filter()`` lets you decide
        which elements to keep.

        Args:
            predicate (Callable[[T], bool]): The ``predicate`` to match the value against.

        Returns:
            Option[T]: The filtered ``Option``.

        Examples:
            Lets assume the following function ``is_positive``::

                def is_positive(x: int) -> bool:
                    return x > 0

            You can now use ``filter`` like this::

                >>> Some(1).filter(is_positive)
                Some(1)

                >>> Some(-42).filter(is_positive)
                Nil

                >>> Nil.filter(is_positive)
                Nil
        """
        raise NotImplementedError

    @abstractmethod
    def or_(self, optb: Option[T]) -> Option[T]:
        """Returns the option if it contains a value, otherwise returns ``optb``.

        Arguments passed to ``or_`` are eagerly evaluated; if you are passing the result of a function call, it is
        recommended to use ``or_else``, which is lazily evaluated.

        Args:
            optb (Option[T]): The other option to return if the current option is ``Nil``.

        Returns:
            Option[T]: The current option if it is ``Some``, otherwise the other option.

        Examples::

            >>> Some(1).or_(Some(2))
            Some(1)

            >>> Some(1).or_(Nil)
            Some(1)

            >>> Nil.or_(Some(2))
            Some(2)

            >>> Nil.or_(Nil)
            Nil
        """
        raise NotImplementedError

    @abstractmethod
    def or_else(self, f: Callable[[], Option[T]]) -> Option[T]:
        """Returns the option if it contains a value, otherwise calls ``f`` and returns the result.

        Args:
            f (Callable[[], Option[T]]): The closure to compute the default value.

        Returns:
            Option[T]: The current option if it is ``Some``, otherwise the result of the closure.

        Examples:

            Lets assume the following functions ``nobody`` and ``vikings``::

                def nobody() -> Option[str]:
                    return Nil

                def vikings() -> Option[str]:
                    return Some("vikings")

            You can now use ``or_else`` like this::

                >>> Some("barbarians").or_else(vikings)
                Some("barbarians")

                >>> Nil.or_else(vikings)
                Some("vikings")

                >>> Nil.or_else(nobody)
                Nil
        """
        raise NotImplementedError

    @abstractmethod
    def xor(self, optb: Option[T]) -> Option[T]:
        """Returns ``Some`` if exactly one of ``self``, ``optb`` is ``Some``, otherwise returns ``Nil``.

        Args:
            optb (Option[T]): The other option to compare with.

        Returns:
            Option[T]: ``Some`` if exactly one of ``self``, ``optb`` is ``Some``, otherwise ``Nil``.

        Examples::

            >>> Some(1).xor(Some(2))
            Nil

            >>> Some(1).xor(Nil)
            Some(1)

            >>> Nil.xor(Some(2))
            Some(2)

            >>> Nil.xor(Nil)
            Nil
        """
        raise NotImplementedError

    @abstractmethod
    def insert(self, value: T) -> Some[T]:
        """Inserts ``value`` into the option, then returns the (newly created) value, for the function to work properly
        override the varibale from which this function is called with the return value if no function chaining is used.

        If the option already contains a value, the old value is dropped.

        See also ``Option::get_or_insert``, which doesn't update the value if the option already contains ``Some``.

        Args:
            value (T): The value to insert.

        Returns:
            Some[T]: The (newly created) value.

        Examples::

            >>> x = Some(1)
            >>> x = x.insert(2)
            >>> x
            Some(2)
        """
        raise NotImplementedError

    @abstractmethod
    def get_or_insert(self, value: T) -> Some[T]:
        """Inserts ``value`` into the option if it is ``Nil``, then returns the (newly created) value, for the function
        to work properly override the varibale from which this function is called with the return value if no function
        chaining is used.

        See also ``Option::insert``, which updates the value even if the option already contains ``Some``.

        Args:
            value (T): The value to insert.

        Returns:
            Some[T]: The (newly created) value.

        Examples::

            >>> x = Nil
            >>> x = x.get_or_insert(2)
            >>> x
            Some(2)

            >>> x = Some(1)
            >>> x = x.get_or_insert(2)
            >>> x
            Some(1)
        """
        raise NotImplementedError

    @abstractmethod
    def get_or_insert_default(self, t: Type[T]) -> Some[T]:
        """Inserts the default value into the option if it is ``Nil``, then returns the (newly created) value, for the
        function to work properly override the varibale from which this function is called with the return value if
        no function chaining is used. The default value is retrieved from the ``Default`` trait of the type ``T``.

        Args:
            t (Type[T]): The type to get the default value from.

        Returns:
            Some[T]: The (newly created) value.

        Raises:
            ValueError: If the type ``T`` does not implement the ``Default`` trait.

        Examples:
            Lets assume the following dataclass that implements the ``Default`` trait::

                from dataclasses import dataclass
                from typing import TypeVar, Type
                from rusttypes.traits import Default

                T = TypeVar("T")

                @dataclass
                class MyType(Default):
                    value: int

                    @classmethod
                    def default(cls: Type[T]) -> T:
                        return MyType(42)

            You can now use ``get_or_insert_default`` like this::

                >>> x = Nil
                >>> x = x.get_or_insert_default(MyType)
                >>> x.value
                42

                >>> x = Some(MyType(1))
                >>> x = x.get_or_insert_default(MyType)
                >>> x.value
                1
        """
        raise NotImplementedError

    @abstractmethod
    def get_or_insert_with(self, f: Callable[[], T]) -> Some[T]:
        """Inserts a value computed from ``f`` into the option if it is ``Nil``, then returns the (newly created) value,
        for the function to work properly override the varibale from which this function is called with the return
        value if no function chaining is used.

        Args:
            f (Callable[[], T]): The closure to compute the value.

        Returns:
            Some[T]: The (newly created) value.

        Examples::

            >>> x = Nil
            >>> x = x.get_or_insert_with(lambda: 2)
            >>> x
            Some(2)

            >>> x = Some(1)
            >>> x = x.get_or_insert_with(lambda: 2)
            >>> x
            Some(1)
        """
        raise NotImplementedError

    @abstractmethod
    def take(self) -> Tuple[NilType, Option[T]]:
        """Takes the value out of the option, leaving a None in its place. The first value in the tuple is ``Nil``
        and should be written to the variable from which this function is called if no function chaining is used.

        Returns:
            Tuple[NilType, Option[T]]: A tuple containing ``Nil`` and the value.

        Examples::

            >>> x = Some(1)
            >>> x, y = x.take()
            >>> x
            Nil
            >>> y
            Some(1)
        """
        raise NotImplementedError

    @abstractmethod
    def replace(self, value: T) -> Tuple[Option[T], Option[T]]:
        """Replaces the actual value in the option by the value given in parameter, returning the old value if
        present, leaving a ``Some`` in its place. The first value in the tuple is the new value and should be written
        to the variable from which this function is called if no function chaining is used.

        Args:
            value (T): The value to insert.

        Returns:
            Tuple[Option[T], Option[T]]: A tuple containing the new value and the old value.

        Examples::

            >>> x = Some(1)
            >>> x, y = x.replace(2)
            >>> x
            Some(2)
            >>> y
            Some(1)
        """
        raise NotImplementedError

    @abstractmethod
    def zip(self, other: Option[U]) -> Option[Tuple[T, U]]:
        """Zips ``self`` with another ``Option``.

        If ``self`` is ``Some(s)`` and ``other`` is ``Some(o)``, this method returns ``Some((s, o))``. Otherwise,
        ``Nil`` is returned.

        Args:
            other (Option[U]): The other option to zip with.

        Returns:
            Option[Tuple[T, U]]: The zipped option.

        Examples::

            >>> Some(1).zip(Some("foo"))
            Some((1, "foo"))

            >>> Some(1).zip(Nil)
            Nil

            >>> Nil.zip(Some("foo"))
            Nil
        """
        raise NotImplementedError

    @abstractmethod
    def zip_with(self, other: Option[U], f: Callable[[ T, U ], R]) -> Option[R]:
        """Zips ``self`` and another ``Option`` with function ``f``.

        If ``self`` is ``Some(s)`` and ``other`` is ``Some(o)``, this method returns ``Some((s, o))``. Otherwise,
        ``Nil`` is returned.

        Args:
            other (Option[U]): The other option to zip with.
            f (Callable[[ T, U ], R]): The function to apply to the zipped values.

        Returns:
            Option[R]: The zipped option.

        Examples:
            Lets assume the following dataclass ``Point``::

                from dataclasses import dataclass

                @dataclass
                class Point:
                    x: int
                    y: int

            You can now use ``zip_with`` like this::

                >>> Some(1).zip_with(Some(2), Point)
                Some(Point(1, 2))

                >>> Some(1).zip_with(Nil, Point)
                Nil

                >>> Nil.zip_with(Some(2), Point)
                Nil
        """
        raise NotImplementedError

    @abstractmethod
    def unzip(self) -> Tuple[Option[Any], Option[Any]]:
        """Unzips an option containing a tuple of two options.

        If self is ``Some((a, b))`` this method returns ``(Some(a), Some(b))``. Otherwise, ``(Nil, Nil)`` is returned.

        Returns:
            Tuple[Option[Any], Option[Any]]: The unzipped options.

        Raises:
            ValueError: If the inner type is not a tuplelike of length 2.

        Examples::

            >>> Some((1, "foo")).unzip()
            (Some(1), Some("foo"))

            >>> Nil.unzip()
            (Nil, Nil)

            >>> Some((1, "foo", 3)).unzip()
            ValueError: Can not unzip tuple with more/less than 2 elements
        """
        raise NotImplementedError

    @abstractmethod
    def transpose(self) -> r.Result[Option[T], Any]:
        """Transposes an ``Option`` of a ``Result`` into a ``Result`` of an ``Option``.

        ``Nil`` will be mapped to ``Ok(Nil)``. ``Some(Ok(_))`` and ``Some(Err(_))`` will be mapped to ``Ok(Some(_))``
        and ``Err(_)``.

        Returns:
            Result[Option[T], Any]: The transposed result.

        Raises:
            ValueError: If the inner type is not a ``Result``.

        Examples::

            >>> Some(Ok(1)).transpose()
            Ok(Some(1))

            >>> Some(Err("error")).transpose()
            Err("error")

            >>> Nil.transpose()
            Ok(Nil)
        """
        raise NotImplementedError

    @abstractmethod
    def flatten(self) -> Option[T]:
        """Converts from ``Option[Option[T]]`` to ``Option[T]``.

        Returns:
            Option[T]: The flattened option.

        Raises:
            ValueError: If the inner type is not an ``Option``.

        Examples::

            >>> Some(Some(1)).flatten()
            Some(1)

            >>> Some(Nil).flatten()
            Nil

            >>> Nil.flatten()
            ValueError: Can not flatten if .inner is non-option type
        """
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

    def is_nil(self) -> bool:
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

    def filter(self, predicate: Callable[[T], bool]) -> Option[T]:
        return self if predicate(self.inner) else Nil

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

    def is_nil(self) -> bool:
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

    def filter(self, predicate: Callable[[T], bool]) -> Option[T]:
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
"""A final instance of the ``NilType`` class, representing a ``Nil`` value."""


def to_option(opt: Optional[T]) -> Option[T]:
    """Converts a Python ``Optional`` to a ``Option``.

    Args:
        opt (Optional[T]): The optional value to convert.

    Returns:
        Option[T]: The converted option.

    Examples::

        >>> to_option(1)
        Some(1)

        >>> to_option(None)
        Nil
    """
    return Nil if opt is None else Some(opt)
