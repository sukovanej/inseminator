# Inseminator

[![codecov](https://codecov.io/gh/sukovanej/container/branch/master/graph/badge.svg)](https://codecov.io/gh/sukovanej/container)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

*(definition from dictionary.com)*

> a technician who introduces prepared ~semen~ **dependencies** into the ~genital tract 
> of breeding animals~ python classes, especially ~cows and mares~ pure classes with 
> proper IoC, for ~artificial insemination~ well coupled components and clear classes 
> signatures.

Python library for type-based dependency injection. Write code without global state
and noisy boilerplate. Inseminator is meant to be used in an entry-point layer of your
application and the only thing it requires is properly type-hinted classes 
dependencies.

*(Under development)*

## Usage

You start by defining the *container* of your dependencies. Whenever you want the container
to resolve a dependency, it uses the container to search for existing objects and a 
resolver automatically creates desired dependencies.

```Python
from inseminator import Container


class DomainModel:
    def __init__(self):
        self.__logic_constant = 1

    def domain_logic(self, input_value: int) -> int:
        return input_value + self.__logic_constant


class Controller:
    def __init__(self, domain_model: DomainModel):
        self.__domain_model = domain_model

    def handler(self, input_value: int) -> int:
        return self.__domain_model.domain_logic(input_value)


# entry-point of your application

container = Container()

# view layer handling

controller = container.resolve(Controller)
result = controller.handler(1)
print(result)
```

The strategy for resolving `Controller` is its constructor signature. The resolver works as follows.

  1) We ask the `container` to resolve a dependency `Controller` -> `container.resolve(Controller)`.
  2) Resolver inside the `container` checks the `Controller`'s constructor signature, i.e. **type hints**
     of `__init__` method and sees `domain_models: DomainModel`.
  3) If an instance of `DomainModel` class is already known by the `container` it uses that instance.
     In the opposite case, the container starts the same resolving machinery for `DomainModel` - which
     is the exact case we are facing now.
  4) Because `DomainModel` doesn't have any dependencies it can construct it directly.
  5) Now the resolver has all the dependencies for `Controller` constructor and can instantiate it.

If we programmed against an interface instead of implementation the example is modified like this.

```Python
from inseminator import Container

from typing import Protocol

class DomainModel(Protocol):
    def domain_logic(self, input_value: int) -> int:
        ...

class Controller:
    def __init__(self, domain_model: DomainModel):
        self.__domain_model = domain_model

    def handler(self, input_value: int) -> int:
        return self.__domain_model.domain_logic(input_value)


# domain model implementation


class ConcreteDomainModel:
    def __init__(self):
        self.__logic_constant = 1

    def domain_logic(self, input_value: int) -> int:
        return input_value + self.__logic_constant


# entry point of your application

container = Container()
container.register(DomainModel, value=ConcreateDomainModel())

# view layer handling

controller = container.resolve(Controller)
result = controller.handler(1)
print(result)
```

In this situation, protocol `DomainModel` doesn't hold implementation details, only interface.
Using 

```
container.register(DomainModel, value=ConcreateDomainModel())
```

we're guiding the resolver to use instance of `ConcreateDomainModel` in case someone asks
for `DomainModel`.

## Docs

 - [Clean architecture introduction (draft version)](docs/introduction.md)
