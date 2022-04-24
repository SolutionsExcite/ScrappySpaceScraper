from bs4 import BeautifulSoup
import requests


if __name__ == '__main__':
    page_url = 'https://stfc.space/'
    s = requests.Session()
    s.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}

    # visit the homepage to populate session with necessary cookies
    res = s.get(page_url)
    res.raise_for_status()

    json_url = 'https://in.global.nba.com/stats2/league/playerlist.json?locale=en'
    res = s.get(json_url)
    res.raise_for_status()
    data = res.json()

    player_names = [p['playerProfile']['displayName'] for p in data['payload']['players']]
    print(player_names)




