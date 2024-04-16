import random

import aiohttp
from bs4 import BeautifulSoup
from requests import RequestException

from config import PICTURES_URL, SCHEDULE_URL


class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        print(f'Возникла ошибка при загрузке страницы {url}')


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        raise ParserFindTagException(error_msg)
    return searched_tag


def get_date(soup):
    date_str = soup.find('h4', {'class': 'card-title'})
    if date_str:
        date_arr = date_str.text.strip().split('\r\n')
        date_arr = [string.strip() for string in date_arr]
        ret_str = ' '.join(date_arr)
        return ret_str
    return None


def get_time(soup):
    time_str = soup.find('td', {'class': 'time'})
    if time_str:
        time_arr = time_str.text.strip().split('\r\n')
        time_arr = [string.strip() for string in time_arr]
        ret_str = ' - '.join(time_arr)
        return ret_str
    return None


def get_discipline(soup):
    disciplines = soup.find_all('td', {'class': 'diss'})
    ret_val = []
    lesson = []
    if disciplines:
        for diss in disciplines:
            lesson_arr = diss.text.strip().split('\r\n')
            for les_str in lesson_arr:
                if len(les_str.strip()) > 1:
                    lesson.append(les_str.strip())
            if lesson:
                ret_val.append(' '.join(lesson))
        return ' '.join(ret_val)
    return None


def get_auditory(soup):
    auditories = soup.find_all('td', {'class': 'who-where'})
    ret_val = []
    places = []
    if auditories:
        for auditory in auditories:
            room_arr = auditory.text.strip().split('\n')
            for room in room_arr:
                if len(room.strip()) > 1:
                    places.append(room.strip())
            if places:
                ret_val.append(' '.join(places))
        return ' '.join(ret_val)
    return None


async def async_http_get(url):
    print(url)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                response = await resp.read()
        return response.decode('utf-8')
    except Exception as e:
        return None


async def get_random_picture():
    response = await async_http_get(PICTURES_URL)

    if response is None:
        return None

    soup = BeautifulSoup(response, features='lxml')
    card_blocks = soup.find_all('div', {'class': 'fotocontext'})
    rand_card_block = card_blocks[random.randint(0, len(card_blocks) - 1)]
    picture = rand_card_block.find('a')['href']
    print(picture)
    return picture


async def read_schedule(group='ВМ2233'):

    response = await async_http_get(f'{SCHEDULE_URL}{group}')

    if response is None:
        return {}

    soup = BeautifulSoup(response, features='lxml')
    card_blocks = soup.find_all('div', {'class': 'card-block'})[:3]
    schedule = {}
    for card_block in card_blocks:
        table = card_block.find('table', {'class': 'table'})
        tr = table.find_all('tr')
        date = get_date(card_block)
        rasp_list = []
        for rasp in tr:
            time = get_time(rasp)
            if time:
                discipline = get_discipline(rasp)
                auditory = get_auditory(rasp)
                if discipline and auditory:
                    rasp_list.append([time, discipline, auditory])
        schedule[date] = rasp_list
    return schedule


def parser():
    schedule = read_schedule()
    for dat in schedule.items():
        print(f'{dat[0]} ')
        for lesson in dat[1]:
            print(' '.join(lesson))

    # pdf_a4_tag = find_tag(table_tag,
    #                       'a',
    #                       {'href': re.compile(r'.+pdf-a4\.zip$')}
    #                       )



if __name__ == '__main__':
    # parser()
    get_random_picture()
