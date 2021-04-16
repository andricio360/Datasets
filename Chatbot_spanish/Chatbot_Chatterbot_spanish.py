from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

bot = ChatBot('bot')

while True:
    message = input('Tú: ')
    if message.strip() != 'Adios':
        reply = bot.get_response(message)
        print('ChatBot: ',reply)
    if message.strip()== 'Adios':
        print('ChatBot: Adios')
        break
