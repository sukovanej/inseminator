from inseminator import Container, Depends
from inseminator.integrations import celery_task

from .celery_factory import celery_factory
from .domain import DomainLogic

container = Container()
celery = container.resolve(celery_factory)


@celery_task(celery, container)
def inseminate(number_of_cows_to_inseminate: int, domain_logic: Depends(DomainLogic)) -> None:
    domain_logic.inseminate_cow(number_of_cows_to_inseminate)


@celery_task(celery, container)
def add_random_cows(number_of_cows_to_inseminate: int, domain_logic: Depends(DomainLogic)) -> None:
    domain_logic.add_random_cows(number_of_cows_to_inseminate)
