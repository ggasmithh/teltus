import boto3
import telegram
from telegram.ext import CommandHandler, Updater
import logging
from io import BytesIO
from os import environ

BOT_TOKEN = environ['BOT_TOKEN']
BOT_VOICE = environ['BOT_VOICE']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher

class Record:
    __slots__ = ("message", "chat_id", "user", "bot", "audio")

    def __init__(self, bot, update):
        self.message = update.message
        self.chat_id = self.message.chat_id
        self.user = self.message.from_user
        self.bot = bot
        self.audio = None

    def set_tts(self, args):

        message_text = " ".join(args)

        self.audio = self.get_audio(message_text)

    def get_audio(self, message_text):

        self.bot.send_chat_action(chat_id=self.chat_id, action=telegram.ChatAction.RECORD_AUDIO)

        polly_client = boto3.Session(region_name='us-east-2').client('polly')

        return polly_client.synthesize_speech(VoiceId=BOT_VOICE,
                    OutputFormat='mp3',
                    Text = message_text)


def audioSender(record):
    audioStream = record.audio.get("AudioStream")

    if audioStream is not None:

        stream = BytesIO(audioStream.read())

        record.bot.send_voice(
            record.chat_id, stream, 
            reply_to_message_id=record.message.message_id
        )

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hi! I can talk!")

def tts(bot, update, args):
    record = Record(bot, update)
    record.set_tts(args)

    audioSender(record)
    

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

tts_handler = CommandHandler('tts', tts, pass_args=True)
dispatcher.add_handler(tts_handler)

updater.start_polling()

updater.idle()
