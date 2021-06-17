# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)
def scrape():
    browser=init_browser()
    mars_dict={}

    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')

    # Retrieve content title
    url_title = soup.find_all('div', class_ = 'content_title')[0].text

    # Retrieve latest news paragraph
    url_p = soup.find_all('div', class_='article_teaser_body')[0].text
    
    jpl_url = 'https://spaceimages-mars.com/'
    jpl_image_url = 'https://spaceimages-mars.com/image/featured/mars2.jpg'
    browser.visit(jpl_image_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    # Retrieve image link
    img_path = soup.find_all('img')[0]['src']
    
    # Scrape Mars Facts
    url = 'https://galaxyfacts-mars.com/'
    table=pd.read_html(url)
    mars_facts = table[0]
    mars_facts = mars_facts.rename(columns={0:"Mars - Earth Comparison", 1:"Mars", 2:"Earth"})
    mars_facts.drop(index=mars_facts.index[0], axis=0, inplace=True)
    mars_facts.set_index("Mars - Earth Comparison",inplace=True)
    mars_facts
    facts_html = mars_facts.to_html()
    facts_html.replace('\n', '')

    # Mars Hemispheres
    guss_url = 'https://marshemispheres.com/'
    browser.visit(guss_url)
    html=browser.html
    soup=bs(html,'html.parser')

    # Extract hemispheres item elements
    mars_hems=soup.find('div',class_='collapsible results')
    mars_item=mars_hems.find_all('div',class_='item')
    hemisphere_image_urls=[]

    for item in mars_item:
        #Scrape Title
        hemisphere = item.find('div', class_="description")
        title = hemisphere.h3.text
        
        #Scrape img links
        hems_link = hemisphere.a["href"] 
        browser.visit(guss_url + hems_link)
        image_html = browser.html
        image_soup = bs(image_html, 'html.parser')
        image_link = image_soup.find('div', class_='wide-image-wrapper')
        image_url = image_link.find('img', class_='wide-image')['src']
        
        #Create dictionary to store title and url
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
        hemisphere_image_urls.append(image_dict)

    print(hemisphere_image_urls)

    browser.quit()
    