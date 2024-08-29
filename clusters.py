import requests
from bs4 import BeautifulSoup

# Base URL of the forum's main page
base_url = 'https://clusterbusters.org/forums/'

# Send a GET request to the main forum page
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

# print("Response ", soup)

# Find all the links to individual forum posts
post_links = soup.find_all('h4 a', class_='ipsDataItem_title', limit=10)

print("Starting on ", post_links)

# Loop through the found links to scrape individual posts
for i, link in enumerate(post_links, start=1):
    post_url = link.get('href')
    post_response = requests.get(post_url)
    post_soup = BeautifulSoup(post_response.text, 'html.parser')

    # Extract the title and content of the post
    title = post_soup.find('h1', class_='ipsType_pageTitle').text
    content = post_soup.find('div', class_='cPost_contentWrap').text.strip()

    # Print the title and a snippet of the content
    print(f"Post {i}: {title}")
    print(f"Content: {content[:200]}...")  # Print the first 200 characters of the content
    print("-" * 80)

    # Break if you have 10 posts
    if i == 10:
        break
