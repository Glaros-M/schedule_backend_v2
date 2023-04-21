import datetime

import sqlalchemy

import db
import models

from sqlalchemy.orm import Session
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import delete

import logging
import os

logger = logging.getLogger("INFO")


def create_db_timetable_from_json_model(timetable: models.Timetable, entry_point: str) -> db.Timetable:
    """ Создаем обьект расписания на неделю из JSON представления

    :param timetable: new_models.Timetable - pydantic представление JSON недели
    :param entry_point: str - строка, обозначающая тип загружаемого файла (по структуре УМУ) СПО, ВО, Заочка
    :return: new_db.Timetable - обьект базы данных, конкретная неделя
    """
    logger.debug("Creating db model from JSON")
    group_list: list[db.Group] = []
    for group in timetable.groups:

        lesson_list: list[db.Lesson] = []
        for day in group.days:

            if day.lessons:
                for lesson in day.lessons:
                    db_lesson = db.Lesson(
                        subject=lesson.subject,
                        type=lesson.type,
                        subgroup=lesson.subgroup,
                        time_start=lesson.time_start,
                        time_end=lesson.time_end,
                        time=lesson.time,
                        date=lesson.date,
                        weekday=day.weekday,
                        teachers=lesson.get_str_teachers(),
                        auditories=lesson.get_str_auditories(),
                    )
                    lesson_list.append(db_lesson)

        db_group = db.Group(
            group_name=group.group_name,
            course=group.course,
            lessons=lesson_list
        )
        group_list.append(db_group)

    db_timetable = db.Timetable(
        entry_point=entry_point,
        name=str(timetable.week_number) + entry_point,
        week_number=timetable.week_number,
        date_start=timetable.date_start,
        date_end=timetable.date_end,
        date_update=datetime.datetime.now(),
        groups=group_list
    )
    return db_timetable


def is_timetable_exists(entry_point: str, week_number: int, engine: sqlalchemy.Engine) -> bool:
    """
    Проверяет существование в базе данных конкретной недели расписания с учетом точки загрузки
    :param engine: Подключение к БД
    :param entry_point: str - точка загрузки
    :param week_number: int - номер недели от начала года
    :return: bool - 1 если расписание существует
    """
    stmt = select(db.Timetable).where(db.Timetable.week_number == week_number) \
        .where(db.Timetable.entry_point == entry_point)

    session = Session(engine)

    result = session.execute(stmt).first()
    session.close()
    if result:
        return True
    return False


def upload_timetable_to_db(timetable: db.Timetable, engine: sqlalchemy.Engine):
    """
    Загрузка недели расписания в БД. Если неделя существует, происходит каскадное удаление.
    :param timetable:
    :param engine:
    :return:
    """
    logger.debug("upload model to db")
    session = Session(engine)
    if is_timetable_exists(entry_point=timetable.entry_point, week_number=timetable.week_number, engine=engine):
        stmt = select(db.Timetable).where(db.Timetable.entry_point == timetable.entry_point) \
            .where(db.Timetable.week_number == timetable.week_number)
        res = session.scalars(stmt).all()
        for r in res:
            session.delete(r)
    try:
        session.add(timetable)
    except Exception as e:
        print(e)
        session.rollback()
    session.commit()


def upload_file(path: str, entry_point: str, engine: sqlalchemy.Engine = db.engine) -> str:
    """

    :param path:
    :param entry_point:
    :param engine:
    :return:
    """
    logger.info(f"Uploading file: {path}, entry point: {entry_point}")
    models_list: list[models.Root] = models.get_data_from_file(path)
    updated_weeks = "Обновлены следующие недели:<br/>"
    for root in models_list:
        for timetable in root.timetable:
            timetable_db = create_db_timetable_from_json_model(timetable=timetable, entry_point=entry_point)
            updated_weeks += f"Неделя №{timetable_db.week_number} с {timetable_db.date_start} по {timetable_db.date_end}<br/>"
            upload_timetable_to_db(timetable_db, engine)
    return updated_weeks


def write_log_to_db(log: db.Log, engine: sqlalchemy.Engine = db.engine):
    session = Session(engine)
    try:
        session.add(log)
    except:
        session.rollback()
        raise
    session.commit()
    session.close()


def save_file(file) -> str | None:
    file_path = f"files/{file.filename}"
    file_exists = os.path.exists(file_path)
    if file_exists:
        os.remove(file_path)
    try:
        file.save(file_path)
    except Exception as e:
        logger.error(f"ОШИБКА СОХРАНЕНИЯ ФАЙЛА: {e}")
        return None
    return file_path


if __name__ == "__main__":
    # pass
    logger.setLevel(logging.DEBUG)

    info_console_handler = logging.StreamHandler()
    info_formatter = logging.Formatter(f"%(levelname)s %(asctime)s %(module)s > %(message)s ")

    info_console_handler.setFormatter(info_formatter)

    logger.addHandler(info_console_handler)
    db.create_db(engine=db.engine)
    logger.info("UPLOAD FILE")
    upload_file(path="Raspisanie SPO.json", entry_point="spo", engine=db.engine)
    upload_file(path="Raspisanie VO.json", entry_point="vo", engine=db.engine)
    upload_file(path="Raspisanie ZO.json", entry_point="z", engine=db.engine)
