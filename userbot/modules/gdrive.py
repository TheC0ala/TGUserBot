# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# UserLand - by BABAŞ #

import asyncio
import math
import os
import time
from pySmartDL import SmartDL
from telethon import events
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from userbot import (G_DRIVE_CLIENT_ID, G_DRIVE_CLIENT_SECRET,
                     G_DRIVE_AUTH_TOKEN_DATA, GDRIVE_FOLDER_ID, BOTLOG_CHATID,
                     TEMP_DOWNLOAD_DIRECTORY, CMD_HELP, LOGS)
from userbot.events import register
from mimetypes import guess_type
import httplib2
from userbot.modules.upload_download import progress, humanbytes
from userbot.cmdhelp import CmdHelp

G_DRIVE_TOKEN_FILE = "./auth_token.txt"
CLIENT_ID = G_DRIVE_CLIENT_ID
CLIENT_SECRET = G_DRIVE_CLIENT_SECRET
OAUTH_SCOPE = "https://www.googleapis.com/auth/drive.file"
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
parent_id = GDRIVE_FOLDER_ID
G_DRIVE_DIR_MIME_TYPE = "application/vnd.google-apps.folder"


@register(pattern=r"^.gdrive(?: |$)(.*)", outgoing=True)
async def gdrive_upload_function(dryb):
    await dryb.edit("İşlənir...")
    input_str = dryb.pattern_match.group(1)
    if CLIENT_ID is None or CLIENT_SECRET is None:
        return
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
        required_file_name = None
    if "|" in input_str:
        url, file_name = input_str.split("|")
        url = url.strip()
        # https://stackoverflow.com/a/761825/4723940
        file_name = file_name.strip()
        head, tail = os.path.split(file_name)
        if head:
            if not os.path.isdir(os.path.join(TEMP_DOWNLOAD_DIRECTORY, head)):
                os.makedirs(os.path.join(TEMP_DOWNLOAD_DIRECTORY, head))
                file_name = os.path.join(head, tail)
        downloaded_file_name = TEMP_DOWNLOAD_DIRECTORY + "" + file_name
        downloader = SmartDL(url, downloaded_file_name, progress_bar=False)
        downloader.start(blocking=False)
        c_time = time.time()
        display_message = None
        while not downloader.isFinished():
            status = downloader.get_status().capitalize()
            total_length = downloader.filesize if downloader.filesize else None
            downloaded = downloader.get_dl_size()
            now = time.time()
            diff = now - c_time
            percentage = downloader.get_progress() * 100
            speed = downloader.get_speed()
            elapsed_time = round(diff) * 1000
            progress_str = "[{0}{1}] {2}%".format(
                ''.join(["▰" for i in range(math.floor(percentage / 10))]),
                ''.join(["▱"
                         for i in range(10 - math.floor(percentage / 10))]),
                round(percentage, 2))
            estimated_total_time = downloader.get_eta(human=True)
            try:
                current_message = f"{status}...\
                \nURL: {url}\
                \nFayl adı: {file_name}\
                \n{progress_str}\
                \n{humanbytes(downloaded)} of {humanbytes(total_length)}\
                \nBitiş: {estimated_total_time}"

                if round(diff %
                         10.00) == 0 and current_message != display_message:
                    await dryb.edit(current_message)
                    display_message = current_message
            except Exception as e:
                LOGS.info(str(e))
                pass
        if downloader.isSuccessful():
            await dryb.edit(
                "`{}` yükləmə uğurludur. \nGoogle Drive'a yükləmə başladılır..."
                .format(downloaded_file_name))
            required_file_name = downloaded_file_name
        else:
            await dryb.edit("Keçərsiz URL\n{}".format(url))
    elif input_str:
        input_str = input_str.strip()
        if os.path.exists(input_str):
            required_file_name = input_str
            await dryb.edit(
                "`{}` faylı serverdə tapıldı. Google Drive'a yükləmə başladılır.."
                .format(input_str))
        else:
            await dryb.edit(
                "Serverdə fayl tapılmadı. Zəhmət olmasa düzgün fayl yolunu yazın.")
            return False
    elif dryb.reply_to_msg_id:
        try:
            c_time = time.time()
            downloaded_file_name = await dryb.client.download_media(
                await dryb.get_reply_message(),
                TEMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop(
                ).create_task(progress(d, t, dryb, c_time, "Yüklənilir...")))
        except Exception as e:
            await dryb.edit(str(e))
        else:
            required_file_name = downloaded_file_name
            await dryb.edit(
                "`{}` yeirnə yükləmə uğurla başa çatdı. \nGoogle Drive'a yükləmə başladılır..."
                .format(downloaded_file_name))
    if required_file_name:
        if G_DRIVE_AUTH_TOKEN_DATA is not None:
            with open(G_DRIVE_TOKEN_FILE, "w") as t_file:
                t_file.write(G_DRIVE_AUTH_TOKEN_DATA)
        if not os.path.isfile(G_DRIVE_TOKEN_FILE):
            storage = await create_token_file(G_DRIVE_TOKEN_FILE, dryb)
            http = authorize(G_DRIVE_TOKEN_FILE, storage)
        http = authorize(G_DRIVE_TOKEN_FILE, None)
        file_name, mime_type = file_ops(required_file_name)
        try:
            g_drive_link = await upload_file(http, required_file_name,
                                             file_name, mime_type, dryb,
                                             parent_id)
            await dryb.edit(
                f"Fayl :`{required_file_name}`\nUpload uğuruludur! \nYükləmə linki: [Google Drive]({g_drive_link})!"
            )
        except Exception as e:
            await dryb.edit(
                f"Google Drive'a yükləmə uğursuz.\nXəta kodu:\n`{e}`")


