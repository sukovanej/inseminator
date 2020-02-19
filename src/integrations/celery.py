from typing import TypeVar, Protocol, Callable


from ..container import Container


T = TypeVar("T")


class Celery(Protocol):
    def task(self, fn: Callable[..., T]) -> T:
        ...


def celery_task(celery: Celery, container: Container) -> Callable:
    def decorator(fn: Callable) -> Callable:
        return celery.task(container.inject(fn))

    return decorator
