from jinja2 import Environment, FileSystemLoader

import download_data

import datetime
import logging

""" 
Генерация представлений из данных. Необходимо прописать функцию для вызова - зависит от того как будет
                                                                                происходить вызов из API.
"""

env = Environment(
    loader=FileSystemLoader('./templates')
)

logger = logging.getLogger("INFO")

DAYS_OF_WEEK = {
    1: "Пн.",
    2: "Вт.",
    3: "Ср.",
    4: "Чт.",
    5: "Пт.",
    6: "Сб.",
    7: "Вс."
}


def get_table_by_teacher_name(teacher: str) -> str:
    if download_data.is_teacher_exists(teacher):
        return _render_table_by_teacher_name(teacher=teacher)
    return "<h2>Пожалуйста, введите корректно Фамилию и инициалы преподавателя или выберите из списка!</h2>"


def _render_table_by_teacher_name(teacher: str) -> str:
    # Почти идентично получению таблицы по имени группы. Возможно переделать?
    today = datetime.date.today()
    days_lessons_list = []
    for i in range(14):
        date = _format_date(today + datetime.timedelta(days=i))
        logger.debug(f'{date=}')
        day_lessons_group_name = download_data.get_lessons_for_teacher_and_date(teacher=teacher, date=date)
        day_lessons = []
        group_names = []
        for lesson, group_name in day_lessons_group_name:
            day_lessons.append(lesson)
            group_names.append(group_name)

        if len(day_lessons) > 0:
            days_lessons_list.append((day_lessons, len(day_lessons), date, group_names))
        else:
            days_lessons_list.append((None, 1, date, None))

    template = env.get_template('teacher_lessons.html')
    return template.render(days_lessons_list=days_lessons_list, days_name=DAYS_OF_WEEK)


def get_table_by_group_name(group_name: str) -> str:
    if download_data.is_group_exists(group_name):
        return _render_table_by_group_date(group_name=group_name)
    return "<h2>Пожалуйста, введите корректный номер группы или выберите из списка!</h2>"


def _render_table_by_group_date(group_name: str) -> str:
    today = datetime.date.today()
    days_lessons_list = []
    for i in range(14):
        date = _format_date(today + datetime.timedelta(days=i))
        logger.debug(f'{date=}')
        day_lessons = download_data.get_lessons_for_group_and_date(group_name=group_name, date=date)
        if len(day_lessons) > 0:
            days_lessons_list.append((day_lessons, len(day_lessons), date))
        else:
            days_lessons_list.append((None, 1, date))

    template = env.get_template('group_lessons.html')
    return template.render(days_lessons_list=days_lessons_list, days_name=DAYS_OF_WEEK)


def _format_date(date: datetime.date) -> str:
    """
    В JSON файлах даты проставлены в формате 1-04-2023 а не 01-04-2023
    """

    str = date.strftime("%d-%m-%Y")
    if str[0] == '0':
        return str[1:]
    return str


def get_upload_form(status: str | None = None, description: str | None = None, entry_point: str | None = None, file_name: str | None = None) -> str:
    template = env.get_template('upload_template.html')
    post_addr = "/upload_form"
    return template.render(post_addr=post_addr,
                           status=status,
                           description=description,
                           entry_point=entry_point,
                           file_name=file_name)


if __name__ == "__main__":
    f = open("teweeeeest.html", 'w', encoding='utf8')
    f.write(_render_table_by_group_date("ИС1-221-ОТ"))
    f.close()
