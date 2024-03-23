CREATE TABLE SP500 (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    ticker VARCHAR(10) NOT NULL
);


CREATE TABLE RedditPosts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subreddit VARCHAR(255),
    post_title TEXT NOT NULL,
    post_score FLOAT,
    created_utc TIMESTAMP
);

CREATE TABLE RedditComments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID REFERENCES RedditPosts(id),
    subreddit VARCHAR(255),
    comment_body TEXT NOT NULL,
    comment_score FLOAT,
    created_utc TIMESTAMP
);

CREATE TABLE TrendingStocks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    Date TIMESTAMP,
    ticker VARCHAR(50) NOT NULL,
    Company_Name VARCHAR(255),
    Analyst_Rating VARCHAR(50)
);

CREATE TABLE YahooNews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trending_stock_id UUID REFERENCES TrendingStocks(id) NULL,
    publish_date TIMESTAMP
);

CREATE TABLE Yahoo_Reddit_Collection (
    ID UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    Ticker VARCHAR(255),
    Company_Name VARCHAR(255),
    Yahoo_Headline TEXT,
    Yahoo_sentiment TEXT, 
    Yahoo_Date TIMESTAMP,
    Type VARCHAR(50),
    Reddit_Text TEXT,
    subreddit VARCHAR(255),
    Reddit_sentiment TEXT,
    Reddit_Date TIMESTAMP,
    Insertion_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Ticker_Sync_Data (
    ID UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    Ticker VARCHAR(255),
    Company_Name VARCHAR(255),
    Number_of_InSync INT,
    Number_of_OutSync INT,
    dependency INT,
    reliability FLOAT,
    Insertion_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE hate_speech (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID,
    comment_id UUID,
    subreddit VARCHAR(255),
    Type VARCHAR(50), 
    text_body TEXT,
    text_score FLOAT,
    created_utc TIMESTAMP,
    is_hate_speech BOOLEAN
);

CREATE TABLE Reddit_Posts_Politics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id VARCHAR(255),
    subreddit VARCHAR(255),
    created_utc TIMESTAMP
);

CREATE TABLE Reddit_Comments_Politics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    comment_id VARCHAR(255),
    subreddit VARCHAR(255),
    created_utc TIMESTAMP
);