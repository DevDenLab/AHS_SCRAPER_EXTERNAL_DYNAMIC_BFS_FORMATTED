import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pdfminer.high_level import extract_text
from urllib.parse import urljoin
from copy import copy
total_visited_urls=0
def scrape_url(url, visited_urls, all_urls, output_file, max_links=1, max_total_urls=5):
    global total_visited_urls  # Declare the global variable

    if total_visited_urls >= max_total_urls:
        return  # Stop visiting URLs if the limit is reached

    if url in visited_urls:
        return

    # Mark the URL as visited
    visited_urls.add(url)
    all_urls[url] = True  # Mark the URL as found in the all_urls dictionary
    total_visited_urls += 1  # Increment the total_visited_urls counter
    text=""
    # Make an HTTP request to the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        all_urls[url] = False
        return

    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # Extract text and save to the output file
        # Select elements with content inside div.container
        elements_with_content = soup.select('body > div.container :not(:empty)')
        
        elements_tobe_removed = soup.select("body > div.container > div:nth-child(1) > div :not(:empty):not(:has(*))")
        elements_with_content = [element for element in elements_with_content if element not in elements_tobe_removed]
        
        elements_tobe_removed_hidden=soup.select('body > div.container .hidden :not(:empty):not(:has(*))')
        elements_with_content = [element for element in elements_with_content if element not in elements_tobe_removed_hidden]

        title_div = soup.select_one('#extContentBodyTop')
        text_content = title_div.get_text().strip()
        text+="\n"
        text+="\t\t\t\t\t\t"
        text+=f"Page No.{total_visited_urls}: {text_content.upper()}"
        text+="\n"
        elements_without_children = []
