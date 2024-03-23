from flask import Flask, render_template, request, jsonify
import psycopg2
import io
import base64
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import random

app = Flask(__name__)

db_params = {
    'dbname': 'postgres',
    'user': 'postgres',   
    'password': 'postgres',
    'host': 'localhost'
}

def fetch_data(query, params=None):
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as curs:
            curs.execute(query, params)
            columns = [desc[0] for desc in curs.description]
            data = curs.fetchall()
            return [dict(zip(columns, row)) for row in data]

def reddit_data_plot_urls(fetch_data, selected_subreddit):
    start_date = datetime.date(2023, 11, 1)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = datetime.datetime.now().strftime('%Y-%m-%d')

    # Adjust the posts and comments queries to filter by the selected subreddit
    posts_query = f"""
    SELECT DATE(created_utc) AS date, COUNT(*) AS count
    FROM RedditPosts
    WHERE subreddit = '{selected_subreddit}' 
    AND DATE(created_utc) >= '{start_date_str}' AND DATE(created_utc) <= '{end_date_str}'
    GROUP BY DATE(created_utc)
    ORDER BY DATE(created_utc);
    """
    posts_data = fetch_data(posts_query)

    comments_query = f"""
    SELECT DATE(created_utc) AS date, COUNT(*) AS count
    FROM RedditComments
    WHERE subreddit = '{selected_subreddit}' 
    AND DATE(created_utc) >= '{start_date_str}' AND DATE(created_utc) <= '{end_date_str}'
    GROUP BY DATE(created_utc)
    ORDER BY DATE(created_utc);
    """
    comments_data = fetch_data(comments_query)

    # Query for hate speech data
    hate_speech_query_true = f"""
    SELECT DATE(created_utc) AS date, COUNT(*) AS count
    FROM hate_speech
    WHERE subreddit = '{selected_subreddit}' 
    AND is_hate_speech = TRUE
    AND DATE(created_utc) >= '{start_date_str}' AND DATE(created_utc) <= '{end_date_str}'
    GROUP BY DATE(created_utc)
    ORDER BY DATE(created_utc);
    """
    hate_speech_data_true = fetch_data(hate_speech_query_true)

    
    hate_speech_query_false = f"""
    SELECT DATE(created_utc) AS date, COUNT(*) AS count
    FROM hate_speech
    WHERE subreddit = '{selected_subreddit}' 
    AND is_hate_speech = FALSE
    AND DATE(created_utc) >= '{start_date_str}' AND DATE(created_utc) <= '{end_date_str}'
    GROUP BY DATE(created_utc)
    ORDER BY DATE(created_utc);
    """
    hate_speech_data_false = fetch_data(hate_speech_query_false)

    def plot_hate_speech_data(data_true, data_false, title):
        if not data_true and not data_false:
            return "no_data"

        plt.figure(figsize=(12, 6))
        if data_true:
            dates_true = [item['date'] for item in data_true]
            counts_true = [item['count'] for item in data_true]
            plt.plot(dates_true, counts_true, marker='o', linestyle='-', color='red', label='Hate Speech (True)')

        if data_false:
            dates_false = [item['date'] for item in data_false]
            counts_false = [item['count'] for item in data_false]
            plt.plot(dates_false, counts_false, marker='o', linestyle='-', color='green', label='Non-Hate Speech (False)')

        plt.xlabel('Date')
        plt.ylabel('Count')
        plt.title(title)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.xticks(rotation=90)
        plt.legend()
        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches="tight")
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        plt.close()

        return plot_url

    posts_plot_urls = {}
    comments_plot_urls = {}
    hate_speech_plot_url = {}

    def plot_data(data, title):
        if not data:
            return "no_data"
        color = (random.random(), random.random(), random.random())

        dates = [item['date'] for item in data]
        counts = [item['count'] for item in data]

        plt.figure(figsize=(12, 6))
        plt.plot(dates, counts, marker='o', linestyle='-', color=color)
        plt.xlabel('Date')
        plt.ylabel('Count')
        plt.title(title)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1)) # date interval
        plt.xticks(rotation=80)
        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches="tight")
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        plt.close()

        return plot_url

    subreddit_posts = [item for item in posts_data]
    subreddit_comments = [item for item in comments_data]

    posts_plot_urls[selected_subreddit] = plot_data(subreddit_posts, f'Posts: {selected_subreddit}')
    comments_plot_urls[selected_subreddit] = plot_data(subreddit_comments, f'Comments: {selected_subreddit}')
    hate_speech_plot_url[selected_subreddit] = plot_hate_speech_data(hate_speech_data_true, hate_speech_data_false, f'Hate Speech: {selected_subreddit}')


    return posts_plot_urls, comments_plot_urls, hate_speech_plot_url

def plot_stock_graph(company_name):
    query = """
    SELECT DATE(Reddit_Date) AS date, COUNT(Reddit_Text) AS count
    FROM Yahoo_Reddit_Collection
    WHERE company_name = %s
    GROUP BY DATE(Reddit_Date)
    ORDER BY DATE(Reddit_Date);
    """
    params = (company_name,)
    data = fetch_data(query, params)
    dates = [item['date'] for item in data]
    counts = [item['count'] for item in data]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, counts, marker='o')
    plt.xlabel('Date')
    plt.ylabel('Count of interaction')
    plt.title('Count of Entries Per Date')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.xticks(rotation=90)
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches="tight")
    img.seek(0)
    plot_stock_graph = base64.b64encode(img.getvalue()).decode('utf8')

    return plot_stock_graph

