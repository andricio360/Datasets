from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

bot = ChatBot('bot')
trainerDataset = ListTrainer(bot)
for files in os.listdir('/Users/mac/Documents/Datasets/Chatbot_spanish/chatterbot_dataset_spanish/'):
    data = open('/Users/mac/Documents/Datasets/Chatbot_spanish/chatterbot_dataset_spanish/'+files,'r').readlines()
    trainerDataset.train(data)
