import requests
from bs4 import BeautifulSoup
from requests.exceptions import MissingSchema
from concurrent.futures import ThreadPoolExecutor
import csv

broken_links = []

def check_link(post_url, link):
    if link.startswith('/'):
        link = f"https://txt.cohere.com{link}"
    try:
        response = requests.get(link)
        if response.status_code == 404:
            broken_links.append((post_url, link))
    except MissingSchema:
        pass

def is_link_to_check(url):
    return not url.startswith('javascript:void(0)') and not url.startswith('#')

def check_links_in_post(post_url):
  if post_url.startswith('/'):
    post_url = f"https://txt.cohere.com{post_url}"
  print(f"Checking post: {post_url}")

  response = requests.get(post_url)
  soup = BeautifulSoup(response.text, 'html.parser')

  # Assuming all links are under 'a' tags
  links = set([a['href'] for a in soup.find_all('a', href=True) if is_link_to_check(a['href'])])

  # Use ThreadPoolExecutor to speed up the process
  with ThreadPoolExecutor(max_workers=20) as executor:
      executor.map(lambda link: check_link(post_url, link), links)

def is_blog_post(url):
    return url.startswith('/') and not url.startswith('/author') and not url.startswith('/tag')

def scrape_blog_posts(main_url):
    page = 1
    while True:
        print(f"Scraping page: {page}")
        
        url = f"{main_url}/page/{page}/"
        response = requests.get(url)

        # If the page doesn't exist, stop the loop
        if response.status_code == 404:
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        # Assuming all blog posts are under 'a' tags
        posts = set([a['href'] for a in soup.find_all('a', href=True) if is_blog_post(a['href'])])

        print(f"Posts for page {page}: {posts}")

        # Use ThreadPoolExecutor to speed up the process
        with ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(check_links_in_post, posts)

        page += 1

    print(f"Broken links: {broken_links}")

    # Write the broken links to a CSV file
    with open('broken_links.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["blog_post_url", "broken_link"])
        writer.writerows(broken_links)

scrape_blog_posts('https://txt.cohere.com')
