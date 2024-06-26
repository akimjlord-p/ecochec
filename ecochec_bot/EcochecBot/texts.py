from db_func import check_user
from db_func import get_user_city, get_city_by_id


def get_start_text(id_tg):
    if check_user(str(id_tg)):
        city_id = get_user_city(str(id_tg))
        city = str(get_city_by_id(str(city_id)))
        return f'Привет. Ну что, посмотрим как сегодня на улице в городе {city}?'
    else:
        return 'Привет. В каком городе ты живешь? Давай выберем твой город. Напиши - <b>выбрать город</b>'


def choose_city_switch():
    return 'Выберите город <-- Переключение страниц -->'


def admin_info():
    return ('Добавление новой аппаратной системы - <b>добавить устройство</b>\n'
            'Добавление нового города - <b>добавить город</b>\n'
            'Просмотр всех устройств в городе - <b>все устройства города</b>')


def set_city(city):
    return f'Вы установили город {city}'


def list_of_cities():
    return '<i>Список городов</i>'


def list_of_devices(city):
    return f'<i>Список устройств в городе <b>{city}</b></i>'


def choose_device_switch():
    return 'Выберите устройство <-- Переключение страниц -->'


def device_data(t, g, s, time, address, city):
    return (f'<ins>Адрес устройства</ins>: <b>{city} {address}</b>\n'
            f'<ins>Время последнего обновления</ins>: <b>{time}</b>\n'
            f'<ins>Температура</ins>: <b>{t}</b> C\n'
            f'<ins>Загрязненность воздуха</ins>: <b>{g}</b> <i>PPM</i>\n'
            f'<ins>Уровень шума</ins>: <b>{s} Дб</b>')


def info():
    return ('<b>Ecochec</b> - программно аппаратный комплекс,'
            'созданный для мониторинга эколоческой ситуации в городе')


def add_city(city, city_id):
    return f'Город <b>{city}</b> с id <b>{city_id}</b>успешно добавлен'


def error_address():
    return f'Произошла ошибка при получении адреса'


def error_city():
    return f'Город уже создан'
