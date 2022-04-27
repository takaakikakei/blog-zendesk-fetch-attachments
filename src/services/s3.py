import logging

import boto3.session
from botocore.config import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class S3Service:
    def __init__(self):
        self.session = boto3.session.Session()
        self.resource = self.session.resource("s3", config=Config())

    def upload_file(self, file_name: str, bucket: str, key=None):
        if key is None:
            key = file_name
        self.resource.meta.client.upload_file(file_name, bucket, key)
        return
