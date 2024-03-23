select count(*) from redditcomments;

select count(*) from redditposts;

select count(*) from redditposts where subreddit='wallstreet';

select count(*) from redditposts where subreddit='stocks';

select count(*) from redditposts where subreddit='Trading';

select count(*) from redditposts where subreddit='StockMarket';

select count(*) from redditposts where subreddit='finance';

select * from redditposts where subreddit='politics';

SELECT count(*) from yahoonews;

SELECT count(*) from trendingstocks;

select count(*) from redditposts where subreddit='wallstreetbets';

select count(*) from redditposts where subreddit='politics';

select * from redditcomments where subreddit='wallstreetbets' where comment_body not empty;

select count(*) from redditcomments where subreddit='politics';

select count(*) from redditcomments;

select * from redditposts where subreddit='wallstreetbets';

select * from redditcomments where subreddit='wallstreetbets';

SELECT DISTINCT DATE_TRUNC('day', created_utc)
FROM redditposts where subreddit='wallstreet' and DATE_TRUNC('day', created_utc)>='2023-11-01'::date;

SELECT count(DISTINCT DATE_TRUNC('day', created_utc))
FROM redditposts where subreddit='wallstreet' and DATE_TRUNC('day', created_utc)>='2023-11-01'::date;

SELECT DISTINCT DATE_TRUNC('day', created_utc)
FROM redditcomments where subreddit='wallstreet' and DATE_TRUNC('day', created_utc)>='2023-11-01'::date;

SELECT count(DISTINCT DATE_TRUNC('day', created_utc))
FROM redditcomments where subreddit='wallstreet' and DATE_TRUNC('day', created_utc)>='2023-11-01'::date;


SELECT count(DISTINCT DATE_TRUNC('day', created_utc))
FROM redditcomments where subreddit='politics';

SELECT count(DISTINCT DATE_TRUNC('day', created_utc))
FROM redditposts where subreddit='politics';

SELECT * from yahoo_reddit_collection LIMIT 10;

select * FROM ticker_sync_data;

SELECT count(DISTINCT TO_CHAR(DATE_TRUNC('day', created_utc), 'YYYY-MM-DD')) AS truncated_date
FROM redditposts
WHERE subreddit='politics' AND DATE_TRUNC('day', created_utc) >= '2023-11-01'::date;


select count(*) from hate_speech;

select count(*) from redditcomments where subreddit='wallstreetbets';

select count(*) from Reddit_Comments_Politics;

select count(*) from Reddit_Posts_Politics;

SELECT count(DISTINCT TO_CHAR(DATE_TRUNC('day', created_utc), 'YYYY-MM-DD')) AS truncated_date
FROM redditposts
WHERE subreddit='wallstreet' AND DATE_TRUNC('day', created_utc) >= '2023-11-01'::date;

SELECT count(DISTINCT TO_CHAR(DATE_TRUNC('day', created_utc), 'YYYY-MM-DD')) AS truncated_date
FROM Reddit_Posts_Politics
WHERE DATE_TRUNC('day', created_utc) >= '2023-11-01'::date;

SELECT count(DISTINCT TO_CHAR(DATE_TRUNC('day', created_utc), 'YYYY-MM-DD')) AS truncated_date
FROM Reddit_Comments_Politics
WHERE DATE_TRUNC('day', created_utc) >= '2023-11-01'::date;

select count(*) from hate_speech where is_hate_speech = 'TRUE';
select count(*) from hate_speech where is_hate_speech = 'FALSE';select coint* from hate_speech;


select count(*) from hate_speech;

select * from hate_speech;


SELECT * FROM hate_speech;

select count(*) from redditcomments where subreddit='wallstreetbets';

select count(*) from Reddit_Comments_Politics;


select count(*)
from Reddit_Posts_Politics;


select ticker, dependency, reliability from ticker_sync_data;


SELECT * FROM Reddit_Posts_Politics;

select * from yahoo_reddit_collection ORDER BY Insertion_Date DESC;

select * from ticker_sync_data;

select * from hate_speech;
