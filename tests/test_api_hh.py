from unittest.mock import Mock, patch

import requests

from src.get_api.api_hh import HeadHunterAPI

API_VACANCIES_URL = "https://api.hh.ru/vacancies"
API_EMPLOYERS_URL = "https://api.hh.ru/employers"
HEADERS = {"User-Agent": "HH-User-Agent"}
PARAMS = {"page": 0, "per_page": 100, "only_with_salary": "true", "currency": "RUR", "employer_id": 0}


def test_init_object(api_hh: HeadHunterAPI) -> None:
    """
    Тест инициализации объекта класса HeadHunterAPI.

    :param hh_api: Инициализированный объект класса HeadHunterAPI.
    """
    assert api_hh._HeadHunterAPI__vacancies_url == API_VACANCIES_URL
    assert api_hh._HeadHunterAPI__employers_url == API_EMPLOYERS_URL
    assert api_hh._HeadHunterAPI__headers == HEADERS
    assert api_hh._HeadHunterAPI__params == PARAMS
    assert api_hh._HeadHunterAPI__vacancies_items == []
    assert api_hh._HeadHunterAPI__employers_data == []


@patch("src.get_api.api_hh.requests.get")
def test_connect_to_api_successful(mock_get: Mock, api_hh: HeadHunterAPI) -> None:
    """
    Тест положительного результата при проверке успешности подключения.

    :param mock_get: Mock объект для метода get.
    :param hh_api: Инициализированный объект класса HeadHunterAPI.
    """
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    response = api_hh._connect_to_api()
    assert response is True
    mock_get.assert_any_call(url=API_VACANCIES_URL, headers=HEADERS)
    mock_get.assert_any_call(url=API_EMPLOYERS_URL, headers=HEADERS)


@patch("src.get_api.api_hh.requests.get")
def test_connect_to_api_unsuccessful(mock_get: Mock, api_hh: HeadHunterAPI) -> None:
    """
    Тест отрицательного результата при проверке успешности подключения.

    :param mock_get: Mock объект для метода get.
    :param hh_api: Инициализированный объект класса HeadHunterAPI.
    """
    mock_get.side_effect = requests.RequestException("Ошибка при запросе к API")
    result = api_hh._connect_to_api()

    assert result is False
    mock_get.assert_called_once_with(url=API_VACANCIES_URL, headers=HEADERS)


def test_validate_correct_id(api_hh: HeadHunterAPI) -> None:
    """
    Тест валидации корректного ID.

    :param hh_api: Инициализированный объект класса HeadHunterAPI.
    """
    result = api_hh._HeadHunterAPI__validate_id(1122462)
    expected = 1122462

    assert result == expected


def test_validate_incorrect_id(api_hh: HeadHunterAPI) -> None:
    """
    Тест валидации некорректного ID.

    :param hh_api: Инициализированный объект класса HeadHunterAPI.
    """
    result = api_hh._HeadHunterAPI__validate_id(-222)
    expected = 0

    assert result == expected


@patch("src.get_api.api_hh.requests.get")
def test_existing_check_employer_id(mock_get: Mock, api_hh: HeadHunterAPI) -> None:
    """
    Тест положительной проверки существования ID компании.

    :param mock_get: Mock объект для метода get.
    :param hh_api: Инициализированный объект класса HeadHunterAPI.
    """
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    response = api_hh._HeadHunterAPI__check_employer_id(1122462)
    assert response is True
    mock_get.assert_called_once_with(f"{API_EMPLOYERS_URL}/1122462", headers=HEADERS)


@patch("src.get_api.api_hh.requests.get")
def test_non_existent_check_employer_id(mock_get: Mock, api_hh: HeadHunterAPI) -> None:
    """
    Тест отрицательной проверки существования ID компании.

    :param mock_get: Mock объект для метода get.
    :param hh_api: Инициализированный объект класса HeadHunterAPI.
    """
    mock_get.side_effect = requests.RequestException("Ошибка при запросе к API")
    result = api_hh._HeadHunterAPI__check_employer_id(999_999_999_999)

    assert result is False
    mock_get.assert_called_once_with(f"{API_EMPLOYERS_URL}/999999999999", headers=HEADERS)


@patch("src.get_api.api_hh.requests.get")
def test_get_vacancies_by_id(mock_get: Mock, api_hh: HeadHunterAPI, vacancy_hh_data: list[dict]) -> None:
    """
    Тест поиска вакансий у конкретной компании по ее ID.

    :param mock_get: Mock объект для метода get.
    :param hh_api: Инициализированный объект класса HeadHunterAPI.
    :param vacancy_hh_data: Данные полученные от API.
    """
    mock_response = Mock()
    mock_response.json.return_value = {"items": vacancy_hh_data, "pages": 1}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    params = PARAMS | {"employer_id": 1122462}
    api_hh._HeadHunterAPI__get_vacancies_by_id(1122462)

    assert api_hh._HeadHunterAPI__vacancies_items == vacancy_hh_data
    mock_get.assert_called_once_with(API_VACANCIES_URL, headers=HEADERS, params=params)


@patch("src.get_api.api_hh.requests.get")
def test_get_employer_by_id(mock_get: Mock, api_hh: HeadHunterAPI, employers_hh_data: list[dict]) -> None:
    """
    Тест получения данных о компании по ее ID.

    :param mock_get: Mock объект для метода get.
    :param hh_api: Инициализированный объект класса HeadHunterAPI.
    :param employers_hh_data: Данные полученные от API.
    """
    employer_hh_data = employers_hh_data[0]

    mock_response = Mock()
    mock_response.json.return_value = employer_hh_data
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    api_hh._HeadHunterAPI__get_employer_by_id(1122462)

    assert api_hh._HeadHunterAPI__employers_data == [employer_hh_data]
    mock_get.assert_called_once_with(f"{API_EMPLOYERS_URL}/1122462", headers=HEADERS)
