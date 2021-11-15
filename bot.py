import telebot
import constant as keys
import dfa as main


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
    bot.send_message(message.chat.id, "I'm Alive :)")

@bot.message_handler(commands=['sudostart'])
def response(message):
    bot.send_message(message.chat.id, 'Service Initializing')
    main.checkprocess()

@bot.message_handler(commands=['sudostop'])
def response(message):
    main.closeWebdrv()

bot.polling()
