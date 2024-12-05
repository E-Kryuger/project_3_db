from typing import Generator

import requests

from src.get_api.get_vacancies_api import GetVacanciesAPI


class HeadHunterAPI(GetVacanciesAPI):
    """
    Класс для работы с API HeadHunter.
    Позволяет получать данные о вакансиях и работодателях.
    """

    def __init__(self) -> None:
        """
        Конструктор для инициализации объекта, работающего с API.
        """
        self.__vacancies_url: str = "https://api.hh.ru/vacancies"
        self.__employers_url: str = "https://api.hh.ru/employers"
        self.__headers: dict[str, str] = {"User-Agent": "HH-User-Agent"}
        self.__params: dict[str, str | int] = {
            "page": 0,
            "per_page": 100,
            "only_with_salary": "true",
            "currency": "RUR",
            "employer_id": 0,
        }
        self.__vacancies_items: list[dict] = []
        self.__employers_data: list[dict] = []

    def _connect_to_api(self) -> bool:
        """Проверка успешности подключения"""
        try:
            # Выполнение запроса к вакансиям
            response = requests.get(url=self.__vacancies_url, headers=self.__headers)
            response.raise_for_status()

            # Выполнение запроса к работодателям
            response = requests.get(url=self.__employers_url, headers=self.__headers)
            response.raise_for_status()

        except requests.RequestException as err:
            print(f"Ошибка при запросе к API: {err}")
            return False
        else:
            return True

    @staticmethod
    def __validate_id(emp_id: int) -> int:
        """Валидация ID компании:
        - проверяет, является ли переданное значение положительным целым числом"""
        if isinstance(emp_id, int) and emp_id > 0:
            return emp_id
        else:
            return 0

    def __check_employer_id(self, emp_id: int) -> bool:
        """Проверка существования ID компании"""
        try:
            url = f"{self.__employers_url}/{emp_id}"
            response = requests.get(url, headers=self.__headers)
            response.raise_for_status()
        except requests.RequestException as err:
            print(f"Ошибка при запросе к API: {err}")
            return False
        else:
            return True

    def __get_vacancies_by_id(self, employer_id: int) -> None:
        """Поиск вакансий у конкретной компании по ее ID"""
        # Настройка параметров для поиска вакансий
        self.__params["employer_id"] = employer_id
        self.__params["page"] = 0  # Обнуление страницы

        # Поиск вакансий
        while True:
            try:
                response = requests.get(self.__vacancies_url, headers=self.__headers, params=self.__params)
                response.raise_for_status()
            except requests.RequestException as err:
                print(f"Ошибка при запросе к API: {err}")
                break
            else:
                data = response.json()
                self.__vacancies_items.extend(data["items"])

                if self.__params["page"] >= data["pages"] - 1:
                    break

                self.__params["page"] += 1

    def __get_employer_by_id(self, employer_id: int) -> None:
        """Получение данных о компании по ее ID"""
        employer_url = f"{self.__employers_url}/{employer_id}"
        try:
            response = requests.get(employer_url, headers=self.__headers)
            response.raise_for_status()
        except requests.RequestException as err:
            print(f"Ошибка при запросе к API: {err}")
        else:
            data = response.json()
            self.__employers_data.append(data)

    def get_data(
        self, emp_ids: list[int] | Generator[int, None, None]
    ) -> tuple[list, list] | tuple[list[dict], list[dict]]:
        """Получение данных о выбранных компаниях от API HeadHunter"""
        if self._connect_to_api():
            for employer_id in emp_ids:
                # Проверка ID
                employer_id = self.__validate_id(employer_id)
                if not employer_id or not self.__check_employer_id(employer_id):
                    continue

                # Получение данных
                self.__get_employer_by_id(employer_id)
                self.__get_vacancies_by_id(employer_id)

        return self.__employers_data, self.__vacancies_items
