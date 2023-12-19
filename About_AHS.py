import os
import requests
from bs4 import BeautifulSoup

# Initialize variables
base_url = "https://www.albertahealthservices.ca/ac/ac.aspx"
# Function to scrape a webpage
def About_Pagetitle_Scrape(url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Use the specific CSS selector to find the container div
            container_div = soup.select_one('#extContentBodyTop')
            text_content = container_div.get_text().strip()
            print(f"Page Title: {text_content}")

def About_PageContent1_Scrape(url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            # Use the specific CSS selector to find the container div
            container_div = soup.select_one('#extContentBodyBottom > div > div.col-md-8')
            elements = [element for element in container_div.children if not isinstance(element, str)]
            for divs in elements:
                text = divs.get_text().strip()
                if text and not divs.find('a'):
                    print(text)
                if divs.find_all('li') and divs.find('a'):
                     for lists in divs.find_all('li'):
                        a_tag = lists.find('a')
                        if a_tag:
                            print(f"{a_tag.get_text(strip=True)}[{a_tag['href']}]")
                     
                # if divs.find('ul'):
                #     for sub_li in divs.find_all('ul')[0].find_all('li', recursive=False):  # assuming you want to access the first ul
                #         # Print the text and link of <a> in the inner <ul>
                #         a_tag = sub_li.find('a', recursive=False)
                #         if a_tag:
                            # print(f"{a_tag.get_text(strip=True)}[{a_tag['href']}]")
                #         else:
                #             print(sub_li.get_text(strip=True))
             
                  
def About_PageContent2_Scrape(url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Use the specific CSS selector to find the container div
            container_div = soup.select_one('#extContentBodyBottom > div > div.col-md-4')
            for divs in container_div.children:
                  if divs.name == "ul":
                        for i in divs.find_all('li'):
                            print(f"{i.get_text()}[{i.find_all('a')[0]["href"]}]")
                            # print(divs.find_all('li')[0].find_all('a')[0]["href"])
                  else:
                        print(divs.get_text().strip().replace('\n\n','\n'))
if __name__ == "__main__":
    About_Pagetitle_Scrape(base_url)
    # About_PageContent1_Scrape(base_url)
    # About_PageContent2_Scrape(base_url)
