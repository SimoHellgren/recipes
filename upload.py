import boto3
from pathlib import Path

s3 = boto3.client("s3")

for file in Path("./build").glob("*"):
    s3.upload_file(
        file,
        "assume-garlic",
        file.name,
        ExtraArgs={"ContentType": "text/html; charset=utf-8"},
    )
