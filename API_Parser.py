import requests
from Auxiliary_scripts import extract_titles
from DB_Worker import DB_Worker
import DB_Initialize


class API_Parser:

    def __init__(self):
        pass

    def __get_json(self, app_id: str, count: int = 5, max_length: int = 1000, format_type: str = 'json'):
        url = "http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/"
        params = {
            'appid': app_id,
            'count': count,
            'maxlength': max_length,
            'format': format_type
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return response.json()

    def get_news_using_api(self, entered_game_name):
        app_id = 0
        games_getter = DB_Worker()
        games_rows = games_getter.get_data_from_DB(DB_Initialize.Games)
        for row in games_rows:
            game_name = row.Game_Name
            game_code = str(row.Game_Code)
            if game_name == entered_game_name:
                app_id = game_code
        if app_id == 0:
            print(f"Can not find game, named - {entered_game_name}")
            return None
        response = self.__get_json(app_id=app_id)
        titles = list(extract_titles(response))
        print("Recent news:")
        try:
            for title in titles:
                print(title)
        except TypeError as e:
            print(f"Caused error: {e}")
