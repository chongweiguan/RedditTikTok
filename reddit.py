import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
from google.cloud import texttospeech_v1beta1 as tts
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
import random
import re


load_dotenv()

reddit_api_url = "https://oauth.reddit.com"
reddit_access_token_url = "https://www.reddit.com/api/v1/access_token"
reddit_app_username = os.getenv('REDDIT_APP_USERNAME')
reddit_app_secret = os.getenv('REDDIT_APP_SECRET')
reddit_username = os.getenv('USERNAME')
reddit_password = os.getenv('PASSWORD')

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'sa_redtok.json'
client = tts.TextToSpeechClient()

def get_reddit_access_token():
    auth = HTTPBasicAuth(reddit_app_username, reddit_app_secret)
    data = {
        'grant_type': 'password',
        'username': reddit_username,
        'password': reddit_password
    }

    response = requests.post(reddit_access_token_url, auth=auth, data=data)
    if response.status_code == 200:
        r = response.json()
        return r['access_token']
    return None


def get_reddit_posts(subreddit):
    suffix = f"/r/{subreddit}/top?t=year"
    url = reddit_api_url + suffix
    access_token = get_reddit_access_token()

    reddit_headers = {
        "User-Agent": os.getenv("USERAGENT"),
        "Authorization": f"bearer {access_token}"
    }
    
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


def filter_text(text):
    replacements = {
        "&amp": "and",
        "&": "and",
        "&lt;": "<",
        "&gt;": ">",
        "&quot;": "\"",
        "&apos;": "'",
        "\\n": " ",
        "\\t": " ",
        "\\r": " ",
        "\u200b": "",
        "\u200c": "",
        "\u200d": "",
        "\u2060": "",
        "±": "plus-minus",
        "×": "times",
        "÷": "divided by",
        "√": "square root",
        "$": "dollars",
        "€": "euros",
        "£": "pounds",
        "¥": "yen",
        "©": "copyright",
        "®": "registered",
        "™": "trademark",
        "AITA": "Am I the A hole",
        "aita": "Am I the A hole"
    }

    for key, value in replacements.items():
        text = text.replace(key, value)

    # Remove any remaining special characters
    pattern = r'[^a-zA-Z0-9\s\'.,!?]'
    text = re.sub(pattern, '', text)

    # Remove emoji and non-ASCII characters
    text = text.encode('ascii', 'ignore').decode('ascii')
    return text


def create_ssml(text):
    text = filter_text(text)
    words = text.split()
    ssml_text = "<speak>"
    segment = ""
    segments = []  # List to store segments
    segment_index = 0  # Initialize segment index

    for i, word in enumerate(words):
        if len(segment) + len(word) + 1 <= 20:  # +1 for the space
            if segment:
                segment += " "
            segment += word
        else:
            ssml_text += f'<mark name="{segment_index}" />{segment} '
            segments.append(segment)
            segment = word
            segment_index += 1

    if segment:
        ssml_text += f'<mark name="{segment_index}" />{segment} '
        segments.append(segment)

    ssml_text += "</speak>"
    return ssml_text, segments


def create_audio(text):
    text = filter_text(text)
    ssml_text, segments = create_ssml(text)

    synthesis_input = tts.SynthesisInput(ssml=ssml_text)

    voice = tts.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C"
    )

    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3,
        effects_profile_id=['small-bluetooth-speaker-class-device'],
        speaking_rate=1
    )

    request = tts.SynthesizeSpeechRequest(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
        enable_time_pointing=["SSML_MARK"]
    )
    
    response = client.synthesize_speech(request=request)

    with open("output.mp3", "wb") as output:
        output.write(response.audio_content)
        print("Audio content written to file output.mp3")

    file = open("timestamps.txt", "w")

    time_points = []
    for time_point in response.timepoints:
        time_points.append({
            "mark_name": time_point.mark_name,
            "time_seconds": time_point.time_seconds
        })
        file.write(f"Word: {time_point.mark_name}, Timestamp: {time_point.time_seconds}\n")

    return "output.mp3", time_points, segments


def get_random_section(duration):
    video_path = random.choice(["minecraft1.mov", "minecraft2.mov"])

    video = VideoFileClip(video_path)
    video_duration = video.duration  # Duration of the video in seconds
    if video_duration < duration:
        raise ValueError("Video duration is shorter than the desired section length.")
    start_time = random.uniform(0, video_duration - duration)
    end_time = start_time + duration
    return video.subclip(start_time, end_time)


def create_video(audio_file_path, time_stamps, segments):
    audio = AudioFileClip(audio_file_path)
    duration = audio.duration
    video_clip = get_random_section(duration)

    video_clip = video_clip.resize(height=1080)  # Set height to 1080p
    video_clip = video_clip.crop(width=608, height=1080, x_center=video_clip.w / 2, y_center=video_clip.h / 2)

    text_clips = []
    check = time_stamps[0]['mark_name'] is not None
    print(f"Timestamps? {check}")

    for i in range(len(time_stamps)):
        text_duration = 1
        if i == len(time_stamps)-1:
            text_duration = duration - time_stamps[i]['time_seconds']
        else:
            text_duration = time_stamps[i+1]['time_seconds'] - time_stamps[i]['time_seconds']
        
        txt_clip = (TextClip(
                    segments[i], 
                    fontsize=50, 
                    font='Arial-Bold',  # Ensure this font is installed on your system
                    color='white', 
                    stroke_color='black', 
                    stroke_width=2)  # Adjust stroke_width as needed
                .set_position('center')
                .set_duration(text_duration)
                .set_start(time_stamps[i]['time_seconds']))
        
        text_clips.append(txt_clip)

    final_clip = CompositeVideoClip([video_clip, *text_clips])
    final_clip = final_clip.set_audio(audio)
    final_clip.write_videofile('output_video.mp4', fps=24, codec='libx264', audio_codec='aac')

    print("Video creation complete!")

    return 'output_video.mp4'

def get_random_reddit_post():
    titles = set()
    file = open('titles.txt', 'r+')

    lines = file.readlines()
    for line in lines:
        titles.add(line.strip())

    reddit_posts = get_reddit_posts('amitheasshole')

    text = ""

    for post in reddit_posts:
        if post[0] in titles or len(post[1]) < 1500:
            continue
        text = post[1]
        file.write('\n')
        file.write(post[0])
        break

    file.close()
    return text


def create_random_reddit_tiktok_clip():
    text = get_random_reddit_post()
    audio_file, time_points, segments = create_audio(text)
    video_path = create_video(audio_file, time_points, segments)

    return video_path


def create_reddit_tiktok_clip(text):
    audio_file, time_points, segments = create_audio(text)
    video_path = create_video(audio_file, time_points, segments)
    return video_path

