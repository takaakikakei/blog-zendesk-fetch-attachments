import logging

import src.use_cases.fetch

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context) -> None:
    """
    fetchのエントリーポイント
    event:
    {
        "zendesk_id": "12345"
    }
    """
    logger.info(f"event: {event}")

    try:
        zendesk_id = event["zendesk_id"]
        src.use_cases.fetch.exec(zendesk_id)
        return
    except Exception as e:
        logger.exception(e)
        raise e
