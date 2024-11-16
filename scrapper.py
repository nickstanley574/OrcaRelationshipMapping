import requests
from bs4 import BeautifulSoup
import json

def get_li_hrefs(url):

    if url == 'https://killerwhales.fandom.comNone':
        return []

    print(f"Getting all hrefs for: {url}")

    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all <ul> elements with class "mw-allpages-chunk"
        next_page_link = soup.find('a', string=lambda text: text and 'Next page' in text)
        next_page_href = next_page_link['href'] if next_page_link else None

        # Find all <ul> elements with class "mw-allpages-chunk"
        ul_chunks = soup.find_all('ul', class_='mw-allpages-chunk')
        
        # Extract 'href' from all <li> tags within those <ul> elements
        hrefs = get_li_hrefs(f"https://killerwhales.fandom.com{next_page_href}")
        for ul in ul_chunks:
            hrefs.extend([a['href'] for a in ul.find_all('a', href=True)])
        
        return hrefs
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def get_datasource_elements(url):

    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all elements with role="region"
        region_elements = soup.find_all(attrs={"role": "region"})
        
        # Extract all elements with a 'data-source' attribute within those regions
        datasource_elements = []
        for region in region_elements:
            datasource_elements.extend(region.find_all(attrs={"data-source": True}))
        
        return datasource_elements
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def extract_data_from_element(element):

    try:

        # Check if the element is the special case: <h2> with a "data-source" attribute
        if element.name == "h2" and element.get("data-source"):
            data_source = element.get("data-source")
            label = "Title"  # Default label for this special case
            value = element.get_text(strip=True)
            return data_source, label, value
        
        # Regular case: Extract the 'data-source' attribute
        data_source = element.get("data-source")
        
        # Extract the text content of the pi-data-label
        label_element = element.find("h3", class_="pi-data-label")
        label_text = label_element.get_text(strip=True) if label_element else None
        
        # Extract the text content of the pi-data-value
        value_element = element.find("div", class_="pi-data-value")
        value_text = value_element.get_text(strip=True) if value_element else None
        
        return data_source, label_text, value_text
    
    except Exception as e:
        print(f"An error occurred while extracting data: {e}")
        return None, None, None


def strip_value(value):
    if value != None:
        r = value.replace('\"', '')
        r = r.lstrip("\u2640 ") # Removes ♀ and any leading spaces
        r = r.lstrip("\u2642") # Removes ♂ and any leading spaces
        r = r.strip()
        return r
    else:
        return value


def get_all_items():

    items = []

    url = "https://killerwhales.fandom.com/wiki/Local_Sitemap"

    print(f"Root URL: {url}")

    hrefs = get_li_hrefs(url)

    for href in hrefs:

        url = f"https://killerwhales.fandom.com{href}"

        # No need wasting time of check the Videos_ pages
        if ("Videos_" in url or "Photos_" in url):

            print(f"Skipping {url}")

        else:

            print(f"Getting {url}")

            datasource_elements = get_datasource_elements(url)

            item = {}

            for element in datasource_elements:

                data_source, label, value = extract_data_from_element(element)

                # Exclude some of the data that is always empty
                if data_source not in ['image1', 'extended_family']:
                    item[data_source] = strip_value(value)

            if item != {}:
                item['url'] = url
                items.append(item)

    return items

filename = "killerwhales_fandom.json"

with open(filename, "w") as fp:
    json.dump(get_all_items(), fp, sort_keys=True, indent=4) 


