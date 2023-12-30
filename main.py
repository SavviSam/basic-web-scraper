from bs4 import BeautifulSoup, BeautifulStoneSoup
from selenium import webdriver
from datetime import date
import time
import pandas as pd
import os

#read keyword file
df_keywords = pd.read_excel('keywords.xlsx')

# number of top n results to be extracted
n_result = 50

# initializing array and keyword count
se_results = []
n_keyword = 0

# loop over keyword list
for keyword in list(df_keywords['Keywords']):

  # Start webdriver
  options = webdriver.ChromeOptions()
  options.add_experimental_option("detach", True)
  options.add_argument("--headless")
  driver = webdriver.Chrome(options=options)

  n_rank = 0 # reset rank
  n_keyword += 1
  url = f'https://www.google.com/search?num={n_result}&q={keyword}'
  print(f'#{n_keyword} --- {keyword} --- {url}')
  driver.get(url)
  page_source = driver.page_source
  soup = BeautifulSoup(page_source, "lxml")

  #Grab Organic and SEM results
  results_selector = soup.select('div[class*="yuRUbf"], div[class*="v5yQqb"]' )

  for result in results_selector:
    if result['class'][0].startswith("yuRUbf"):
      domain_name_class = 'tjvcx'
      result_type = 'Organic'
      domain_name = result.select(f'cite[class*="{domain_name_class}"]')[0].get_text()
    else:
      domain_name_class = 'x2VHCd'
      result_type = 'SEM'
      domain_name = result.select(f'span[class*="{domain_name_class}"]')[0].get_text()
    link = result.select('a')[0]['href']
    n_rank += 1
    temp_dict = {
      'query_date': date.today().strftime("%m/%d/%Y"),
      'keyword': keyword,
      'rank': n_rank,
      'result_type': result_type,
      'domain_name': domain_name,
      'link': link
      }
    se_results.append(temp_dict)
  time.sleep(5)
  driver.close()
  driver.quit()


df_se_results = pd.DataFrame(se_results)

# output name
output_name = f'se_result_{date.today().strftime("%Y-%m-%d")}.xlsx'

try:
  with pd.ExcelWriter(output_name, engine='openpyxl') as writer:
    df_se_results.to_excel(writer, index=False)
except Exception as error:
  print(f"Error: {error}")





