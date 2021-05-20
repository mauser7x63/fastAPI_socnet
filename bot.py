import requests
import json
from faker import Faker
from requests.api import post

fake = Faker()
Faker.seed(0)
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
    
    def createPost(self, user_id, text):
        url = f'{endpoint}{user_id}/post/'
        return

    def ratePost(self, post_id, like=True):
        if like: 
            rate = 'like'
        else:
            rate = 'dislike'
        url = f'{endpoint}post/{post_id}/{rate}?token={self.token}'
        print('request to URL:', url)
        res = requests.post(url=url, headers=headers, data={})
        if res.status_code == 200:
            pprint(res.json())
            return {'message': f'post id={post_id} was liked'}
        else:
            print('something goes wrong, error: ', res.status_code)
            return res.status_code     

if __name__=="__main__":
    from pprint import pprint
    print('bot standalone runned')
    rules = loadConfig()
    pprint(rules)
    
    for _ in range(rules['number_of_users']):
        #bot = Bot(name=fake.first_name_nonbinary(), passwd=fake.pystr())
        #print(f'user: {bot.username} with passwd: {bot.password}')
        print(fake.paragraph(nb_sentences=3))
        print('*'*20)

        
    
    bot = Bot(name=fake.first_name_nonbinary(), passwd=fake.pystr())
    print(f'user: {bot.username} with passwd: {bot.password}')
    #print(fake.paragraph(nb_sentences=3))
    print(bot.token)
    print(bot.ratePost(post_id=1, like=False))
