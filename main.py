from bs4 import BeautifulSoup
import requests
import pandas as pd

def collect_collections(date):
    movies = []
    collection = []
    rows = []
    body = requests.get(f"https://www.boxofficemojo.com/year/world/{date}/")
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

        fields = ['Movies', 'Worldwide Collections']
        collections = pd.DataFrame(rows, columns=fields)
        collections.to_csv(f"list_movies_with_collections_{date}.csv")
        print(f"Done...\nRecords has been saved in list_movies_with_collections_{date}.csv file")
    else:
        print(f"Error occured while fetching data from https://www.boxofficemojo.com/year/world/{date}/")

if __name__ == '__main__':
    date = input("Enter Year: ")
    print("Initializing...")
    collect_collections(date)
