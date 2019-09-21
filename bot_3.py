import requests
import json
import time
import random


class ChatTester():
    def __init__(self):
        self.token = ''
        self.username = ''
        self.password = ''
        self.token_url = ''
        self.create_chat_url = ''
        self.current_chat_uri = ''
        self.user_create_url = ''
        self.get_user_conf()

    @staticmethod
    def get_json_file(f_name):
        with open('{}.json'.format(f_name)) as file:
            return json.load(file)

    def get_user_conf(self, user_cfg=''):

        user_conf = self.get_json_file('user_config') or user_cfg

        self.username = user_conf['username']
        self.password = user_conf['password']

        self.token_url = self.get_json_file('urls')['token_url']
        self.create_chat_url = self.get_json_file('urls')['create_chat_url']
        self.user_create_url = self.get_json_file('urls')['create_user_url']

    def create_token(self):
        self.get_user_conf()

        url = self.token_url

        data = {
            'username': self.username,
            'password': self.password
        }

        try:
            res = requests.post(url, data).text
            self.token = json.loads(res)['auth_token']

        except:
            print('Ошибка получения токена')

        else:
            with open('tokens.json', 'w') as file:
                file.write(res)
            print('токен успешно получен')

    def create_chat(self):

        self.get_user_conf()
        url = self.create_chat_url
        self.checking_token()

        headers = {
            'Authorization': 'Token {}'.format(self.token)
        }

        try:
            chat_conf = requests.post(url, headers=headers).text
        except:
            print('Не удалось создать чат.')
        else:
            with open('chat.json', 'w') as log:
                log.write(chat_conf)
            print('Новый чат создан')

    def checking_token(self):

        if (self.token is None) or (len(self.token) < 1):
            self.json_exception('tokens', 'auth_token')

    def json_exception(self, file, name):
        print('Проверка наличия токена')
        try:
            self.token = self.get_json_file(file)[name]
        except:
            print('не удается получить токен')
            self.create_token()
            self.json_exception(file, name)

    def add_to_chat(self, user=''):
        self.get_user_conf()
        self.checking_token()

        url = '{}{}/'.format(self.create_chat_url, self.get_json_file('chat')['uri'])

        data = {
            'username': 'tester3' if not user else user
        }

        headers = {
            'Authorization': 'Token {}'.format(self.token)
        }

        res = requests.patch(url, data=data, headers=headers)

    def create_user(self, username='', password=''):

        self.get_user_conf()
        url = self.user_create_url
        a = ''

        data = {
            'username': username or 'test{}'.format(random.randint(1, 10000)),
            'password': '{}{}'.format(random.randint(10000, 1000000), (username or 'test')),
        }

        res = requests.post(url, data)

        if res.status_code == 201:
            with open('./users/{}.json'.format(data['username']), 'w') as file:
                file.write(json.dumps(data))
        else:
            print(res.status_code)

    def send_massage_to_chat(self, message=''):

        # self.get_user_conf()
        self.checking_token()

        url = '{}{}/messages/'.format(self.create_chat_url, self.get_json_file('chat')['uri'])

        data = {
            'message': message or 'Hello!'
        }

        headers = {
            'Authorization': 'Token {}'.format(self.token)
        }

        res = requests.post(url, data=data, headers=headers)

    def chat_log(self):

        self.get_user_conf()
        self.checking_token()

        url = '{}{}/messages/'.format(self.create_chat_url, self.get_json_file('chat')['uri'])

        headers = {
            'Authorization': 'Token {}'.format(self.token)
        }

        res = requests.get(url, headers=headers)

        if res.status_code == 200:
            with open('chat_log.json', 'w') as file:
                file.write(res.text)


test = ChatTester()
test.send_massage_to_chat()
test.chat_log()

# def add_to_chat():
#     url = '{}{}/'.format(get_json_file('urls')['create_chat_url'], get_json_file('chat')['uri'])
# url_2 = '{}{}/'.format(url, json.loads(res.text)['uri'])
# res = requests.patch(url_2, data=data, headers=headers)
#
# url_3 = '{}messages/'.format(url_2)
# data = {
#     'message': 'Hello!'
# }
# res = requests.post(url_3, data=data, headers=headers)
# print(res)
