from typing import Optional

import psycopg2


class DBManager:
    """Класс для работы с существующей БД"""

    def __init__(self, params: dict, db_name: str = "company_jobs_db") -> None:
        """Конструктор для инициализации объекта, работающего с БД"""
        self.__params = params
        self.__db_name = db_name

    def _execute_query(self, query: str, query_values: Optional[tuple] = None) -> list[tuple]:
        """Подключается к БД и выполняет запрос"""
        with psycopg2.connect(dbname=self.__db_name, **self.__params) as conn:
            with conn.cursor() as cur:
                cur.execute(query=query, vars=query_values)
                fetched = cur.fetchall()

        conn.close()
        if isinstance(fetched, list):  # Проверка для mypy
            return fetched
        return [()]

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """Получает список всех компаний и количество вакансий у каждой компании"""
        query = """
            SELECT employers.employer_name, COUNT(*)
            FROM vacancies
            INNER JOIN employers USING(employer_id)
            GROUP BY employer_name
            ORDER BY COUNT(*) DESC;
            """
        return self._execute_query(query)

    def get_all_vacancies(self) -> list[tuple]:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию"""
        query = """
            SELECT employers.employer_name, vacancy_name, salary, vacancy_url
            FROM vacancies
            INNER JOIN employers USING(employer_id)
            ORDER BY salary DESC;
            """
        return self._execute_query(query)

    def get_avg_salary(self) -> list[tuple]:
        """Получает среднюю зарплату по всем вакансиям"""
        query = "SELECT AVG(salary) FROM vacancies;"
        return self._execute_query(query)

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """Получает список вакансий с зарплатой выше средней"""
        query = """
            SELECT vacancy_name, salary, vacancy_url
            FROM vacancies
            WHERE salary > (SELECT AVG(salary) FROM vacancies)
            ORDER BY salary DESC;
            """
        return self._execute_query(query)

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """Получает список всех вакансий, в названии которых содержится переданное в метод слово"""
        keyword = keyword.strip()
        if not keyword:
            raise ValueError("Слово, по которому должны выводиться вакансии, не было передано в метод объекта")
        kw_lower = f"%{keyword.lower()}%"
        kw_capitalize = f"%{keyword.capitalize()}%"

        query = """
            SELECT vacancy_name, salary, vacancy_url
            FROM vacancies
            WHERE vacancy_name LIKE %s
               OR vacancy_name LIKE %s
            ORDER BY salary DESC;
            """
        return self._execute_query(query, query_values=(kw_lower, kw_capitalize))
