from .cow_repository import CowRepository
from .models import Cow
from .random_name_api_client import RandomNameApiClient


class DomainLogic:
    def __init__(self, cow_repository: CowRepository, random_name_api_client: RandomNameApiClient) -> None:
        self.__cow_repository = cow_repository
        self.__random_name_api_client = random_name_api_client

    def inseminate_cow(self, number_of_cows_to_inseminate: int) -> None:
        print(f"Inseminating {number_of_cows_to_inseminate} cows.")
        cows = self.__cow_repository.get_not_pregnant_cows(number_of_cows_to_inseminate)

        for cow in cows:
            self.__cow_repository.inseminate_cow(cow)
            print(f"{cow.name} is now inseminated.")

        self.__cow_repository.commit()

    def add_random_cows(self, number_of_cows_to_add: int) -> None:
        for cow in range(number_of_cows_to_add):
            name = self.__random_name_api_client.get_random_name()
            cow = self.__cow_repository.add_cow(name=name)
            print(f"{cow.name} added to the farm.")

        self.__cow_repository.commit()
