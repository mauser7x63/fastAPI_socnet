import requests
import json
from faker import Faker
from requests.api import post

fake = Faker()
Faker.seed(3)
endpoint = 'http://127.0.0.1:8000/'
headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

def loadFromJSNON(fileName):
    '''
    загрузить из JSON. Принимает строку с именем файла 
    '''
    with open(fileName) as f:
        fileStuff = f.read()
        loadedStructure = json.loads(fileStuff)
    return loadedStructure
   
def saveToJSON(fileName, data):
    '''
    сохранить структуру в JSON-формате. Принимает строку с именем файла и структуру для сохранения
    '''
    with open(fileName, 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)
    return

def loadBots():
    bots = loadFromJSNON('fastAPI_socnet/bots.json')
    if rules['number_of_users']>len(bots):
        for user in range(0, rules['number_of_users']-len(bots)):
            bot = Bot(name=fake.first_name_nonbinary(), passwd=fake.pystr())
            print(f'user: {bot.username} with passwd: {bot.password}')
            bots.update({
                bot.username: bot.password
            })
        saveToJSON(fileName='fastAPI_socnet/bots.json', data=bots)
        print(len(bots), ' bots has been saved')
    return bots

def prepearBots(botsDict):
    for user in botsDict:
        user = Bot(name=user, passwd=botsDict[user])
        print(user.username)
    

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
        url = f'{endpoint}newpost/?token={self.token}'
        print(url)
        body = {
            "content": text,
            "user_id": user_id,
            "token": self.token
        }
        res = requests.post(url=url, headers=headers, json=body)
        if res.status_code == 200:
            return res.json()
        else:
            print("failed to post", res.status_code)
            return res.status_code

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
    rules = loadFromJSNON('fastAPI_socnet/bots_config.json')
    pprint(rules)
    
    #for _ in range(rules['number_of_users']):
        #bot = Bot(name=fake.first_name_nonbinary(), passwd=fake.pystr())
        #print(f'user: {bot.username} with passwd: {bot.password}')
        #print(fake.paragraph(nb_sentences=3))
        #print('*'*20)
users = loadBots()
prepearBots(users)