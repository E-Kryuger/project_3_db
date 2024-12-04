def prepare_employers_data_to_insert(employers_data: list[dict]) -> list[dict]:
    """Подготавливает данные о сотрудниках к сохранению в БД"""
    prepared_data = []

    for employer_data in employers_data:
        # Извлечение нужных значений
        employer_id = employer_data["id"]
        employer_name = employer_data["name"]
        description = employer_data.get("description")
        site_url = employer_data.get("site_url")
        hh_url = employer_data["alternate_url"]
        area_id = employer_data["area"]["id"]

        # Хранение выбранных значений в виде словаря
        prepared_data.append(
            {
                "employer_id": employer_id,
                "employer_name": employer_name,
                "description": description,
                "site_url": site_url,
                "hh_url": hh_url,
                "area_id": area_id,
            }
        )

    return prepared_data


def prepare_vacancies_data_to_insert(vacancies_data: list[dict]) -> tuple[list[dict], list[dict]]:
    """Подготавливает данные о вакансиях к сохранению в БД"""
    prepared_areas_data = []
    prepared_vacancies_data = []

    for vacancy_data in vacancies_data:
        # Данные для таблицы areas
        area_id = vacancy_data["area"]["id"]
        area_name = vacancy_data["area"]["name"]
        area_dict = {"area_id": area_id, "area_name": area_name}

        if area_dict not in prepared_areas_data:
            prepared_areas_data.append(area_dict)

        # Данные для таблицы vacancies
        vacancy_id = vacancy_data["id"]
        vacancy_name = vacancy_data["name"]

        salary = vacancy_data["salary"]
        from_ = salary.get("from")
        to_ = salary.get("to")
        if from_ and to_:
            salary = round((from_ + to_) / 2)
        else:
            salary = from_ if from_ else to_

        vacancy_url = vacancy_data["alternate_url"]
        employer_id = vacancy_data["employer"]["id"]

        # Хранение выбранных значений в виде словаря
        vacancy_dict = {
            "vacancy_id": vacancy_id,
            "vacancy_url": vacancy_url,
            "vacancy_name": vacancy_name,
            "salary": salary,
            "area_id": area_id,
            "employer_id": employer_id,
        }

        if vacancy_dict not in prepared_vacancies_data:
            prepared_vacancies_data.append(vacancy_dict)

    return prepared_areas_data, prepared_vacancies_data
