import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Danh sách các định dạng ảnh mà chúng ta muốn theo dõi
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
DEBOUNCE_INTERVAL = 5  # Khoảng thời gian dedup tính bằng giây.

class ImageHandler(FileSystemEventHandler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.processed_files = {}  # Bộ nhớ đệm để lưu tên file và thời gian xử lý

    def _should_process_file(self, file_path):
        """Kiểm tra xem file đã được xử lý gần đây chưa."""
        file_name = os.path.basename(file_path)
        current_time = time.time()
        
        last_processed_time = self.processed_files.get(file_name, 0)
        
        if current_time - last_processed_time > DEBOUNCE_INTERVAL:
            self.processed_files[file_name] = current_time
            return True
        return False

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            # Bỏ qua tệp tạm thời trên macOS
            if os.path.basename(file_path).startswith('.'):
                return
            self._handle_event(file_path)

    def on_moved(self, event):
        if not event.is_directory:
            file_path = event.dest_path
            self._handle_event(file_path)
    
    def _handle_event(self, file_path):
        """Hàm nội bộ để xử lý logic chung cho các sự kiện."""
        _, file_extension = os.path.splitext(file_path)
        
        if file_extension.lower() in IMAGE_EXTENSIONS:
            if self._should_process_file(file_path):
                print(f"Phát hiện ảnh mới: {file_path}")
                self.callback(file_path)
            else:
                print(f"File trùng lặp cho {os.path.basename(file_path)}, đã bỏ qua.")


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
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

