import boto3
import os
import sys
import uuid
import PIL
from PIL import Image
import PIL.Image

     
s3_client = boto3.client('s3')

#resize image function (Added Aris, 18 Aug 2019)
def resize_image(image_path, resized_path):
    size = 128, 128
    with Image.open(image_path) as image:
        image.thumbnail(size)
        image.save(resized_path)
     
def lambda_handler(event, context):
    
    print("create-thumbnail function is called!")
    bucket = str(event["Bucket"])
    key = str(event["Filename"])
    print(bucket)
    print(key)
    
    download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
    upload_path = '/tmp/resized-{}'.format(key)
        
    s3_client.download_file(bucket, key, download_path)
    resize_image(download_path, upload_path)
    s3_client.upload_file(upload_path, '{}resized'.format(bucket), key)
    
    
    
