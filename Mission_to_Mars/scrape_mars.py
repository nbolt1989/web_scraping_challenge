# Dependencies
# I will need BS, os, request
from bs4 import BeautifulSoup as bs
import requests
import os
from splinter import Browser
import time
import pandas as pd

def scrape():
    
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser('chrome', executable_path, headless=False)
    news_title, news_para  = scrape_mars_news(browser)
    return{
        "News_Title": news_title,
        "Paragraph": news_para,
        "Featured_Image":featured_image_url(browser),
        "Index_Table": mars_facts(browser),
        "Hemispheres": mars_hemis(browser)
    }

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

def featured_image_url(browser):
    imageurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(imageurl)

    time.sleep(3)

    html = browser.html
    soup = bs(html, "html.parser")

    image = soup.find("a", class_="button fancybox")["data-fancybox-href"]
    featured_image_url = "https://www.jpl.nasa.gov" + image

    return featured_image_url

def mars_facts(browser):
    
#create a new URL for JPL
    
    
    JPLurl = "https://space-facts.com/mars/"
    # browse the article
    
    tables = pd.read_html(JPLurl)
    first_table_df = tables[0]
    test = first_table_df.rename(columns={0: "Desc", 1:"Mars"})
    final_table = test.set_index("Desc")
    
    return final_table.to_html()

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
    
        

    #hemi_df = pd.DataFrame(hemi_list)
    #for x in hemi_df['imageURL']:
        #urls = [x]
        
        #return urls
    #for x in hemi_list:
        #url = x
        #return url'''


