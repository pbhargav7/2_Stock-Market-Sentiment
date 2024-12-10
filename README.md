

<!-- 
# Project Title

## Table of Contents
1. [Introduction](#introduction)
2. [File Descriptions](#file-descriptions)
3. [Installation](#installation)
4. [Usage](#usage)

## Introduction
Brief description of the project.

## File Descriptions
- `file1.ext`: Brief description of what `file1.ext` does.
- `file2.ext`: Brief description of what `file2.ext` does.
- `file3.ext`: Brief description of what `file3.ext` does.
- `directory/`: Brief description of what files in `directory/` do.

## Installation
Instructions for how to install and setup your project.

## Usage
Instructions for how to use your project after it's installed. -->

# Project: Data Visualization 📊

## 🌟 Overview
This project is an extension of Project 2, incorporating a data visualization component into a Flask web application 🌐. The primary focus is on stock market data 📈 and Reddit and Yahoo post analysis, interfacing with a PostgreSQL database and displaying data through various visualizations.

## 📁 Project Components

### 📂 Folders and Files:

- `🖌️ Data Visualization/`
  - `📄 templates/`: Contains HTML templates for the web interface.
    - `🏠 index.html`: Main page of the web application, offering options to view different data visualizations.
    - `📊 stock_details.html`: Displays detailed visualizations and data about selected stocks.
    - `💬 reddit_data.html`: Shows visualizations related to Reddit data analysis.
    - `📝 ticker_sync_data.html`: Presents information and analytics for various stock tickers.
  - `🚀 app.py`: The Flask application file that routes and renders pages with appropriate data and visualizations.

### 🐍 Python Scripts:

- `🔗 db_connection.py`: Defines functions to establish and close connections to the PostgreSQL database.
- `⚙️ connection_config.py`: Configures Faktory worker for job processing and handling.

### 🗃️ SQL Files:

- `ddl.sql`: Contains Data Definition Language (DDL) statements for creating the necessary tables in the PostgreSQL database.

### 📊 Data Folders:

- `🔍 dataset_analysis/`: Files responsible for data sentiment analysis.
- `🧹 dataset_measurement/`: Files for data integration and cleaning.
- `🔬 measuring_toxicity/`: Files for measuring toxicity using ModerateHateSpeech API.
- `🎨 plotting/`: Basic scripts used for plotting graphs.
- `🗞️ politics_scraping/`: Scripts for scraping data from the r/politics subreddit.
- `👥 reddit_scraping/`: Scripts for scraping Reddit data.
- `☣️ toxicity_scraping/`: Responsible for scraping data from r/wallstreetbets for toxicity analysis.
- `📰 yahoo_scraping/`: Scripts for scraping Yahoo news related to trending stocks.


## 🚀 Usage

### 🖱️ Run Flask Application
1. **Navigate** to the `Data Visualization` folder within your project directory.
2. **Start** the Flask application by executing `app.py`. Use the command `python app.py` in your terminal.

### 🌐 Accessing the Web Application
1. **🌍 Open** a web browser and navigate to the URL indicated in the terminal (usually `http://localhost:5001/`).
2. The `index.html` serves as the **landing page**, offering various data visualization options.

### 💻 Interacting with the Application

1. **📈 Stock Details:** Choose a company and optionally a subreddit for stock analysis from dropdown menus.
2. **💬 Reddit Details:** Select a subreddit to gain insights from Reddit community data.
3. **📊 Processed Data Overview:** View key metrics like total posts, comments, stocks fetched, and hate speech processed.
4. **🎨 Visualization:** Submit selections to generate detailed visualizations for stocks and Reddit data.
5. **🔭 Explore Features:** Use 'View Reddit Data' and 'Get All Stocks' for extended analysis.

## 🛠️ Dependencies:

Ensure the following dependencies are installed:

- `Python 3` (Core programming language used for the project)
- `flask` (Web framework for building the web app)
- `matplotlib` (library used for creating visualizations)
- `psycopg2` (for PostgreSQL connection)
- `faktory` (for job queue management)
- `requests` (for making HTTP requests)
- `BeautifulSoup` (for web scraping)

## 📝 Notes:

- Ensure all dependencies are installed and the PostgreSQL server is running before starting the Flask application.
- For detailed information on each script and its functionality, refer to the script files.

