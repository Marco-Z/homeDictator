from telegram.ext import Updater, CommandHandler
from homeDictator.spesa import spesa as s

updater = Updater(token='284339274:AAGZ5n8_dpD4wa4PkjZeKtS_Xjc7rTo7iMc')

dispatcher = updater.dispatcher

def start(bot, update):
	user = update.message.chat_id
	bot.sendMessage(chat_id=user, text="/spesa per avere la lista")

def spesa(bot,update):
	print('spesa')
	user = update.message.chat_id
	lista = s()
	bot.sendMessage(chat_id=user, text=lista.leggi())

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

spesa_handler = CommandHandler('spesa', spesa)
dispatcher.add_handler(spesa_handler)

updater.start_polling()

updater.idle()
