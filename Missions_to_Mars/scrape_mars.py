from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from flask_table import Table, Col
import time
import pandas as pd


def setup_splinter():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    # NASA Mars News
    browser = setup_splinter()
    # give url and let browser to visit this website
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(1)
    # create soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # extract the latest news title by find the first news title
    news_title = soup.find('div', class_='content_title').text
    # extract the latest news paragreph by find the first news paragreph
    news_p = soup.find('div', class_='article_teaser_body').text
    # close browser
    browser.quit()

    # JPL Mars Space Images - Featured Image
    browser = setup_splinter()
    # give url and let browser to visit this website
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    time.sleep(1)
    # create soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # get the image link by combining url and relative path
    relative_image_path = soup.find_all('img', class_='headerimage')[0]["src"]
    featured_image_url = url + relative_image_path
    # close browser
    browser.quit()

    # Mars Facts
    url = 'https://galaxyfacts-mars.com/'
    # get tables in the website
    tables = pd.read_html(url)
    # only need the first table in the website
    df = tables[0]
    df.head()
    # Rename the columns
    df.columns = ['Description', 'Mars', 'Earth']
    # Set the index as Description 
    df.set_index('Description', inplace=True)
    # repalce new lines ('\n') to ''
    mars_factor_table = df.to_html()
    mars_factor_table = mars_factor_table.replace('dataframe','table table-striped')
    mars_factor_table.replace('\n','')

    # Mars Hemispheres
    browser = setup_splinter()
    # give url and let browser to visit this website
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    time.sleep(1)
    # create soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # find item class from soup
    items = soup.find_all('div', class_="item")
    browser.quit()
    # create a new empty list to hold title and url later
    hemisphere_image_urls = []

    for item in items:
        browser = setup_splinter()
        # find the relative path for high resolution image
        relative_path = item.find('div', class_="description").a['href']
        hemisphere_link = url + relative_path
        #visit the image link
        browser.visit(hemisphere_link)
        time.sleep(1)
        html = browser.html
        # create soup for image link
        soup = BeautifulSoup(html, 'html.parser')
        browser.quit()
        # find relative path for image
        img_path = soup.find('div', class_="downloads").a['href']
        mars_hemisphere_img_path = url + img_path
        # find title for image
        title = soup.find('h2', class_="title").text
        # store the information in a dictionary
        hemisphere_dict = {
            "title": title, "img_url": mars_hemisphere_img_path
        }
        # append the dictionary to list
        hemisphere_image_urls.append(hemisphere_dict)

    # store data in a dictionary
    mission_to_mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_factor_table": mars_factor_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }
    # return data
    return mission_to_mars_dict