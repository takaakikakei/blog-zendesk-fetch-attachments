import logging

import src.use_cases.fetch

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    """
    fetchのエントリーポイント
    event:
    {
        "zendesk_id": "12345"
    }
    return:
        TBD
    """
    logger.info(f"event: {event}")

    try:
        zendesk_id = event["zendesk_id"]
        resp = src.use_cases.fetch.exec(zendesk_id)
        logger.info(f"src.use_cases.fetch.exec -> {resp}")
        return resp
    except Exception as e:
        logger.exception(e)
        raise e