@register(pattern=r"^.ggd(?: |$)(.*)", outgoing=True)
async def upload_dir_to_gdrive(event):
    await event.edit("İşlənilir...")
    if CLIENT_ID is None or CLIENT_SECRET is None:
        return
    input_str = event.pattern_match.group(1)
    if os.path.isdir(input_str):
        if G_DRIVE_AUTH_TOKEN_DATA is not None:
            with open(G_DRIVE_TOKEN_FILE, "w") as t_file:
                t_file.write(G_DRIVE_AUTH_TOKEN_DATA)
        storage = None
        if not os.path.isfile(G_DRIVE_TOKEN_FILE):
            storage = await create_token_file(G_DRIVE_TOKEN_FILE, event)
        http = authorize(G_DRIVE_TOKEN_FILE, storage)
        dir_id = await create_directory(
            http, os.path.basename(os.path.abspath(input_str)), parent_id)
        await DoTeskWithDir(http, input_str, event, dir_id)
        dir_link = "https://drive.google.com/folderview?id={}".format(dir_id)
        await event.edit(f"Google Drive bağlantınız [buradadır]({dir_link})")
    else:
        await event.edit(f"{input_str} tapılmadı.")


@register(pattern=r"^.list(?: |$)(.*)", outgoing=True)
async def gdrive_search_list(event):
    await event.edit("İşlənilir...")
    if CLIENT_ID is None or CLIENT_SECRET is None:
        return
    input_str = event.pattern_match.group(1).strip()
    if G_DRIVE_AUTH_TOKEN_DATA is not None:
        with open(G_DRIVE_TOKEN_FILE, "w") as t_file:
            t_file.write(G_DRIVE_AUTH_TOKEN_DATA)
    storage = None
    if not os.path.isfile(G_DRIVE_TOKEN_FILE):
        storage = await create_token_file(G_DRIVE_TOKEN_FILE, event)
    http = authorize(G_DRIVE_TOKEN_FILE, storage)
    await event.edit(f"Google Drive'ınızda {input_str} axtarılır...")
    gsearch_results = await gdrive_search(http, input_str)
    await event.edit(gsearch_results, link_preview=False)


@register(
    pattern=
    r"^.gsetf https?://drive\.google\.com/drive/u/\d/folders/([-\w]{25,})",
    outgoing=True)
