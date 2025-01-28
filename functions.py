import requests
from bs4 import BeautifulSoup
import json
import xml.etree.ElementTree as ET

class RSSParser:
    def __init__(self, rss_url, category):
        self.rss_url = rss_url
        self.category = category
        self.rss_data = None
        self.items = []

    def fetch_rss_data(self):
        # Fetch the RSS feed from the provided URL
        response = requests.get(self.rss_url)
        if response.status_code == 200:
            self.rss_data = response.text
        else:
            print(f"Failed to fetch RSS feed from {self.rss_url}. Status code: {response.status_code}")

    def parse_rss_data(self):
        if self.rss_data:
            # Parse the XML from the fetched RSS data
            root = ET.fromstring(self.rss_data)

            # Find all the 'item' elements in the RSS feed
            for item in root.findall(".//item"):
                title = item.find("title").text
                link = item.find("link").text
                description = item.find("description").text
                # pub_date = item.find("pubDate").text
                enclosure_url = item.find(".//enclosure").get("url") if item.find(".//enclosure") is not None else None

                # If no image URL is found, set a placeholder
                image_url = enclosure_url if enclosure_url else "https://via.placeholder.com/150"

                # Extract additional details from the article
                content, authors, date_published, article_title, subtitle = self.extract_article_details(link)

                # Append to the items list as separate columns
                self.items.append({
                    "title": article_title,
                    "description": description,
                    "url": link,
                    "image_url": image_url,
                    "type": self.category,  # Add the category
                    "Author": authors,
                    "Date Published": date_published,
                    "Headline": subtitle,
                    "Content": content,

                })

    def extract_article_details(self, url):
        # Extract content, authors, date published, title, and subtitle
        try:
            response = requests.get(url)
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the main content by selecting relevant <p> tags
            main_content = []

            # Find all paragraphs with content (you might filter more based on class names)
            for p in soup.find_all('p'):
                # Skip paragraphs that are part of the header, date, or non-content elements
                if not any(cls in p.get('class', []) for cls in ['sdc-article-header', 'sdc-site-video', 'sdc-article-date__date-time', 
                                                                'sdc-article-header__sub-title', 'sdc-site-component-header--h2',
                                                                'sdc-site-video__accessibility-message','ui-app-promo-headline','ui-app-promo-cta',
                                                                'sdc-article-strapline__text','strong']):
                    main_content.append(p.get_text())

            # Join the list of paragraphs into a full article text
            content = " ".join(main_content)

            # Extract JSON metadata from <script> tag
            script_tag = soup.find('script', type='application/ld+json')
            json_data = json.loads(script_tag.string) if script_tag else {}

            # Extract author(s)
            authors = []
            if "author" in json_data:
                author_info = json_data["author"]
                if isinstance(author_info, list):
                    authors = [author.get("name", "Unknown") for author in author_info]
                else:
                    authors = [author_info.get("name", "Unknown")]
            authors_text = ", ".join(authors)

            # Extract publication date
            date_published = json_data.get("datePublished", "No publication date found.")

            # Extract title and subtitle
            article_title = soup.find('h1', class_='sdc-article-header__title')
            title_text = article_title.find('span', class_='sdc-article-header__long-title').get_text() if article_title else "No title found"

            subtitle = soup.find('p', class_='sdc-article-header__sub-title')
            subtitle_text = subtitle.get_text() if subtitle else "No subtitle found"

            return content, authors_text, date_published, title_text, subtitle_text
        except Exception as e:
            print(f"Error extracting details from {url}: {e}")
            return "Failed to extract content", "Unknown", "Unknown", "Unknown", "Unknown"

    def get_articles(self):
        return self.items

    def filter_by_date(self):
        # Replace invalid date entries with NaT
        self.df['Date Published'] = pd.to_datetime(
            self.df['Date Published'], 
            errors='coerce',  # This will convert invalid dates to NaT
            format='%Y-%m-%dT%H:%M:%S.%f%z'  # Adjust the format if necessary
        )
        
        # Get today's date and subtract one day
        today = datetime.now().date() - timedelta(days=1)
        
        # Filter articles published today, ignoring NaT
        filtered_df = self.df[self.df['Date Published'].dt.date == today]
        
        return filtered_df

    @staticmethod
    def convert_to_json(df, file_path):
        """
        Save the dataframe as a JSON file.
        :param file_path: Path to the output JSON file.
        """
        try:
            # Convert dataframe to dictionary
            data_dict = df.to_dict(orient='records')
            
            # Ensure Timestamp objects are converted to strings
            for record in data_dict:
                if 'Date Published' in record:
                    record['Date Published'] = record['Date Published'].strftime('%Y-%m-%d %H:%M:%S')
    
            # Save the dictionary as a JSON file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, ensure_ascii=False, indent=4)
    
            print(f"Data successfully saved to {file_path}")
        except Exception as e:
            print(f"Failed to save data as JSON: {e}")  
