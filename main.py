import DB_Initialize
from Interface import UserInterface
from API_Parser import API_Parser
from HTML_Parser import HTMLProcessor
from DB_Worker import DB_Worker
from Auxiliary_scripts import link_holder, get_date


def user_out(end_msg):
    output = UserInterface()
    output.output_end_msg(end_msg)


def API_work():
    user = UserInterface()
    entered_game_name = user.get_user_game()
    api_parser = API_Parser()
    api_parser.get_news_using_api(entered_game_name)


def DB_init():
    params = "" # using PostgreSQL local database or outer DB
    DB_Initialize.DB_init(params=params)


def update_genres(link, end_msg):
    html_processor = HTMLProcessor(link)
    genres_dict = html_processor.get_genres_from_HTML()
    db_processor = DB_Worker()
    db_processor.set_genres_in_DB(genres=genres_dict)
    user_out(end_msg)


def update_games(end_msg):
    db_processor = DB_Worker()
    genres_rows = db_processor.get_data_from_DB(DB_Initialize.Genre)
    for row in genres_rows:
        genre = row.Genre_Name
        link = row.Genre_Ref
        html_processor = HTMLProcessor()
        games_dict = html_processor.get_games_from_HTML(link)
        db_processor.set_games_in_DB(genre_name=genre, games_dict=games_dict)
    user_out(end_msg)


def update_online(link, end_msg):
    db_processor = DB_Worker()
    games_data = db_processor.get_data_from_DB(DB_Initialize.Games)
    for row in games_data:
        game_name = row.Game_Name
        game_code = str(row.Game_Code)
        game_genre = row.Genre_Name
        html_processor = HTMLProcessor(link)
        online_num, actual_url = html_processor.get_online_num(game_code)
        html_processor.url = actual_url
        actual_game_code = html_processor.extract_app_id_from_url()
        db_processor.set_record_in_DB(game_name=game_name, game_code=actual_game_code, genre_name=game_genre,
                                      online_num=online_num,
                                      date=get_date())
        html_processor.url = link
    user_out(end_msg)


def switch_case(value):
    if value == 0:
        exit("\nProgram finished")
    elif value == 1:
        DB_init()
    elif value == 2:
        update_genres(link_holder(0), "genres")
    elif value == 3:
        update_games("games")
    elif value == 4:
        update_online(link_holder(1), "online")
    elif value == 5:
        API_work()
    else:
        return '\nEntered wrong task number\n'


def main():
    user = UserInterface()
    task = user.get_user_input()
    switch_case(task)


if __name__ == '__main__':
    main()