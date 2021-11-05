from typing import Any, Callable, Generic, Protocol, TypeVar

from ..container import Container

T = TypeVar("T")


class Celery(Generic[T], Protocol):
    def task(self, fn: Callable[..., T]) -> Callable[..., T]:
        raise NotImplementedError


def celery_task(celery: Celery[T], container: Container) -> Callable[[Callable[..., Any]], Callable[..., T]]:
    def decorator(fn: Callable[..., Any]) -> Callable[..., T]:
        return celery.task(container.inject(fn))

    return decorator
