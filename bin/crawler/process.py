#!/usr/bin/env python

from .logging import default_logger
import time


def do_some(data, task, updated,
            sleep_sec=1,
            updated_message='{item} updated',
            nochange_message='{item} nochange',
            failed_message='{item} failed',
            logger=default_logger):
    for item in data:
        try:
            r = task(item)
            if updated(r):
                logger.info(updated_message.format(item=item))
                time.sleep(sleep_sec)
            else:
                logger.info(nochange_message.format(item=item))
        except Exception as e:
            logger.warn(failed_message.format(item=item))
            logger.debug(e)


def do_batch(paginate, task, updated,
             sleep_sec=1,
             updated_message='{item} updated',
             nochange_message='{item} nochange',
             failed_message='{item} failed',
             logger=default_logger):
    for data in paginate:
        time.sleep(sleep_sec)
        do_some(data, task, updated,
                updated_message=updated_message,
                nochange_message=nochange_message,
                failed_message=failed_message)
        time.sleep(sleep_sec)
