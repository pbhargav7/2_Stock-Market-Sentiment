import psycopg2
from textblob import TextBlob

db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost'
}

def get_sentiment_label(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return 'positive'
    elif polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def update_sentiments_in_db():
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            fetch_query = "SELECT id, reddit_text, yahoo_headline FROM Yahoo_Reddit_Collection"
            cur.execute(fetch_query)
            rows = cur.fetchall()

            # Performing sentiment analysis on the data and updating the database
            for row in rows:
                id, reddit_text, yahoo_headline = row

                reddit_sentiment = get_sentiment_label(reddit_text)
                yahoo_sentiment = get_sentiment_label(yahoo_headline)

                update_query = """
                UPDATE Yahoo_Reddit_Collection
                SET reddit_sentiment = %s, yahoo_sentiment = %s
                WHERE id = %s;
                """
                cur.execute(update_query, (reddit_sentiment, yahoo_sentiment, id))

            conn.commit()

update_sentiments_in_db()