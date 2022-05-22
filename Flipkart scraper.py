# OUTLINE
# We are going to scrape https://github.com/topics
# We 'll get list of topics. For each topic get topic name, page URl, topic description
# For each page we 'll collect top 25 repositories in the topic from the topic page
# For each repository we 'll grab the repository name, username, repo URL and stars
# For each topic we will create a CSV file in the following format
'''
name,prize,offer,url
JUARI BE A GENTLEMAN Men Vest,₹499,72% off,https://www.flipkart.com/juari-gentleman-men-vest/p/itmae2305366f121?pid=VESFZPAYSEHTCYFF&lid=LSTVESFZPAYSEHTCYFFEH7ZTS&marketplace=FLIPKART&store=clo&srno=b_1_1&otracker=clp_omu_Fashion%2BTop%2BDeals_7_2.dealCard.OMU_offers-store_offers-store_3L3DQEVF47D8_1&otracker1=clp_omu_PINNED_neo%2Fmerchandising_Fashion%2BTop%2BDeals_NA_dealCard_cc_7_NA_view-all_1&fm=organic&iid=en_Rw1ytxgOTzE9kh1a1Y68sj3YJaJLX%2F1H7Rh1%2B3hpeF95W4J5SYlhXWmlXfLvlD07zxuIGenHbbCE2qUbPdUbPQ%3D%3D&ppt=None&ppn=None&ssid=c9buxz5gnk0000001653214185030
Solid Men Reversible Multicolor T-Shirt,₹449,85% off,https://www.flipkart.com/solid-men-reversible-multicolor-t-shirt/p/itmb259f9c3594cd?pid=XPTG7G9AMTTGKKQX&lid=LSTXPTG7G9AMTTGKKQXEGNLIT&marketplace=FLIPKART&store=clo&srno=b_1_2&otracker=clp_omu_Fashion%2BTop%2BDeals_7_2.dealCard.OMU_offers-store_offers-store_3L3DQEVF47D8_1&otracker1=clp_omu_PINNED_neo%2Fmerchandising_Fashion%2BTop%2BDeals_NA_dealCard_cc_7_NA_view-all_1&fm=organic&iid=en_Rw1ytxgOTzE9kh1a1Y68sj3YJaJLX%2F1H7Rh1%2B3hpeF%2BMqoonCGzTKJeOdPU5LZ%2FGJ5CmolrrTR%2FFyj5DeEJLEw%3D%3D&ppt=None&ppn=None&ssid=c9buxz5gnk0000001653214185030
Men & Women Solid Ankle Length,₹105,73% off,https://www.flipkart.com/winget-men-women-solid-ankle-length/p/itm27cc2896cdb64?pid=SOCGCT2CGZYHUMWY&lid=LSTSOCGCT2CGZYHUMWYRNRGTC&marketplace=FLIPKART&store=clo&srno=b_1_3&otracker=clp_omu_Fashion%2BTop%2BDeals_7_2.dealCard.OMU_offers-store_offers-store_3L3DQEVF47D8_1&otracker1=clp_omu_PINNED_neo%2Fmerchandising_Fashion%2BTop%2BDeals_NA_dealCard_cc_7_NA_view-all_1&fm=organic&iid=5a59a573-3e24-4b92-a1d5-431c2e9c3ce5.SOCGCT2CGZYHUMWY.SEARCH&ppt=None&ppn=None&ssid=c9buxz5gnk0000001653214185030
'''
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.flipkart.com/offers-store?otracker=nmenu_offer-zone&fm=neo%2Fmerchandising&iid=M_ec9d801d-e711-4c42-a57b-ed46d47d5d33_1_372UD5BXDFYS_MC.G6ZC4RAJ9OHU&otracker=hp_rich_navigation_1_1.navigationCard.RICH_NAVIGATION_Top%2BOffers_G6ZC4RAJ9OHU&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_1_L0_view-all&cid=G6ZC4RAJ9OHU'
response = requests.get(url)  # Use the requests library to download webpage
print(response.status_code)  # To check whether the response is successful(200 -299)
deal_content = response.text
with open('top.html', 'w',  encoding='utf - 8') as f:
    f.write(deal_content)
# Use BeautifulSoup to parse and extract information
doc = BeautifulSoup(deal_content, 'html.parser')
title_tags = doc.findAll('div', {'class': '_3LU4EM'})
link_tags = doc.findAll('a', {'class': '_6WQwDJ'})
deal_name = title_tags[9].string
base_url = 'https://www.flipkart.com'
print(base_url + link_tags[1]['href'])
print(len(title_tags))
print(len(link_tags))
deal_titles = []
deal_urls = []
for tag in title_tags:
    deal_titles.append(tag.text.strip())
