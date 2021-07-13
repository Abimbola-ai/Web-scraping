from bs4 import BeautifulSoup 
import numpy as np
import pandas as pd
import re
import requests

def getLastPageNumber(url):
    """Gets the maximum page on the website"""
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    regex = r"page=(.*)#"
    target_tag = soup.find("a", {"aria-label": "Last Page"})
    last_page = int((re.search(regex, target_tag.get("href")).group(1)))
    return last_page

def getData(last_page, base_url,category):
    """This function takes in a page number and a base url,
    and outputs the scraped data to a datafame"""
    page = 1
    post_title = []
    post_url = []
    post_price = []
    post_thumb_url = []

    while page != last_page+1:
        url = base_url + f"?page={page}"
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        title= [{"post_title": title.text} for title in soup.find_all("h3", class_="name")]
        post_title.extend(title)
        url= [{"post_url": base_url + link.attrs['href']} for link in soup.find_all("a",\
        class_="core") if 'href' in link.attrs]
        post_url.extend(url)
        price = [{"post_price": price.text} for price in soup.find_all("div", class_="prc")]
        post_price.extend(price)
        thumb_url= [{"post_thumb_url": link.attrs['data-src']} for link in soup.find_all("img")\
                if 'data-src' in link.attrs]
        post_thumb_url.extend(thumb_url)
        page = page + 1 

    df_list = [post_title, post_url, post_price, post_thumb_url]
    for i in df_list:
        df = pd.DataFrame(i)
        data = pd.concat(df, axis=1)
    data["category"] = category
    data = data.astype(str)
    data['post_price'] = data['post_price'].apply(Clean_price)
    data['post_title'] = data['post_title'].replace({",":""}, regex = True)
    data['post_price'] = data['post_price'].replace({"₦":"",",":""}, regex = True)
    data = data.replace(r'^\s*$', np.NaN, regex=True)
    return data

def Clean_price(post_price):
    """This function takes out the price range used by the website"""
    if re.search('\-.*', post_price):
        pos = re.search('\-.*', post_price).start()
        return post_price[:pos]
    else:
        return post_price