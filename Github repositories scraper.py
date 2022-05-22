# OUTLINE
# We are going to scrape https://github.com/topics
# We 'll get list of topics. For each topic get topic name, page URl, topic description
# For each page we 'll collect top 25 repositories in the topic from the topic page
# For each repository we 'll grab the repository name, username, repo URL and stars
# For each topic we will create a CSV file in the following format
'''
Repo Name,Username,Stars,Repo URL
three.js,mrdoob,81900,https://github.com/mrdoob/three.js
react-three-fiber,pmndrs,17900,https://github.com/pmndrs/react-three-fiber
babylon.js,BabylonJS,17300,https://github.com/BabylonJS/Babylon.js
'''

from bs4 import BeautifulSoup
# Use the requests library to download webpage
import requests
import pandas as pd
import os

topics_url = 'https://github.com/topics'
response = requests.get(topics_url)
print(response.status_code)  # To check whether the response is successful(200 -299)
page_content = response.text
print(len(page_content))
print(page_content[:1000])
with open('web_page.html', 'w', encoding='utf - 8') as f:
    f.write(page_content)
# Use BeautifulSoup to parse and extract information
doc = BeautifulSoup(page_content, 'html.parser')
print(type(doc))
# find title tags in topic page
topic_title_tags = doc.findAll('p', {'class': 'f3 lh-condensed mb-0 mt-1 Link--primary'})
print(len(topic_title_tags))
print(topic_title_tags[:5])
# find title description tags in topic page
topic_desc_tags = doc.findAll('p', {'class': 'f5 color-fg-muted mb-0 mt-1'})
print(len(topic_desc_tags))
print(topic_desc_tags[:5])
topic_title_tags0 = topic_title_tags[0]
# We will find link tags in topic for that we can take parent of title tag
print(topic_title_tags0.parent)
topic_link_tags = doc.findAll('a', {'class': 'no-underline flex-grow-0'})
print(len(topic_link_tags))
# Check URL tag
topic0_url = 'https://github.com' + topic_link_tags[0]['href']
print(topic0_url)

# Now get topic title , topic description and topic URL from topic page
topic_title = []
for tag in topic_title_tags:
    topic_title.append(tag.text)
print(topic_title[:5])

topic_desc = []
for tag in topic_desc_tags:
    topic_desc.append(tag.text.strip())
print(topic_desc[:5])

topic_url = []
base_url = 'https://github.com'
for tag in topic_link_tags:
    topic_url.append(base_url + tag['href'])
print(topic_url[:5])

# Create a dictionary with info
topics_dict = {'title': topic_title, 'description': topic_desc, 'url': topic_url}
print(topics_dict)
topics_df = pd.DataFrame(topics_dict)
print(topics_df)

topics_df.to_csv('topics.csv', index=None)
# In this point we have a CSV file of topic info ie, title, description, URL

# GETTING INFORMATION OUT OF A TOPIC PAGE
topic_page_url = topic_url[0]
print(topic_url[0])
response = requests.get(topic_page_url)
print(response.status_code)
print(len(response.text))
topic_doc = BeautifulSoup(response.text, 'html.parser')
# Username and repo name is a child class of h3 tag
repo_tags = topic_doc.findAll('h3', {'class': 'f3 color-fg-muted text-normal lh-condensed'})
print(len(repo_tags))
# From h3 tag get a tags containing username and repo name
a_tags = repo_tags[0].findAll('a')
print(a_tags)
user_name = a_tags[0].text.strip()
print(user_name)
repo_name = a_tags[1].text.strip()
print(repo_name)
base_url = 'https://github.com'
# Now find the repo URL
repo_url = base_url + a_tags[1]['href']
print(repo_url)
# Find stars for each repo
star_tags = topic_doc.findAll('span', {'class': 'Counter js-social-count'})
print(star_tags[0].text.strip())
# Converting star value to a number
def parse_star_count(star_str):
    star_str = star_str.strip()
    if star_str[-1] == 'k':
        return int(float(star_str[:-1]) * 1000)
    return star_str

print(parse_star_count(star_tags[0].text.strip())) # Checking if it works
# Creating a function which returns user_name, repo_name, stars, repo_url in one go
def get_repo_info(h3_tag, star_tag):
    a_tags = h3_tag.findAll('a')
    user_name = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    repo_url = base_url + a_tags[1]['href']
    stars = parse_star_count(star_tag.text.strip())
    return user_name, repo_name, stars, repo_url
