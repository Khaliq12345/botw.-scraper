import os
os.system("playwright install chromium")
os.system('playwright install-deps')
import streamlit as st
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
ua = UserAgent()

company_list = []

def start_scrape(category, pages):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent=ua.random)
        for x in range(1, pages):
            print(f"page {x}")
            try:
                page.goto(f"https://botw.org/{category}/{pages}", wait_until= 'commit')
                page.wait_for_selector('.d-md-block h5 > a')
                html = page.inner_html('.description > .container')
                soup = BeautifulSoup(html, 'html.parser')
                cards = soup.select('.lock')

                for card in cards:
                    try:
                        name = card.select_one('.d-md-block h5 > a').text
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
        st.markdown('<h3>Data Frame of the scraped data</h3>', unsafe_allow_html=True)
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
    st.caption('1. Note that all category to be input should be in lowercase')
    st.caption('2. Check the listing of the category you wish to scrape to know the total pages to avoid error')
    st.markdown('Top categories includes: auotmative, buisness, computer, health e.t.c...', unsafe_allow_html=True)
    st.caption('Check out more category here https://botw.org/directory/')

    with st.form('Scraper form'):
        category = st.text_input('Enter the category you wish to scrape')
        pages = st.number_input('Number of pages you wish to scrape')

        button = st.form_submit_button('scrape')
    if button:
        st.text('Scraping started')
        start_scrape(category, int(pages))
        st.balloons()
        st.success('Success')
