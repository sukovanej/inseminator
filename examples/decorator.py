from inseminator import Container, Depends


class Dependency:
    def __init__(self):
        self.x = 1


container = Container()


@container.inject
def my_handler(input_value: int, dependency: Dependency = Depends(Dependency)):
    return input_value + dependency.x
