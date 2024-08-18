import time
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def index():
   latest = 'news-releases-list/'
   res = scrap(latest)
   return res

@app.get("/business")
async def business():
   bus = 'financial-services-latest-news/financial-services-latest-news-list/'
   res = scrap(bus)
   return res

@app.get("/entertainment")
async def entertainment():
   ent = 'entertainment-media-latest-news/entertainment-media-latest-news-list/'
   res = scrap(ent)
   return res

@app.get("/sports")
async def sports():
   sp = 'sports-latest-news/sports-latest-news-list/'
   res = scrap(sp)
   return res

@app.get("/health")
async def health():
   hl = 'health-latest-news/health-latest-news-list/'
   res = scrap(hl)
   return res

@app.get("/technology")
async def technology():
   tech = 'consumer-technology-latest-news/consumer-technology-latest-news-list/'
   res = scrap(tech)
   return res

@app.get("/science")
async def science():
   sci = 'energy-latest-news/energy-latest-news-list/'
   res = scrap(sci)
   return res

@app.get("/environment")
async def environment():
   env = 'environment-latest-news/environment-latest-news-list/'
   res = scrap(env)
   return res

@app.get("/crypto")
async def crypto():
   cry = 'financial-services-latest-news/cryptocurrency-list/'
   res = scrap(cry)
   return res

# web3
# blockchain
# ai



if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

genai.configure(api_key="AIzaSyCWna-D27sTjqf3IuIBgd_BD5ZFfvIfQrA")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
]

si = 'Respond like a news reporter for a english speaking news channel. Present the news in about a minute long summary when provided the headline and the content of the news article. Make sure to use only the neccessary details as a professional news anchor would do but also be as elaborative as possible. The output needs to be exactly as if you are speaking the result as an actual anchor and add some humanness to the result as well. Do not include any useless symbols, just the speech content for around one minute of reading time.'
model = genai.GenerativeModel(model_name="gemini-1.5-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings,
                              system_instruction=si)

url = 'https://www.prnewswire.com/news-releases/'

def scrap(typ):   
   # Main Webpage Url to get specific articles
   urlS = url + typ

   response = requests.get(urlS)
   soup = BeautifulSoup(response.content, 'html.parser')

   # List to store links
   links = []


   # Finding and storing the links in the list
   for news_item in soup.find_all('a', class_='newsreleaseconsolidatelink display-outline w-100'):
      links.append(news_item['href'])

   u = 'https://www.prnewswire.com'

   count = 1
   newsDict = {}

   for link in links:
      if count <= 10:
               # Generating the web-accessable link 
               al = str(u+link) 

               # Initializing the scrapper
               headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
               res = requests.get(al, headers=headers)
               doc = BeautifulSoup(res.content, 'html.parser')
               
               # Extracting the Headline
               head = doc.find('h1')
               head = head.text
               head = head.split('\n')[0]

               # Extracting Content of the article
               content = doc.find('div', class_='col-lg-10 col-lg-offset-1')
               content = content.text
               content = content.strip()

               # print("\n Headline: "+head+"\n Content: "+content+"\n")

               # Confiuring the prompt to get the desired format as result of the content. 
               tr = f'The heading of the news article is "{head}" and the content is: {content}.'
               # prompt_parts = [
               #       f"As an anchor for an English speaking news channel, present the news in about a minute long summary with the headline {head} and its content as {content}. Make sure to use only the neccessary details as a professional news anchor would do but also be as elaborative as possible. The output needs to be exactly as if you are speaking the result as an actual anchor and add some humanness to the result as well. Do not include any useless symbols, just the speech content."]
               pr = model.generate_content(tr)
               # print(response.text)
               # response = model.generate_content(prompt_parts)
               promtRes = pr.text   

               # Appending the news to the dictionary as a storage
               newsDict.update({head : promtRes}) 
               # print("\n PROMPT RES OF "+str(count)+" : \n")
               # print(promtRes)

               count = count + 1
               time.sleep(15)
         
   return newsDict