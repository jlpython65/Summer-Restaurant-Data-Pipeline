
import io
import os

from dotenv import load_dotenv
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
    "GOOGLE_CLIENT_SECRET_FILE",
    os.path.join(os.path.dirname(__file__), "credentials.json"),
)


def download_file(real_file_id):
  """Downloads a file."""
  creds, _ = google.auth.default()

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
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while done is False:
      status, done = downloader.next_chunk()
      print(f"Download {int(status.progress() * 100)}.")

  except HttpError as error:
    print(f"An error occurred: {error}")
    file = None

  return file.getvalue()


if __name__ == "__main__":
  download_file(real_file_id=os.getenv("GOOGLE_DRIVE_FILE_ID"))