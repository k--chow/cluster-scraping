import requests
from bs4 import BeautifulSoup

# URL of the specific forum topic
url = 'https://clusterbusters.org/forums/topic/11127-new-nat-geo-documentary/'

# Send a GET request to the forum topic page
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the posts on the page
posts = soup.find_all('article', class_='cPost')

# Loop through each post and extract relevant information
for i, post in enumerate(posts, start=1):
    # Extract the username of the poster
    username = post.find('h3', class_='ipsType_sectionHead').text.strip()
    
    # Extract the date of the post
    post_date = post.find('time').text.strip()

    # Extract the content of the post
    content = post.find('div', class_='cPost_contentWrap').text.strip()
    
    print(f"Post {i}:")
    print(f"Username: {username}")
    print(f"Date: {post_date}")
    print(f"Content: {content[:200]}...")  # Print the first 200 characters of the content
    print("-" * 80)
