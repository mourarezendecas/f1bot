import os
import json
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

def list_folders(folder_name):
    bucket_name = "f1storage"
    prefixo = f"races/{folder_name}/"

    paginator = s3_client.get_paginator("list_objects_v2")
    pastas = []

    for pagina in paginator.paginate(Bucket=bucket_name, Prefix=prefixo, Delimiter="/"):
        for p in pagina.get("CommonPrefixes", []):
            pastas.append(p["Prefix"])

    return pastas

def get_json_to_dict(s3_key):
    response = s3_client.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=s3_key
    )

    if 'Contents' not in response:
        raise FileNotFoundError(f"Nenhum arquivo encontrado em s3://{BUCKET_NAME}/{s3_key}")

    json_files = [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith('.json')]

    if not json_files:
        raise FileNotFoundError(f"Nenhum arquivo JSON encontrado em s3://{BUCKET_NAME}/{s3_key}")

    json_key = json_files[0]
    print(f"Lendo arquivo: s3://{BUCKET_NAME}/{json_key}")

    obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=json_key)
    json_data = json.loads(obj['Body'].read().decode('utf-8'))

    return json_data