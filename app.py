
from flask import Flask
import re
from datetime import datetime
import requests
import requests
from publisher import  *
from requests.exceptions import HTTPError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

URL = 'https://www.googleapis.com/youtube/v3/'
# Enter API KEY here
API_KEY = 'AIzaSyCCWYchGheAuT1Bf_It5jvY8g5hkAP9zeI'



@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/hello")
def hello_there():
    data={
        'key': "128172",
        'part': 'snippet',
        'videoId': "video_id",
        'order': 'relevance',
        'textFormat': 'plaintext',
        'maxResults': 100,
    }
    addCommentsToKafka(str(data).encode())
    return "success"

@app.route("/fetchcomments/<video_id>")
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
        comment_info['channelid']=video_id
        saveComments(comment_info)
        
      
        # print('{:0=4}\t{}\t{}\t{}\t{}'.format(no, text.replace('\n', ' '), like_cnt, user_name, reply_cnt))
        if reply_cnt > 0:
            cno = 1
            print_video_reply(no, cno, video_id, next_page_token, parentId,content)
        no = no + 1

    if 'nextPageToken' in resource:
        print_video_comment(video_id,no,  resource["nextPageToken"])
    # if content:
    #     # delivery_report(content)
    return "success"

@app.route("/test")
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
      
        comment_info['channelid']=video_id
        content.append(comment_info)
        saveComments(comment_info)
        cno = cno + 1
      
    if 'nextPageToken' in resource:
        print_video_reply(no, cno, video_id, resource["nextPageToken"], id,content)


def saveComments(data):
    url = "https://youtubecrudmongo-x5p245odzq-uc.a.run.app"
    try:
        addCommentsToKafka(str(data).encode())
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
   

if __name__ == "__main__":
    app.run(debug=True)