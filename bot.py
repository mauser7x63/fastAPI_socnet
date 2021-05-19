import requests
import json
from faker import Faker

fake = Faker()
Faker.seed(3)
endpoint = 'http://127.0.0.1:9000/'
headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

def loadConfig():
    with open('bots_config.json') as f:
        fileStuff = f.read()
        configJson = json.loads(fileStuff)
    return configJson


class Bot():
    def __init__(self, name, passwd):
        self.username = name
        self.password = passwd
        self.token = self.login()

    def signUp(self):
        url = endpoint+'signup'
        body = {
            'username': self.username,
            'password': self.password 
        }
        res = requests.post(url=url, headers=headers, json=body)
        if res.status_code == 200:
            print(f'request to {url} is ok')
            return res.json()
        else:
            print('something goes wrong, error: ', res.status_code)
            return res.status_code     

    def login(self):
        url = endpoint+'login'
        body = {
            'username': self.username,
            'password': self.password 
        }
        res = requests.post(url=url, headers=headers, json=body)
        if res.status_code == 200:
            print(f'request to {url} is ok')
            token = res.json().get('access_token')
            if not token:
                print('login failed. try to signup')
                self.signUp()
                token = self.login()
            return token
        else:
            print('something goes wrong, error: ', res.status_code)
            return res.status_code     
    
    def createPost(self):
        pass

    def likePost(self):
        pass

    def dislikePost(self):
        pass
 
if __name__=="__main__":
    from pprint import pprint
    print('bot standalone runned')
    rules = loadConfig()
    pprint(rules)
    '''
    for _ in range(rules['number_of_users']):
        bot = Bot(name=fake.first_name_nonbinary(), passwd=fake.pystr())
        print(f'user: {bot.username} with passwd: {bot.password}')
    '''
    bot = Bot(name=fake.first_name_nonbinary(), passwd=fake.pystr())
    print(f'user: {bot.username} with passwd: {bot.password}')
