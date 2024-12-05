import os
from unittest.mock import Mock, mock_open, patch

import pytest

from src.utils.file_utils import config, employer_ids


@patch("src.utils.file_utils.ConfigParser.read")
@patch("src.utils.file_utils.ConfigParser.items")
@patch("src.utils.file_utils.ConfigParser.has_section")
def test_config_successful(mock_has_section: Mock, mock_items: Mock, mock_read: Mock) -> None:
    """
    Тест успешного получения параметров соединения с базой данных.

    :param mock_has_section: Mock объект для замены метода has_section.
    :param mock_items: Mock объект для замены метода items.
    :param mock_read: Mock объект для замены метода read.
    """
    expected = {"host": "localhost", "port": "5432", "user": "postgres", "password": "12345"}

    mock_path_exists = Mock(return_value=True)
    os.path.exists = mock_path_exists
    mock_items.return_value = expected
    mock_has_section.return_value = True

    result = config()
    assert result == expected


def test_config_file_not_found() -> None:
    """
    Тест получения параметров из несуществующего файла.
    """
    mock_path_exists = Mock(return_value=False)
    os.path.exists = mock_path_exists
    with pytest.raises(FileNotFoundError) as exception_info:
        config()

    assert str(exception_info.value) == "Файл 'database.ini' не найден"


@patch("builtins.open", new_callable=mock_open)
@patch("json.load")
def test_employer_ids(mock_json_load: Mock, mock_file_open: Mock) -> None:
    """
    Тест получения ID работодателей из json-файла.

    :param mock_json_load: Mock объект для замены функции json.load.
    :param mock_file_open: Mock объект для замены функции open.
    """
    mock_path_exists = Mock(return_value=True)
    os.path.exists = mock_path_exists
    mock_json_load.return_value = [{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"}]

    result = [emp_id for emp_id in employer_ids()]
    expected = [1, 2]

    assert result == expected