async def download(set):
    await set.edit("İşlənilir...")
    input_str = set.pattern_match.group(1)
    if input_str:
        parent_id = input_str
        await set.edit(
            "Xüsusi qovluq ID'si uğurla ayarlandı. Sonrakı uploadlar buraya uploadlanacaq: {parent_id} (`.gsetclear` komandasını vermədiyinizcə)"
        )
        await set.delete()
    else:
        await set.edit(
            ".gdrivesp <GDrive Klasörü> komandası ilə yeni qovluqların uploadlanacağı qovluğu yaza bilərsiniz."
        )


@register(pattern="^.gsetclear$", outgoing=True)
async def download(gclr):
    await gclr.reply("İşleniyor ...")
    parent_id = GDRIVE_FOLDER_ID
    await gclr.edit("Xüsusi qovluq ID'si uğurla təmizləndi.")


@register(pattern="^.gfolder$", outgoing=True)
async def show_current_gdrove_folder(event):
    if parent_id:
        folder_link = f"https://drive.google.com/drive/folders/" + parent_id
        await event.edit(
            f"UserBot'um qovluqları [buraya]({folder_link}) uploadlanır.")
    else:
        await event.edit(
            f"UserBot'um faylları Google Drive'ın kökünə uploadlayır.\
            \nUploadlanan fayllar [burada](https://drive.google.com/drive/my-drive)"
        )


def file_ops(file_path):
    mime_type = guess_type(file_path)[0]
    mime_type = mime_type if mime_type else "text/plain"
    file_name = file_path.split("/")[-1]
    return file_name, mime_type


