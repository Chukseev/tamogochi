from minio import Minio
from PIL import Image
from io import BytesIO
import yaml

with open('config1.yaml', 'r') as file:
    config = yaml.safe_load(file)

config_minio = config['minio']

client = Minio(
    endpoint=config_minio['endpoint'],
    access_key=config_minio['access_key'],
    secret_key=config_minio['secret_key'],
    secure=False
)

bucket_name = config_minio['bucket_name']


def get_img(object_name):
    image_object = client.get_object(bucket_name, object_name)
    image_data = BytesIO(image_object.read())
    image = Image.open(image_data)
    image_object.close()
    return image

