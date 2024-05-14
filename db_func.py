from create_connection import cursor, conn
import pytz
from datetime import datetime
from geopy.exc import GeocoderUnavailable
from geopy.geocoders import Nominatim
import uuid


def add_user(id_tg: str, city_id: str):
    cursor.execute(f'INSERT INTO users (id_tg, city_id) VALUES (?, ?)', (id_tg, city_id, ))
    conn.commit()


def check_user(id_tg: str):
    cursor.execute('SELECT city_id FROM users WHERE id_tg = ?', (id_tg,))
    user = cursor.fetchall()
    if user:
        return True
    else:
        return False


def get_user_city(id_tg: str):
    cursor.execute('SELECT city_id FROM users WHERE id_tg = ?', (id_tg,))
    city_id = cursor.fetchall()[0][0]
    return city_id


def add_city(city: str):
    city_id = 'c' + str(uuid.uuid4()).replace('-', '')
    cursor.execute(f'INSERT INTO cities (city, city_id) VALUES (?, ?)', (city, city_id, ))
    conn.commit()
    return city_id


def check_city(city: str):
    cursor.execute('SELECT city_id FROM cities WHERE city = ?', (city,))
    user = cursor.fetchall()
    if user:
        return True
    else:
        return False


def get_cities():
    cursor.execute('SELECT * FROM cities')
    cities = cursor.fetchall()
    res = []
    for city in cities:
        res.append({'city': city[0], 'city_id': city[1]})
    return res


def add_device(city_id: str):
    device_id = 'c' + str(uuid.uuid4()).replace('-', '')
    cursor.execute(f'INSERT INTO devices (device_id, city_id, t, g, s, latitude, longitude, time) VALUES (?, ?, ?, ?, ?, ?, '
                   f'?, ?)',
                   (device_id, city_id, 'нет данных', 'нет данных', 'нет данных', 'нет данных', 'нет данных', 'нет данных'))

    conn.commit()
    return device_id


def set_data_to_device(device_id: str, t: str, g: str, s: str, latitude: str, longitude: str):
    try:
        tz = pytz.timezone('Europe/Moscow')
        dtime = datetime.now(tz)
        time = f'{dtime.hour}:{dtime.minute}'
        cursor.execute(f'UPDATE devices SET t = ?, g = ?, s = ?, latitude = ?, longitude = ?, time = ? WHERE '
                       f'device_id = ?',
                    (t, g, s, latitude, longitude, time, device_id))
        conn.commit()
        return 'OK'
    except Exception as ex:
        print(ex)
        return 'ERROR'


def get_city_by_id(city_id: str):
    cursor.execute(f'SELECT city FROM cities WHERE city_id = ?', (city_id,))
    res = cursor.fetchall()
    return res[0][0]


def get_data_from_device(device_id: str):
    cursor.execute('SELECT * FROM devices WHERE device_id = ?', (device_id,))
    device = cursor.fetchall()
    device = device[0]
    res = {'device_id': device[0],
           'city_id': device[1],
           't': device[2],
           'g': device[3],
           's': device[4],
           'latitude': device[5],
           'longitude': device[6],
           'time': device[7]}
    return res


def change_city(id_tg: str, city_id: str):
    cursor.execute('UPDATE users SET city_id = ? WHERE id_tg = ?', (city_id, id_tg))
    conn.commit()


def get_devices(city_id: str):
    cursor.execute('SELECT device_id, latitude, longitude FROM devices WHERE city_id = ?', (city_id,))
    devices = cursor.fetchall()
    res = []
    for device in devices:
        if device[1] != 'нет данных':
            res.append({'device_id': device[0], 'address': get_addr([device[1], device[2]])})
    return res


def is_admin(id_tg: str):
    cursor.execute('SELECT * FROM admins WHERE id_tg = ?', (id_tg,))
    res = cursor.fetchall()
    if res:
        return True
    else:
        return False


def get_addr(location: list, test=0) -> str:
    if test == 0:
        try:
            geo_loc = Nominatim(user_agent='GetLoc')
            loc_name = geo_loc.reverse(location)
            res = loc_name.address.split(',')
            return f'{res[1]} {res[0]}'
        except GeocoderUnavailable:
            return 'Ошибка'
    else:
        geo_loc = Nominatim(user_agent='GetLoc')
        loc_name = geo_loc.reverse(location)
        return loc_name.address.split(',')


