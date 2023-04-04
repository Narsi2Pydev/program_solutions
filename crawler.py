import requests
from bs4 import BeautifulSoup
import json
import re
# Set the URL to be crawled and maximum depth

# Create an empty dictionary to store crawled URLs
crawled = {}
crawled_list = []
crawled_list_dict = []
images_sec = []


def crawl_page(url, depth):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        #soup_href = BeautifulSoup(response_href.content, 'html.parser')
        images = soup.find_all('img', {'src': re.compile('.jpg|.jpeg|.png|.gif|.bmp', re.IGNORECASE)})

        # Add the images to the crawled dictionary with their source URL
        for image in set(images):
            src = image['src']
            if 'https:' + src not in images_sec:
                if src.startswith('//'):
                    src = 'https:' + src
                crawled['imageUrl'] = src
                crawled['sourceUrl'] = url
                crawled['depth'] = depth

                crawled_list_dict.append(crawled)
            images_sec.append(src)


        max_depth = 1 #default
        # Extract all the links and images on the page
        links = soup.find_all('a')
        if depth == 0 or depth == 1:
            max_depth = 1
        else:
            max_depth = depth
        #links.insert(0, url)
        for index, link in enumerate(links):
            try:
                if index == max_depth:
                   return crawled_list_dict
                # Get the href attribute of each link
                href = link.get('href')
                # If the link is relative, add the domain name to it
                domain = url.split('//')
                domain_name = domain[1].split('/')[0]
                if href.startswith('//'):
                    domain = url.split('//')
                    domain_name = domain.split('/') [0]
                    href = domain[0]+'//'+domain_name + url + href
                elif domain_name  not in href:
                    href = domain[0] + '//' + domain_name + href
                else:
                    pass

                if href not in crawled_list:
                    response_href = requests.get(href)
                    soup_href = BeautifulSoup(response_href.content, 'html.parser')
                    images = soup_href.find_all('img', {'src': re.compile('.jpg|.jpeg|.png|.gif|.bmp', re.IGNORECASE)})

                    # Add the images to the crawled dictionary with their source URL
                    for image in set(images):
                        src = image['src']
                        if 'https:' + src not in images_sec:
                            if src.startswith('//'):
                                src = 'https:' + src
                            crawled['imageUrl'] = src
                            crawled['sourceUrl'] = href
                            crawled['depth'] = depth

                            crawled_list_dict.append(crawled)
                        images_sec.append(src)
                    crawled_list.append(href)
            except Exception as exe:
                print(str(exe))
                pass
        return crawled_list_dict
    except Exception as exe:
        print(str(exe))
        if crawled_list_dict:
            return crawled_list_dict
        return 'No Image Found'


if __name__ == "__main__":
    # Call the crawl_page function with the initial URL and a depth of 0
    url = 'https://www.flickr.com/photos/vwalters10/30735855818/in/photolist-NQ2i7A-5YDW4w-pwe2cA-cJDCub-kBS1DB-oPHFaW-9hMyN4-kBRpS4-kBT78S-rV85K9-WmLNA9-9o1mXS-iTmyAJ-9TeAzw-cJDCyo-qzyEXB-efTfzZ-kBRuEP-nRZW1T-qihS4a-jzbxoo-FepYUZ-7diW4t-pZSEPG-Swi5fn-pCY9iV-8uSq9w-dV26un-dV7EPy-8GuvS4-jGng3d-nxJzW6-4xPVTq-d9sv9d-22rHq6o-RFSz1b-oxLukt-bFejiC-er5CuS-hvv58J-dvc8TX-pwd75x-dvhHeG-24jjc81-qPuSm3-ZU9KzM-63zc5E-YPFHgw-2fBHYfi-S157hB'  #str(input()) #specify the url and test
    depth = 0 #int(input())
    output = crawl_page(url, depth)
    if output != 'No Image Found':
        # Save the crawled URLs to a JSON file
        with open('request.json', 'w') as file:
            json.dump({'result': output}, file, indent=4)
