"""
download data from aws s3 bucket pandas-coverage
"""

import boto3

client = boto3.client("s3")
s3 = boto3.resource("s3")

bucket = s3.Bucket("pandas-coverage")

myfiles = list(bucket.objects.all())
for file in myfiles:
    client.download_file("pandas-coverage", file.key, file.key)
