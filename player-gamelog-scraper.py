import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_player_gamelog(url_unformatted, start_year, end_year, player_name):
    years = range(start_year, end_year + 1)
    dfs = []
    for year in years:
        url = url_unformatted.format(year)
        data = requests.get(url)
        html = data.text

        soup = BeautifulSoup(html, "html.parser")
        for row in soup.find_all('tr', class_="thead"):
            row.decompose()
        gamelog_table = soup.find(id="pgl_basic")
        gamelog = pd.read_html(str(gamelog_table))[0]
        dfs.append(gamelog)

    gamelogs = pd.concat(dfs)
    del gamelogs['Rk']
    del gamelogs['G']
    del gamelogs['GS']
    del gamelogs['GmSc']
    del gamelogs['Unnamed: 5']
    gamelogs = gamelogs.rename(columns={'Unnamed: 7': 'W/L'})
    gamelogs.to_csv('gamelogs/{}.csv'.format(player_name), index=False)


if __name__ == '__main__':
    url = 'https://www.basketball-reference.com/players/g/gilgesh01/gamelog/{}'
    scrape_player_gamelog(url, 2019, 2024, 'Shai Gilgeous-Alexander')
