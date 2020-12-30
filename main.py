from telegram import ChatAction, Update
from telegram.ext import CommandHandler, Updater, CallbackContext
import logging
from os import environ
from tempfile import mkstemp

TELTUS_BACKEND = environ['TELTUS_BACKEND']
TELTUS_TOKEN = environ['TELTUS_TOKEN']
TELTUS_CHAT_ID = environ['TELTUS_CHAT_ID']

try:
    TELTUS_VOICE = environ['TELTUS_VOICE']
except:
    TELTUS_VOICE = None

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Basic setup / sanity checks
if TELTUS_BACKEND == 'polly':
    import boto3

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

    if TELTUS_VOICE not in POLLY_VOICES:
        raise Exception("Invalid voice selection for Polly Backend!")

    def text_to_audio(message_text: str):
        polly_client = boto3.Session(region_name="us-east-2").client('polly')

        polly_response = polly_client.synthesize_speech(VoiceId=TELTUS_VOICE,
                    OutputFormat='mp3',
                    Text = message_text)

        return (None, polly_response.get("AudioStream"))

elif TELTUS_BACKEND == 'gtts':
    from gtts import gTTS

    def text_to_audio(message_text: str):
        fd, path = mkstemp()
        tts = gTTS(message_text, lang='en')
        tts.save(path)

        return (fd, path)

else:
    raise Exception('Invalid backend preference!\nValid backends: polly, gtts')

def start(update: Update, context: CallbackContext) -> None:
    if str(update.message.chat_id) == str(TELTUS_CHAT_ID):
        update.message.reply_text("Hi! I can talk!")

def say(update: Update, context: CallbackContext) -> None:
    if str(update.message.chat_id) == str(TELTUS_CHAT_ID):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.RECORD_AUDIO)
        fd, audio_path = text_to_audio(update.message.text)

        if audio_path is not None:
            update.message.reply_voice(audio_path, reply_to_message_id=update.message.message_id)
        
        if fd is not None:
            fd.close()

def main():
    # Set up the telegram interface
    updater = Updater(TELTUS_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('say', say))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
