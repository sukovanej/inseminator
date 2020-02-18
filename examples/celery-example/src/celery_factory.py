from celery import Celery

from .configuration import Configuration


def celery_factory(configuration: Configuration) -> Celery:
    return Celery("tasks", broker=configuration.redis_connection_string)
