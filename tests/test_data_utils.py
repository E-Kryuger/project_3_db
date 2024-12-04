from src.utils.data_utils import prepare_employers_data_to_insert, prepare_vacancies_data_to_insert


def test_prepare_employers_data_to_insert(employers_hh_data: list[dict], prepared_employers_data: list[dict]) -> None:
    """
    Тест функции подготавливающей данные полученные от API к заполнению таблицы employers.

    :param employers_hh_data: Данные полученные от API.
    :param prepared_employers_data: Подготовленные данные.
    """
    result = prepare_employers_data_to_insert(employers_hh_data)
    expected = prepared_employers_data

    assert result == expected


def test_prepare_empty_employers_data_to_insert() -> None:
    """
    Тест функции подготавливающей данные полученные от API к заполнению таблицы employers.
    Тест проводится с пустыми данными полученными от API.
    """
    result = prepare_employers_data_to_insert([])
    assert result == []


def test_prepare_vacancies_data_to_insert_a(vacancy_hh_data: list[dict], prepared_areas_data: list[dict]) -> None:
    """
    Тест функции prepare_vacancies_data_to_insert на подготовку данных к заполнению таблицы areas.

    :param vacancy_hh_data: Данные полученные от API.
    :param prepared_areas_data: Подготовленные данные.
    """
    result = prepare_vacancies_data_to_insert(vacancy_hh_data)[0]
    expected = prepared_areas_data

    assert result == expected


def test_prepare_empty_vacancies_data_to_insert_a() -> None:
    """
    Тест функции prepare_vacancies_data_to_insert на подготовку данных к заполнению таблицы areas.
    Тест проводится с пустыми данными полученными от API.
    """
    result = prepare_vacancies_data_to_insert([])[0]
    assert result == []


def test_prepare_vacancies_data_to_insert_v(vacancy_hh_data: list[dict], prepared_vacancy_data: list[dict]) -> None:
    """
    Тест функции prepare_vacancies_data_to_insert на подготовку данных к заполнению таблицы vacancies.

    :param vacancy_hh_data: Данные полученные от API.
    :param prepared_vacancy_data: Подготовленные данные.
    :return:
    """
    result = prepare_vacancies_data_to_insert(vacancy_hh_data)[1]
    excepted = prepared_vacancy_data

    assert result == excepted


def test_prepare_empty_vacancies_data_to_insert_v() -> None:
    """
    Тест функции prepare_vacancies_data_to_insert на подготовку данных к заполнению таблицы vacancies.
    Тест проводится с пустыми данными полученными от API.
    """
    result = prepare_vacancies_data_to_insert([])[1]
    assert result == []
