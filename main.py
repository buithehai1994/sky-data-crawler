from functions.py import FilteredArticles

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

# Create the main class instance
filtered_articles = FilteredArticles(world_news)

def main():
    try:
        # Fetch RSS articles
        df_articles = filtered_articles.fetch_rss_articles()
        
        # Fetch webpage metadata
        df_metadata = filtered_articles.fetch_webpage_metadata()
        
        # Filter articles published today
        df_filtered = filtered_articles.filter_by_date()

        # Save the filtered DataFrame as a JSON file to be pushed to GitHub
        file_path = f'processed_files/sky_articles_{yesterday}.json'
        result_dict = filtered_articles.convert_to_json(df_filtered, file_path)
        
        return result_dict  # Return the dictionary

    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Return None if an error occurs
