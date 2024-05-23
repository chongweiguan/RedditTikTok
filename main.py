import requests
from dotenv import load_dotenv
import os
import json
from google.cloud import texttospeech
import numpy as np
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
import re
import random
import pyautogui
import time

load_dotenv()

reddit_api_url = "https://oauth.reddit.com"
reddit_headers = {
    "Accept": "application/json",
    "User-Agent": os.getenv("USERAGENT"),
    "Authorization": f"bearer {os.getenv('AUTHORIZATION')}"
}

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'sa_redtok.json'
client = texttospeech.TextToSpeechClient()


def get_reddit_posts(subreddit):
    suffix = f"/r/{subreddit}/top?t=year"
    url = reddit_api_url + suffix
    
    response = requests.get(url, headers=reddit_headers)

    if response.status_code != 200:
        return []

    data = response.json()
    posts = data["data"]["children"]

    res = []

    for post in posts:
        title = post["data"]["title"]
        text = post["data"]["selftext"]
        text = text.replace('\n', '')
        full_text = title + ". " + text

        full_text = full_text.replace("AITA", "Am I the A hole")
        full_text = full_text.replace("aita", "Am I the A hole")

        res.append([title, full_text])

    return res;

def create_audio(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        effects_profile_id=['small-bluetooth-speaker-class-device'],
        speaking_rate=1,
        pitch=1
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open("output.mp3", "wb") as output:
        output.write(response.audio_content)
        print("Audio content written to file output.mp3")

        return "output.mp3"
    
def get_random_section(duration):
    video_path = random.choice(["minecraft1.mov", "minecraft2.mov"])

    video = VideoFileClip(video_path)
    video_duration = video.duration  # Duration of the video in seconds
    if video_duration < duration:
        raise ValueError("Video duration is shorter than the desired section length.")
    start_time = random.uniform(0, video_duration - duration)
    end_time = start_time + duration
    return video.subclip(start_time, end_time)


def create_video(text, audio_file_path):
    audio = AudioFileClip(audio_file_path)
    duration = audio.duration
    video_clip = get_random_section(duration)
    final_clip = video_clip.set_audio(audio)
    final_clip.write_videofile('output_video.mp4', fps=24)

    print("Video creation complete!")

def capcut():
    time.sleep(4)
    pyautogui.moveTo(387,522,duration=3) # clicks on new video
    pyautogui.click()
    pyautogui.click()

    time.sleep(4)
    pyautogui.moveTo(889,346,duration=3) # clicks upload
    pyautogui.click()

    time.sleep(4)
    pyautogui.moveTo(1012,319,duration=3) # clicks on edited video
    pyautogui.click()

    time.sleep(4)
    pyautogui.moveTo(1010,673,duration=3) # clicks open
    pyautogui.click()

    time.sleep(4)
    pyautogui.moveTo(854,300,duration=3) # clicks on fill
    pyautogui.click()

    time.sleep(4)
    pyautogui.moveTo(35,496,duration=3) # clicks on caption
    pyautogui.click()

    time.sleep(4)
    pyautogui.moveTo(258,194,duration=3) # clicks on auto caption
    pyautogui.click()

    time.sleep(4)
    pyautogui.moveTo(219,403,duration=3) # clicks on generate
    pyautogui.click()

    time.sleep(5)
    pyautogui.moveTo(897,578,duration=3) # key down to drag
    pyautogui.mouseDown()

    time.sleep(4)
    pyautogui.moveTo(897,405,duration=3) # release drag
    pyautogui.mouseUp()

    time.sleep(4)
    pyautogui.moveTo(1414,178,duration=3) # click presets
    pyautogui.click()

    time.sleep(4)
    pyautogui.moveTo(1335,447,duration=3) # click text font
    pyautogui.click()

    time.sleep(4)
    pyautogui.moveTo(1220,116,duration=3) # click export
    pyautogui.click()

    time.sleep(4)
    pyautogui.moveTo(1227,632,duration=3) # click download
    pyautogui.click()

    time.sleep(4)
    pyautogui.moveTo(1179,789,duration=3) # click export
    pyautogui.click()

    time.sleep(60)
    pyautogui.moveTo(472,20,duration=3) # click back to home page
    pyautogui.click()


def main():
    titles = set()
    file = open('titles.txt', 'r+')

    lines = file.readlines()
    for line in lines:
        titles.add(line.strip())

    reddit_posts = get_reddit_posts('amitheasshole')

    texts = []

    count = 0
    for post in reddit_posts:
        # print(f"title: {post[0]}\ntext: {post[1]}\n")
        if count == 1:
            break
        if post[0] in titles or len(post[1]) < 1500:
            continue
        texts.append(post[1])
        file.write(post[0])
        count += 1

    for text in texts:
        print(text)
        audio_file = create_audio(text)
        # create_video(text, audio_file)
        # capcut()

def get_position():
    time.sleep(2)
    current_mouse_position = pyautogui.position()
    print(f"Current mouse position: {current_mouse_position}")


main()
