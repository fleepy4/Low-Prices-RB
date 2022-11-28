import datetime


def hello_text():
    hours = datetime.datetime.now().hour
    if 6 > hours >= 0:
        return "Доброй ночи!"
    elif 12 > hours >= 6:
        return "Доброе утро!"
    elif 18 > hours >= 12:
        return "Добрый день!"
    elif 24 > hours >= 18:
        return "Добрый вечер!"