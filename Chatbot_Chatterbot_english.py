from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

Chatbot = ChatBot('Charlie')


trainerDataset_english = ListTrainer(Chatbot)
for files in os.listdir('/Users/mac/Documents/Datasets/chatterbot_dataset_english/'):
    data_english = open('/Users/mac/Documents/Datasets/chatterbot_dataset_english/'+files,'r').readlines()
    trainerDataset_english.train(data_english)

while True:
    message = input('You: ')
    if message.strip() != 'Bye':
        reply = Chatbot.get_response(message)
        print('ChatBot: ',reply)
    if message.strip()== 'Bye':
        print('ChatBot: Bye')
        break
