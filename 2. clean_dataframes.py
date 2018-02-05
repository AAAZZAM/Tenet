
# coding: utf-8

# #### In this script, we'll process and clean our dataframes.
# 
# We'll need to convert things like dates to datetime objects, but normalize things like states and districts.

# In[79]:


import pandas as pd
import re
import os
from multiprocessing import Pool
import datetime


# In[80]:


# This data is pretty messy. Things published in 2018 simply don't have 
# years. Everything is in the form 'MM DD, YY' but sometimes the month
# isn't abbreviated the way that datetime likes. We'll need to fix that. 

def date_convert(date):
    # If the input date doesn't have a year, we'll need to add 2018 to it.
    
    date_split = re.findall(r'\w+', date)
    
    # If date_split has two elements, this means the year is absent. So we'll
    # add 2018 to it. 
    
    if len(date_split) == 2:
        date = date + ' 2018'
    
    # We'll need to convert the months that datetime can't handle to
    # the proper abbreviations. 
    
    mo_dict = {'March':'Mar','April':'Apr','June':'Jun','July':'Jul','Sept':'Sep'}
    
    # Let's pull the month. It'll be the first string of consecutive letters.
    
    month = date_split[0]

    # If the month is one of these poorly formatted dates, we'll need to transform it.
    
    if month.title() in list(mo_dict.keys()):
        date = date.replace(month,mo_dict[month.title()])
        
    else:
        date = date.replace(month,month.title())
        
    # We'll put everything into a datetime format.
    
    pen_ult = datetime.datetime.strptime(date.replace(',',''),'%b %d %Y')
    
    # We'll return the month, day, and year. 
    return(pen_ult.month,pen_ult.day, pen_ult.year,pen_ult)


# In[ ]:


# We'll also normalize the state data. This is wildly inconsistent, so we'll convert
# everything to their standard two letter abbreviation.

state_dict = {'Calif.': 'CA', 'N.Y.': 'NY', 'Texas': 'TX', 'W.Va.': 'WV', 'Ohio': 'OH', 
              'Fla.': 'FL', 'Va.': 'VA', 'N.J.': 'NJ', 'Ill.': 'IL', 'Pa.': 'PA', 
              'Wis.': 'WI', 'Wash.': 'WA', 'Ga.': 'GA', 'Mass.': 'MA', 'N.C.': 'NC', 
              'Mo.': 'MO', 'Ariz.': 'AZ', 'Conn.': 'CT', 'Mich.': 'MI', 'N.D.': 'ND', 
              'Md.': 'MD', 'Ore.': 'OR', 'Iowa': 'IA', 'Tenn.': 'TN', 'Maine': 'ME', 
              'Minn.': 'MN', 'Ind.': 'IN', 'Colo.': 'CO', 'R.I.': 'RI', 'N.M.': 'NM',
              'Ark.': 'AR', 'Nev.': 'NV', 'Ky.': 'KY', 'N.H.': 'NH', 'Del.': 'DE', 
              'Hawaii': 'HI', 'Mont.': 'MT', 'Vt.': 'VT', 'Okla.': 'OK', 'La.': 'LA',
              'Kan.': 'KS', 'Ala.': 'AL', 'Utah': 'UT', 'S.C.': 'SC', 'Miss.': 'MS', 
              'S.D.': 'SD', 'Neb.': 'NE', 'Wyo.': 'WY', 'Alaska': 'AK', 
              'Northern Marina Islands': 'MP', 'Idaho': 'ID', 'D.C.': 'DC', 
              'American Samoa': 'AS', 'Virgin Islands': 'VI', 'Guam': 'GU', 
              'Puerto Rico': 'PR', None: None}


# In[122]:


# We'll define a function that cleans a given dataframe. 

def clean(dataframe):
    
    # A typical name entry looks like 'Lamar Alexander' with some exceptions like
    # Debbie Wasserman Schultz. The problem is that Paul Ryan is often listed as 
    # Paul D. Ryan. Luckily middle names are always abbreviated. So we need a way of
    # normalizing these names. Basically, we'll remove all the abbreviated letters
    # and break off the first name. 
    
    # The first name is just the first word returned. So we split by spaces.
    
    dataframe['first'] = dataframe['Member'].apply(lambda x: re.split('\s')[0])
    
    # We want to find the last word or last two words only separated by a space. 
    
    dataframe['last'] = dataframe['Member'].apply(lambda x: re.findall('\w+| \w+\W\w+',x)[-1])
    
    # With names cleaned, we have to clean name and districts. A typical string will look like
    # Calif.-37. So we need to split before and after the dash.     
    
    dataframe['state'] = dataframe['State / District'].apply(lambda x: re.split('\-',x)[0])
    
    # We only want to return a number if there's an actual district.
    
    dataframe['district'] = dataframe['State / District'].apply(lambda x: int(''.join(re.findall(r'\d+',x))))
    
    # Now we'll fill in the month, date, and year. 
    
    dataframe['month'] = dataframe['Date'].apply(lambda x: date_convert(x)[0])
    dataframe['day'] = dataframe['Date'].apply(lambda x: date_convert(x)[1])
    dataframe['year'] = dataframe['Date'].apply(lambda x: date_convert(x)[2])
    dataframe['datetime'] = dataframe['Date'].apply(lambda x: date_convert(x)[3])
    
    # Having cleaned up the date, state, and person, let's drop those. 
    
    dataframe.drop(['Date','State / District','Member'],axis=1,inplace=True)
    
    # Let's clean up the state names now. 
    
    dataframe['ST']=dataframe['state'].apply(lambda x: dicti[x])
    dataframe=dataframe.drop('state',axis=1)
    
    # Now I want to have a binary senate variable that tells me if the statement was 
    # made by a member of the house or senate. 
    
    dataframe['senate'] = dataframe['url'].apply(lambda x: 1 if re.findall('senate',str(x))!=[] else 0)
    dataframe['house'] = 1 - dataframe['senate']
    
    # Now we'll drop the redundant columns, and reorder them appropriately. 
    
    dataframe = dataframe[['last','first','house','senate','ST','district','Party','datetime','month','day','year','text','url','html']]
    dataframe.columns = ['last','first','house','senate','state','district','party','datetime','month','day','year','text','url','html']
   
    return(dataframe)


# In[78]:


# We do the usual business; define an integer-input function so we can use multiprocessing.

def cleanpath(i):
    df = clean(pd.read_pickle('ProPublicaProcessed/'+str(i)))
    destination = 'ProPublicaClean/' + str(i)
    df.to_pickle(destination)


# In[124]:


# Now we clean. 

dirs = os.listdir('ProPublicaProcessed/')
p = Pool(5)
p.map(cleanpath,files)
p.terminate()
p.join()

