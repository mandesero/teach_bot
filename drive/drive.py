from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build
import pprint as pp
import io
import os


def get_folder_id(name):
    files = service.files().list(fields="files(id, name, mimeType)").execute()["files"]
    for file in files:
        if file["name"] == name and file["mimeType"] == "application/vnd.google-apps.folder":
            return file["id"]
    return ""


def get_folder_parent_id(name):
    file_id = get_folder_id(name)
    return service.files().get(fileId=file_id, fields="parents").execute()["parents"][0]


def create_folder(parent_name, name):
    parent_id = get_folder_id(parent_name)
    file_metadata = {
        "name": name,
        "mimeType": 'application/vnd.google-apps.folder',
        "parents": [parent_id]
    }
    return service.files().create(body=file_metadata, fields='id').execute()["id"]


def upload_work(lesson, work):
    folder_id = get_folder_id("Lesson_" + str(lesson))
    name = str(lesson) + "_" + str(work) + "_W.py"
    file_path = os.path.abspath(f"../works/{name}")

    file_metadata = {
        'name': name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    return service.files().create(body=file_metadata, media_body=media, fields='id').execute()["id"]


def delete_work():
    pass


SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "C:\\Users\\Mandesero\\Desktop\\Curse Bot\\leafy-clone-344520-cd97be7971a5.json"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

# results = service.files().list(pageSize=10,
#                                fields="nextPageToken, files(id, name, mimeType)").execute()
# pp.pprint(
#     service.files().list(pageSize=10, fields="nextPageToken, files(id, name, mimeType)").execute()["files"]
# )
# ===================parents id=======================
# file_id = get_folder_id("New folder")
# print(file_id)
# r = service.files().get(fileId=file_id, fields="parents").execute()
# pp.pprint(service.files().list(fields="files(id, name, mimeType)").execute()["files"])

# create_folder(parent_name="School", name="1")

# file_path = os.path.abspath("../works/1_1_W.py")
# print(file_path)
# results["files"]

# school = results["files"][0]["id"]
#
#
# name = "New folder"
# file_metadata = {
#     "name": name,
#     "mimeType": 'application/vnd.google-apps.folder',
#     "parents": [school]
# }
# r = service.files().create(body=file_metadata, fields='id').execute()
# pp.pprint(r)

# upload_work(1, 1)

# create_folder("school", "Lesson_1")

# pp.pprint(get_folder_id("Lesson_" + str(1)))
