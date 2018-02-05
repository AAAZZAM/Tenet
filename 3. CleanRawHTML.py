
# coding: utf-8

# #### In this part, we'll clean the actual text to feed into our model. 

# In[74]:


# We'll import the usual text processing libraries. 
import pandas as pd
import nltk, re, pprint
from bs4 import Comment
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters


# In[75]:


# The first script uses beautiful soup to read raw_html and remove
# all text associated with inivisible elements. 

def cleanmyhtml(html):
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True
    
    def text_from_html(body):
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)  
        return u" ".join(t.strip() for t in visible_texts)
    
    html2text=re.split(r'    ',text_from_html(html))
    argmaxy = np.argmax([len(str(x)) for x in html2text])
    html2text = html2text[argmaxy]
    return(html2text)


# In[76]:


def clean(text):
    # Returns cleaned, tokenized documents from raw HTML text. 
    
    text = cleanmyhtml(url)
    
    # We need to remove things like (R-NE). There are some wacky abbreviations
    # for states, but all fall under five.
    text = re.sub(r'\w{1}\-\w{1,5}\.','',text)
    
    # U.S. needs to become US or else it'll tokenize weirdly. Same with 
    # H.R. (house resolution).
    text = re.sub(r'U\.S\.','US',text)
    text = re.sub(r'H\.R\.','HR',text)
    
    # NLTK is pretty poor at tokenizing sentences that contain ." or .'
    # We'll insert a space into these. 

    text = re.sub(r'\.\"','. \"',text)
    text = re.sub(r'\"\.','. \'',text)
    
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr','reps','Reps','H.R','h.r','hr','HR','vs', 'mr', 'ms','pres,','mrs', 'prof', 'inc', 'sens','Sens','Sen','sen'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)
    sentences = sentence_splitter.tokenize(text)
    return(sentences)
    