print(get_repo_info(repo_tags[0], star_tags[0])) #Checking
# Now create a dictionary which have topic repository information
topic_repos_dict = {'username': [],
                    'repo_name': [],
                    'stars': [],
                    'repo_url': []
                    }
# Now we have username in repo_info[0], repo_name in repo_info[1], stars in repo_info[2] & repo_url in repo_info[3]
for i in range(len(repo_tags)):
    repo_info = get_repo_info(repo_tags[i], star_tags[i])
    topic_repos_dict['username'].append(repo_info[0])
    topic_repos_dict['repo_name'].append(repo_info[1])
    topic_repos_dict['stars'].append(repo_info[2])
    topic_repos_dict['repo_url'].append(repo_info[3])

topic_repos_df = pd.DataFrame(topic_repos_dict)
# print(topic_repos_df)
# topic_repos_df.to_csv('repo.csv')
# Inorder to get information for each page let us create a function
def get_topic_page(topic_url):
    # Download the page
    response = requests.get(topic_url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topic_url))
    # Parse using BeautifulSoup
    topic_doc = BeautifulSoup(response.text, 'html.parser')
    return topic_doc

def get_repo_info(h3_tag, star_tag):
    a_tags = h3_tag.findAll('a')
    user_name = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    repo_url = base_url + a_tags[1]['href']
    stars = parse_star_count(star_tag.text.strip())
    return user_name, repo_name, stars, repo_url

def get_topic_repos(topic_doc):
    # Get the h3 tags containing Repo title, Repo URL, username
    repo_tags = topic_doc.findAll('h3', {'class': 'f3 color-fg-muted text-normal lh-condensed'})
    # Get star_tags
    repo_stars = topic_doc.findAll('span', {'class': 'Counter js-social-count'})
    topic_repos_dict = {'username': [],
                        'repo_name': [],
                        'stars': [],
                        'repo_url': []
                        }
    # Get repo info
    for i in range(len(repo_tags)):
        repo_info = get_repo_info(repo_tags[i], repo_stars[i])
        topic_repos_dict['username'].append(repo_info[0])
        topic_repos_dict['repo_name'].append(repo_info[1])
        topic_repos_dict['stars'].append(repo_info[2])
        topic_repos_dict['repo_url'].append(repo_info[3])

    return pd.DataFrame(topic_repos_dict)
repo_df = pd.DataFrame(get_topic_repos(get_topic_page(topic_url[4])))

def scrape_topic(topic_url, topic_name):
    fname = topic_name + 'csv'
    if os.path.exists(fname):
        print('The file {} is already exist. Skipping..'.format(fname))
        return
    topic_df = get_topic_repos(get_topic_page(topic_url))
    topic_df.to_csv(fname, index=None)

'''
# Get the list of topics from the topic page
#Get the list of top repos from the individual topic page
#For each topic, create a CSV of the top repos for the topic
'''
def get_topic_title(doc):
    topic_title_tags = doc.findAll('p', {'class': 'f3 lh-condensed mb-0 mt-1 Link--primary'})
    topic_titles = []
    for tag in topic_title_tags:
        topic_titles.append(tag.text)
    return topic_titles

def get_topic_desc(doc):
    topic_desc_tags = doc.findAll('p', {'class': 'f5 color-fg-muted mb-0 mt-1'})
    topic_desc = []
    for tag in topic_desc_tags:
        topic_desc.append(tag.text.strip())
    return topic_desc

def get_topic_url(doc):
    topic_link_tags = doc.findAll('a', {'class': 'no-underline flex-grow-0'})
    topic_url = []
    base_url = 'https://github.com'
    for tag in topic_link_tags:
        topic_url.append(base_url + tag['href'])
    return topic_url
def scrape_topics():
    topics_url = 'https://github.com/topics'
    response = requests.get(topics_url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topic_url))
    topics_dict = {'title': get_topic_title(doc), 'description': get_topic_desc(doc), 'url': get_topic_url(doc)}

    return pd.DataFrame(topics_dict)

def scrape_topics_repos():
    print('Scraping list of topics')
    topics_df = scrape_topics()
    for index, row in topics_df.iterrows():
        print('Scraping top repositories for "{}"'.format(row['title']))
        scrape_topic(row['url'], row['title'])

scrape_topics_repos()













