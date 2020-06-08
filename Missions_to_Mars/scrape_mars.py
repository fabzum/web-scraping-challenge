from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time
import re
import pymongo


def scrape():

    #Initialize Dictionary
    mars = {}

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)
    news_html = browser.html
    soup = BeautifulSoup(news_html, 'html.parser')
    news_title = soup.find('div', class_='list_text').find('a').text
    news_p = soup.find('div', class_='list_text').find('div',class_='article_teaser_body').text

  
    base_url = 'https://www.jpl.nasa.gov'
    working_url = base_url + '/spaceimages'
    browser.visit(working_url)
    time.sleep(3)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')
    image_html = browser.html
    soup = BeautifulSoup(image_html, 'html.parser')
    image_add_on = soup.find('img', class_='main_image')['src']
    featured_image_url = base_url + image_add_on

    
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(5)
    twitter_html = browser.html
    soup = BeautifulSoup(twitter_html, 'html.parser')
    pattern = re.compile(r'sol')
    mars_weather = soup.find('span', text=pattern)
    mars_weather = mars_weather.text
    mars_weather = mars_weather.replace('\n', '  ')

    facts_url = 'https://space-facts.com/mars/'
    html_table = pd.read_html(facts_url)
    html_table = html_table[0]
    html_table.columns=['Description','Values']
    html_table.set_index('Description', inplace=True)
    facts_table = html_table.to_html()
    facts_table = facts_table.replace('\n', ' ')

    start_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(start_url)
    time.sleep(3)
    title_html = browser.html
    soup = BeautifulSoup(title_html, "html.parser")
    hemispheres = []
    results = soup.find_all('div', class_='description')
    for result in results:
        result.find('h3').text
        hemispheres.append(result.find('h3').text)
    hemi_url_list = []
    for j in hemispheres:
        browser.visit(start_url)
        time.sleep(2)
        browser.click_link_by_partial_text(j)
        hemisphere_html = browser.html
        soup2 = BeautifulSoup(hemisphere_html, "html.parser")
        hemisphere_url = soup2.find('li').a['href']
        hemi_url_list.append(hemisphere_url)
    
    hemisphere_image_urls = [{"title": n, "img_url": i} for n, i in zip(hemispheres, hemi_url_list)]

    browser.quit()

    mars = {
        'news_title' : news_title,
        'news_p' : news_p,
        'featured_image_url' : featured_image_url,
        'mars_weather' : mars_weather,
        'facts_table' : facts_table,
        'hemisphere_image_urls' : hemisphere_image_urls
    }
    
    return mars

if __name__ == "__main__":
    print(scrape())