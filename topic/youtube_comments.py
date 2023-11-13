from googleapiclient.discovery import build

API_KEY = 'AIzaSyCEjv-oJ2zNbrxEyCCkmRvw5LWHzfAJ2qw'

youtube = build(serviceName='youtube', version='v3', developerKey=API_KEY)

def get_comments(video_id:str)->list:
    comments_lst = []
    next_page_token = ''
    i=1
    while len(comments_lst) >= 0:
        if next_page_token == '':
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=100).execute()
        else:
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token).execute()

        comments_lst += response['items']
        if 'nextPageToken' not in response:
            print(i)
            break
        next_page_token = response.get('nextPageToken')

        i+=1
    comments=[item['snippet']['topLevelComment']['snippet']['textOriginal'] for item in comments_lst]
    # print(comments)
    return comments
