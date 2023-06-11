import re
import urllib.parse
import os

import extraction
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


def gen_gdrive_file_name(gdrive_id):
    url = f"https://drive.google.com/open?id={gdrive_id}"
    html = requests.get(url).text
    return extraction.Extractor().extract(html, source_url=url).title


def gdrive_extract_id(gdrive_link):
    match = re.match(
        r"^https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)/?.*$", gdrive_link
    )
    if match:
        return match.group(1)
    query_params = urllib.parse.parse_qs(urllib.parse.urlparse(gdrive_link).query)
    if "id" in query_params:
        return query_params["id"][0]
    return None


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value
    return None


def download(update: Update, context: CallbackContext):
    gd_id = context.args[0]
    if gd_id != "":
        id = gd_id
        URL = "https://docs.google.com/uc?export=download"
        session = requests.Session()
        response = session.get(URL, params={"id": id, "confirm": 1}, stream=True)
        token = get_confirm_token(response)
        if token:
            params = {"id": id, "confirm": token}
            response = session.get(URL, params=params, stream=True)

        file_name = gen_gdrive_file_name(id)
        with open(file_name, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        update.message.reply_document(
            document=open(file_name, "rb"),
            filename=file_name,
            caption=f"Here's your file: {file_name}",
        )
        os.remove(file_name)

    else:
        update.message.reply_text("Invalid Link")


def upload(update: Update, context: CallbackContext):
    file_path = context.args[0]
    if os.path.isdir(file_path):
        for file_name in os.listdir(file_path):
            full_path = os.path.join(file_path, file_name)
            if os.path.isfile(full_path):
                update.message.reply_document(
                    document=open(full_path, "rb"),
                    filename=file_name,
                    caption=f"Here's your file: {file_name}",
                )
            else:
                update.message.reply_text(
                    f"{file_name} is not a file and will not be uploaded."
                )
    else:
        update.message.reply_text(f"{file_path} is not a directory.")


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Telegram Google Drive Downloader bot!")


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("YOUR_BOT_TOKEN_HERE")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add handlers for /start, /download, and /upload commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("download", download))
    dp.add_handler(CommandHandler("upload", upload))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == "__main__":
    main()
