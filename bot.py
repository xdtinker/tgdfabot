import telebot
import constant as keys
from dfa import start_driver
from dfa import kill_driver
from dfa import tgGetLogs


bot = telebot.TeleBot(keys.API_KEY)

@bot.message_handler(commands=['start'])
def response(message):
    bot.send_message(message.chat.id, 'Greetings, Human.')

@bot.message_handler(commands=['hi'])
def response(message):
    bot.send_message(message.chat.id, 'Hi Dev')
 
@bot.message_handler(commands=['help'])
def response(message):
    bot.send_message(message.chat.id, "There's no help")

@bot.message_handler(commands=['status'])
def response(message):
    bot.send_message(message.chat.id, "I'm alive :>")

@bot.message_handler(commands=['sudostart'])
def response(message):
    bot.send_message(message.chat.id, 'Service Initializing')
    start_driver()

@bot.message_handler(commands=['sudostop'])
def response(message):
    bot.send_message(message.chat.id, 'okay lods')
    kill_driver()

bot.polling()