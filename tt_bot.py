import tweepy
import time
import xlrd
import random
import configparser

#Keys from twitter
config = configparser.ConfigParser()
config.read('config.ini')
consumer_key = config['KEYS']['consumer_key']
consumer_secret = config['KEYS']['consumer_secret']
key = config['KEYS']['key']
secret = config['KEYS']['secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)

FILE_NAME = 'check.txt'
workbook = xlrd.open_workbook('out.xls')
worksheet = workbook.sheet_by_name('Sheet1')

def read_check(FILE_NAME):
    file_read = open(FILE_NAME, 'r')
    last_id = int(file_read.read().strip())
    file_read.close()
    return last_id

def store_id(FILE_NAME, last_id):
    file_write = open(FILE_NAME, 'w')
    file_write.write(str(last_id))
    file_write.close()

def reply():
    tweets = api.mentions_timeline(read_check(FILE_NAME), tweet_mode='extended')
    for tweet in reversed(tweets):
        print("Replied to ID --> " + str(tweet.id))
        random_movie = random.randint(1,8585)
        print(worksheet.cell(random_movie, 0).value)

        api.update_status(f"Olá @{tweet.user.screen_name} 😁, vou te recomendar um filme muito legal! "
                          f"O nome é '{worksheet.cell(random_movie, 0).value}', "
                          f"lançado no ano de {worksheet.cell(random_movie, 1).value}. "
                          f"Os gêneros deste filme são: {worksheet.cell(random_movie, 2).value}. "
                          f" Possui uma duração de  {worksheet.cell(random_movie, 3).value} minutos. Espero que goste 🔥." , tweet.id)

        api.create_favorite(tweet.id)
        api.retweet(tweet.id)
        store_id(FILE_NAME, tweet.id)

while True:
    reply()
    time.sleep(15)





