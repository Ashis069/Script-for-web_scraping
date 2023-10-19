# import all the python pakages
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd


if __name__ == '__main__':

    # Creat a empty Dataframe

    final_df = pd.DataFrame()

    for i in range(1, 40):

        # Header for request
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60',
                  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"}

        # URL for request

        url = f"https://www.flipkart.com/search?q=5g+phone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&&page={i}"

        # Dely the request for 1sec

        time.sleep(1)

        # Request url

        web = requests.get(url, headers=header)

        # creat soup object

        soup = BeautifulSoup(web.content, "html.parser")
        soup.prettify()

        # Store all div tag using .find_all method

        table = soup.find_all('div', attrs={'class': "_13oc-S"})

        # Creat empty list

        title = []
        price = []
        description = []
        rating = []

        for item in table:
            title.append(item.find('div', attrs={'class': '_4rR01T'}).text)
            description.append(item.find('ul').text)
            try:
                price.append(
                    item.find('div', attrs={'class': '_30jeq3 _1_WHN1'}).text)
            except:
                try:
                    price.append(
                        item.find('div', attrs={'class': '_30jeq3 _1_WHN1'}).text)
                except:
                    price.append(
                        item.find('div', attrs={'class': '_3utEwz'}).span.text)

            try:
                rating.append(
                    item.find('div', attrs={'class': '_3LWZlK'}).text)
            except:
                rating.append("Rating: Not Available")

        # Store all the list data into dict

        dict = {'TITLE': title,
                'DESCRIPTION': description,
                'RATING': rating,
                'PRICE': price}

        # Covert df into pandas data data frame

        df = pd.DataFrame(dict)

        # Append the the dataframe into blank dataframe

        final_df = pd.concat([final_df, df], ignore_index=True, names=[
            'TITLE', 'DESCRIPTION', 'RATING', 'PRICE'])

    # Drop all empty raws

    final_df.dropna(inplace=True)

    # Reset the index after drop the empty raws

    final_df.reset_index(drop=True, inplace=True)

    # Save the datafame into .csv file

    final_df.to_csv('Flipkar_5G_Mobile_Phone_Exctracted_data.csv')
