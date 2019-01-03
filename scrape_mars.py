from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)
    
def scrape():
    browser = init_browser()
    
    scraped_data = {}

    # URL of NASA Mars News site
    nasa_news_url = 'https://mars.nasa.gov/news/'

    # Navigating with the browser.visit method of Splinter
    browser.visit(nasa_news_url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html_nasa = browser.html
    soup = bs(html_nasa, 'html.parser')

    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    
    scraped_data["news_title"] = news_title
    scraped_data["news_p"] = news_p

    # URL of JPL Mars Space Images site
    jpl_base_url = 'https://www.jpl.nasa.gov'
    jpl_mars_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Navigating with the browser.visit method of Splinter
    browser.visit(jpl_mars_url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html_jpl = browser.html
    soup = bs(html_jpl, 'html.parser')

    # Using Splinter - find_by_xpath method to find and click on the full size featured Mars image

    img_xpath = '//*[@id="page"]/section[3]/div/ul/li[1]/a'

    # Finding the full size image by xpath
    find_img = browser.find_by_xpath(img_xpath)
    image = find_img[0]
    image.click()

    # Using BeautifulSoup to get the url of full size featured Mars image
    link = soup.find('a',class_="fancybox")
    featured_image_url = jpl_base_url + link['data-fancybox-href']
    
    scraped_data["featured_image_url"] = featured_image_url

    # Mars Weather
    # Scraping Mars Weather twitter account and scraping the latest Mars weather tweet

    # URL of Mars weather twitter account
    twitter_mars_url = 'https://twitter.com/marswxreport?lang=en'

    # Navigating with the browser.visit method of Splinter
    browser.visit(twitter_mars_url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html_twitter = browser.html
    soup = bs(html_twitter, 'html.parser')

    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    scraped_data["mars_weather"] = mars_weather


    # ### Mars Facts
    # Scraping the Mars Facts webpage using Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # using Pandas to convert the data to a HTML table string.

    # URL of Mars Facts webpage
    mars_facts_url = 'https://space-facts.com/mars/'

    # Navigating with the browser.visit method of Splinter
    browser.visit(mars_facts_url)

    # Creating BeautifulSoup object; parse with 'html.parser'
    html_marsfacts = browser.html
    soup = bs(html_marsfacts, 'html.parser')

    # Use the read_html function to automatically scrape any tabular data from a page.
    tables = pd.read_html(mars_facts_url)
    mars_facts_df = tables[0]
    mars_facts_df.columns = ["Description", "Value"]
    mars_facts_df.set_index("Description", inplace=True)
    mars_facts_df.head()

    # generate HTML table from DataFrame
    html_table = mars_facts_df.to_html()
    

    # Clean the table by stripping unwanted newlines
    html_table = html_table.replace('\n', '')

    # Save the table
    mars_facts_df.to_html('mars_facts_table.html')
    scraped_data["mars_table"] = html_table

    # ### Mars Hemispheres
    # Scraping the USGS Astrogeology site to obtain high resolution images for each of Mars' hemispheres.<br>

    # URL of USGS Astrogeology site
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Navigating with the browser.visit method of Splinter
    browser.visit(usgs_url)

    # Creating BeautifulSoup object; parse with 'html.parser'
    usgs_html = browser.html
    soup = bs(usgs_html, 'html.parser')

    usgs_base_url = 'https://astrogeology.usgs.gov'

    results = soup.find_all("div", class_="description")

    hemisphere_image_urls = []
    #titles = []

    for result in results:
        title = result.find("h3").text
        title = ' '.join(title.split(' ')[:-1])
        #titles.append(title)
        button = result.find("a", class_="itemLink product-item")['href']
        url = usgs_base_url + button

        # Using browser.visit method to navigate to each link
        browser.visit(url)

        # Creating BeautifulSoup object for the navigated page; parse with 'html.parser'
        link_html = browser.html
        soup = bs(link_html, 'html.parser')

        # Finding the url for the full resolution hemisphere image on the navigated page
        link = soup.find("img", class_="wide-image")["src"]

        # Creating a dictionary to store title and url for each hemisphere
        dict = {'title':title, 'img_url':usgs_base_url + link}

        # Appending the dictionaries to a list
        hemisphere_image_urls.append(dict)


        scraped_data["hemisphere_image_urls"] = hemisphere_image_urls
        
    return scraped_data
   



