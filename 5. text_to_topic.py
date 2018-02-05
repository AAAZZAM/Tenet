
# coding: utf-8

# In[2]:


import pickle
from sklearn.feature_extraction.text import CountVectorizer


# In[4]:


vocab = pickle.load(open('vocab','rb'))
model = pickle.load(open('model','rb'))
tf_vectorizer = CountVectorizer(vocabulary=vocab)


# In[ ]:


topic_dict = {0:'Congressional Committee Affairs', 1: "Immigration", 2:"Constituent Services",3:"Agricultural Issues",
        4:'Environmental Policy', 5:'Banking and Consumer Finance', 6:'Miscellany', 28:'National Security and Defense Spending',
        24:'Telecommunications and Net Neutrality', 23:'Health care', 22:'The Opioid Epidemic',
       21: 'Veteran Affairs', 20: 'Russia Investigation',18: 'Civil Rights and Protections', 17: 'International Affairs and Foreign Policy',
       16: 'Supreme Court and Civil Liberties', 15:'Disaster Relief', 14 : 'Senate Legislation',
       13: 'Military Academy Graduation',8:'Law Enforcement and Crime', 11: 'Trade Policy and U.S. Manufacturing', 10:'Federal Agencies', 7: 'Public Health',
       25: 'Taxes', 26:'Federal Grants', 27:'Domestic Policy', 19:'Speeches', 9:'Bipartisan Legislation',
       29: 'House Legislation', 12:'Campaigning and Election Politics', 13:'Honoring Constituents'}


# In[ ]:


def fit_topic_to_text(text):
    # For user input text, returns which topic best fits the input. 
    tf = tf_vectorizer.fit_transform(list(text))
    return(model.transform(tf))

