import requests

class VkUser:
    '''Создание класса пользователя ВК по его токену'''
    url = 'https://api.vk.com/method/'
    def __init__(self, token: str, version):
        self.params = {'access_token': token, 'v': version}

    def user_get_id(self):
        '''Метод получает id и scree_name пользователя по токену или id'''
        user_get_id_url = self.url + 'users.get'        
        user = requests.get(user_get_id_url, params={**self.params, **{'fields': 'screen_name'}}).json()
        if 'error' in user:            
            return None, 'Неверный токен ВКонтакте. Введите правильный токен.'        
        else:
            return user['response'][0]['id'], user['response'][0]['screen_name']

    def get_foto(self, user_id):
        '''Метод получает массив объектов фотографий пользователя по его id'''
        get_foto_url = self.url + 'photos.get'
        get_foto_params = {'owner_id': user_id, 'extended': 1, 'album_id': 'profile'}
        foto_list = requests.get(get_foto_url, params={**self.params, **get_foto_params}).json()
        print('Всего можно скачать фотографий:', foto_list['response']['count'])
        return foto_list


    def user_seach(self, user_data):
        user_search_url = self.url + 'users.get'
        user_search_params = {'user_ids': user_data, 'fields': 'screen_name'}
        user = requests.get(user_search_url, params={**self.params, **user_search_params}).json()
        if user['response'] == []:            
            return        
        return user['response'][0]['id']
