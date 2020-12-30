# teltus (NON-FUNCTIONAL)
teltus is a simple Telegram Text-To-Speech bot. It can use the following as speech synthesis engines:
* Amazon's Polly engine
* Google's gTTS engine

## usage
Before running, teltus must be configured by setting the following environment variables. Additionally, the Boto client needs to be set up.

### ```TELTUS_BACKEND```
This should be set either to ```polly``` or ```gtts```, for usage with Polly or gTTS, respectively

### ```TELTUS_VOICE```
For now, voice selection is only supported with the Polly engine. Valid selections can be found in ```main.py``` or [in Amazon's documentation.](https://docs.aws.amazon.com/polly/latest/dg/voicelist.html).

### ```TELTUS_TOKEN```
Your telegram bot token goes here. Get it from BotFather on telegram.

### ```TELTUS_CHAT_ID```
Set this to your chat ID so teltus knows which group to talk to! I do it this way rather than letting it join just any group so that random people cannot run up my VM quotas.

---

under no circumstances should you use this in your telegram group.
