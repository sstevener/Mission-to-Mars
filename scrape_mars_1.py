# Import Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests
import time

# Initialize browser
def init_browser(): 
    executable_path = {'executable_path': '/app/.chromedriver/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=True)

# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

def scrape_mars_info():
    
# NASA MARS NEWS
    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit Nasa news url through splinter module
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML Object
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        # Retrieve the latest element that contains news title and news_paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

    finally:

        browser.quit()

# FEATURED IMAGE
    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit Mars Space Images through splinter module
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)# Visit Mars Space Images through splinter module

        # HTML Object 
        html_image = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_image, 'html.parser')

        # Retrieve background-image url from style tag 
        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Website Url 
        main_url = 'https://www.jpl.nasa.gov'

        # Concatenate website url with scrapped route
        featured_image_url = main_url + featured_image_url

        # Display full link to featured image
        featured_image_url 

    finally:

        browser.quit()

# Mars Weather 
    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit Mars Weather Twitter through splinter module
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        # HTML Object 
        html_weather = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_weather, 'html.parser')

        # Find all elements that contain tweets
        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

        # Retrieve all elements that contain weather related words to exclude non weather related tweets
        for tweet in latest_tweets: 
            weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break
            else: 
                pass

    finally:

        browser.quit()

# Mars Facts

    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    # Save html code to folder Assets
    mars_facts = mars_df.to_html()

# MARS HEMISPHERES
    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit hemispheres website through splinter module 
        hemispheres_url = 'http://web.archive.org/web/20181114171728/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_hemispheres, 'html.parser')
       
        # Retreive all items that contain mars hemispheres information
        products = soup.find('div', class_='result-list')
        hemispheres = products.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hemisphere_image_urls = []

        # Loop through the items previously stored
        for hemisphere in hemispheres:
            time.sleep(5)                                               
            title = hemisphere.find('div', class_='description')
    
            title_text = title.a.text                                                
            title_text = title_text.replace(' Enhanced', '')
            browser.click_link_by_partial_text(title_text)                           
    
            usgs_html = browser.html                                                 
            soup = BeautifulSoup(usgs_html, 'html.parser')                                 
    
            image = soup.find('div', class_='downloads').find('ul').find('li')  
            img_url = image.a['href']
    
            hemisphere_image_urls.append({'title': title_text, 'img_url': img_url})

        # Define mars_info
        mars_info = {
            "news_title": news_title, 
            "news_paragraph": news_p,
            "featured_image_url": featured_image_url, 
            "weather_tweet": weather_tweet, 
            "mars_facts": mars_facts, 
            "hemisphere_image_urls": hemisphere_image_urls,
        }

    finally:

        browser.quit()

        # Return mars_data dictionary 
        return mars_info
