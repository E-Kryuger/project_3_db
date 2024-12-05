from datetime import datetime

import psycopg2
from tabulate import tabulate

from config.paths import CONFIG_DIR, create_filepath


def print_query_results(query_result: list | list[tuple], user_query: str) -> None:
    """
    Вспомогательная функция для вывода результата запроса в консоль.

    :param query_result: Результат запроса к БД.
    :param user_query: Номер выбранного запроса.
    """
    count_records = len(query_result)
    table_headers = {
        "1": ("Название компании", "Количество вакансий"),
        "2": ("Название компании", "Название вакансии", "Зарплата", "Ссылка на вакансию"),
        "3": ("Параметр", "Значение"),
        "4": ("Название вакансии", "Зарплата", "Ссылка на вакансию"),
        "5": ("Название вакансии", "Зарплата", "Ссылка на вакансию"),
    }

    print("\n== Просмотр данных ==")
    if user_query == "3":
        avg_salary = round(query_result[0][0])
        query_result = [("Средняя зарплата", avg_salary)]
    if user_query in "245" and count_records > 50:
        print("Всего вакансий:", count_records)
        print("1. Показать весь список")
        print("2. Показать список Топ-N вакансий")
        print("=====================")
        while True:
            user_choice = input("Выберите пункт меню (1-2): ").strip().replace(".", "")
            if user_choice == "1":
                print("\n=== Просмотр всех ===")
                break
            if user_choice == "2":
                while True:
                    n_str = input("Какой Топ-N хотите получить?: ").strip()
                    if n_str.isdigit() and int(n_str) < count_records:
                        n = int(n_str)
                        print(f"\n=== Топ-{n} ===")
                        query_result = query_result[:n]
                        break
                break

    print(tabulate(query_result, headers=table_headers[user_query], tablefmt="fancy_grid"))
    print("=====================")


class LastRequestDate:
    """
    Вспомогательный класс для работы с датой последнего запроса.
    """

    def __init__(self, filename: str = "RequestDate.txt") -> None:
        """
        Конструктор для инициализации объекта с заданным именем файла.

        :param filename: Имя файла, в котором хранится дата последнего запроса (опционально).
        """
        self.__filepath = create_filepath(CONFIG_DIR, filename)

    def save(self) -> None:
        """
        Сохранение даты запроса в файл.
        """
        date_request = datetime.now().strftime("%d.%m.%y")
        with open(self.__filepath, "w") as file:
            file.write(date_request)

    def get(self) -> str:
        """
        Получение даты запроса из файла в виде строки.
        Если дата запроса неизвестна, возвращается пустая строка.

        :return: Последняя дата запроса.
        """
        try:
            with open(self.__filepath, "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return ""


def initialization_menu(last_date: str) -> str:
    """
    Вспомогательная функция на случай, если данные уже имеются в БД.

    :return: Выбор пользователя.
    """
    print("=== Меню инициализации ===")
    print(f"Имеются данные от {last_date if last_date else 'неизвестной даты'}")
    print("1. Работать с имеющимися данными\n" "2. Сделать новый поиск вакансий")
    print("==========================")
    while True:
        user_choice = input("Выберите пункт меню (1-2): ").strip().replace(".", "")
        if user_choice in "12":
            return user_choice


def main_menu() -> str:
    """
    Вспомогательная функция для выбора запроса пользователем.

    :return: Выбранный номер запроса.
    """
    print("\n=== Главное меню ===")
    print(
        "1. Получить список всех компаний и количество вакансий у каждой компании\n"
        "2. Получить список всех вакансий с указанием названия компании, названия вакансии "
        "и зарплаты и ссылки на вакансию\n"
        "3. Получить среднюю зарплату по вакансиям\n"
        "4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
        "5. Получить список всех вакансий, в названии которых содержится переданное в метод слово\n"
        "6. Выйти"
    )
    print("====================")
    while True:
        user_choice = input("Выберите пункт меню (1-6): ").strip().replace(".", "")
        if user_choice in "123456":
            return user_choice


def does_db_exist(params: dict) -> bool:
    """Вспомогательная функция для проверки наличия данных в БД"""
    try:
        with psycopg2.connect(dbname="company_jobs_db", **params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM employers;")
                fetched = cur.fetchall()

                return bool(fetched)

    except (psycopg2.OperationalError, psycopg2.errors.UndefinedTable):
        return False
