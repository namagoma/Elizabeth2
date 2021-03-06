import tweepy
import requests
import sys
import random
import MyAPI
import traceback
import re
import pathlib

auth = tweepy.OAuthHandler(MyAPI.consumer_key_send, MyAPI.consumer_secret_send)
auth.set_access_token(MyAPI.access_token_send, MyAPI.access_secret_send)
api = tweepy.API(auth)


def find_level(tweet):
    levels = []
    tweet = tweet.replace('＋', '+')
    for level in re.findall("1[0-3]\+|1[0-4]\.[0-9]|1[0-4]", tweet):
        levels.append(level)
    if len(levels) == 0:
        l = []
        for i in range(120, 141):
            l.append(str(i / 10))
        random_song = ['']
    else:
        return levels


def choice_song(levels):
    choiced_songs = []
    for i in range(len(levels)):
        path = "data/"
        if "+" in levels[i]:
            path += levels[i] + "/"
            r = [7, 8, 9]
            path += levels[i][:-1] + "." + str(random.choice(r)) + "/"
        elif '.' in levels[i]:
            if int(levels[i][-1]) >= 7:
                path += levels[i][:-2] + "+/" + levels[i] + "/"
            else:
                path += levels[i][:-2] + "/" + levels[i] + "/"
        else:
            path += levels[i] + "/"
            r = [0, 1, 2, 3, 4, 5, 6]
            path += levels[i] + "." + str(random.choice(r)) + "/"
        print(path)
        songs = []
        for song in pathlib.Path(path).glob("*.png"):
            songs.append({"file_path": song, "file_name": str(
                song)[:-4].replace(path, '')})
        choiced_songs.append(random.choice(songs))
    return choiced_songs

def generating_challenge():
    notes_decision = ("Great", "Good", "Miss")
    Riquest_Great = (1, 2, 4, 8, 10, 15, 20, 25, 30, 35, 40, 45, 50)
    Riquest_Good_or_Miss = (1, 5, 10, 15, 20)
    
    choiced = random.choice(notes_decision)
    if choiced == notes_decision[0]:
        return [choiced, random.choice(Riquest_Great)]
    else:
        return [choiced, random.choice(Riquest_Good_or_Miss)]

# def serch_genre(text):
#     genre_list = []
#     ジャンルの指定をつくる

def reply(tw_text, tw_user_name, tw_id, tw_author_screen_name, tw_retweeted):
    level = find_level(tw_text)
    choiced_song = choice_song(level)
    #条件を生成
    challenge_request = generating_challenge()
    try:
        api.create_favorite(tw_id)
    except:
        pass
    tweet_url = "https://twitter.com/" + tw_author_screen_name + "/status/" + str(tw_id)
    tweet_buf = "私の選んだ課題曲は" + "「" + choiced_song[0]["file_name"] + "」" + "!!\n" + challenge_request[0] + " " + str(challenge_request[1]) + "以下を目指そう!!\n"+ tweet_url
    try:
        api.update_with_media(filename=choiced_song[0]["file_path"], status=tweet_buf)
    except:
        traceback.print_exc()
    