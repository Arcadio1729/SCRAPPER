import pandas as pd
import json
class Helper:

    positions_df = pd.DataFrame
    subpositions_df = pd.DataFrame(columns=['name','website_name'])
    positions_json_str = ""

    names_df = pd.DataFrame(columns=['name'])

    def __init__(self):
        with open('data/positions.json') as pos_json:
            pos_dict = json.load(pos_json)
            pos_str = json.dumps(pos_dict)
            self.positions_json_str = pos_str

    def load_tickers(self):
        df_tickers = pd.read_json('data/tickers.json')
        df_tickers.columns=["NAME"]
        df_full_names = pd.read_csv('data/FullNames2.csv',lineterminator=";",header=None)
        df_full_names.columns=["NAME"]
        df = pd.concat([df_tickers,df_full_names]).dropna()
        self.names_df=df.copy()

    def load_subpostions(self,main_position):
        j = json.loads(self.positions_json_str)
        j_str = str("[" + str(j[main_position][0]["sub_positions"])[1:-1] + "]").replace('\'', '\"')
        self.subpositions_df = pd.read_json(j_str, orient='records')