# soup.select_one('#extContentBodyTop').find_all(recursive=False)#task completion line
        # Iterate through children of the parent_div
        for element in elements_with_content:
             # Create a copy of the element before decomposing its children
            element_copy = copy(element)

            # Decompose children of the original element
            for child in element_copy.find_all():
                child.decompose()

            # Append the modified element_copy to the list
            elements_without_children.append(element_copy)
        
        for element in elements_without_children:
            if element.name=="a":
                # If the element has a link, append the URL in brackets
                url_text=""
                url_element = element["href"]
                url_element = urljoin(url, url_element)
                url_text += element.get_text()
                text += f"{url_text} [{url_element}]"
                text+="\n"
            elif all(char.isspace() for char in element.get_text()):
                continue
            elif element.name=="ul" or "hidden" in str(element):#[]"hidden" in str(element)
                continue
            elif element.name.startswith('h') and element.name[1:].isdigit():
                text+="\n"
                text+= element.text.upper()
                text+="\n"
            else:
                text+="\n"
                text += element.get_text().strip()
                text+="\n"

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print(f"THis URL caused the ERROR:{url}")
        print(f"{total_visited_urls} URLs has been visited")

     # Your code to save 'text' to the output file goes here
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write(text + '\n')
    print(f"VISITED THIS URL=>{url}")

    # Find all links in the page
    links_container = soup.select_one("body > div.container")

    # Exclude the div with a specific selector
    exclude_div = links_container.select_one("body > div.container > div:nth-child(1)")

    links = [
    link for link in links_container.find_all('a', href=True) 
    if link not in exclude_div.find_all('a', href=True) and
    not link['href'].lower().endswith('.pdf') and
    "youtube.com" not in link['href'] and
    "youtu.be" not in link['href'] and
    "mailto:" not in link['href'] and
    "http://waittimes.alberta.ca/" not in link['href'] and 
    "http://www.health.alberta.ca/" not in link['href'] and 
    "http://myhealth.alberta.ca/" not in link['href'] and 
    "http://www.hqca.ca/" not in link['href'] and 
    "http://www.statcan.gc.ca" not in link['href'] and
    "#shr-pg-pnl1" not in link['href'] and
    "/about/websitefeedback.aspx" not in link['href'] and
    "#" not in link['href'] and
    "?src=/about/Page3229.aspx" not in link['href'] and
    "/assets/" not in link['href'] and 
    "tel:811" not in link['href'] and 
    "https://albertafindadoctor.ca/pcn" not in link["href"] and 
    "/ems/Page18290.aspx" not in link["href"] and 
    "https://myhealth.alberta.ca/" not in link["href"] and 
    "/alberta-pcns/pages/map.aspx" not in link["href"] and
    "https://www.pcnpmo.ca/alberta-pcns/pages/map.aspx" not in link["href"] and
    "https://search.cpsa.ca/physiciansearch" not in link["href"] and
    "https://abpharmacy.ca/" not in link["href"] and
    "#contentStart" not in link['href'] and
    "https://albertafindadoctor.ca/" not in link['href'] and
    "https://www.albertahealthservices.ca/findhealth/service.aspx?id=1003853" not in link['href'] and
    "http://www.albertahealthservices.ca/findhealth/service.aspx?id=1003853" not in link['href'] and
    "https://itunes.apple.com/" not in link['href'] and
    "https://play.google.com/" not in link['href'] and 
    "https://ahsems.com" not in link['href'] and
    "https://creativecommons.org/licenses/by-nc-sa/4.0/" not in link['href'] and
    "https://csd.ahs.ca/medhf/" not in link['href'] and
    "http://itunes.apple.com/" not in link['href'] and
    "http://play.google.com/" not in link['href'] and
    "http://ahsems.com" not in link['href'] and
    "https://vendor.purchasingconnection.ca" not in link['href'] and
    "https://www.alberta.ca/provincial-EMS-advisory-committee.aspx" not in link['href'] and
    "http://www.cbc.ca/" not in link['href'] and
    "https://www.mygrandeprairienow.com/" not in link['href'] and
    "https://www.cbc.ca/" not in link['href'] and 
    "https://www.mtroyal.ca" not in link['href'] and
    "http://www.mtroyal.ca" not in link['href'] and
    "https://insite.albertahealthservices.ca/" not in link['href'] and
    "https://apps.apple.com/" not in link['href'] and 
    "http://apps.apple.com/" not in link['href'] and
    "https://ahsparkingservices.t2hosted.ca/" not in link['href'] and 
    "http://ahsparkingservices.t2hosted.ca/" not in link['href'] and
    "www.informalberta.ca" not in link['href'] and
    "www.dynalife.ca" not in link['href'] and
    "tel:1-855-550-2555" not in link['href'] and
    "together4health.albertahealthservices.ca" not in link['href'] and 
    "redcap.albertahealthservices.ca" not in link['href'] and
    "ahamms01.https.internapcdn.net" not in link['href'] and
    "bccewh.bc.ca" not in link['href'] and
    "trauma-informed.ca" not in link['href'] and
    "store.samhsa.gov" not in link['href'] and
    "www.cdc.gov" not in link['href'] and
    "www.isst-d.org" not in link['href'] and
    "nctsnet.org" not in link['href'] and
    "developingchild.harvard.edu" not in link['href'] and
    "www.traumacenter.org" not in link['href'] and
    "childtrauma.org" not in link['href'] and
    "traumastewardship.com" not in link['href'] and
    "ticcollective.ca" not in link['href'] and
    "www.instagram.com/albertahealthservices/" not in link['href'] and
    "ahamms01.https.internapcdn.net/ahamms01" not in link['href'] and
    "redcap.albertahealthservices.ca" not in link['href'] and 
    "www.healthyparentshealthychildren.ca" not in link['href'] and
    "www.uwo.ca" not in link['href']
    # "nctsnet.org/" not in link['href']

]
    for link in links[:max_links]:
        if link['href'] in ["/default.aspx"]:
            continue
        elif link['href'].lower().endswith('.pdf'):
            continue
        elif "youtube.com" in link['href'] or "youtu.be" in link['href']:
            continue
        elif "mailto:" in link['href']:
            continue
        else:
            new_url = urljoin(url, link['href'])
            scrape_url(new_url, visited_urls, all_urls, output_file, max_links, max_total_urls)

    # If it's a PDF, extract text and save to the output file
    if url.lower().endswith('.pdf'):
        pdf_text = extract_text(url)
        with open(output_file, 'a', encoding='utf-8') as file:
            file.write(pdf_text + '\n')

if __name__ == "__main__":
    start_url = "https://www.albertahealthservices.ca/about/about.aspx"
    output_file = "scraped_data.txt"
    visited_urls = set()
    all_urls = {}  # Dictionary to store all found URLs with their visited status

    # Set max_links parameter to 5
    scrape_url(start_url, visited_urls, all_urls, output_file, max_links=20)

    # Print the all_urls dictionary after scraping
    print("All URLs:")
    for url, visited in all_urls.items():
        print(f"{url}: {'Visited' if visited else 'Not Visited'}")
