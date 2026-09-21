import io
import os

from dotenv import load_dotenv
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

load_dotenv()


def oauth2_authentication():
  client_secret_file = os.getenv(
      "GOOGLE_CLIENT_SECRET_FILE",
      os.path.join(os.path.dirname(__file__), "credentials.json"),
  )
  flow = InstalledAppFlow.from_client_secrets_file(
      client_secret_file,
      scopes=[
          "https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/drive.readonly",
      ],
  )

  # Redirects user to local server to fetch credentials.
  flow.run_local_server()

  creds = flow.credentials
  return creds


def download_file(real_file_id, creds):
  """Downloads a file."""

  try:
    service = build(
        "drive",
        "v3",
        credentials=creds,
        developerKey=os.getenv("GOOGLE_DEVELOPER_KEY", ""),
    )

    file_id = real_file_id

    request = service.files().get_media(fileId=file_id)
    file = io.BytesIO()
    print(request)
    print("\n\n\n")

    downloader = MediaIoBaseDownload(file, request)
    done = False
    while done is False:
      status, done = downloader.next_chunk()
      print(f"Download {int(status.progress() * 100)}.")

  except HttpError as error:
    print(f"An error occurred: {error}")
    file = None

  with open("downloaded_file.pdf", "wb") as f:
    f.write(file.getvalue())

  return file.getvalue()


if __name__ == "__main__":
  download_file(os.getenv("GOOGLE_DRIVE_FILE_ID"), oauth2_authentication())
  