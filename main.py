
import configparser
import os
import vkuser
import ya_uploader
 
def create_config(path):
    'Создание config файла с данными пользователя'  
    file_exist = ''  
    if os.path.exists(path):
        file_exist = input('Обнаружен файл settings.ini, в котором могут храниться токены.\nХотите воспользоваться ими (введите любой символ), \nили ввести новые токены (нажмите ENTER)?\n')
        if file_exist != '':
            config = configparser.ConfigParser()
            config.read(path)
            token_vk = config['VK']['token']         
            vk_client = vkuser.VkUser(token_vk, '5.131')         
            token_yd = config['YD']['token']        
            uploader = ya_uploader.YaUploader(token_yd) 
            print('Давайте проверим эти токены.\n')      
            token_id, token_screen_name = vk_client.user_get_id()  
            if token_id == None:
                print(token_screen_name)
                file_exist = ''
            else:
                file_exist = True
                print('Токен ВКонтакте ОК.')
            token_yd_check = uploader.token_check()
            if token_yd_check == 401:
                print('\nНеверный токен ЯндексДиск. Введите правильный токен.\n') 
                file_exist = ''
            else:
                file_exist = True
                print('Токен ЯндексДиск ОК.')
      
    if file_exist == '':
        print('Необходимо ввести "token" пользователя ВКонтакте\nи "token" пользователя Яндекс Диск.\n')            
        token_id = None
        while token_id == None:
            token_vk = input('Введите "token" пользователя ВКонтакте: ')
            vk_client = vkuser.VkUser(token_vk, '5.131')
            token_id, token_screen_name = vk_client.user_get_id()                      
            if token_id == None:
                print(token_screen_name)  
            else:
                print('\nВведенный token действителен.\n')   
        token_yd_check = 401
        while token_yd_check == 401:
              token_yd = input('Введите "token" пользователя Яндекс Диск: ')
              uploader = ya_uploader.YaUploader(token_yd) 
              token_yd_check = uploader.token_check()
              if token_yd_check == 401:
                  print('\nВведенный token недействителен.\n') 
              else:
                  print('\nВведенный token действителен.\n')     
    print('\nВы можете ввести для скачивания фотографий\nпользователя ВКонтакте его "id" или "screen_name".\n')
    screen_name = ''
    user_id_check = None
    while user_id_check == None:
        user_id = input('Введите "id" пользователя ВКонтакте или\nнажмите ENTER, если хотите ввести "screen_name": ')
        if user_id == '':
            break
        user_id_check = vk_client.user_seach(user_id)
        if user_id_check == None:
            print('\nТакого "id" не существует во ВКонтакте. Введите правильный "id".')            
    if user_id == '':
        user_id = None
        while user_id == None:
            screen_name = input('\nВведите "screen_name" пользователя ВКонтакте: ')
            user_id = vk_client.user_seach(screen_name)
            if user_id == None:
                print('Такого "screen_name" не существует во ВКонтакте.\nВведите правильны "screen_name".\n')
        user_id = str(user_id)    
    config = configparser.ConfigParser()
    config.add_section('VK')
    config.set('VK', 'token', token_vk)    
    config.add_section('YD')
    config.set('YD', 'token', token_yd) 
    config.set('VK', 'id', user_id)
    config.set('VK', 'screen_name', screen_name)  
    with open(path, "w") as config_file:
        config.write(config_file)    
    return config

if __name__ == '__main__':

    path_ini = 'settings.ini'
    config = create_config(path_ini)    
    token_vk = config['VK']['token']          
    user_id = config['VK']['id']
    user_screen_name = config['VK']['screen_name']
    token_yd = config['YD']['token']
    vk_client = vkuser.VkUser(token_vk, '5.131')    
    foto_list = vk_client.get_foto(user_id)
    uploader = ya_uploader.YaUploader(token_yd)            
    folder = uploader.create_folder()        
    path_folder = uploader.upload_name_likes(folder, foto_list)
    file_data = uploader.file_data(path_folder)   
    uploader.foto_file_upload(file_data)
    
    print('Конец программы.')
