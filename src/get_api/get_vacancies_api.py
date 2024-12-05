from abc import ABC, abstractmethod
from typing import Generator


class GetVacanciesAPI(ABC):
    """Абстрактный класс для работы с API HeadHunter"""

    @abstractmethod
    def _connect_to_api(self) -> bool:
        """Абстрактный метод проверки успешности подключения к API"""
        pass

    @abstractmethod
    def get_data(
        self, emp_ids: list[int] | Generator[int, None, None]
    ) -> tuple[list, list] | tuple[list[dict], list[dict]]:
        """Абстрактный метод получения данных от API HeadHunter"""
        pass
