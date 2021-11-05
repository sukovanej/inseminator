from inseminator.container import Container
from inseminator.decorator import Depends
from inseminator.integrations.celery import celery_task


def test_dummy_celery_injector():
    container = Container()

    class Dependency:
        def __init__(self):
            self.x = 1

    class Celery:
        def task(self, fn):
            return fn

    celery = Celery()

    @celery_task(celery, container)
    def my_function(dependency: Dependency = Depends(Dependency)):
        return dependency.x

    assert my_function() == 1
