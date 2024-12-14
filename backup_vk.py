import requests
import configparser
from pprint import pprint

# api_key = 'dict.1.1.20241122T090405Z.c4d0e5f6d4c05169.3fc0db6773ad473bc6fa5b369cc22d5f6fadebe5'


config = configparser.ConfigParser()
config.read('settings.ini')

vk_token = config['Tokens']['vk_token']


class VK:
    def __init__(self, access_token, version='5.199'):
        self.base_address = 'https://api.vk.com/method/'
        self.access_token = access_token
        self.version = version
        self.params = {
            'access_token': access_token,
            'v': version
        }

    def get_user_photos(self, id_user):
        url = f'{self.base_address}photos.get'
        params = {'owner_id': id_user, 'album_id': 'wall'}
        params.update(self.params)
        response = requests.get(url, params=params)
        return response.json()


class VKPhoto:
    def __init__(self, access_token, user_id, version='5.199'):
        self.user_id = user_id
        self.vk = VK(access_token, version)

    def __enter__(self):
        response = self.vk.get_user_photos(self.user_id)
        return response['response']['items']

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Перестал работать контекстный менеджер')


with VKPhoto(vk_token, '207129311') as photos:
    # print(photos)
    for photo_item in photos:
        print(photo_item['sizes'])


print('Программа работает дальше')


# vk = VK(vk_token)
# pprint(vk.get_user_photos('207129311'))
