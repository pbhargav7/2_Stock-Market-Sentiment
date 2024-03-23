import psycopg2

db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost'
}

def calculate_and_insert_sync_data():
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                # Query to calculate insync and outsync for each ticker
                query_to_truncate = """
                Truncate table Ticker_Sync_Data
                """
                cur.execute(query_to_truncate)

                query_sync_data = """
                SELECT Ticker, Company_Name,
                       SUM(CASE WHEN Reddit_sentiment = Yahoo_sentiment THEN 1 ELSE 0 END) AS Number_of_InSync,
                       SUM(CASE WHEN Reddit_sentiment <> Yahoo_sentiment THEN 1 ELSE 0 END) AS Number_of_OutSync
                FROM Yahoo_Reddit_Collection
                GROUP BY Ticker, Company_Name
                """
                cur.execute(query_sync_data)
                sync_data = cur.fetchall()

                # Insert the calculated data into Ticker_Sync_Data
                for row in sync_data:
                    ticker, company_name, insync, outsync = row
                    dependency = (insync / (insync + outsync)) * 100
                    insert_query = """
                    INSERT INTO Ticker_Sync_Data (Ticker, Company_Name, Number_of_InSync, Number_of_OutSync, Dependency)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING ID
                    """
                    cur.execute(insert_query, (ticker, company_name, insync, outsync, dependency))
                    sync_data_id = cur.fetchone()[0]

                conn.commit()

                update_reliability_query = """
                WITH RankedData AS (
                    SELECT ID, PERCENT_RANK() OVER (ORDER BY (Number_of_InSync + Number_of_OutSync)) AS rank
                    FROM Ticker_Sync_Data
                )
                UPDATE Ticker_Sync_Data
                SET Reliability = 100 * (SELECT rank FROM RankedData WHERE ID = Ticker_Sync_Data.ID)
                """
                cur.execute(update_reliability_query)

                conn.commit()

    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

calculate_and_insert_sync_data()
