from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from DB_Initialize import Genre, Games, OnlineRecord


class DB_Worker:
    params = ""  # same as in main.py line 22

    def __init__(self):
        pass

    def __get_session(self):
        user, password, host, port, dbname = self.params
        engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    def set_genres_in_DB(self, genres):
        session = self.__get_session()
        last_id = session.query(func.max(getattr(Genre, "ID_Genre"))).scalar()
        id = last_id + 1 if last_id is not None else 1
        for genre_name, genre_ref in genres.items():
            new_genre = Genre(id, genre_name=genre_name, genre_ref=genre_ref)
            session.add(new_genre)
            try:
                session.commit()
            except Exception as err:
                print(print(f"Caused error: {err}"))

        session.close()

    def set_games_in_DB(self, genre_name, games_dict):
        session = self.__get_session()
        last_id = session.query(func.max(getattr(Games, "ID_Game"))).scalar()
        id = last_id + 1 if last_id is not None else 1
        for game_name, game_code in games_dict.items():
            new_game = Games(id=id, game_name=game_name, game_code=game_code, game_genre=genre_name)
            session.add(new_game)
            try:
                session.commit()
            except Exception as err:
                print(print(f"Caused error: {err}"))
        session.close()

    def set_record_in_DB(self, game_name, game_code, genre_name, online_num, date):
        session = self.__get_session()
        last_id = session.query(func.max(getattr(OnlineRecord, "ID_Record"))).scalar()
        id = last_id + 1 if last_id is not None else 1
        new_record = OnlineRecord(id=id, game_name=game_name, genre_name=genre_name, online_num=online_num,
                                  date_of_rec=date, game_code=game_code)
        session.add(new_record)
        try:
            session.commit()
        except Exception as err:
            print(print(f"Caused error: {err}"))
        session.close()

    def get_data_from_DB(self, table):
        session = self.__get_session()
        query = session.query(table).all()
        session.close()
        return query
