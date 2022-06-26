

import requests
from datetime import date
import json

class YaUploader:
    '''Создание класса пользователя Яндекс Диск по его токену'''
    url = 'https://cloud-api.yandex.net/v1/disk/resources/'
    def __init__(self, token: str):
        self.token = token

    def upload_url(self, folder, foto_name, foto_url):
        '''Метод загружает файл на Я.Д. по ссылке с заданным именем в конкретную папку'''
        url_upload_url = self.url + 'upload'
        path_folder = 'disk:/' + folder
        path_file = path_folder + '/' + foto_name
        params = {'path': path_file, 'url': foto_url}
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {self.token}'}
        response = requests.post(url_upload_url, headers=headers, params=params)
        response.raise_for_status   
        if response.status_code in range(200, 203):  
            print(f'Фотография "{path_file}" загружена (код ответа - {response.status_code}).')
        else:
            print(f'Ошибка (код ответа - {response.status_code}), обратитесь к разработчику.')
        return path_folder

    def upload_name_likes(self, folder, foto_list):
        set = input('\nВы хотите загрузить все фотографии (нажмите ENTER),\nили какой-то их диапазон (введите любой симовл)?')
        if set != '':
            set = True
            while set:
                start = int(input('\nВведите номер первой загружаемой фотографии: '))
                finish = int(input('\nВведите номер последней загружаемой фотографии: '))
                all = len(foto_list['response']['items'])
                if start < 1 or start > finish or finish > all:
                    print('\nВы ввели неверный диапазон.')
                else:
                    print('\nДиапазон принят, начнем загрузку.')
                    set = False
        else:
            start = 1
            finish = len(foto_list['response']['items'])
        print('\nЗагрузка файлов на Я.Д. с именами по количеству лайков:')
        foto_name_list = []        
        for i in range(start - 1, finish):
            foto_url = foto_list['response']['items'][i]['sizes'][-1]['url']
            foto_name = str(foto_list['response']['items'][i]['likes']['count']) + '.jpg'
            if foto_name in foto_name_list:
                foto_name  = str(foto_list['response']['items'][i]['likes']['count']) + ' ' + str(date.today()) + '.jpg'
            foto_name_list.append(foto_name)            
            path_folder = self.upload_url(folder, foto_name, foto_url)
        return path_folder
                        
    def create_folder(self):
        '''Метод создает папку на Я.Д.'''
        set = None
        while set == None:        
            folder = input('\nВведите имя новой папки: ')
            if folder == '':
                print('\nВы не ввели имя новой папки.')
                continue
            params = {'path': folder}
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {self.token}'}
            response = requests.put(self.url, headers=headers, params=params)
            response.raise_for_status
            if response.status_code == 409:
                print(f'\nПапка "{folder}" уже существует, начните заново и введите другое имя папки.')  
                continue
            elif response.status_code == 201:
                print(f'\nПапка "{folder}" создана (код ответа - {response.status_code}).')
                return folder
            else:
                print(f'\nНестандартный код ответа {response.status_code}, обратитесь к разработчику.')
                continue 
      
    def file_data(self, path_folder):
        '''Метод запрашивает информацию с Я.Д. о всех файлах в папке'''
        print(f'\nПолучение спика файлов из "{path_folder}".')
        headers = {'Accept': 'application/json',  'Authorization': f'OAuth {self.token}'}
        params = {'path': path_folder}
        response = requests.get(self.url, headers=headers, params=params)
        response.raise_for_status   
        if response.status_code in range(200, 203):  
            print(f'\nСписок файлов из папки: "{path_folder}", получен (код ответа - {response.status_code}).')
        else:
            print(f'\nОшибка (код ответа - {response.status_code}), обратитесь к разработчику.')            
        return response.json()


    def foto_file_upload(self, file_data):
        print('\nФормирование файла "foto_file_upload.json" с информацией по сохраненным фотографиям.')
        foto_files = []
        for i in range(len(file_data['_embedded']['items'])):
            foto_file = {}
            foto_file['file_name'] = file_data['_embedded']['items'][i]['name']
            foto_file['size'] = file_data['_embedded']['items'][i]['size']
            foto_files.append(foto_file)    
        with open('foto_file_upload.json', 'w') as f:
            json.dump(foto_files, f)
        print('\nФайл сформирован и сохранен в текущей папке.')
    
    def token_check(self):
        '''Метод проверяет токен Я.Д.'''
        headers = {'Accept': 'application/json',  'Authorization': f'OAuth {self.token}'}
        params = {'path': 'disk:/'}
        response = requests.get(self.url, headers=headers, params=params)
        response.raise_for_status
        return response.status_code  
    