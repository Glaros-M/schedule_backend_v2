import datetime

from pydantic import BaseModel

import logging

logger = logging.getLogger("INFO")


class Root(BaseModel):
    timetable: list["Timetable"]


class Timetable(BaseModel):
    week_number: int
    date_start: str
    date_end: str
    groups: list["Groups"]


class Groups(BaseModel):
    # id: int
    group_name: str
    course: int
    days: list["Days"] | None = None

    def __repr__(self):
        s = f"{self.group_name}\n"
        for day in self.days:
            s += "\t\t" + str(day) + "\n"
        return s

    def __str__(self):
        return self.__repr__()


class Days(BaseModel):
    # id: int
    weekday: int
    lessons: list["Lessons"] | None = None

    def __repr__(self):

        s = f"{self.weekday}\n"
        if self.lessons:
            for lesson in self.lessons:
                s += "\t\t\t" + str(lesson) + "\n"
        else:
            s += "\t\t\tNo lessons"
        return s

    def __str__(self):
        return self.__repr__()


class Lessons(BaseModel):
    # id: int
    subject: str  # Название предмета
    type: str  # Тип занятия. "лек.", "лаб.", "прак."
    subgroup: int  # Подгруппа 0-вся группа, 1 - первая, 2 - вторая
    time_start: str | datetime.time  # Вот тут возможно словарь с соотношением номера пары и времени
    time_end: str | datetime.time
    time: int  # Порядковый номер пары
    week: int  # Номер недели от начала года, вродебы (?)
    date: str  # Дата занятия
    teachers: list["Teachers"]
    auditories: list["Auditories"]

    def get_str_teachers(self) -> str:
        s = ""
        for teach in self.teachers:
            s += str(teach) + " "
        return s

    def get_str_auditories(self) -> str:
        s = ""
        for aud in self.auditories:
            s += str(aud) + " "
        return s

    def __repr__(self):
        s = f"{self.time_start}-{self.subject} {self.type} {self.subgroup} п.г.\n"
        for teach in self.teachers:
            s += "\t\t\t\t" + str(teach) + "\n"
        for aud in self.auditories:
            s += "\t\t\t\t" + str(aud) + "\n"
        return s

    def __str__(self):
        return self.__repr__()


class Teachers(BaseModel):
    # id: int
    teacher_name: str  # "Вакансия" или "Фамилия И.О."

    def __repr__(self):
        return f"{self.teacher_name}"

    def __str__(self):
        return self.__repr__()


class Auditories(BaseModel):
    # id: int
    auditory_name: str  # "201к/7к" или "Спортзал Гл.к."

    def __repr__(self):
        return f"{self.auditory_name}"

    def __str__(self):
        return self.__repr__()


def get_data_from_file(path: str) -> list[Root]:
    with open(path, encoding="utf8") as file:
        data = file.read()

    new_roots = []
    n = 1
    for part in data.split('}\n{'):

        if part[0]!= "{":
            part = '{' + part
        if part[-2]!= '}':
            part = part + '}'
        try:
            #print(part)
            root = Root.parse_raw(part)
            new_roots.append(root)
        except Exception as e:
            # TODO: Какие тут могут быть ошибки? УКАЗАТЬ КОНКРЕТНО
            logger.exception(f"Exception in new_models.get_data_from_file {path=}, line={n}\n excp = {e}")
        n += 1
        #new_roots.append(root)
    return new_roots



Lessons.update_forward_refs()
Days.update_forward_refs()
Groups.update_forward_refs()
Timetable.update_forward_refs()
Root.update_forward_refs()




if __name__ == "__main__":
    data = get_data_from_file("RaspisanieVO.json")
    print(len(data))
    #print(len(data[0].timetable))
    for d in data:
        print(len(d.timetable))