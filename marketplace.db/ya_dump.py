from YaDiskClient.YaDiskClient import YaDisk
from dotenv import load_dotenv
import time
import os


def make_connection(username, password):
    return YaDisk(username, password)


def upload_gzip_file_with_timestamp(conn, src, dst):
    src = f'{src}.tar.gz'
    timestamp = str(time.time()).split('.')[0]
    file_name = f'{dst}{timestamp}.tar.gz'
    conn.upload(src, file_name)


def main():
    load_dotenv()
    username = os.getenv('YANDEX_DISK_USERNAME')
    password = os.getenv('YANDEX_DISK_PASSWORD')
    user_image_dir_name = os.getenv('USER_IMAGE_DIR_NAME')
    disk = make_connection(username, password)
    upload_gzip_file_with_timestamp(disk, user_image_dir_name, user_image_dir_name)


if __name__ == '__main__':
    main()