print(len(deal_titles))
print(deal_titles[:5])
for tag in link_tags:
    deal_urls.append(base_url + tag['href'])
print(len(deal_urls))
print(deal_urls[:5])
# create a function which returns a dataframe
def get_deal_info():
        url = 'https://www.flipkart.com/offers-store?otracker=nmenu_offer-zone&fm=neo%2Fmerchandising&iid=M_ec9d801d-e711\
        -4c42-a57b-ed46d47d5d33_1_372UD5BXDFYS_MC.G6ZC4RAJ9OHU&otracker=hp_rich_navigation_1_1.navigationCard.\
        RICH_NAVIGATION_Top%2BOffers_G6ZC4RAJ9OHU&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising\
        _NA_NAV_EXPANDABLE_navigationCard_cc_1_L0_view-all&cid=G6ZC4RAJ9OHU'
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception('Failed to load page {}'.format(url))
        doc = BeautifulSoup(deal_content, 'html.parser')
        title_tags = doc.findAll('div', {'class': '_3LU4EM'})
        link_tags = doc.findAll('a', {'class': '_6WQwDJ'})
        deal_titles = []
        deal_urls = []
        for tag in title_tags:
            deal_titles.append(tag.string.strip())
        for tag in link_tags:
            deal_urls.append(base_url + tag['href'])

        deal_dict = {'title': deal_titles, 'url': deal_urls}
        return pd.DataFrame(deal_dict)  # using pandas as pd

# Now get the product details from the category page
page_url = deal_urls[0]
response = requests.get(page_url)
print(response.status_code)
page_content = response.text
page_doc = BeautifulSoup(page_content, 'html.parser')
product_tags = page_doc.findAll('a', {'class': 'IRpwTa'})
print(len(product_tags))
print(product_tags[:5])
product_title = product_tags[0].text.strip()
print(product_title)
product_url = base_url + product_tags[0]['href']
print(product_url)
prize_tags = page_doc.findAll('div', {'class': '_30jeq3'})
print(len(prize_tags))
print(prize_tags[:5])
product_prize = prize_tags[0].string
print(product_prize)
offer_tags = page_doc.findAll('div', {'class': '_3Ay6Sb'})
print(len(offer_tags))
print(offer_tags[:5])
product_offer = offer_tags[0].string
print(product_offer)
# create list and append each tag info
title = []
url = []
prize = []
offer = []
for tag in product_tags:
    title.append(tag.text.strip())
print(len(title))
print(title[:5])
for tag in product_tags:
    url.append(base_url+tag['href'])
print(len(url))
print(url[:5])
for tag in prize_tags:
    prize.append(tag.text.strip())
print(len(prize))
print(prize[:5])
for tag in offer_tags:
    offer.append(tag.text.strip())
print(len(offer))
print(offer[:5])
# create a function to get product information
# information ie, title, url, prize, offer
def get_product_info(deal_urls):
    page_url = deal_urls
    response = requests.get(page_url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(deal_urls))
    page_content = response.text
    page_doc = BeautifulSoup(page_content, 'html.parser')
    product_tags = page_doc.findAll('a', {'class': 'IRpwTa'})
    prize_tags = page_doc.findAll('div', {'class': '_30jeq3'})
    offer_tags = page_doc.findAll('div', {'class': '_3Ay6Sb'})
    title = []
    url = []
    prize = []
    offer = []
    for tag in product_tags:
        title.append(tag.text.strip())
    for tag in product_tags:
        url.append(base_url + tag['href'])
    for tag in prize_tags:
        prize.append(tag.text.strip())
    for tag in offer_tags:
        offer.append(tag.text.strip())

    product_dict = {'name': title, 'prize': prize, 'offer': offer, 'url': url}
    print(product_dict)
    return pd.DataFrame(product_dict)  # create Dataframe using panda as pd which have product info

'''
Get the list of categories from deals of the day page
Get the list of top products from the individual category page
For each category, create a CSV of the top products information 
'''
def deal_scrape(deal_urls, deal_name):
    fname = deal_name + 'csv'
    if os.path.exists(fname):
        print('The file {} is already exists skipping filename'.format(fname))
        return
    product_df = get_product_info(deal_urls)
    product_df.to_csv(fname, index=None)

def scrape_products_info():
    print('Scraping top deals of the day')
    p_df = get_deal_info()
    for index, row in p_df.iterrows():
        print('Scraping top products for {}'.format(row['title']))
        deal_scrape(row['url'], row['title'])

scrape_products_info()

