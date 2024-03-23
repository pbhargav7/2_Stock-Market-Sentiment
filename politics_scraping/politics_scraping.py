import requests
import json
import re
from datetime import datetime
from html import unescape
import psycopg2
import logging
from faktory import Worker
from datetime import datetime, timedelta
import logging
import faktory
from datetime import datetime, timedelta
from faktory import Worker

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')


def politics(subreddit_name):
    db_params = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': 5432
    }
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    print(f"Fetching data from 'hot' posts in r/{subreddit_name}...")
    headers = {'User-Agent': 'socialmedia_project'}
    response = requests.get(f"https://www.reddit.com/r/{subreddit_name}/hot.json", headers=headers)
    posts = json.loads(response.text)['data']['children']

    for post_data in posts:
        # uuid added to it
        post = post_data['data']
        #gen
        cursor.execute(
            "INSERT INTO Reddit_Posts_Politics (post_id, subreddit , created_utc) VALUES (%s, %s, %s) RETURNING id",
            (post['id'],subreddit_name, datetime.utcfromtimestamp(post['created_utc']))
        )

        post_uuid = cursor.fetchone()[0]
        
        response = requests.get(f"https://www.reddit.com{post['permalink']}.json", headers=headers)
        comments_data = json.loads(response.text)[1]['data']['children']
        for comment_data in comments_data:
            comment = comment_data['data']
            cursor.execute(
                "INSERT INTO Reddit_Comments_Politics (comment_id, subreddit, created_utc) VALUES (%s, %s, %s)",
                (comment['id'], subreddit_name, datetime.utcfromtimestamp(comment.get('created_utc', 0)))
            )

    conn.commit()
    cursor.close()
    conn.close()

def crawl_politics():
    with faktory.connection("tcp://:some_password@localhost:7419") as client:
        # Schedule the politics job to run 1 hour from now
        run_at_politics = datetime.utcnow() + timedelta(minutes=1)
        run_at_politics = run_at_politics.isoformat()[:-7] + "Z"
        logging.info(f'Scheduling wallstreet job to run at: {run_at_politics}')
        client.queue("politics", args=('politics',), queue="politics", at=run_at_politics)

       
        run_at = datetime.utcnow() + timedelta(hours=10)
        run_at = run_at.isoformat()[:-7] + "Z"
        logging.info(f'scheduling a new reddit crawl to run at: {run_at}')        
        client.queue("crawl_politics", queue="crawl_politics", at=run_at)

if __name__ == "__main__":
    w = Worker(faktory="tcp://:some_password@localhost:7419", queues=["politics","crawl_politics"], use_threads=True)
    w.register("crawl_politics", crawl_politics)
    w.register("politics", politics)
    w.run()
