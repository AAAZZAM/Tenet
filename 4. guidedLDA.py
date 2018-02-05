
# coding: utf-8

# #### This is where the heavy lifting gets done. We import our corpus, clean the text, and run our guidedLDA model. We save the results in a pickled file. 

# In[16]:


import guidedlda
import sklearn
import numpy as np
import nltk
import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


# In[17]:


# We'll take the usual english stopwords but throw out some more domain
# specific common words. 

stopwords = nltk.corpus.stopwords.words('english')

additional = ['senator','senate','congressman','congresswoman','congress',
              'congressperson','government','united state','United States',
              'united_states','said','america','americans','mr','ms','mrs',
              'miss','new','said','going','year','make','think','want','don',
              'know','way','like']

stopwords.extend(additional)


# In[ ]:


# We'll need to clean all of our text. 

from cleanRawHTML import clean


# In[19]:


# We add the cleaned text to our list of documents. 
docs = []
for i in range(1,1670):
    df = pd.read_pickle('ProPublicaClean/'+str(i))
    docs.extend(df['html'].apply(clean).values.tolist())


# In[20]:


# Now we initialize our model. We specifically go to 4grams because 
# legislation nicknames only are three or four words long. 

# We'll first vetorize our corpus.
Y = CountVectorizer(ngram_range=(1,4), min_df=1,max_df=.80,stop_words=stopwords)
X = Y.fit_transform(docs)
vocab = Y.vocabulary_
tf_feature_names = Y.get_feature_names()

# We'll dump them all for future use. 
pickle.dump(Y, open('CountVectorizer', 'wb'))
pickle.dump(X, open('CountVectorizer.fit_transform', 'wb'))
pickle.dump(tf_feature_names, open('tf_feature_names', 'wb'))
pickle.dump(vocab,open('vocab','wb'))

word2id = dict((v, idx) for idx, v in enumerate(vocab))

# We'll use Guided LDA with seed topics.
seed_topic_list = [['senate','confirmation','gorsuch'],['russia','election','collusion','comey','mueller'],
                   ['iran','nuclear','regime','north','korea','missile','ballistic'],
                   ['tps','daca','amnesty','dreamers','immigration'],
                   ['sexual','harassment','assault'],['net','neutrality','privacy','fcc'],
                   ['obamacare','healthcare','repeal','replace'],
                   ['climate','environment','drilling','oil'],
                   ['lgbt','lgbtq','transgender'],
                   ['hurricane','fema','puerto','rico']]

# We'll load our guidedLDA model. 
model = guidedlda.GuidedLDA(n_topics=30, n_iter=400, random_state=7, refresh=20)

seed_topics = {}
for t_id, st in enumerate(seed_topic_list):
    for word in st:
        seed_topics[word2id[word]] = t_id

# We'll let our model run, and dump it afterwords. We seed with a mild 10% confidence. 
# Caution: This will take awhile. 
a = model.fit(X, seed_topics=seed_topics, seed_confidence=0.1)
pickle.dump(model, open('model','wb'))


# In[22]:


n_top_words = 1
topic_word = model.topic_word_

no_top_words = 40

def display_topics(feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print(topic_idx)
        print("/".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))
        
display_topics(tf_feature_names, no_top_words)

