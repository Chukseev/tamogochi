from minio import Minio
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env
load_dotenv()

# Чтение параметров MinIO из .env
minio_config = {
    'endpoint': os.getenv('MINIO_ENDPOINT'),
    'access_key': os.getenv('MINIO_ACCESS_KEY'),
    'secret_key': os.getenv('MINIO_SECRET_KEY'),
    'bucket_name': os.getenv('MINIO_BUCKET_NAME'),
}

# Инициализация клиента MinIO
client = Minio(
    endpoint=minio_config['endpoint'],
    access_key=minio_config['access_key'],
    secret_key=minio_config['secret_key'],
    secure=False
)

bucket_name = minio_config['bucket_name']


def get_img(object_name):
    """Загрузка изображения из MinIO и его обработка с помощью PIL."""
    image_object = client.get_object(bucket_name, object_name)
    image_data = BytesIO(image_object.read())
    image = Image.open(image_data)
    image_object.close()
    return image
