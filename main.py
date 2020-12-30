import telegram
from telegram.ext import CommandHandler, Updater
import logging
from io import BytesIO
from os import environ

TELTUS_BACKEND = environ['TELTUS_BACKEND']
TELTUS_VOICE = environ['TELTUS_VOICE']
TELTUS_TOKEN = environ['TELTUS_TOKEN']

# Valid choices of voices for Amazon Polly
# From https://docs.aws.amazon.com/polly/latest/dg/voicelist.html
POLLY_VOICES = ["Zeina", "Zhiyu", "Naja", "Mads", "Lotte", "Ruben", "Nicole", 
    "Olivia", "Russell", "Amy", "Emma", "Brian", "Aditi", "Raveena", "Ivy", 
    "Joanna", "Kendra", "Kimberly", "Salli", "Joey", "Justin", "Kevin", 
    "Matthew", "Geraint", "Celine", "Léa", "Mathieu", "Chantal", "Marlene", 
    "Vicki", "Hans", "Aditi", "Dora", "Karl", "Carla", "Bianca", "Giorgio", 
    "Mizuki", "Takumi", "Seoyeon", "Liv", "Ewa", "Maja", "Jacek", "Jan", 
    "Camila", "Vitoria", "Ricardo", "Ines", "Cristiano", "Carmen", "Tatyana", 
    "Maxim", "Conchita", "Lucia", "Enrique", "Mia", "Lupe", "Penelope", "Miguel", 
    "Astrid", "Filiz", "Gwyneth"]

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Basic setup / sanity checks
if TELTUS_BACKEND == 'polly':
    import boto3

    if TELTUS_VOICE not in POLLY_VOICES:
        raise Exception("Invalid voice selection for Polly Backend!")

    def text_to_audio(message_text):
        polly_client = boto3.Session(region_name="us-east-2").client('polly')

        return polly_client.synthesize_speech(VoiceId=TELTUS_VOICE,
                    OutputFormat='mp3',
                    Text = message_text)

    
elif TELTUS_BACKEND == 'gtts':
    from gtts import gTTS
    
    #if TELTUS_VOICE not in uhhhh find a list of voices or smthn idk:
    #    raise Exception("Invalid voice selection for gtts Backend!")

    def text_to_audio(message_text):
        fp = BytesIO()
        tts = gTTS(message_text, lang='en')
        tts.write_to_fp(fp)

        return fp

else:
    raise Exception('Invalid backend preference!\nValid backends: polly, gtts')

# Set up the telegram interface
updater = Updater(token=TELTUS_TOKEN)
dispatcher = updater.dispatcher

class Record:
    __slots__ = ("message", "chat_id", "user", "bot", "audio")

    def __init__(self, bot, update):
        self.message = update.message
        self.chat_id = self.message.chat_id
        self.user = self.message.from_user
        self.bot = bot
        self.audio = None

    def set_audio(self, args):
        message_text = " ".join(args)
        self.audio = self.get_audio(message_text)

    def get_audio(self, message_text):
        self.bot.send_chat_action(chat_id=self.chat_id, action=telegram.ChatAction.RECORD_AUDIO)

        return text_to_audio(message_text)


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

def say(bot, update, args):
    record = Record(bot, update)
    record.set_audio(args)

    audioSender(record)
    
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

say_handler = CommandHandler('say', say, pass_args=True)
dispatcher.add_handler(say_handler)

updater.start_polling()

updater.idle()