def plot_subreddit_graph(company_name, subreddit):
    query = """
    SELECT DATE(Reddit_Date) AS date, COUNT(Reddit_Text) AS count
    FROM Yahoo_Reddit_Collection
    WHERE company_name = %s AND subreddit = %s
    GROUP BY DATE(Reddit_Date)
    ORDER BY DATE(Reddit_Date);
    """
    params = (company_name, subreddit)
    data = fetch_data(query, params)
    if not data:
        return "no_data"
    
    dates = [item['date'] for item in data]
    counts = [item['count'] for item in data]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, counts, marker='o')
    plt.xlabel('Date')
    plt.ylabel('Count of interaction')
    plt.title('Count of Entries Per Date')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.xticks(rotation=90)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches="tight")
    img.seek(0)
    plot_subreddit_graph = base64.b64encode(img.getvalue()).decode('utf8')

    return plot_subreddit_graph

def get_trending_dates(company_name):
    query = """
    SELECT DISTINCT DATE(Date) AS trending_date
    FROM TrendingStocks
    WHERE Company_Name = %s
    ORDER BY DATE(Date);
    """
    params = (company_name,)
    return fetch_data(query, params)

def get_table_counts():
    reddit_posts_count = """
    SELECT 'RedditPosts' AS table_name, COUNT(*) AS count FROM RedditPosts"""
    reddit_comments_count = """
    SELECT 'RedditComments', COUNT(*) FROM RedditComments"""
    trending_stocks_count = """
    SELECT 'TrendingStocks', COUNT(*) FROM TrendingStocks"""
    yahoo_news_count = """
    SELECT 'YahooNews', COUNT(*) FROM YahooNews"""
    yahoo_reddit_collection_count = """
    SELECT 'Yahoo_Reddit_Collection', COUNT(*) FROM Yahoo_Reddit_Collection"""
    ticker_sync_count = """
    SELECT 'Ticker_Sync_Data', COUNT(*) FROM Ticker_Sync_Data"""
    hate_speech_count = """
    SELECT 'Ticker_Sync_Data', COUNT(*) FROM hate_speech"""
    
    reddit_posts_count = fetch_data(reddit_posts_count)
    reddit_comments_count = fetch_data(reddit_comments_count)
    trending_stocks_count = fetch_data(trending_stocks_count)
    yahoo_news_count = fetch_data(yahoo_news_count)
    yahoo_reddit_collection_count = fetch_data(yahoo_reddit_collection_count)
    ticker_sync_count = fetch_data(ticker_sync_count)
    hate_speech_count = fetch_data(hate_speech_count)
    dir = {}
    dir['Total Posts Fetched'] = reddit_posts_count[0]['count']
    dir['Total Comments Fetched'] = reddit_comments_count[0]['count']
    dir['Total Stocks Fetched'] = trending_stocks_count[0]['count']
    dir['Total Connections Found'] = yahoo_reddit_collection_count[0]['count']
    dir['Total Stocks Analysed'] = ticker_sync_count[0]['count']
    dir['Total Processed Hate Speech'] = hate_speech_count[0]['count']
    return dir

@app.route('/')
def index():
    company_query = "SELECT DISTINCT company_name FROM Ticker_Sync_Data;"
    companies_data = fetch_data(company_query)
    companies = [company['company_name'] for company in companies_data]

    subreddit_query = "SELECT DISTINCT subreddit FROM Yahoo_Reddit_Collection;"
    subreddit_data = fetch_data(subreddit_query)
    subreddits = [subreddit['subreddit'] for subreddit in subreddit_data]

    # Get table counts
    table_counts = get_table_counts()

    return render_template('index.html', companies=companies, subreddits=subreddits, table_counts=table_counts)

@app.route('/view-ticker-sync-data')
def view_ticker_sync_data():
    query = "SELECT * FROM Ticker_Sync_Data;"
    ticker_sync_data = fetch_data(query)
    return render_template('ticker_sync_data.html', ticker_sync_data=ticker_sync_data)

@app.route('/view-reddit-data')
def view_reddit_data():
    selected_subreddit = request.args.get('subreddit')
    posts_plot_url, comments_plot_url, hate_speech_plot_url = reddit_data_plot_urls(fetch_data, selected_subreddit)
    return render_template('reddit_data.html', 
                           subreddit = selected_subreddit,
                           posts_plot_url=posts_plot_url, 
                           comments_plot_url=comments_plot_url,
                           hate_speech_plot_url=hate_speech_plot_url)

@app.route('/stock-details', methods=['POST'])
def stock_details():
    company_name = request.form.get('company')
    subreddit_name = request.form.get('subreddit') or None

    query = "SELECT * FROM Ticker_Sync_Data WHERE company_name = %s;"
    params = (company_name,)
    stock_data = fetch_data(query, params)

    stock_plot_url = plot_stock_graph(company_name)

    subreddit_plot_url = None
    if subreddit_name:
        subreddit_plot_url = plot_subreddit_graph(company_name, subreddit_name)

    trending_dates = get_trending_dates(company_name)

    if stock_data:
        stock = stock_data[0]
        stock['reliability'] = "{:.2f}".format(stock['reliability'])
        return render_template('stock_details.html', stock=stock, stock_plot_url=stock_plot_url, subreddit_plot_url=subreddit_plot_url, trending_dates=trending_dates)
    else:
        return render_template('stock_details.html', error_message='Stock not found', stock_plot_url=stock_plot_url, subreddit_plot_url=subreddit_plot_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001,debug=True)