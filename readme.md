# Container

[![codecov](https://codecov.io/gh/sukovanej/container/branch/master/graph/badge.svg)](https://codecov.io/gh/sukovanej/container)

Python library for type-based dependency injection

*Under development*

## Installation

*Not published yet, you can build yourself at the moment*

## Usage

You start by defining *container* of your dependencies. Whenever you want the container to resolve a dependency 
it uses the container to search for existing objects and a resolver automatically creates desired dependencies.

```Python
from container import Container

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


# entry point of you application

container = Container()

# view layer handling

controller = container.resolve(Controller)
result = controller.handler(1)
print(result)
```
