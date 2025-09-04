import os
from io import BytesIO
from aws_services_common.aws_services import AWSConnection

BUCKET_NAME = os.getenv('BUCKET_NAME')
aws_services = AWSConnection()
s3_client = aws_services.get_client('s3')

def save_file(content, file_name, folder_name):
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=f'{folder_name}/{file_name}',
        Body=content.encode("utf-8"),
        ContentType="application/json"
    )