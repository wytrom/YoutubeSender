import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Credenciais do YouTube
DEVELOPER_KEY = "AIzaSyDiH8KAkBw1KWeQIDXeQe-m_8biq0nkjEA"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Pasta com vídeos
VIDEOS_FOLDER = "C:\\Users\\Administrator\\Desktop\\Youtube sender1\\videos"

def upload_video(video_path, title, tags):
    try:
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

        # Cria o objeto MediaFileUpload
        media = MediaFileUpload(video_path, resumable=True)

        # Cria o objeto video
        video = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "tags": tags,
                    "categoryId": "22"
                },
                "status": {
                    "privacyStatus": "public"
                }
            },
            media_body=media
        ).execute()

        print("Upload realizado com sucesso:", video['id'])

    except HttpError as error:
        print("An error occurred:", error)
        video = None

    return video

# Obtém todos os arquivos de vídeo na pasta
videos = [f for f in os.listdir(VIDEOS_FOLDER) if f.endswith(".mp4")]

# Percorre cada vídeo
for video in videos:
    video_path = os.path.join(VIDEOS_FOLDER, video)
    title = video.replace(".mp4", "")
    tags = title.split(" ")

    # Envia o vídeo para o YouTube
    upload_video(video_path, title, tags)
