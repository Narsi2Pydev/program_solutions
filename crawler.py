import requests
from bs4 import BeautifulSoup
import json
import re

# Set the URL to be crawled and maximum depth
url = 'https://example.com'

# Create an empty dictionary to store crawled URLs
crawled = {}
crawled_list = []
crawled_list_dict = []

def crawl_page(url, depth):

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    max_depth = 1 #default
    # Extract all the links and images on the page
    links = soup.find_all('a')
    if depth == 0 or depth == 1:
        max_depth = 1
    else:
        max_depth = depth
    links.insert(0, url)
    for index, link in enumerate(links):
        if index == max_depth:
            return crawled_list_dict
        # Get the href attribute of each link
        href = link.get('href')
        # If the link is relative, add the domain name to it
        if href.startswith('/'):
            href = url + href

        if href not in crawled_list:
            response_href = requests.get(href)
            soup_href = BeautifulSoup(response_href.content, 'html.parser')
            images = soup_href.find_all('img', {'src': re.compile('.jpg|.jpeg|.png|.gif|.bmp', re.IGNORECASE)})

            # Add the images to the crawled dictionary with their source URL
            for image in images:
                src = image['src']
                if src.startswith('//'):
                    src = 'https:' + src
                crawled['imageUrl'] = src
                crawled['sourceUrl'] = href
                crawled['depth'] = depth

                crawled_list_dict.append(crawled)
    return crawled_list_dict


if __name__ == "__main__":
    # Call the crawl_page function with the initial URL and a depth of 0
    url = 'http://store.steampowered.com/tags/en-us/RPG/'  #str(input()) #specify the url and test
    depth = 1 #int(input())
    output = crawl_page(url, depth)

    # Save the crawled URLs to a JSON file
    with open('request.json', 'w') as file:
        json.dump({'result': output}, file, indent=4)
