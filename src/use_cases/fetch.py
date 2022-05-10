import glob
import json
import logging
import os
import uuid
from typing import List

import boto3
from src.services.s3 import S3Service
from src.services.zendesk import ZendeskService
from zenpy import Zenpy

TOKYO = "ap-northeast-1"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class FetchAttachmentsUseCase:
    def __init__(self, zendesk_service: ZendeskService, s3_service: S3Service):
        self.zendesk_service = zendesk_service
        self.s3_service = s3_service

    def exec(self, zendesk_id: str) -> None:
        # 対象チケットの最新コメントから添付ファイルを取得する
        comments: List = self.zendesk_service.get_ticket_comments(zendesk_id)
        latest_comment = comments[len(comments) - 1]
        attachments: List = self.zendesk_service.get_attachments(latest_comment)

        for attachment in attachments:
            attachment_id = attachment.id
            destination = f"/tmp/{uuid.uuid4()}"
            self.zendesk_service.download_attachment(attachment_id, destination)
            self.s3_service.upload_file(destination, "zendesk")

        logger.info(os.listdir("/tmp/"))
        for p in glob.glob("/tmp/" + "*"):
            if os.path.isfile(p):
                os.remove(p)
        logger.info(os.listdir("/tmp/"))

        return


def _init_use_case() -> FetchAttachmentsUseCase:
    # fetch secret
    secret_name = os.environ["SECRET"]
    secretsmanager = boto3.client("secretsmanager", region_name=TOKYO)
    resp = secretsmanager.get_secret_value(SecretId=secret_name)
    secret = json.loads(resp["SecretString"])

    # zendesk service
    credentials = {
        "token": secret["token"],
        "email": secret["email"],
        "subdomain": secret["subdomain"],
    }
    zenpy_client = Zenpy(**credentials)
    zendesk_service = ZendeskService(zenpy_client)

    # s3 service
    bucket = secret["bucket"]
    s3_service = S3Service(bucket)

    return FetchAttachmentsUseCase(zendesk_service, s3_service)


def exec(zendesk_id: str) -> None:
    use_case = _init_use_case()
    return use_case.exec(zendesk_id)
