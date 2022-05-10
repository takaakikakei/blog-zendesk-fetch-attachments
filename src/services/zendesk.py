import logging
from typing import List

from zenpy import Zenpy

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ZendeskService:
    def __init__(self, zenpy_client: Zenpy):
        self._client = zenpy_client

    def get_ticket_comments(self, ticket_id: str) -> List:
        comments = list(self._client.tickets.comments(ticket_id))
        logger.info(comments)
        return comments

    def get_attachments(self, comment) -> List:
        attachments: List = comment.attachments
        logger.info(attachments)
        return attachments

    def download_attachment(self, attachment_id, destination) -> None:
        logger.info("ダウンロード開始")
        resp = self._client.attachments.download(attachment_id, destination)
        logger.info(resp)
        logger.info("ダウンロード完了")
        return
