import telebot
from telebot import custom_filters
import constant as keys
import dfa as main

bot = telebot.TeleBot(keys.API_KEY)

@bot.message_handler(commands=['start'])
def response(message):
    bot.send_message(message.chat.id, "Greetings, {name}!".format(name=message.from_user.first_name))

@bot.message_handler(text=['hi' ,'hello'])
def response(message):
    bot.send_message(message.chat.id, "Hi, {name}!")
 
@bot.message_handler(commands=['help'])
def response(message):
    bot.send_message(message.chat.id, "I Can't help you at the moment.")

@bot.message_handler(chat_id=[keys.DEV_ID], commands=['sudostart'])
def response(message):
    bot.send_message(message.chat.id, 'Ok')
    main.checkprocess()

@bot.message_handler(commands=['sudostart'])
def response(message):
    bot.send_message(message.chat.id, 'Access Denied.')

@bot.message_handler(chat_id=[keys.DEV_ID], commands=['sudostop'])
def response(message):
    bot.send_message(message.chat.id, 'Ok')
    main.closeWebdrv()

@bot.message_handler(commands=['sudostop'])
def response(message):
    bot.send_message(message.chat.id, 'Access Denied.')

@bot.message_handler(commands=['status'])
def response(message):
    bot.send_message(message.chat.id, "I'm Alive")

@bot.message_handler(commands=['commands'])
def response(message):
    bot.send_message(message.chat.id,
    """Available commands:

/start > Greetings
/help > help?
/status > Check Bot status
/sudostart > Start Session
/sudostop > Close Session   
    """)

bot.add_custom_filter(custom_filters.ChatFilter())
bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.add_custom_filter(custom_filters.TextStartsFilter())

bot.polling()