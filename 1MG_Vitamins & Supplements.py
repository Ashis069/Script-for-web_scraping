
# import all the python pakages
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup


if __name__ == '__main__':

    # Creat a empty Dataframe

    final_df = pd.DataFrame()

    for i in range(1, 20):

        # URL for request

        url = f"https://www.1mg.com/categories/fitness-supplements/vitamins-minerals-9?filter=true&pageNumber={i}"

        # Header for request

        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60',
                  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"}

        # Dely the request for 2sec

        time.sleep(2)

        # Request url

        r = requests.get(url, headers=header)

        # Creat soup object

        soup = BeautifulSoup(r.content, features="html5lib")

        # Store all div tag using .find_all method

        links = soup.find_all(
            'div', attrs={'class': "style__product-box___liepi"})

        # Iterate all div tag using compre

        list_link = [('https://www.1mg.com'+item.a['href']) for item in links]

        # It also be itrate using for loop

        """ for item in links:
            item = item.a['href']

            # creat link of indivisual div
            link = 'https://www.1mg.com'+item

            list_link.append(link) """

    # Creat empty list

        title = []
        brand_name = []
        pack_size = []
        price = []
        rating = []

        for url in list_link:
            time.sleep(1)
            r = requests.get(url, headers=header)
            soup = BeautifulSoup(r.content, features="html5lib")

            try:
                title.append(soup.find('h1').text)
            except:
                title.append('')

            try:
                brand_name.append(
                    soup.find('div', attrs={'class': "ProductTitle__manufacturer___sTfon"}).text)
            except:
                brand_name.append('')

            try:
                pack_size.append(soup.find(
                    'span', attrs={'class': "PackSizeLabel__single-packsize___3KEr_"}).text)
            except:
                pack_size.append('')

            try:
                price.append(soup.find('span', attrs={
                    'class': "PriceBoxPlanOption__margin-right-4___2aqFt PriceBoxPlanOption__stike___pDQVN"}).text[3:])
            except:
                price.append('')

            try:
                rating.append(soup.find(
                    'div', attrs={'class': "RatingDisplay__ratings-container___3oUuo"}).span.text)
            except:
                rating.append('')

        # Store all the list data into dict

        df = {'TITLE': title,
              'BRAND': brand_name,
              'PACK_SIZE': pack_size,
              'PRICE': price,
              'RATING': rating
              }

        # Covert df into pandas data data frame

        df = pd.DataFrame(df)

        # Append the the dataframe into blank dataframe

        final_df = pd.concat([final_df, df], ignore_index=True)

    # Drop all empty raws

    final_df.dropna(inplace=True)

    # Reset the index after drop the empty raws

    final_df.reset_index(drop=True, inplace=True)

    # Save the datafame into .csv file

    final_df.to_csv("1MG_Vitamins & Supplements.csv")

#