async def create_token_file(token_file, event):
    flow = OAuth2WebServerFlow(CLIENT_ID,
                               CLIENT_SECRET,
                               OAUTH_SCOPE,
                               redirect_uri=REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()
    async with event.client.conversation(BOTLOG_CHATID) as conv:
        await conv.send_message(
            f"Bu linkə get və kodu kopyalayıb cavabla: {authorize_url}"
        )
        response = conv.wait_event(
            events.NewMessage(outgoing=True, chats=BOTLOG_CHATID))
        response = await response
        code = response.message.message.strip()
        credentials = flow.step2_exchange(code)
        storage = Storage(token_file)
        storage.put(credentials)
        return storage


def authorize(token_file, storage):
    if storage is None:
        storage = Storage(token_file)
    credentials = storage.get()
    http = httplib2.Http()
    credentials.refresh(http)
    http = credentials.authorize(http)
    return http


async def upload_file(http, file_path, file_name, mime_type, event, parent_id):
    drive_service = build("drive", "v2", http=http, cache_discovery=False)
    media_body = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
    body = {
        "title": file_name,
        "description": "UserLand işlədilərək yükləndi.",
        "mimeType": mime_type,
    }
    if parent_id:
        body["parents"] = [{"id": parent_id}]
    permissions = {
        "role": "reader",
        "type": "anyone",
        "value": None,
        "withLink": True
    }

    file = drive_service.files().insert(body=body, media_body=media_body)
    response = None
    display_message = ""
    while response is None:
        status, response = file.next_chunk()
        await asyncio.sleep(1)
        if status:
            percentage = int(status.progress() * 100)
            progress_str = "[{0}{1}] {2}%".format(
                "".join(["▰" for i in range(math.floor(percentage / 10))]),
                "".join(["▱"
                         for i in range(10 - math.floor(percentage / 10))]),
                round(percentage, 2))
            current_message = f"Google Drive'a uploadlanır.\nFayl adı: {file_name}\n{progress_str}"
            if display_message != current_message:
                try:
                    await event.edit(current_message)
                    display_message = current_message
                except Exception as e:
                    LOGS.info(str(e))
                    pass
    file_id = response.get("id")
    drive_service.permissions().insert(fileId=file_id,
                                       body=permissions).execute()
    file = drive_service.files().get(fileId=file_id).execute()
    download_url = file.get("webContentLink")
    return download_url


async def create_directory(http, directory_name, parent_id):
    drive_service = build("drive", "v2", http=http, cache_discovery=False)
    permissions = {
        "role": "reader",
        "type": "anyone",
        "value": None,
        "withLink": True
    }
    file_metadata = {
        "title": directory_name,
        "mimeType": G_DRIVE_DIR_MIME_TYPE
    }
    if parent_id:
        file_metadata["parents"] = [{"id": parent_id}]
    file = drive_service.files().insert(body=file_metadata).execute()
    file_id = file.get("id")
    drive_service.permissions().insert(fileId=file_id,
                                       body=permissions).execute()
    LOGS.info("Created Gdrive Folder:\nName: {}\nID: {} ".format(
        file.get("title"), file_id))
    return file_id


async def DoTeskWithDir(http, input_directory, event, parent_id):
    list_dirs = os.listdir(input_directory)
    if len(list_dirs) == 0:
        return parent_id
    r_p_id = None
    for a_c_f_name in list_dirs:
        current_file_name = os.path.join(input_directory, a_c_f_name)
        if os.path.isdir(current_file_name):
            current_dir_id = await create_directory(http, a_c_f_name,
                                                    parent_id)
            r_p_id = await DoTeskWithDir(http, current_file_name, event,
                                         current_dir_id)
        else:
            file_name, mime_type = file_ops(current_file_name)
            g_drive_link = await upload_file(http, current_file_name,
                                             file_name, mime_type, event,
                                             parent_id)
            r_p_id = parent_id
    # Ediləcəklər: Burada bir bug var :/
    return r_p_id


async def gdrive_list_file_md(service, file_id):
    try:
        file = service.files().get(fileId=file_id).execute()
        # LOGS.info(dosya)
        file_meta_data = {}
        file_meta_data["title"] = file["title"]
        mimeType = file["mimeType"]
        file_meta_data["createdDate"] = file["createdDate"]
        if mimeType == G_DRIVE_DIR_MIME_TYPE:
            file_meta_data["mimeType"] = "directory"
            file_meta_data["previewURL"] = file["alternateLink"]
        else:
            # bir dosya ise
            file_meta_data["mimeType"] = file["mimeType"]
            file_meta_data["md5Checksum"] = file["md5Checksum"]
            file_meta_data["fileSize"] = str(humanbytes(int(file["fileSize"])))
            file_meta_data["quotaBytesUsed"] = str(
                humanbytes(int(file["quotaBytesUsed"])))
            file_meta_data["previewURL"] = file["downloadUrl"]
        return json.dumps(file_meta_data, sort_keys=True, indent=4)
    except Exception as e:
        return str(e)


async def gdrive_search(http, search_query):
    if parent_id:
        query = "'{}' in parents and (title contains '{}')".format(
            parent_id, search_query)
    else:
        query = "title contains '{}'".format(search_query)
    drive_service = build("drive", "v2", http=http, cache_discovery=False)
    page_token = None
    res = ""
    while True:
        try:
            response = drive_service.files().list(
                q=query,
                spaces="drive",
                fields="nextPageToken, items(id, title, mimeType)",
                pageToken=page_token).execute()
            for file in response.get("items", []):
                file_title = file.get("title")
                file_id = file.get("id")
                if file.get("mimeType") == G_DRIVE_DIR_MIME_TYPE:
                    res += f"`[FOLDER] {file_title}`\nhttps://drive.google.com/drive/folders/{file_id}\n\n"
                else:
                    res += f"`{file_title}`\nhttps://drive.google.com/uc?id={file_id}&export=download\n\n"
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break
        except Exception as e:
            res += str(e)
            break
    msg = f"**Google Drive Axtarışı**:\n`{search_query}`\n\n**Nəticələr**\n\n{res}"
    return msg

CmdHelp('gdrive').add_command(
    'gdrive', '<fayl yolu / cavablayaraq / URL|qovluq-adı>', 'Seçilən faylı Google Drive\'a upload edər.'
).add_command(
    'gsetf', '<GDrive Qovluq URL\'si>', 'Yeni faylların upladlanacağı qovluqu seçər.'
).add_command(
    'gsetclear', None, 'Hal hazırdakı işlənən upload yeirni göstərər.'
).add_command(
    'list', '<sorğu>', 'Google Drive\'da olan fayllr.'
).add_command(
    'ggd', '<serverdəki-qovluq-yolu>', 'Seçilən yerdəki bütün faylları Google Drive\'a upload edər.'
).add()
