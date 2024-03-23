import requests
import json
import re
from datetime import datetime
from html import unescape
import psycopg2
import logging
from faktory import Worker
from datetime import datetime, timedelta
import faktory


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')


def reddit_toxic(subreddit_name):
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
            "INSERT INTO redditposts (subreddit, post_title, post_score, created_utc) VALUES (%s, %s, %s, %s) RETURNING id",
            (subreddit_name, post['title'], float(post['score']), datetime.utcfromtimestamp(post['created_utc']))
        )

        post_uuid = cursor.fetchone()[0]
        
        response = requests.get(f"https://www.reddit.com{post['permalink']}.json", headers=headers)
        comments_data = json.loads(response.text)[1]['data']['children']
        for comment_data in comments_data:
            comment = comment_data['data']
            text = re.sub(r'http\S+', '', comment.get('body', ''))
            text = re.sub(r'\[.*?\]\(.*?\)', '', text)
            text = unescape(text)
            text = ' '.join(text.split())
            text = re.sub(r'[^\w\s,]', '', text)
            cursor.execute(
                "INSERT INTO redditcomments (post_id, subreddit, comment_body, comment_score, created_utc) VALUES (%s, %s, %s, %s, %s)",
                (post_uuid, subreddit_name, text, float(comment.get('score', 0)), datetime.utcfromtimestamp(comment.get('created_utc', 0)))
            )

    conn.commit()
    cursor.close()
    conn.close()

def crawl_reddit_toxic():
    with faktory.connection("tcp://:some_password@localhost:7419") as client:
        run_at_wallstreet = datetime.utcnow() + timedelta(minutes=30)
        run_at_wallstreet = run_at_wallstreet.isoformat()[:-7] + "Z"
        logging.info(f'Scheduling wallstreet job to run at: {run_at_wallstreet}')
        client.queue("reddit_toxic", args=('wallstreetbets',), queue="reddit_toxics", at=run_at_wallstreet)


        run_at = datetime.utcnow() + timedelta(hours=10)
        run_at = run_at.isoformat()[:-7] + "Z"
        logging.info(f'scheduling a new reddit crawl to run at: {run_at}')
        client.queue("crawl_reddit_toxic", queue="crawl_reddit_toxics", at=run_at)


if __name__ == "__main__":
    w = Worker(faktory="tcp://:some_password@localhost:7419", queues=["reddit_toxics","crawl_reddit_toxics"], use_threads=True)
    w.register("crawl_reddit_toxic", crawl_reddit_toxic)
    w.register("reddit_toxic", reddit_toxic)
    w.run()
