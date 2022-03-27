import requests
from json.decoder import JSONDecodeError
import datetime

ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da' \
               '72454d235c274f1a2be5f45ee711'
API_URL = 'https://api.vk.com/method'
V = '5.81'


def calc_age(uid):
    try:
        payload = {'access_token': ACCESS_TOKEN, 'user_ids': uid, 'v': V}
        r = requests.get(f'{API_URL}/users.get', params=payload)
        ids = r.json()['response'][0]['id']
    except (JSONDecodeError, IndexError, KeyError):
        ids = None

    try:
        payload = {'access_token': ACCESS_TOKEN, 'user_id': ids, 'v': V,
                   'fields': 'bdate'}
        r = requests.get(f'{API_URL}/friends.get', params=payload)
        friends = (r.json()['response']['items'])
    except (JSONDecodeError, KeyError):
        friends = None

    if not friends:
        return
    years = {}
    for friend in friends:
        bdate = friend.get('bdate')
        if not bdate or len(bdate.split('.')) != 3:
            continue
        age = datetime.date.today().year - int(bdate.split('.')[2])
        years.setdefault(age, 0)
        years[age] += 1

    return sorted(years.items(), key=lambda x: (x[1], -x[0]), reverse=True)


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)

######################################################################################################################
# Решение задания по requests от преподавателей
######################################################################################################################
# from json.decoder import JSONDecodeError
# from datetime import datetime
# import requests
#
# ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da' \
#                '72454d235c274f1a2be5f45ee711'
# API_URL = 'https://api.vk.com/method'
# V = '5.71'
#
#
# def get_user_id(uid):
#     users_get = '{}/users.get'.format(API_URL)
#     resp = requests.get(users_get, params={
#         'access_token': ACCESS_TOKEN,
#         'user_ids': uid,
#         'v': V
#     })
#     try:
#         resp = resp.json()
#         resp = resp['response']
#         user = resp[0]
#         return user['id']
#     except (JSONDecodeError, IndexError, KeyError):
#         pass
#
#
# def get_friends(user_id):
#     friends_get = '{}/friends.get'.format(API_URL)
#     resp = requests.get(friends_get, params={
#         'access_token': ACCESS_TOKEN,
#         'user_id': user_id,
#         'fields': 'bdate',
#         'v': V
#     })
#     try:
#         resp = resp.json()
#         resp = resp['response']
#         return resp['items']
#     except (JSONDecodeError, KeyError):
#         pass
#
#
# def calc_age(uid):
#     user_id = get_user_id(uid)
#     if user_id is None:
#         return
#
#     friends = get_friends(user_id)
#     if friends is None:
#         return
#
#     years = {}
#     cur_year = datetime.now().year
#
#     for friend in friends:
#         bdate = friend.get('bdate')
#         if not bdate:
#             continue
#
#         bdate = bdate.split('.')
#         if len(bdate) != 3:
#             continue
#
#         year = int(bdate[2])
#         diff = cur_year - year
#         years.setdefault(diff, 0)
#         years[diff] += 1
#
#     return sorted(years.items(), key=lambda v: (v[1], -v[0]), reverse=True)
