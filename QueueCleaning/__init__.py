import logging

import azure.functions as func
from time import sleep

def main(msg: func.QueueMessage) -> None:
    sleep(20)
    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))
