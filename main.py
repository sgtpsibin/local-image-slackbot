import os
from dotenv import load_dotenv
load_dotenv()
from SendMessage import send_image_to_slack
from ImageWatch import start_watching

watch_dir = os.getenv("IMAGE_WATCH_DIR")


if __name__ == "__main__":
    start_watching(watch_dir, send_image_to_slack)