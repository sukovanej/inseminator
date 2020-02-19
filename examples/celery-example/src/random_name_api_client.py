import requests


class RandomNameApiClient:
    def __init__(self) -> None:
        self.__url = "https://uinames.com/api/"

    def get_random_name(self) -> str:
        response = requests.get(self.__url, params={"gender": "female"})
        response.raise_for_status()

        return response.json()["name"]
