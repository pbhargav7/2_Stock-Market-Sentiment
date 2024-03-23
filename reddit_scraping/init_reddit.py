import logging
import time
import faktory
from datetime import datetime, timedelta
from faktory import Worker

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')


with faktory.connection(faktory="tcp://:some_password@localhost:7419") as client:
    run_at = datetime.utcnow() + timedelta(minutes=5)
    run_at = run_at.isoformat()[:-7] + "Z"
    logging.info(f'run_at: {run_at}')
    client.queue("crawl_catalog", queue="crawl_catalogs", at=run_at)