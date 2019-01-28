import os, sys
import random
import json
import requests
from time import sleep

#Enter the unique token
TOKEN = ''

comics = []
for item in os.listdir (os.path.join(os.getcwd(), 'comics')):
	comics.append (item)

base_url = "https://api.telegram.org/bot{token}/".format(token = TOKEN)

current_offset = 0

def getMe ():
	url = ''.join ([base_url, 'getMe'])
	return requests.get (url).json()

def sendMessage (chatId, text):
	url = ''.join([base_url, 'sendMessage'])
	requests.get(url, params={
		'chat_id': chatId,
		'text': text
		})
	
def sendPhoto(chatId):
	url = ''.join([base_url, 'sendPhoto'])
	image = {
	'photo' : open('comics/{filename}'.format(filename = random.choice(comics)), 'rb')
	}
	requests.post(url, files=image, data={'chat_id' : chatId})

def getUpdates():
	print("Called")
	url = ''.join([base_url, 'getUpdates'])
	x = requests.get(url, params= {'offset' : current_offset}).json()
	print("Hiiiiii")
	return x

while True:
	results=getUpdates()['result']
	for result in results:
		update_id = result['update_id']
		chat_id = result['message']['chat']['id']
		print(result['message']['text'])
		if current_offset <= update_id:
			current_offset = update_id + 1;

			if result['message']['text'] == 'hitme' or 'send' in result['message']['text']:
				sendPhoto (chat_id)
		else:
			sendMessage (chat_id, 'Ask for a comic')
	sleep (2)
