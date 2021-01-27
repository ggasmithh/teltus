# teltus
teltus is a simple Telegram Text-To-Speech bot. It can use the following as speech synthesis engines:
* Amazon's Polly engine
* Google's TTS engine by way of the gTTS library

The name doesn't mean anything, I just chose it because its sounds like "tell [it] to us"

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

Once all that is done, I usually just run it like this, because I'm too lazy to install ```screen``` or ```tmux```

```
python3 teltus.py
ctrl+z
bg
disown -h
```


---

under no circumstances should you use this in your telegram group.
