import requests
import json
import datetime
from Lesson import Lesson

Days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
week = []


def parse_all_schedule(group_name):
    clean_schedule()
    try:
        my_json = requests.post('https://miet.ru/schedule/data?group=' + group_name).text
        global ready_json
        ready_json = json.loads(my_json)
    except ValueError:
        my_json = requests.post('https://miet.ru/schedule/data?group=МП-10').text
        ready_json = json.loads(my_json)

    curr_week = int((datetime.datetime.now() - (datetime.datetime.strptime("2016-08-29", "%Y-%m-%d"))).days / 7)
    while curr_week > 4:
        curr_week -= 4

    mo = []
    tu = []
    we = []
    th = []
    fr = []
    sa = []

    for qu in ready_json['Data']:
        if qu['Day'] == 1 and qu['DayNumber'] == curr_week:
            mo.append(Lesson(qu['Class']['Name'], qu['Room']['Name'], qu['Time']['Time']))
        if qu['Day'] == 2 and qu['DayNumber'] == curr_week:
            tu.append(Lesson(qu['Class']['Name'], qu['Room']['Name'], qu['Time']['Time']))
        if qu['Day'] == 3 and qu['DayNumber'] == curr_week:
            we.append(Lesson(qu['Class']['Name'], qu['Room']['Name'], qu['Time']['Time']))
        if qu['Day'] == 4 and qu['DayNumber'] == curr_week:
            th.append(Lesson(qu['Class']['Name'], qu['Room']['Name'], qu['Time']['Time']))
        if qu['Day'] == 5 and qu['DayNumber'] == curr_week:
            fr.append(Lesson(qu['Class']['Name'], qu['Room']['Name'], qu['Time']['Time']))
        if qu['Day'] == 6 and qu['DayNumber'] == curr_week:
            sa.append(Lesson(qu['Class']['Name'], qu['Room']['Name'], qu['Time']['Time']))

    week.append(mo)
    week.append(tu)
    week.append(we)
    week.append(th)
    week.append(fr)
    week.append(sa)

    return week


def parse_week():
    ret_message = ''
    try:
        if week:
            for i, day in enumerate(week):
                if len(day) > 0:
                    ret_message = ret_message + Days[i] + '\n'
                for j in range(8):
                    for lesson in week[i]:
                        if int(lesson.number[0]) == j:
                            ret_message = ret_message + '•' + lesson.number + ' | ' + lesson.name + ' | ' + lesson.room + '\n'
                if len(day) > 0: ret_message = ret_message + '------------------------------\n'
    except IndexError:
        ret_message = 'Ошибка. Слишком частые запросы. Мой ноутбук с этим не справляется :с'

    return ret_message


def parse_today():
    ret_message = ''
    today = datetime.datetime.now().weekday()
    try:
        for i, day in enumerate(week):
            if i == today and len(day) > 0:
                ret_message = ret_message + Days[i] + '\n'
                for j in range(8):
                    for lesson in week[i]:
                        if int(lesson.number[0]) == j:
                            ret_message = ret_message + '•' + lesson.number + ' | ' + lesson.name + ' | ' + lesson.room + '\n'
        if not ret_message: ret_message = 'Выходной'
    except IndexError:
        ret_message = 'Ошибка. Слишком частые запросы. Мой ноутбук с этим не справляется :с'

    return ret_message


def parse_tomorrow():
    ret_message = ''
    today = datetime.datetime.now().weekday()
    try:
        for i, day in enumerate(week):
            if i == today + 1 and len(day) > 0:
                ret_message = ret_message + Days[i] + '\n'
                for j in range(8):
                    for lesson in week[i]:
                        if int(lesson.number[0]) == j:
                            ret_message = ret_message + '•' + lesson.number + ' | ' + lesson.name + ' | ' + lesson.room\
                                          + '\n'
        if not ret_message:
            ret_message = 'Выходной'
    except IndexError:
        ret_message = 'Ошибка. Слишком частые запросы. Мой ноутбук с этим не справляется :с'

    return ret_message


def clean_schedule():
    week.clear()
