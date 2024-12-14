import requests
import configparser

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
        pass


def get_max_size_photo(dict_photos):
    max_size = 0
    max_photo = 0
    for i in range(len(dict_photos)):
        photo_size = dict_photos[i].get('width') * dict_photos[i].get('height')
        if photo_size > max_size:
            max_size = photo_size
            need_elem = i
    return dict_photos[max_photo].get('url'), dict_photos[max_photo].get('type')


if __name__ == '__main__':

    with VKPhoto(vk_token, '207129311') as photos:
        print(len(photos))
        for photo_item in photos:
            # print(photo_item['sizes'])
            print(get_max_size_photo(photo_item['sizes']))
