# Dependencies
# I will need BS, os, request
from bs4 import BeautifulSoup as bs
import requests
import os
from splinter import Browser
import time
import pandas as pd

#Set up my main function, this will return my main dictionary
def scrape():
    # exectuable path and browser
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser('chrome', executable_path, headless=False)

    # set my news title and paragraph variable
    news_title, news_para  = scrape_mars_news(browser)

    # return my dictionary which will encompass my title, para, featured image, mars facts, and hemispheres
    return{
        "News_Title": news_title,
        "Paragraph": news_para,
        "Featured_Image":featured_image_url(browser),
        "Index_Table": mars_facts(browser),
        "Hemispheres": mars_hemis(browser)
    }

# my function for scraping mars news title and paragraph; this will be almost identical to my Jupyter notebook
def scrape_mars_news(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    
    time.sleep(3)

    html = browser.html
    soup = bs(html, "html.parser")

    # The most recent news article title
    news_title = soup.find('div',class_= "list_text").find('div',class_="content_title").text
    # The most recent news article's paragraph
    news_para = soup.find('div', class_="article_teaser_body").text

    return news_title, news_para

# my function for grabbing the featured image; this will be almost identical to my Jupyter notebook
def featured_image_url(browser):
    imageurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(imageurl)

    time.sleep(3)

    html = browser.html
    soup = bs(html, "html.parser")

    image = soup.find("a", class_="button fancybox")["data-fancybox-href"]
    featured_image_url = "https://www.jpl.nasa.gov" + image

    return featured_image_url

# my function for scraping mars facts; this will be almost identical to my Jupyter notebook
def mars_facts(browser):
    
    #create a new URL for JPL
    JPLurl = "https://space-facts.com/mars/"
    # browse the article
    
    tables = pd.read_html(JPLurl)
    first_table_df = tables[0]
    test = first_table_df.rename(columns={0: "Desc", 1:"Mars"})
    final_table = test.set_index("Desc")
    
    return final_table.to_html()

# my function for scraping for the mars hemispheres; this will be almost identical to my Jupyter notebook
def mars_hemis(browser):
    
    astro_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(astro_url)
    time.sleep(3)

    hemi_list = []
    html = browser.html
    soup = bs(html, 'html.parser')

    title_results = soup.find_all('div',class_='description')

    for i in title_results:
    
        try:
            #grab the title here, they look to all be h3:
            title = i.find('h3').text
            browser.click_link_by_partial_text(title)
        
            html = browser.html
            soup = bs(html, 'html.parser')
    
            #browser.click_link_by_partial_text('Sample')
            imageurl = soup.find('div','downloads').find('a')['href']
        
            post = { 
                    "title": title,
                    "imageURL":imageurl
            }
        
            hemi_list.append(post)
        
        except Exception as e:
            print(e)

        browser.back()
    
    return hemi_list
