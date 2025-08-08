import slack_sdk
import os

# Lấy token từ môi trường hoặc gán trực tiếp (không khuyến khích)
# Tốt nhất là lưu token trong biến môi trường
slack_token = os.getenv("SLACK_TOKEN")
# Thay thế channel ID hoặc channel name của bạn
channel_id = os.getenv("SLACK_CHANNEL_ID") 
client = slack_sdk.WebClient(token=slack_token)

def send_image_to_slack(file_path, message=""):
    try:
        # check file_path exist
        if not os.path.exists(file_path):
            print(f"File {file_path} không tồn tại.")
            return
        # check if is temp or hidden file
        if os.path.basename(file_path).startswith('.'):
            print(f"Bỏ qua file {file_path} là file tạm hoặc ẩn.")
            return
        # Gửi tệp ảnh lên Slack
        response = client.files_upload_v2(
            channel=channel_id,
            file=file_path,
            initial_comment=message  # Thêm một tin nhắn văn bản kèm theo ảnh
        )
        print(f"Ảnh đã được gửi thành công. File ID: {response['file']['id']}")
    except slack_sdk.errors.SlackApiError as e:
        print(f"Lỗi khi gửi ảnh: {e.response['error']}")

def send_slack_message(message):
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            text=message
        )
        print(f"Tin nhắn đã được gửi thành công. Timestamp: {response['ts']}")
    except slack_sdk.errors.SlackApiError as e:
        print(f"Lỗi khi gửi tin nhắn: {e.response['error']}")

