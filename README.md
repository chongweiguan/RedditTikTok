# TikTok Reddit Bot

Have you noticed the viral trend of videos on TikTok, YouTube, and Instagram featuring a monotone voice narrating interesting Reddit posts while Minecraft parkour plays in the background? These videos actually garner **MILLIONS** of views. With a little bit of editing, these videos typically take 10 minutes to create. 

<img src="https://github.com/chongweiguan/RedditTikTok/assets/75872136/7c8a27c0-55a0-40c8-b34c-80103a749136" width="300"/>
<img src="https://github.com/chongweiguan/RedditTikTok/assets/75872136/c06bcf72-6522-4914-9030-7bbbaf92d74a" width="300"/>

<br>
<br>
What if we could automate this process and create such a video in just 2-3 minutes with a single click of a button?
<br>
<br>

Introducing the TikTok Reddit Bot – your ultimate tool for creating viral videos with ease! With our bot, you can effortlessly produce engaging content that captivates millions. Users can choose to retrieve a random post from Reddit or input their own story. The bot utilizes the Google Text-to-Speech API to convert text into speech and generate precise word timestamps. Then, using Moviepy, it seamlessly integrates the audio, video clip, and subtitles.
<br>
<br>
What sets this bot apart is its convenience – you can generate videos from anywhere, and it takes less than 3 minutes to receive your completed video. Join the trend and start creating viral TikTok content effortlessly with our TikTok Reddit Bot!
<br>
<br>
You can actually check out some of my videos on TikTok @reddit_coolest_story

## Features

- **Random Post Retrieval**: Fetches a random post from a subreddit.
- **Custom Story Input**: Allows users to type in their own stories.
- **Text-to-Speech Conversion**: Uses Google Text-To-Speech API to convert text to .mp3 files with word timestamps.
- **Video Generation**: Utilizes MoviePy to create videos with the generated audio and subtitles.
- **Telegram Integration**: Sends the created videos to users via a Telegram bot.

## Requirements
- Python 3.9

## Set up
1. Clone this repository
2. Run `pip install -r requirements.txt`
3. Take two videos that are at least 5 minutes long, name them `vid1.mp4` and `vid2.mp4` and add them to the repository.
4. Register for a Reddit account if you don't already have one, take note of your username and password
5. Follow this [tutorial](https://www.youtube.com/watch?v=x9boO9x3TDA) to retrieve your Reddit app username and Reddit app secret
6. Follow this [tutorial](https://www.youtube.com/watch?v=GVPWz-nhJhg) to retrieve your Google Cloud Text-To-Speech key, it should be a `.json` file. Name it `sa_redtok.json`, and add it to the repository
7. Create a Telegram Bot using BotFather on Telegram, and retrieve the bot's token.
8. Create a `.env` file with the following content and add it to the repository:

   ```plaintext
   USERAGENT=ChangeMeClient/0.1 by YourUsername

   REDDIT_APP_USERNAME={your reddit app username}
   REDDIT_APP_SECRET={your reddit app secret}
   USERNAME={your reddit username}
   PASSWORD={your reddit password}

   TELEGRAM_TOKEN={your telegram bot token}
   ```

9. Run `python3 telegram_bot.py` to run the telegram bot
10. Open up your bot on telegram and type `/start`
11. Follow the instructions to use the bot!



https://github.com/chongweiguan/RedditTikTok/assets/75872136/07c9b415-e3c8-4f79-9575-d2a5ffa03dc5

## Example Video


https://github.com/chongweiguan/RedditTikTok/assets/75872136/3c7ab049-4afe-4b90-8726-7b899ebf491e




## Disclamer
- The bot might take 2-3 minutes to create and send the video, especially if the video is very long.
- Google Cloud Text-To-Speech API is not completely free. Please refer to [this](https://cloud.google.com/text-to-speech/pricing) before deciding to use Google Cloud Text-To-Speech API. 
