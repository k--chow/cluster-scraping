import requests
from bs4 import BeautifulSoup
import csv
import time

base_url = 'https://clusterbusters.org/forums/'
max_posts = 10  # Limit the number of posts to scrape
post_count = 0  # Counter for the number of posts scraped
csv_file = 'forum_posts.csv'  # Output CSV file

# Initialize the CSV file with headers
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Category', 'Subcategory', 'Post Date', 'Content'])

# A function to scrape individual posts
def scrape_post(post_url, category, subcategory):
    global post_count
    if post_count >= max_posts:
        return

    post_response = requests.get(post_url)
    post_soup = BeautifulSoup(post_response.text, 'html.parser')

    title = post_soup.find('h1', class_='ipsType_pageTitle').text.strip()
    content = post_soup.find('div', class_='cPost_contentWrap').text.strip()
    post_date = post_soup.find('time').text.strip()

    post_data = [title, category, subcategory, post_date, content]

    # Append the post data to the CSV file
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(post_data)

    print(post_data)
    post_count += 1  # Increment the post counter

    if post_count >= max_posts:
        return  # Stop further scraping once the limit is reached

# A function to recursively scrape categories and posts
def scrape_category(category_url, category_name):
    global post_count
    if post_count >= max_posts:
        return

    category_response = requests.get(category_url)
    category_soup = BeautifulSoup(category_response.text, 'html.parser')

    # Find all category links within <h4> tags
    subcategories = category_soup.find_all('h4', class_='ipsDataItem_title')

    for subcategory in subcategories:
        if post_count >= max_posts:
            return
        
        # Extract the URL and name of the subcategory or post
        subcategory_link = subcategory.find('a')
        subcategory_name = subcategory_link.text.strip()
        subcategory_url = subcategory_link['href']
        
        if 'topic' in subcategory_url:  # If it's a post
            scrape_post(subcategory_url, category_name, subcategory_name)
        else:  # If it's a subcategory
            scrape_category(subcategory_url, category_name)  # Recursive call

    # Handle pagination if present
    next_page = category_soup.find('a', rel='next')
    if next_page and post_count < max_posts:
        next_page_url = next_page['href']
        scrape_category(next_page_url, category_name)

# Start scraping from the forum's main page
def scrape_forum(base_url):
    global post_count
    main_response = requests.get(base_url)
    main_soup = BeautifulSoup(main_response.text, 'html.parser')

    # Find all main categories from the forum's main page
    categories = main_soup.find_all('h4', class_='ipsDataItem_title')

    for category in categories:
        if post_count >= max_posts:
            break
        
        category_link = category.find('a')
        category_name = category_link.text.strip()
        category_url = category_link['href']
        
        # Recursively scrape each category
        scrape_category(category_url, category_name)
        time.sleep(1)  # Add delay to prevent being blocked

# Run the scraper
scrape_forum(base_url)
