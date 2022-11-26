import os
os.system("playwright install chromium")
from time import sleep
import streamlit as st
import asyncio
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
ua = UserAgent()


company_list = []

def scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent=ua.random)
        progress = st.metric('Pages scraped', 0)
        col1, col2 = st.columns(2)
        for x in range(1, int(pages)):
            col1.metric('Pages Scraped', x)
            page.goto(f"https://botw.org/{category}/{x}", wait_until= 'commit')
            try:
                page.wait_for_selector('.justify-content-between:nth-child(1) h5')
                html = page.inner_html('.description > .container')
                soup = BeautifulSoup(html, 'html.parser')
                cards = soup.select('.lock')

                for card in cards:
                    try:
                        name = card.select_one('h5').text
                    except:
                        name = None
                    try:
                        address = card.select_one('strong').text
                    except:
                        address = None
                    try:
                        description = card.select_one('strong+ p').text
                    except:
                        description = None
                    try:
                        website = card.select_one('.listing_website_url a')['href']
                    except:
                        website = None
                    try:
                        phone = card.select_one('.ml-1').text
                    except:
                        phone = None
                    try:
                        star = card.select_one('.list-5 a').text
                    except:
                        star = None

                    company_info = {
                        'Name': name,
                        'Address': address,
                        'Description': description,
                        'Website': website,
                        'Phone': phone,
                        'Review star': star
                    }
                    company_list.append(company_info)
            except:
                pass

        df = pd.DataFrame(company_list)
        with st.spinner("Loading..."):
            sleep(5)
            
        col2.metric('Total data scraped', value = len(df))
        st.dataframe(df)

        csv = df.to_csv().encode('utf-8')
        st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f'{category}-data.csv',
        mime='text/csv'
        )

        browser.close()

if __name__ =='__main__':
    st.title('BOTW.ORG SCRAPER')
    st.caption('Fields to be scraped are: Company Name, Address, Phone, Website, About and Review score')
    st.caption('Check out the categories here https://botw.org/directory/')

    with st.form('Scraper form'):
        category = st.selectbox(
        "What category will you like to scrape?",
        ("automotive", "business", "health", 'computers-and-it', 'home-and-family-1', 
        'home-services', 'lawyers', 'personal-services', 'recreation-and-hobbies', 'reference-28', 'restaurants', 'shopping')
           )
        pages = st.number_input('Number of pages you wish to scrape')
        button = st.form_submit_button('scrape')
    if button:
        scrape()
        st.balloons()
        st.success('Done!')
        
