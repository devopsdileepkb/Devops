import boto3
import zipfile
import os
from datetime import datetime

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = os.environ['BUCKET_NAME']
    prefix = "mydir/"
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    zip_key = f"{prefix}archive-{timestamp}.zip"

    objects = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    if 'Contents' not in objects:
        return {"status": "No files found"}

    with zipfile.ZipFile("/tmp/archive.zip", 'w') as z:
        for obj in objects['Contents']:
            key = obj['Key']
            if key.endswith("/"):
                continue
            tmp_path = f"/tmp/{os.path.basename(key)}"
            s3.download_file(bucket, key, tmp_path)
            z.write(tmp_path, arcname=os.path.basename(key))

    s3.upload_file("/tmp/archive.zip", bucket, zip_key)
    return {"status": "success", "zip_key": zip_key}