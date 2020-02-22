from typing import Protocol

from inseminator import Container


class DomainModel(Protocol):
    def domain_logic(self, input_value: int) -> int:
        raise NotImplementedError


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


# entry point of you application

container = Container()
container.register(DomainModel, value=ConcreteDomainModel())

# view layer handling

controller = container.resolve(Controller)
result = controller.handler(1)
print(result)
