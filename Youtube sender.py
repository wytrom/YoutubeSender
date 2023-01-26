import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

# Defina o caminho da pasta com os vídeos
VIDEOS_FOLDER = "path/to/videos"

# Carregar as credenciais a partir de um arquivo json
creds = Credentials.from_authorized_user_file("credentials.json", ["https://www.googleapis.com/auth/youtube"])

# Instanciar o cliente da API do YouTube
youtube = build("youtube", "v3", credentials=creds)

# Obter a lista de vídeos na pasta
videos = [f for f in os.listdir(VIDEOS_FOLDER) if f.endswith(".mp4")]

for video in videos:
    try:
        # Obter o nome do vídeo e gerar o título, tags e nome do arquivo
        video_name = video.split(".")[0]
        title = "Título do vídeo " + video_name
        tags = ["tag1", "tag2", "tag3"]
        file_name = video_name + ".mp4"

        # Fazer upload do vídeo
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": "Descrição do vídeo",
                    "tags": tags,
                    "categoryId": 22
                },
                "status": {
                    "privacyStatus": "public"
                }
            },
            media_body=MediaFileUpload(os.path.join(VIDEOS_FOLDER, file_name), resumable=True)
        )
        response = request.execute()
        print(f"Vídeo {title} enviado com sucesso. ID do vídeo: {response['id']}")
    except HttpError as error:
        print(f"An error occurred: {error}")
