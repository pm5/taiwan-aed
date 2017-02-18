#!/usr/bin/env python

from .logging import default_logger
import time


def do_some(data, task, updated,
            sleep_sec=1,
            updated_message='{item} updated',
            nochange_message='{item} nochange',
            failed_message='{item} failed',
            logger=default_logger):
    count = 0
    for i, item in enumerate(data):
        try:
            r = task(item)
            if updated(r):
                logger.info(updated_message.format(item=item))
                count = count + 1
                if i < len(data) - 1:
                    time.sleep(sleep_sec)
            else:
                logger.info(nochange_message.format(item=item))
        except Exception as e:
            logger.warn(failed_message.format(item=item))
            logger.debug(e)
    return count


def do_batch(paginate, task, updated,
             sleep_sec=1,
             updated_message='{item} updated',
             nochange_message='{item} nochange',
             failed_message='{item} failed',
             logger=default_logger):
    for data in paginate:
        time.sleep(sleep_sec)
        r = do_some(data, task, updated,
                    updated_message=updated_message,
                    nochange_message=nochange_message,
                    failed_message=failed_message)
        if r > 0:
            time.sleep(sleep_sec)
