import requests
PARAMS = {
    'user_id': '21594050',
    'v': '5.131',
    'access_token': '10b2e4aa6f4f0c3bd87b2c80c189218bc7044b56de0b20d83cd2b7da410075759f8900a9ae3dda615830e',
    'fields': 'city ,sex, bdate, relation'
}
r = requests.post('https://api.vk.com/method/users.get', params = PARAMS)
target_user_info = r.json()['response'][0]


