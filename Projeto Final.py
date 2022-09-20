#!/usr/bin/env python
# coding: utf-8

# # Projeto Final

# In[29]:


import requests as r


# In[30]:


url = "https://api.covid19api.com/dayone/country/brazil"
resp = r.get(url)


# In[31]:


resp.status_code


# In[32]:


raw_data = resp.json()


# In[33]:


raw_data[0]


# In[34]:


final_data = []
for obs in raw_data:
    final_data.append([obs['Confirmed'],obs['Deaths'],obs['Recovered'],obs['Active'],obs['Date']])
final_data.insert(0,['confirmados','obitos','recuperados','ativos','data'])  
final_data


# In[35]:


confirmados = 0
obitos = 1
recuperados = 2
ativos = 3
data = 4


# In[36]:


for i in range(1, len(final_data)):
    final_data[i][data] = final_data[i][data][:10]


# In[37]:


final_data


# In[38]:


import datetime as dt


# In[39]:


import csv 


# In[40]:


with open("brasil-covid.csv", 'w') as file:
    writer = csv.writer(file)
    writer.writerows(final_data)


# In[41]:


for i in range(1, len(final_data)):
    final_data[i][data] = dt.datetime.strptime(final_data[i][data], "%Y-%m-%d")


# In[42]:


final_data


# In[59]:


def get_datasets(y, labels):
    if type(y[0]) == list :
        datasets = []
        for i in range(len(y)):
            datasets.append({
                'label' : labels[i],
                'data' : y[i]
            })
        return datasets
    else:
        return  [
            {
            'label' : labels[0],
            'data' : y
            
        }
        ]
    


# In[44]:


def set_title(title = ""):
    if title != "":
        display ="true"
    else : 
        display ="false"
    return {
        'title' : title,
        'display' : display
    }


# In[60]:


def create_chart(x, y, labels, kind='bar', title = ''):
    
    datasets = get_datasets(y, labels)
    options = set_title(title)
    
    chart = {
        'type' : kind,
        'data' : {
            'labels': x,
            'datasets' : datasets
        },
        'options': options
    }
    
    return chart
    
    
    
    
    
    


# In[61]:


def get_api_chart(chart):
    
    url_base = "https://quickchart.io/chart"
    resp = r.get(f'{url_base}?c= {str(chart)}')
    return resp.content


# In[62]:


def save_image(path, content):
    with open(path, 'wb') as image:
        image.write(content)
        


# In[63]:


from PIL import Image
from IPython.display import display


# In[64]:


def display_image(path): 
    img_pil = Image.open(path)
    display(img_pil)
    


# In[101]:


y_data_1 = []
for obs in final_data[200:800:30]:
    y_data_1.append(obs[confirmados]/30)
    
y_data_2 = []
for obs in final_data[200:800:30]:
    y_data_2.append(obs[obitos])
    
labels = ['confirmados', 'obitos']

x = []
for obs in final_data[200:800:30]:
    x.append(obs[data].strftime("%d/%m/%Y"))

chart = create_chart(x, [y_data_1, y_data_2], labels, title = "Confirmados vs Recuperados")
chart_content = get_api_chart(chart)
save_image('grafico.png', chart_content)
display_image('grafico.png')


# In[83]:


from urllib.parse import quote


# In[92]:


def get_api_qrcode(link):
    text = quote(link) # parsing do link para url
    url_base = "https://quickchart.io/qr"
    resp = r.get(f'{url_base}?text= {text}')
    return resp.content 


# In[102]:


url_base = "https://quickchart.io/chart"
link = f'{url_base}?c={str(chart)}'
save_image('qr-code.png', get_api_qrcode(link))
display_image('qr-code.png')


# In[ ]:




