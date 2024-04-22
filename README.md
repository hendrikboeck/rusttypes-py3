# `rusttypes-py3` - The power of Rust in Python

- [`rusttypes-py3` - The power of Rust in Python](#rusttypes-py3---the-power-of-rust-in-python)
  - [Why?](#why)
  - [Getting Started](#getting-started)
  - [Documentation](#documentation)
  - [License (_BSD 3-Clause License_)](#license-bsd-3-clause-license)


## Why?

>   Bring the power of Rust to Python! Kind of...

``rusttypes`` is a Python 3 library that provides a set of utilities to write
Python code that is more Rust-like. This includes:

- A ``Result`` type that can be used to return either a value or an error.
- A ``Option`` type that can be used to return either a value or nothing.

It implements all the basic operations that you would expect from these types,
such as ``map``, ``and_then``, ``or_else``, etc.. At least as far as Python
allows it, and I was able to implement it. (:

## Getting Started

Install using `pip`:

```
pip install rusttypes
```

Install using `poetry` CLI:

```
poetry add rusttypes
```

or using `pyproject.toml`:

```toml
[tool.poetry.dependencies]
rusttypes = "^0.0.1"
```

## Documentation

Sphinx Documentation at: [https://hendrikboeck.github.io/rusttypes/](https://hendrikboeck.github.io/rusttypes/)

## License (_BSD 3-Clause License_)

Copyright (c) 2024, Hendrik Böck <<hendrikboeck.dev@protonmail.com>>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.