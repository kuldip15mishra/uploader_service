from asyncio.windows_events import NULL
from flask import Flask
import re
from datetime import datetime
import requests
import requests
from requests.exceptions import HTTPError

main = Flask(__name__)
from . import main

URL = 'https://www.googleapis.com/youtube/v3/'
# Enter API KEY here
API_KEY = 'AIzaSyCCWYchGheAuT1Bf_It5jvY8g5hkAP9zeI'



@main.route("/")
def home():
    return "Hello, Flask!"

@main.route("/hello")
def hello_there():
    data={
        'key': "",
        'part': 'snippet',
        'videoId': "video_id",
        'order': 'relevance',
        'textFormat': 'plaintext',
        'maxResults': 100,
    }
    content = saveComments(data)
    return content

@main.route("/fetchcomments/<video_id>")
def print_video_comment( video_id, no=1, next_page_token=None):
   
    content=[]
    params = {
        'key': API_KEY,
        'part': 'snippet',
        'videoId': video_id,
        'order': 'relevance',
        'textFormat': 'plaintext',
        'maxResults': 100,
    }
    if next_page_token is not None:
        params['pageToken'] = next_page_token
    response = requests.get(URL + 'commentThreads', params=params)
    resource = response.json()
    i=0
    for comment_info in resource['items']:
        i = i+1
        # comment
        text = comment_info['snippet']['topLevelComment']['snippet']['textDisplay']
        # Good number
        like_cnt = comment_info['snippet']['topLevelComment']['snippet']['likeCount']
        # Number of replies
        reply_cnt = comment_info['snippet']['totalReplyCount']
        # username
        user_name = comment_info['snippet']['topLevelComment']['snippet']['authorDisplayName']
        # Id
        parentId = comment_info['snippet']['topLevelComment']['id']
        # fp.write('%s\n{:0=4}\t{}\t{}\t{}\t{}'.format(
        #     no, text.replace('\n', ' '), like_cnt, user_name, reply_cnt))
        content.append(comment_info)
        # print(comment_info)
      
        # print('{:0=4}\t{}\t{}\t{}\t{}'.format(no, text.replace('\n', ' '), like_cnt, user_name, reply_cnt))
        if reply_cnt > 0:
            cno = 1
            print_video_reply(no, cno, video_id, next_page_token, parentId,content)
        no = no + 1

    if 'nextPageToken' in resource:
        print_video_comment(video_id,no,  resource["nextPageToken"])
    # if content:
    #     # delivery_report(content)
    # return content

@main.route("/test")
def print_video_reply(no, cno, video_id, next_page_token, id,content):
    params = {
        'key': API_KEY,
        'part': 'snippet',
        'videoId': video_id,
        'textFormat': 'plaintext',
        'maxResults': 50,
        'parentId': id,
    }

    if next_page_token is not None:
        params['pageToken'] = next_page_token
    response = requests.get(URL + 'comments', params=params)
    resource = response.json()

    for comment_info in resource['items']:
        # comment
        text = comment_info['snippet']['textDisplay']
        # Good number
        like_cnt = comment_info['snippet']['likeCount']
        # username
        user_name = comment_info['snippet']['authorDisplayName']
        # fp.write('%s\n{:0=4}-{:0=3}\t{}\t{}\t{}'.format(no, cno,
        #          text.replace('\n', ' '), like_cnt, user_name))
        # print('{:0=4}-{:0=3}\t{}\t{}\t{}'.format(no, cno, text.replace('\n', ' '), like_cnt, user_name))
        content.append(comment_info)
        cno = cno + 1
      
    if 'nextPageToken' in resource:
        print_video_reply(no, cno, video_id, resource["nextPageToken"], id,content)


def saveComments(data):
    url = "https://crudfirebase-x5p245odzq-uc.a.run.app/"
    try:
        response = requests.post(url, json=data)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        # print('Success!')
        return response.text
    

if __name__ == "__main__":
    main.run(debug=True)