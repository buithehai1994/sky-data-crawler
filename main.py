from functions import RSSParser
import pandas as pd
from datetime import datetime, timedelta
import os

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

        if df_filtered.empty:
            print("No articles were fetched.")
            return None

        # Filter articles published yesterday
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        # Replace invalid dates and filter
        df_filtered['Date Published'] = pd.to_datetime(
            df_filtered['Date Published'], errors='coerce'
        )
        df_filtered = df_filtered[df_filtered['Date Published'].dt.date == yesterday]

        if df_filtered.empty:
            print("No articles were published yesterday.")
            return None

        # Ensure output directory exists
        output_dir = 'processed_files'
        
        # Save the filtered DataFrame as a JSON file
        file_path = f'{output_dir}/sky_articles_{yesterday}.json'
        RSSParser.convert_to_json(df_filtered, file_path)

        print(f"Articles saved to {file_path}")
        return df_filtered  # Return the DataFrame for further use if needed

    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Return None if an error occurs

if __name__ == '__main__':
    main()
