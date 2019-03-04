##
##	TODO: Clean up and deduplicate code
##
import boto3
import tempfile

import telegram
from telegram.ext import MessageHandler, CommandHandler, Filters, Updater
import logging
import atexit

from config import BOT_TOKEN, BOT_VOICE

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hi! I can talk!")

def say(bot, update, args):
    chat_id = update.message.chat_id

    message_text = " ".join(args)


    fullname = ""

    for name in [update.message.from_user.first_name, update.message.from_user.last_name]:
        if name != None:
            fullname += name

    #bot is typing
    bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.RECORD_AUDIO)

    reply_to_message_id = update.message.message_id

    temp = tempfile.mkstemp(suffix=".mp3")

    polly_client = boto3.Session(region_name='us-east-2').client('polly')

    response = polly_client.synthesize_speech(VoiceId=BOT_VOICE,
                OutputFormat='mp3',
                Text = f"{fullname} says, \"{message_text}\"")

    fin = open(temp[1], 'wb')
    fin.write(response['AudioStream'].read())
    fin.close()

    fout = open(temp[1], 'rb')
    bot.send_voice(chat_id, fout, reply_to_message_id=reply_to_message_id)
    fout.close()

def tts(bot, update, args):
    chat_id = update.message.chat_id

    message_text = " ".join(args)

    #bot is typing
    bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.RECORD_AUDIO)

    reply_to_message_id = update.message.message_id

    temp = tempfile.mkstemp(suffix=".mp3")

    polly_client = boto3.Session(region_name='us-east-2').client('polly')

    response = polly_client.synthesize_speech(VoiceId=BOT_VOICE,
                OutputFormat='mp3',
                Text = f"{message_text}")

    fin = open(temp[1], 'wb')
    fin.write(response['AudioStream'].read())
    fin.close()

    fout = open(temp[1], 'rb')
    bot.send_voice(chat_id, fout, reply_to_message_id=reply_to_message_id)
    fout.close()


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

say_handler = CommandHandler('say', say, pass_args=True)
dispatcher.add_handler(say_handler)

tts_handler = CommandHandler('tts', tts, pass_args=True)
dispatcher.add_handler(tts_handler)

updater.start_polling()

updater.idle()





