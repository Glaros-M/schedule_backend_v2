import db
import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
import logging
# from sqlite3 import OperationalError
from sqlalchemy.exc import OperationalError

logger = logging.getLogger("INFO")


def _get_today_week() -> int:
    day = int(datetime.date.today().strftime("%j"))
    return day//7


def get_groups_list() -> list[str]:
    logger.debug("get_groups_list()")
    week = _get_today_week()
    session = Session(db.engine)
    stmt = select(db.Timetable).where(db.Timetable.week_number == week)
    try:
        timetable_list = session.scalars(stmt)
    except OperationalError as e:
        logger.error(f"Ошибка обращения к БД!!!\n {e}")
        return []
    groups_list = []
    for timetable in timetable_list:
        # print('\n'*5)
        # print(timetable.name)
        for group in timetable.groups:
            groups_list.append(group.group_name)
            # print(group.group_name)
    session.close()
    return groups_list


def get_lessons_for_group_and_date(group_name: str, date: str) -> list[db.Lesson]:
    """
    date in strftime("%d-%m-%Y")
    """

    session = Session(db.engine)
    #logging.error(f"{datetime.datetime.now()}  создали подключение для {date}")
    stmt2 = select(db.Group.id).where(db.Group.group_name == group_name)
    gr_id = session.scalars(statement=stmt2).all()
    #logging.error(f"{datetime.datetime.now()}  выполнили первый запрос")
    stmt = select(db.Lesson).where(db.Lesson.date == date)\
        .where(db.Lesson.group_id.in_(gr_id)).order_by(db.Lesson.time)
    
    lessons = session.scalars(stmt).all()
    #logging.error(f"{datetime.datetime.now()}  выполнили второй запрос")
    # TODO: Возвращаемый тип у запроса отличается от List[lesson]
    lesson_list = []
    for lesson in lessons:
        lesson_list.append(lesson)
    return lesson_list


def is_group_exists(group_name: str) -> bool:
    #logging.debug(f"{datetime.datetime.now()}  Вызов проверки существования группы")
    session = Session(db.engine)
    stmt1 = select(db.Timetable.id).where(db.Timetable.week_number == _get_today_week())
    try:
        ids = session.scalars(stmt1).all()
    except OperationalError as e:
        logger.error(f"Ошибка обращения к БД!!!\n {e}")
        return False
    stmt2 = select(db.Group.id).where(db.Group.group_name == group_name).\
        where(db.Group.timetable_id.in_(ids))
    group = session.scalars(stmt2).first()
    session.close()
    if group:
        return True
    return False


def is_teacher_exists(teacher: str) -> bool:
    teacher_list = get_teachers_list()
    if teacher.strip() in teacher_list:
        return True
    return False


def get_teachers_list() -> list[str]:
    logger.debug("get_groups_list()")
    session = Session(db.engine)
    stmt = select(db.Lesson.teachers).group_by(db.Lesson.teachers)
    try:
        teachers_list = session.scalars(stmt)
    except OperationalError as e:
        logger.error(f"Ошибка обращения к БД!!!\n {e}")
        return []
    new_teacher_list = []
    for teacher in teachers_list:
        if not "Вакансия" in teacher:
            new_teacher_list.append(teacher.strip())
    return new_teacher_list


def get_lessons_for_teacher_and_date(teacher: str, date: str) -> list[(db.Lesson, str)]:
    """
    date in strftime("%d-%m-%Y")
    """

    session = Session(db.engine)

    stmt = select(db.Lesson, db.Group.group_name).where(db.Lesson.date == date)\
        .where(db.Lesson.teachers.like(f"%{teacher}%")).where(db.Lesson.group_id == db.Group.id)\
        .order_by(db.Lesson.time)

    lessons = session.execute(stmt).all()

    lesson_list = []
    for lesson in lessons:
        lesson_list.append(lesson)
    return lesson_list


if __name__ == "__main__":
    """group_name = "ИС1-221-ОТ"
    l = get_lessons(group_name)
    for les in l:
        print(les.date, les.time)
        
        Бородина В.В.
        Ребрищева М.Г.
        """
    is_teacher_exists("")