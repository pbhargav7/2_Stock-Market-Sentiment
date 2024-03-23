import requests
from bs4 import BeautifulSoup
from datetime import datetime
import psycopg2
from faktory import Worker
import requests
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

def fetch_trending_data():
    db_params = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': 5432
    }

    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    current_date = datetime.now().strftime('%Y-%m-%d')

    url_trending = "https://finance.yahoo.com/trending-tickers"
    response = requests.get(url_trending)
    soup = BeautifulSoup(response.text, 'html.parser')
    ticker_elements = soup.find_all('tr', {'class': 'simpTblRow'})
    print("Scraping data from Yahoo Finance...")
    # Loop through each trending ticker to fetch its Analyst Rating and related news
    for element in ticker_elements:
        ticker = element.find('td', {'aria-label': 'Symbol'}).text
        company_name = element.find('td', {'aria-label': 'Name'}).text

        url_analyst = f"https://finance.yahoo.com/quote/{ticker}/analysis?p={ticker}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
        response = requests.get(url_analyst, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            table = soup.find('table', {'class': 'W(100%) M(0) BdB Bdc($seperatorColor) Mb(25px)'})
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if cells and cells[0].text.strip() == 'Avg. Estimate':
                    analyst_rating = cells[1].text.strip()
        except AttributeError:
            analyst_rating = None


        url_news = f"https://finance.yahoo.com/quote/{ticker}/news?p={ticker}"
        response = requests.get(url_news, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            related_news = soup.find('h3', {'class': 'Mb(5px)'}).text
        except AttributeError:
            related_news = 'N/A'

        cursor.execute(
            "INSERT INTO trendingstocks (Date, ticker, company_name, analyst_rating) VALUES (%s, %s, %s, %s) RETURNING id",
            (current_date, ticker, company_name, analyst_rating)
        )
        trending_stock_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO yahoonews (trending_stock_id, headline, publish_date) VALUES (%s, %s, %s)",
            (trending_stock_id, related_news, current_date)
        )

    conn.commit()

    cursor.close()
    conn.close()

    print("Scraping completed and data saved to PostgreSQL database.")

def crawl_yahoo():
    with faktory.connection("tcp://:some_password@localhost:7419") as client:
        run_at = datetime.utcnow() + timedelta(minutes=15)
        run_at = run_at.isoformat()[:-7] + "Z"
        logging.info(f'Scheduling yahoo job to run at: {run_at}')
        client.queue("fetch_trending_data", queue="yahoos", at=run_at)


        run_at_time = datetime.utcnow() + timedelta(hours=5)
        run_at_time = run_at_time.isoformat()[:-7] + "Z"
        logging.info(f'scheduling a new yahoo crawl to run at: {run_at_time}')

        client.queue("crawl_yahoo", queue="crawl_yahoos", at=run_at_time)

if __name__ == "__main__":
    w = Worker(faktory="tcp://:some_password@localhost:7419", queues=["yahoos","crawl_yahoos"], use_threads=True)
    w.register("crawl_yahoo", crawl_yahoo)
    w.register("fetch_trending_data", fetch_trending_data)
    w.run()