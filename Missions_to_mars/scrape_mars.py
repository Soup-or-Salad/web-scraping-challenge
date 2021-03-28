from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import os
import time
import requests
import warnings
warnings.filterwarnings('ignore')

def init_browser():
    executable_path = {"executable_path": "C:\\Users\\eniet\\Desktop\Chrome"}
    return Browser("chrome", **executable_path, headless=False)

mars_info = {}

def scrape_mars_news():

        browser = init_browser()

        #browser.is_element_present_by_css("div.content_title", wait_time=1)

        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        
        html = browser.html

        soup = bs(html, 'html.parser')

        # Retrieve the latest element that contains news title and news_paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

        browser.quit()

# FEATURED IMAGE
def scrape_mars_image():

        # Initialize browser 
        browser = init_browser()

        #browser.is_element_present_by_css("img.jpg", wait_time=1)

        # Visit Mars Space Images through splinter module
        featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(featured_image_url)

        html_image = browser.html

        soup = bs(html_image, 'html.parser')

        image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        main_url = 'https://www.jpl.nasa.gov'

        image_url = main_url + image_url

        image_url 

        mars_info['image_url'] = image_url 
        
        browser.quit()

        return mars_info

        

# Mars Weather 
def scrape_mars_weather():

        browser = init_browser()

        #browser.is_element_present_by_css("div", wait_time=1)

        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)
 
        html_weather = browser.html

        soup = bs(html_weather, 'html.parser')

        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

        for tweet in latest_tweets: 
            mars_weather = tweet.find('p').text
            if 'Sol' and 'pressure' in mars_weather:
                #print(mars_weather)
                break
            else: 
                pass
         
        mars_info['mars_weather'] = mars_weather

        browser.quit()

        return mars_info
        
# Mars Facts
def scrape_mars_facts():

        browser = init_browser()
 
        url = 'http://space-facts.com/mars/'
        browser.visit(url)

        tables = pd.read_html(url)
        
        df = tables[1]
    
        df.columns = ['Description', 'Value']
        html_table = df.to_html(table_id="html_tbl_css",justify='left',index=False)

        mars_info['tables'] = html_table

        return mars_info

# Mars Hemisphere
def scrape_mars_hemispheres():

        browser = init_browser()

        # Visit hemispheres website through splinter module 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        html_hemispheres = browser.html

        soup = bs(html_hemispheres, 'html.parser')

        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hiu = []

        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store link that leads to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hemispheres_main_url + partial_img_url)

            partial_img_html = browser.html
             
            soup = bs( partial_img_html, 'html.parser')
            
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            hiu.append({"title" : title, "img_url" : img_url})

        mars_info['hiu'] = hiu
        
        browser.quit()

        # Return mars_data dictionary 
        return mars_info