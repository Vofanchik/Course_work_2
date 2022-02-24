import requests
from datetime import date

def calculate_age(born):
    born = born.split('.')
    today = date.today()
    return today.year - int(born[2]) - ((today.month, today.day) < (int(born[1]), int(born[0])))

def city_search(city, access_token):
    PARAMS = {
        'v': '5.131',
        'q': f'{city}',
        'access_token': f'{access_token}',
        'country_id': '1'
    }
    r = requests.post('https://api.vk.com/method/database.getCities', params = PARAMS)
    return r.json()['response']['items'][0]

def get_user_info(user_id, access_token):
    PARAMS = {
        'user_id': f'{user_id}',
        'v': '5.131',
        'access_token': f'{access_token}',
        'fields': 'city ,sex, bdate'
    }

    r = requests.post('https://api.vk.com/method/users.get', params = PARAMS)

    target_user_info = r.json()['response'][0]


    if 'bdate' in target_user_info.keys() and len(target_user_info['bdate'])>6:
            pass
    else:
        return target_user_info
        # target_user_info['bdate']= input('Не достаточно данных. Введите дату рождения в формате дд.мм.гггг ')


    if 'city' in target_user_info.keys():
        pass
    else:
        return target_user_info
        # target_user_info['city']= city_search(input('Не достаточно данных. Введите город '), access_token)


    return match_search(target_user_info, access_token)


def match_search(target_user_info, access_token):
    PARAMS = {
        'v': '5.131',
        'access_token': f'{access_token}',
        'fields': 'city ,sex, bdate, relation',
        'has_photo': '1',
        # 'count': '10',
        'is_closed': 'False',
        'sort': '0'
        }

    PARAMS['city'] = target_user_info['city']['id']
    if target_user_info['sex'] == 2:
        PARAMS['sex'] = 1
    else:
        PARAMS['sex'] = 2

    PARAMS['status'] = 6
    PARAMS['age_from'] = calculate_age(target_user_info['bdate'])
    PARAMS['age_to'] = calculate_age(target_user_info['bdate'])

    r = requests.post('https://api.vk.com/method/users.search', params = PARAMS)

    target_persons = []

    for targets in r.json()['response']['items']:
        target_persons.append(targets['id'])

    return urls_photo_search(target_persons, access_token)


def urls_photo_search(target_persons, access_token):

    list_of_all_photo_urls = []

    for pers in target_persons:

        PARAMS = {
            'owner_id': f'{pers}',
            'v': '5.131',
            'access_token': f'{access_token}',
            'extended': 'True',
            'album_id': 'profile'
        }

        r = requests.post('https://api.vk.com/method/photos.get', params=PARAMS)

        try:
            # list_of_all_photo_urls.append(pers)
            id_photos = []
            photos_win = sorted(r.json()['response']['items'], key=lambda x: x['likes']['count'])[-1:-4:-1]
            photos_win_urls = []
            for pho in photos_win:
                photos_win_urls.append(pho['sizes'][-1]['url'])
            id_photos.append(pers)
            id_photos.append(photos_win_urls)
        except:
            continue

        list_of_all_photo_urls.append(id_photos)

    return list_of_all_photo_urls








