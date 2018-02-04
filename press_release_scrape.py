
# coding: utf-8

# In[1]:


# We'll need to request and process raw HTML text.
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd


# ProPublica seems to rate limit requests from Python scripts,
# so we'll need to tell it that we're accessing from a browser. 
import time
import random
from fake_useragent import UserAgent

# Despite our rate limiting, scraping is embarasssingly parallelizable. 
from multiprocessing import Pool

# We'll eventually need to access some folders.
import os


# #### The Strategy: 
# 
# The ProPublica repository is paginated, so to use multiprocessing we'll need to define a function that scrapes the links from a specific page so we can employ the multiprocessing library. 

# In[2]:


# This function scrapes the ith page of the ProPublica link database. 
def scrape_onepage(i):
    # ProPublica was *really* keen on rate limiting us. So not only will we
    # spoof a useragent, but we'll randomize the times that we request from 
    # them. 
    time.sleep(.3+random.uniform(.1,.2))
    
    # Now. We'll try twice to access a given webpage before we quit trying
    # and move on. 

    number_of_attempts = 0
    
    while number_of_attempts<2:
        try:
            # We navigate to the ith page from a "Chrome" browser. 
            url = 'https://projects.propublica.org/represent/statements'
            payload = {'page':str(i)}
            r = requests.get(url,params=payload,headers={'User-Agent':str(UserAgent().chrome)})
            
            # We get all the one table present with Panda's read_html function, but
            # keep in mind that it returns a list of tables, so we'll need to concatenate them
            # together. 
            
            press_releases = pd.concat(pd.read_html(r.content))
            
            # The problem is that we have all the information, but pandas only pulled the
            # titles, not the actual URLs. We have to make an actual second pass and pull 
            # those too. 
            
            # We'll load the page into a soup object, and pull all the <a> tags. Note that
            # we're not loading it twice, just processing it a second time. 
            soup = BeautifulSoup(r.content,'lxml')
            
            # We'll need to pull the href links from the <a> tags. 
            press_releases['url'] = pd.Series(soup.find_all("a", href=re.compile("gov"))).apply(lambda x : x['href'])
            
            
            # Now we'll save our results in a pickled dataframe file. 
            df.to_pickle('ProPublica/' + str(i))
            
            # If we've succeeded, then there's no need for further attempts. 
            number_of_attepts = 3
            
        except ConnectionError:
            # If we experience a connection error, then we'll try again. 
            number_of_attempts = number_of_attempts+1
            
    # If we've succeeded, then the number_of_attempts will be 3. If the number_of_attempts
    # was actually two, then we'll need to record this so we can try again later. 
    if number_of_attempts==2:
        file = open('ProPublica/errors','a')
        file.write(str(i) + '\n')
        file.close()


# #### Success!
# Now that we can scrape a single webpage, we can scrape multiple at a time with Multiprocessing.

# In[ ]:


# Let's use five threads. 

p = Pool(5)

# The plague of web scraping is setting up a big job that encounters
# a poorly formatted webpage and throws an error. I'm a big fan of 
# leaving bad webpages behind, and coming back to get them later. 

# To this end, we'll initialize a count. We'll scour all of these webpages, 
# and ignore any page that gives us trouble for any reason. We'll then
# make a few passes at the end to pick up those pages. 

# We initialize the number of passes, called the count. 
number_of_passes = 0

# We're going to scrape 4000 pages of links, for about 400,000 links. 
pages = list(range(1,4000))

# We're doing to delete pages that we've successfully scraped. At the end 
# of one trial we'll go back for those that gave an error. 

while len(pages)>0: 
    # We'll try three times to pick them all up. 
    if number_of_passes < 3:
        try:
            # If we have a file successfully downloaded, we'll delete it from
            # the list of pages we have to download. 
            
            for x in os.listdir('ProPublica'):
                try:
                     if int(x)<4000:
                        pages.remove(int(x))
                except:
                    pass
                
            # Now we'll try to grab everything using our threaded process. 
            p.map(scrape_onepage,pages)
            p.terminate()
            p.join()

        except:
            number_of_passes = number_of_passes+1
            pass
    else:
        pages = []


# #### The Strategy, Part 2: 
# 
# At this point, we have 400,000 or so links corresponding to congressional press releases. 
# We need to go fetch all of the text from these websites. We can clean them after we've fetched them, so we'll just go pull the raw html and add them to every dataframe. 

# In[3]:


# We'll define a function that just pulls the raw html from the webpage. I don't want 
# to pull "404 File Not Found" and not know about it, so I'll just have it return
# None if it encounters a page with anything but a healthy 200 response code. 

def process_page(page):
    # I'm not a fan of lazy try/except blocks, but it's pretty necessary for large
    # scraping operations. 
    try:
        a = requests.get(page,headers = header)
        if a.status_code == 200:
            return(a.content)
        else:
            return(None)
    except:
        return(None)


# In[6]:


# We're going to open up a single file we saved in a previous step, which should contain
# 100 or so links. We want this function to have integer inputs as to make multiprocessing 
# a little easier. 

def process_file(i):
    # This function downloads the html text from each page downloaded in the previous
    # steps. 
    df = pd.read_pickle('ProPublica/'+str(i))
    df['html'] = None
    for j, row in enumerate(df.iterrows()):
        df.iloc[j]['html'] = process_page(row[1]['url'])
    df.to_pickle('ProPublicaProcessed/'+str(i))


# In[ ]:


# We'll open up five threads and go to work. 

files = os.lisdir('ProPublica')

# Remember p = Pool() was defined previously. 

p.map(process_file, files)
p.terminate()
p.join()


# #### Phew. We did it. 
# 
# We now have all the HTML content downloaded locally to our folder ProPublicaProcessed. We'll need to clean it and extract text, but that's for the next segment.
