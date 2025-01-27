from functions import RSSParser
import pandas as pd
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import json
import xml.etree.ElementTree as ET

# RSS feed URLs
world_news = [
    ("https://feeds.skynews.com/feeds/rss/home.xml", "Home"),
    ("https://feeds.skynews.com/feeds/rss/uk.xml", "UK"),
    ("https://feeds.skynews.com/feeds/rss/world.xml", "World"),
    ("https://feeds.skynews.com/feeds/rss/us.xml", "US"),
    ("https://feeds.skynews.com/feeds/rss/business.xml", "Business"),
    ("https://feeds.skynews.com/feeds/rss/politics.xml", "Politics"),
    ("https://feeds.skynews.com/feeds/rss/technology.xml", "Technology"),
    ("https://feeds.skynews.com/feeds/rss/entertainment.xml", "Entertainment"),
    ("https://feeds.skynews.com/feeds/rss/strange.xml", "Strange"),
]

# Initialize an empty list to collect all the articles
all_articles = []

def main():
    try:
        # Loop over each RSS feed URL and parse the data
        for url, category in world_news:
            print(f"Fetching data for category: {category}")
            parser = RSSParser(url, category)
            parser.fetch_rss_data()
            parser.parse_rss_data()
            all_articles.extend(parser.get_articles())
        # Create a DataFrame from the collected articles
        df_filtered = pd.DataFrame(all_articles)
    
        # Define date
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        # Filter articles published yesterday
        df_filtered = filtered_articles.filter_by_date()
        
        # Save the filtered DataFrame as a JSON file to be pushed to GitHub
        file_path = f'processed_files/sky_articles_{yesterday}.json'
        result_dict = parser.convert_to_json(df_filtered, file_path)
        
        return result_dict  # Return the dictionary

    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Return None if an error occurs

if __name__ == '__main__':
    main()
