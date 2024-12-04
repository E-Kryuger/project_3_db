from src.db_manager.db_manager import DBManager
from src.get_api.api_hh import HeadHunterAPI
from src.utils.data_utils import prepare_employers_data_to_insert, prepare_vacancies_data_to_insert
from src.utils.db_utils import create_database, insert_into_db
from src.utils.file_utils import config, employer_ids
from src.utils.interaction_utils import (LastRequestDate, does_db_exist, initialization_menu, main_menu,
                                         print_query_results)


def user_interaction() -> None:
    """
    Функция для взаимодействия с пользователем.
    """
    # Загрузка параметров соединения
    user_db_params = config()

    # Инициализация объекта и получение даты последнего запроса, если имеется
    request_date = LastRequestDate()
    last_date = request_date.get()

    # Проверка существования БД с информацией о вакансиях
    does_exist = does_db_exist(user_db_params)

    # Запуск меню инициализации, если данные в БД уже имеются
    user_choice = None
    if does_exist:
        user_choice = initialization_menu(last_date)

    # Заполнение БД новыми данными, если данных еще нет или если пользователь хочет получить новые данные
    if not does_exist or user_choice == "2":
        # Создание генератора, выдающего ID компаний
        id_generator = employer_ids()

        # Сохранение даты запроса
        request_date.save()

        # Выполнение запроса на получение данных от выбранных компаний
        print("\nЗагрузка вакансий...")
        api = HeadHunterAPI()
        employers_data, vacancies_data = api.get_data(id_generator)

        # Создание | пересоздание  БД
        create_database(params=user_db_params)

        # Подготовка данных к заполнению таблиц
        employers_data = prepare_employers_data_to_insert(employers_data)
        areas_data, vacancies_data = prepare_vacancies_data_to_insert(vacancies_data)

        # Вставка подготовленных данных в таблицы
        insert_into_db(areas_data, employers_data, vacancies_data, params=user_db_params)

    # Создание менеджера базы данных
    db_manager = DBManager(params=user_db_params)

    # Запуск главного меню
    while True:
        query_result = None
        user_choice = main_menu()

        if user_choice == "1":
            query_result = db_manager.get_companies_and_vacancies_count()

        elif user_choice == "2":
            query_result = db_manager.get_all_vacancies()

        elif user_choice == "3":
            query_result = db_manager.get_avg_salary()

        elif user_choice == "4":
            query_result = db_manager.get_vacancies_with_higher_salary()

        elif user_choice == "5":
            user_keyword = input("Слово, по которому будут выведены вакансии: ")
            try:
                query_result = db_manager.get_vacancies_with_keyword(user_keyword)
            except ValueError as error:
                print(error)
                continue

        elif user_choice == "6":
            print("\n=====================")
            print("Выход из программы")
            return None

        print_query_results(query_result, user_query=user_choice)


if __name__ == "__main__":
    user_interaction()
