import logging
import sys
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup


def collect_collections(date):
    movies = []
    collection = []
    rows = []
    body = requests.get(f"https://www.boxofficemojo.com/year/world/{date}/")
    LOG_FILENAME = datetime.now().strftime('log/logfile_%H_%M_%S_%d_%m_%Y.log')
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
    if body.status_code == 200:
        soup = BeautifulSoup(body.content, 'html.parser')
        table = soup.find_all('table')
        for i in table[0].find_all('tr'):
            if i.find('td', class_='mojo-field-type-money') is not None:
                collection.append(i.find('td', class_='mojo-field-type-money').decode_contents())
            for j in i.find_all('td'):
                for k in j.find_all('a', class_="a-link-normal"):
                    movies.append(k.get_text())
        for i in zip(movies, collection):
            rows.append(list(i))
        dataframe_and_csv(rows)
        logging.info(f"Records has been saved in list_movies_with_collections_{date}.csv file")
        print(f"Done...\nRecords has been saved in list_movies_with_collections_{date}.csv file")
    else:
        logging.error(f"Error occured while fetching data from https://www.boxofficemojo.com/year/world/{date}/")
        print(f"Error occured while fetching data from https://www.boxofficemojo.com/year/world/{date}/")


def dataframe_and_csv(rows):
    fields = ['Movies', 'Worldwide Collections']
    collections = pd.DataFrame(rows, columns=fields)
    df = pd.DataFrame(collections)
    df.to_csv(f"Records/list_movies_with_collections_{date}.csv", index=False)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        date = sys.argv[1]
    else:
        date = input("Enter Year: ")
    if not date.isalpha():
        print("Initializing...")
        collect_collections(date)
    else:
        print("Argument must be a Integer !")
