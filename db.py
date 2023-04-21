from sqlalchemy.orm import Session

from sqlalchemy import create_engine

from sqlalchemy import ForeignKey, BigInteger, Integer, String

from sqlalchemy.orm import DeclarativeBase

from typing import List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import select
import datetime
from config import CONNECTION_STRING

# engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)  # БД в оперативке
# engine_lite = create_engine("sqlite+pysqlite:///sqlite3.db", echo=False, max_overflow=100)  # БД в локальная sqlite
engine = create_engine(CONNECTION_STRING,
                       echo=False,
                       max_overflow=100
                       )


class Base(DeclarativeBase):
    pass


class Timetable(Base):
    __tablename__ = "timetable"
    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    entry_point: Mapped[str]
    name: Mapped[str]
    week_number: Mapped[int]
    date_start: Mapped[str]
    date_end: Mapped[str]
    date_update: Mapped[str] = mapped_column(String, nullable=True)
    groups: Mapped[List["Group"]] = relationship(cascade="all, delete")


class Group(Base):
    __tablename__ = "group"
    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    group_name: Mapped[str]
    course: Mapped[int]
    timetable_id: Mapped[int] = mapped_column(ForeignKey("timetable.id"))
    lessons: Mapped[List["Lesson"]] = relationship(cascade="all, delete")


class Lesson(Base):
    __tablename__ = "lesson"
    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    subject: Mapped[str]
    type: Mapped[str]
    subgroup: Mapped[int]
    time_start: Mapped[str]
    time_end: Mapped[str]
    time: Mapped[int]
    date: Mapped[str]
    teachers: Mapped[str]
    auditories: Mapped[str]
    weekday: Mapped[int]
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))


class Log(Base):
    __tablename__ = "log"
    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True, autoincrement=True)
    datetime: Mapped[datetime.datetime]
    module: Mapped[str]
    message: Mapped[str]


def create_db(engine):
    Base.metadata.create_all(engine)


def migrate_data(engine_from, engine_to):
    """
    Тупой прямой перенос данных из одной базы данных в другую построчно и последовательно.
    Пересоздание обьектов на каждом этапе вызвано появлением ошибки SQLAlchemy -
    Обьект принадлежит другой сессии или что то типа того.
    """
    create_db(engine_to)
    session_lite = Session(engine_from)
    stmt1 = select(Timetable)

    timetables = session_lite.scalars(stmt1).all()
    print(f"{len(timetables)=}")

    session_postgre = Session(engine_to)

    for timetable in timetables:

        g_list = []
        for group in timetable.groups:

            l_list = []
            for lesson in group.lessons:
                print("lesson")
                l1 = Lesson(
                    subject=lesson.subject,
                    type=lesson.type,
                    subgroup=lesson.subgroup,
                    time_start=lesson.time_start,
                    time_end=lesson.time_end,
                    time=lesson.time,
                    date=lesson.date,
                    teachers=lesson.teachers,
                    auditories=lesson.auditories,
                    weekday=lesson.weekday,
                    group_id=lesson.group_id
                )
                l_list.append(l1)

            print(group.group_name)
            g1 = Group(
                group_name=group.group_name,
                course=group.course,
                timetable_id=group.timetable_id,
                lessons=l_list
            )
            g_list.append(g1)

        print("timetable", '*' * 10)
        t1 = Timetable(
            entry_point=timetable.entry_point,
            name=timetable.name,
            week_number=timetable.week_number,
            date_start=timetable.date_start,
            date_end=timetable.date_end,
            date_update=None,
            groups=g_list
        )
        session_postgre.add(t1)

    session_postgre.commit()
    session_postgre.close()


if __name__ == "__main__":
    pass
    #create_db(engine)

    #migrate_data(engine_old, engine_new)
