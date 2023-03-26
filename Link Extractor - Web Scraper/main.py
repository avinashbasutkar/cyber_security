import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama

# init the coloroma module 
colorama.init()

# We are going to use colorama just for using different colors when printing, to distinguish between internal and external links:
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

# We will need two global variables, one for all internal links of the website and the other for all the external links:

# initialize the set of links (unique links)
internal_urls = set() # Internal links are URLs that link to other pages of the same website.
external_urls = set() # External links are URLs that link to other websites.

# Since not all links in anchor tags (a tags) are valid, some are links to parts of the website, and some are javascript, 
# so let's write a function to validate URLs:

def is_valid(url):
    # checks whether URL is valid
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme) 
    # This will ensure that a proper scheme (protocol, e.g http or https) and domain name exist in the URL.

def get_all_website_links(url):
    # Return all URLs which are of the same website
    urls = set()

    domain_name = urlparse(url).netloc # Extracted the domain name from the URL. We need it to check whether the link we grabbed is external or internal.
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    # downloaded the HTML content of the web page and wrapped it with a soup object to ease HTML parsing

    # get all HTML a tags (anchor tags that contains all the links of the web page)
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
            
        # we get the href attribute and check if there is something there. Otherwise, we just continue to the next link.

        # Since not all links are absolute, we will have to join relative URLs with their domain name 
        # (e.g when href is "/search" and url is "google.com", the result will be "google.com/search"):

        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)

        # we need to remove HTTP GET parameters from the URLs, since this will cause redundancy in the set, the below code handles that:
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls

    # All we did here is checking:
    # If the URL isn't valid, continue to the next link.
    # If the URL is already in the internal_urls, we don't need that either.
    # If the URL is an external link, print it in gray color and add it to our global external_urls set and continue to the next link.

    # The above function will only grab the links of one specific page

# to extract all links of the entire website

# number of URLs visited so far will be stored here 
total_urls_visited = 0

def crawl(url, max_urls=30):
    """
    Crawls a web page and extracts all links.
    You'll find all links in external_urls and internal_urls global set variables.
    params:
        max_urls(int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

    """
    This function crawls the website, 
    which means it gets all the links of the first page 
    and then calls itself recursively to follow all the links extracted previously. 
    However, this can cause some issues; 
    the program will get stuck on large websites (that got many links) such as google.com. 
    As a result, max_urls parameter is used to exit when we reach a certain number of URLs checked.
    """

if __name__ == "__main__":

    crawl("https://www.thepythoncode.com")
    
    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))
