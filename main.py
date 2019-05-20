import boto3
import telegram
from telegram.ext import MessageHandler, CommandHandler, Filters, Updater
import logging
import atexit
from io import BytesIO

from config import BOT_TOKEN, BOT_VOICE

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher

class Record:
    __slots__ = ("message", "chat_id", "user", "bot")

    def __init__(self, bot, update):
        self.message = update.message
        self.chat_id = self.message.chat_id
        self.user = self.message.from_user
        self.bot = bot

    def tts(self, args):

        message_text = " ".join(args)

        return self.get_audio(message_text)
      
    def say(self, args):

        message_text = " ".join(args)

        fullname = " ".join(name for name in (
            self.user.first_name, self.user.last_name
            ) if name != None
        )

        return self.get_audio(f"{fullname} says, {message_text}")


    def get_audio(self, message_text):

        self.bot.send_chat_action(chat_id=self.chat_id, action=telegram.ChatAction.RECORD_AUDIO)

        polly_client = boto3.Session(region_name='us-east-2').client('polly')

        return polly_client.synthesize_speech(VoiceId=BOT_VOICE,
                    OutputFormat='mp3',
                    Text = message_text)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hi! I can talk!")
 
def say(bot, update, args):
    record = Record(bot, update)
    audio = record.say(args)

    audioStream = audio.get("AudioStream")

    if audioStream is not None:

        stream = BytesIO(audioStream.read())

        bot.send_voice(
            record.chat_id, stream, 
            reply_to_message_id=record.message.message_id
        )

def tts(bot, update, args):
    record = Record(bot, update)
    audio = record.tts(args)

    audioStream = audio.get("AudioStream")

    if audioStream is not None:

        stream = BytesIO(audioStream.read())

        bot.send_voice(
            record.chat_id, stream, 
            reply_to_message_id=record.message.message_id
        )

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

say_handler = CommandHandler('say', say, pass_args=True)
dispatcher.add_handler(say_handler)

tts_handler = CommandHandler('tts', tts, pass_args=True)
dispatcher.add_handler(tts_handler)

updater.start_polling()

updater.idle()





