# ImageWatch.py

import time
import logging
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Danh sách các định dạng ảnh mà chúng ta muốn theo dõi
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

class ImageHandler(FileSystemEventHandler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            _, file_extension = os.path.splitext(file_path)
            # check is temp file name
            if os.path.basename(file_path).startswith('.'):
                print(f"Bỏ qua tệp ẩn hoặc tệp tạm thời: {file_path}")
                return
            if file_extension.lower() in IMAGE_EXTENSIONS:
                print(f"Phát hiện ảnh mới: {file_path}")
                self.callback(file_path)

def start_watching(folder_path, callback):
    """
    Hàm bắt đầu theo dõi một thư mục.
    
    Args:
        folder_path (str): Đường dẫn đến thư mục cần theo dõi.
        callback (function): Hàm sẽ được gọi khi phát hiện ảnh mới.
    """
    event_handler = ImageHandler(callback)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    
    observer.start()
    
    print(f"Bắt đầu theo dõi thư mục: {folder_path}")
    print("Nhấn Ctrl+C để dừng.")

    try:
        while observer.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()