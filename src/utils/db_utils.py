import psycopg2


def create_database(params: dict, db_name: str = "company_jobs_db") -> None:
    """Создает базу данных и необходимые таблицы в ней"""
    # Подсоединение к БД postgres
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    # Удаление создаваемой БД, если она уже была создана
    cur.execute(f"DROP DATABASE IF EXISTS {db_name};")
    # Создание БД
    cur.execute(f"CREATE DATABASE {db_name}")

    # Закрытие курсора и соединения
    cur.close()
    conn.close()

    # Присоединение к созданной БД
    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            # Словарь для создания таблиц
            create_table_queries = {
                "areas": "area_id INTEGER PRIMARY KEY, area_name VARCHAR(200)",
                "employers": (
                    "employer_id INTEGER PRIMARY KEY, employer_name VARCHAR(200) NOT NULL,"
                    "description TEXT, site_url VARCHAR(200), hh_url VARCHAR(200),"
                    "area_id INTEGER REFERENCES areas(area_id)"
                ),
                "vacancies": (
                    "vacancy_id INTEGER PRIMARY KEY, vacancy_name VARCHAR(200),"
                    "salary INTEGER, vacancy_url VARCHAR(200),"
                    "area_id INTEGER REFERENCES areas(area_id),"
                    "employer_id INTEGER REFERENCES employers(employer_id)"
                ),
            }

            # Создание таблиц
            for table_name, table_attributes in create_table_queries.items():
                cur.execute(f"CREATE TABLE {table_name} ({table_attributes});")

    conn.close()


def insert_into_db(
    areas_dict: list[dict],
    employers_dict: list[dict],
    vacancies_dict: list[dict],
    params: dict,
    db_name: str = "company_jobs_db",
) -> None:
    """Добавляет данные в БД"""
    # Присоединение к созданной БД
    conn = psycopg2.connect(dbname=db_name, **params)
    conn.autocommit = True
    cur = conn.cursor()

    # Табличные данные
    tables_names = ("areas", "employers", "vacancies")
    tables_data = (areas_dict, employers_dict, vacancies_dict)

    # Заполнение таблиц
    for i, table_records in enumerate(tables_data):
        table_name = tables_names[i]
        for table_record in table_records:
            # Получение заголовков и значений
            table_headers = list(table_record.keys())
            record_values = list(table_record.values())

            # Формирование строк заголовков и плейсхолдеров
            headers = ", ".join(table_headers)
            placeholders = ", ".join(["%s"] * len(table_headers))

            # Запрос на заполнение таблицы
            cur.execute(f"INSERT INTO {table_name} ({headers}) VALUES ({placeholders});", record_values)

    # Закрытие курсора и соединения
    cur.close()
    conn.close()
