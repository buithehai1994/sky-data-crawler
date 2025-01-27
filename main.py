from functions.py import FilteredArticles

# RSS feed URLs
world_news = [
    'https://feeds.bbci.co.uk/news/business/rss.xml?edition=uk',
    'https://feeds.bbci.co.uk/news/education/rss.xml?edition=uk',
    'https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml?edition=uk',
    'https://feeds.bbci.co.uk/news/health/rss.xml?edition=uk',
    'https://feeds.bbci.co.uk/news/technology/rss.xml?edition=uk',
    'https://feeds.bbci.co.uk/news/world/rss.xml?edition=uk',
    'https://feeds.bbci.co.uk/news/science_and_environment/rss.xml?edition=uk'
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
