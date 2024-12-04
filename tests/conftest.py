import pytest

from src.get_api.api_hh import HeadHunterAPI


@pytest.fixture
def api_hh() -> HeadHunterAPI:
    """
    Фикстура, содержащая объект класса HeadHunterAPI.
    """
    return HeadHunterAPI()


@pytest.fixture
def vacancy_hh_data() -> list[dict]:
    """
    Фикстура, содержащая данные о вакансиях полученные от API HeadHunter.
    """
    return [
        {
            "id": "107948630",
            "name": "Верстальщик",
            "area": {"id": "1", "name": "Москва"},
            "salary": {"from": 50000, "to": 50000},
            "alternate_url": "https://hh.ru/vacancy/107948630",
            "employer": {"id": "1122462", "name": "Skyeng"},
        },
        {
            "id": "107948629",
            "name": "Верстальщик",
            "area": {"id": "2", "name": "Санкт-Петербург"},
            "salary": {"from": 50000, "to": 50000},
            "alternate_url": "https://hh.ru/vacancy/107948629",
            "employer": {"id": "1122462", "name": "Skyeng"},
        },
        {
            "id": "107741634",
            "name": "Куратор образовательных чатов (бадди) по истории и обществознанию",
            "area": {"id": "1", "name": "Москва"},
            "salary": {"from": 40000, "to": 56000},
            "alternate_url": "https://hh.ru/vacancy/107741634",
            "employer": {"id": "1122462", "name": "Skyeng"},
        },
    ]


@pytest.fixture()
def emp_ids() -> list[str]:
    """
    Фикстура, содержащая ID работодателей.
    """
    return ["1122462", "10621831"]


@pytest.fixture
def employers_hh_data() -> list[dict]:
    """
    Фикстура, содержащая данные о работодателях полученные от API HeadHunter.
    """
    return [
        {
            "id": "1122462",
            "name": "Skyeng",
            "description": "Skyeng — это вкладываться в онлайн-образование.",
            "site_url": "http://skyeng.ru",
            "alternate_url": "https://hh.ru/employer/1122462",
            "area": {"id": "1", "name": "Москва"},
        },
        {
            "id": "10621831",
            "name": "JetBrain (OOO Секвойя Консалт)",
            "description": "Динамично развивающаяся межрегиональная компания.",
            "site_url": "",
            "alternate_url": "https://hh.ru/employer/10621831",
            "area": {"id": "88", "name": "Казань"},
        },
    ]


@pytest.fixture
def prepared_vacancy_data() -> list[dict]:
    """
    Фикстура, содержащая подготовленные данные о вакансиях.
    """
    return [
        {
            "vacancy_id": "107948630",
            "vacancy_url": "https://hh.ru/vacancy/107948630",
            "vacancy_name": "Верстальщик",
            "salary": 50000,
            "area_id": "1",
            "employer_id": "1122462",
        },
        {
            "vacancy_id": "107948629",
            "vacancy_url": "https://hh.ru/vacancy/107948629",
            "vacancy_name": "Верстальщик",
            "salary": 50000,
            "area_id": "2",
            "employer_id": "1122462",
        },
        {
            "vacancy_id": "107741634",
            "vacancy_url": "https://hh.ru/vacancy/107741634",
            "vacancy_name": "Куратор образовательных чатов (бадди) по истории и обществознанию",
            "salary": 48000,
            "area_id": "1",
            "employer_id": "1122462",
        },
    ]


@pytest.fixture
def prepared_areas_data() -> list[dict]:
    """
    Фикстура, содержащая подготовленные данные о городах.
    """
    return [{"area_id": "1", "area_name": "Москва"}, {"area_id": "2", "area_name": "Санкт-Петербург"}]


@pytest.fixture
def prepared_employers_data() -> list[dict]:
    """
    Фикстура, содержащая подготовленные данные о работодателях.
    """
    return [
        {
            "employer_id": "1122462",
            "employer_name": "Skyeng",
            "description": "Skyeng — это вкладываться в онлайн-образование.",
            "site_url": "http://skyeng.ru",
            "hh_url": "https://hh.ru/employer/1122462",
            "area_id": "1",
        },
        {
            "employer_id": "10621831",
            "employer_name": "JetBrain (OOO Секвойя Консалт)",
            "description": "Динамично развивающаяся межрегиональная компания.",
            "site_url": "",
            "hh_url": "https://hh.ru/employer/10621831",
            "area_id": "88",
        },
    ]
