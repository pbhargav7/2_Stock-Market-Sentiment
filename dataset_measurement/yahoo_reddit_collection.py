import psycopg2
import pandas as pd

db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost'
}

def fetch_reddit_data_for_stock(cursor, ticker, company_name, yahoo_date):
    query = """
    SELECT rp.post_title AS text, rp.created_utc AS date, 'post' AS type , rp.subreddit as subreddit
    FROM RedditPosts rp
    WHERE ((rp.post_title ~ ('\\m' || %s || '\\M') OR rp.post_title ~ ('\\m' || %s || '\\M'))
           AND DATE(rp.created_utc) BETWEEN %s::DATE - INTERVAL '2 days' AND %s::DATE)
    UNION
    SELECT rc.comment_body AS text, rc.created_utc AS date, 'comment' AS type , rc.subreddit as subreddit
    FROM RedditComments rc
    JOIN RedditPosts rp ON rc.post_id = rp.id
    WHERE ((rp.post_title ~ ('\\m' || %s || '\\M') OR rp.post_title ~ ('\\m' || %s || '\\M'))
           AND DATE(rc.created_utc) BETWEEN %s::DATE - INTERVAL '2 days' AND %s::DATE)
    UNION
    SELECT rc.comment_body AS text, rc.created_utc AS date, 'comment' AS type , rc.subreddit as subreddit
    FROM RedditComments rc
    WHERE rc.post_id IN (
        SELECT rp.id
        FROM RedditPosts rp
        WHERE (rp.post_title ~ ('\\m' || %s || '\\M') OR rp.post_title ~ ('\\m' || %s || '\\M'))
        UNION
        SELECT rc.post_id
        FROM RedditComments rc
        WHERE (rc.comment_body ~ ('\\m' || %s || '\\M') OR rc.comment_body ~ ('\\m' || %s || '\\M'))
    )
    AND DATE(rc.created_utc) BETWEEN %s::DATE - INTERVAL '2 days' AND %s::DATE
    """
    ticker_pattern = f"{ticker}" 
    company_name_pattern = f"{company_name}"
    cursor.execute(query, [ticker_pattern, company_name_pattern, yahoo_date, yahoo_date, ticker_pattern, company_name_pattern, yahoo_date, yahoo_date, ticker_pattern, company_name_pattern, ticker_pattern, company_name_pattern, yahoo_date, yahoo_date])
    return cursor.fetchall()

def insert_into_database(cur, ticker, company_name, yahoo_headline, yahoo_date, reddit_data):
    for text, date, post_type, subreddit in reddit_data:
        check_query = """
        SELECT COUNT(*) 
        FROM Yahoo_Reddit_Collection 
        WHERE Ticker = %s AND Company_Name = %s AND Yahoo_Headline = %s AND 
              Yahoo_Date = %s AND Type = %s AND Reddit_Text = %s AND Reddit_Date = %s AND subreddit = %s;
        """
        cur.execute(check_query, (ticker, company_name, yahoo_headline, yahoo_date, post_type, text ,date,subreddit))
        count = cur.fetchone()[0]

        if count == 0:
            insert_query = """
            INSERT INTO Yahoo_Reddit_Collection 
            (Ticker, Company_Name, Yahoo_Headline, Yahoo_Date, Type, Reddit_Text,subreddit, Reddit_Date) 
            VALUES (%s, %s, %s, %s, %s, %s, %s,%s);
            """
            cur.execute(insert_query, (ticker, company_name, yahoo_headline, yahoo_date, post_type, text,subreddit ,date))

try:
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            yahoo_sp500_query = """
            SELECT ts.ticker, ts.Company_Name, yn.headline, yn.publish_date
            FROM TrendingStocks ts
            JOIN YahooNews yn ON ts.id = yn.trending_stock_id
            JOIN SP500 s ON ts.ticker = s.ticker
            ORDER BY yn.publish_date;
            """
            yahoo_sp500_data = pd.read_sql_query(yahoo_sp500_query, conn)

            for index, row in yahoo_sp500_data.iterrows():
                ticker = row['ticker']
                company_name = row['company_name']
                yahoo_headline = row['headline']
                yahoo_date = row['publish_date']
                reddit_data = fetch_reddit_data_for_stock(cur, ticker, company_name, yahoo_date.strftime('%Y-%m-%d'))
                
                insert_into_database(cur, ticker, company_name, yahoo_headline, yahoo_date, reddit_data)

            conn.commit()
            print("Data insertion complete.")

except psycopg2.DatabaseError as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
