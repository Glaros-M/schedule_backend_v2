import random

import requests


def groups():
    prod_groups = requests.get("https://vgltuapi.ru/groups").text
    preprod_groups = requests.get("https://vgltuapi.ru/debug/groups").text

    print(preprod_groups == prod_groups)

    groups_list = ["АС2-221-ОБ",
                   "ОП2-221-ОБ",
                   "РЭ2-221-ОБ",
                   "НТТС2-221-ОС",
                   "АС2-192-ОБ",
                   "ЛА2-212-ЗБ",
                   "ЗЛ2-191-ЗБ",
                   "ИС1-227-ОТ"]

    for group in groups_list:
        prod_schedule = requests.get(f"https://vgltuapi.ru/schedule?group_name={group}").text
        preprod_schedule = requests.get(f"https://vgltuapi.ru/debug/schedule?group_name={group}").text
        print(group, prod_schedule == preprod_schedule)


def teachers():
    prod_teachers = set(requests.get("https://vgltuapi.ru/teachers").json()["teachers"])
    preprod_teachers = set(requests.get("https://vgltuapi.ru/debug/teachers").json()["teachers"])

    print(preprod_teachers == prod_teachers)
    count = 0
    for i in range(10):
        teacher = random.choice(list(prod_teachers))
        prod_schedule = requests.get(f"https://vgltuapi.ru/teacher?teacher_name={teacher}").text
        preprod_schedule = requests.get(f"https://vgltuapi.ru/debug/teacher?teacher_name={teacher}").text

        if not prod_schedule == preprod_schedule:
            count += 1
            print(teacher, prod_schedule == preprod_schedule)
    print("ИТОГО: ", count)


if __name__ == "__main__":
    teachers()
    groups()
