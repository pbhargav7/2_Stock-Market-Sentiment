import requests
import psycopg2
import logging
from faktory import Worker
from datetime import datetime, timedelta
import faktory


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

def hs_check_comment(comment):
    CONF_THRESHOLD = 0.5
    data = {
        "token": "f0230e932ffc4e09fe3aa276d0ef7494",
        "text": comment
    }
    response = requests.post("https://api.moderatehatespeech.com/api/v1/moderate/", json=data).json()

        # Handle unexpected response types
    if not isinstance(response, dict):
        print(f"WARNING: Unexpected response type: {type(response)}")
        return False

    # Proceed with checks if response is a dictionary
    try:
        # Use get() to safely access the "class" key
        if response.get("class") is None:
            # Handle missing "class" key
            print(f"WARNING: 'class' key missing in response. Assuming non-toxic.")
            return False

        # Check if "class" is "flag" and confidence exceeds threshold
        if response["class"] == "flag" and float(response["confidence"]) > CONF_THRESHOLD:
            return True

        # If not "flag" or confidence below threshold, assume non-toxic
        return False

    except (KeyError, TypeError):
        # Handle any errors accessing keys or casting confidence
        print(f"WARNING: Error accessing response data. Assuming non-toxic.")
        return False


def insert_into_hate_speech(comment_id, post_id, subreddit, text_type, text_body, text_score, created_utc, is_hate_speech):
    db_params = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': 5432
    }
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO hate_speech (post_id, comment_id, subreddit, Type, text_body, text_score, created_utc, is_hate_speech)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, (post_id, comment_id, subreddit, text_type, text_body, text_score, created_utc, is_hate_speech))

    conn.commit()
    cur.close()
    conn.close()

def measure_toxicity():
    db_params = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': 5432
    }
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute("""
    SELECT id, post_id, subreddit, comment_body, comment_score, created_utc
    FROM RedditComments
    WHERE TRIM(BOTH ' ' FROM comment_body) IS NOT NULL 
      AND TRIM(BOTH ' ' FROM comment_body) != ''
      AND id NOT IN (SELECT comment_id FROM hate_speech WHERE comment_id IS NOT NULL);
""")

    for row in cur.fetchall():
        id, post_id, subreddit, comment_body, comment_score, created_utc = row

        # Checking here for hate speech
        is_hate_speech = hs_check_comment(comment_body)

        insert_into_hate_speech(id, post_id, subreddit, 'comment', comment_body, comment_score, created_utc, is_hate_speech)

    cur.close()
    conn.close()

def schedule_measure_toxicity():
    with faktory.connection("tcp://:some_password@localhost:7419") as client:
        run_at_wallstreet = datetime.utcnow() + timedelta(seconds=5)
        run_at_wallstreet = run_at_wallstreet.isoformat()[:-7] + "Z"
        logging.info(f'Scheduling measure toxicity to run at: {run_at_wallstreet}')
        client.queue("measure_toxicity", queue="measure_toxicity", at=run_at_wallstreet)

        run_at = datetime.utcnow() + timedelta(hours=10)
        run_at = run_at.isoformat()[:-7] + "Z"
        logging.info(f'scheduling a new toxicity measurement to run at: {run_at}')
        client.queue("schedule_measure_toxicity", queue="schedule_measure_toxicity", at=run_at)

if __name__ == "__main__":
    w = Worker(faktory="tcp://:some_password@localhost:7419", queues=["measure_toxicity","schedule_measure_toxicity"], use_threads=True)
    w.register("schedule_measure_toxicity", schedule_measure_toxicity)
    w.register("measure_toxicity", measure_toxicity)
    w.run()
