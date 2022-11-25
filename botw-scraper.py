from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
ua = UserAgent()

company_list = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(user_agent=ua.random)
    for x in range(1, 10):
        print(f"page {x}")
        page.goto(f"https://botw.org/automotive/{x}", wait_until= 'commit')
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
        

    df = pd.DataFrame(company_list)
    df.to_csv('company_info.csv', index=False)
    print(df)

    
