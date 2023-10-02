import html
import requests

from bs4 import BeautifulSoup

class SiteScrapper:

    MAIN_URL = "https://www.biznesradar.pl/"
    POSITIONS_PATH = "/content/sample_data/positions.json"
    TICKERS_PATH = "/content/sample_data/tickers.json"
    FULL_NAMES_PATH = "/content/sample_data/FullNames2.csv"

    def __init__(self):
        pass

    def get_from_website(self, tck, pos, part):
        URL = self.MAIN_URL + part + "/" + tck + ",Q,0"
        page = requests.get(URL)

        str = html.unescape(page.text)
        periods = self.__get_periods(str)
        if len(periods) > 0:
            values = self.__get_balance_position(str, pos)
            tcks = [tck] * len(periods)
            parts = [pos] * len(periods)
            return list(zip(tcks, periods, values, parts))
        return []
    def __get_balance_position(self, source, field):
        values = []
        periods = []

        soup = BeautifulSoup(source, "html.parser")
        spans = []

        for el in soup.select("[data-field]"):
            if (el["data-field"] == field):
                spans = el.find_all("span", {"class": "value"})

        for s in spans:
            values.append(float(s.text.replace(' ', '')))

        return values
    def __get_periods(self,sdata):
        periods = []
        soup = BeautifulSoup(sdata,"html.parser")
        myths = soup.find_all("th", class_="thq h")

        for th in myths:
            if "/" in th.text:
                periods.append(th.text.strip()[0:7].replace('/', '-'))

        return periods