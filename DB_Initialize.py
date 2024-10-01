from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey


class Base(DeclarativeBase):
    pass


def DB_init(params):
    user, password, host, port, dbname = params
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")
    Base.metadata.create_all(engine)


class Genre(Base):
    __tablename__ = 'Genre'
    ID_Genre = Column(Integer, primary_key=True, autoincrement=True)
    Genre_Name = Column(String, unique=True)
    Genre_Ref = Column(String)

    games = relationship("Games", back_populates="genre")
    online_records = relationship("OnlineRecord", back_populates="genre")

    def __init__(self, id, genre_name, genre_ref):
        self.ID_Genre = id
        self.Genre_Name = genre_name
        self.Genre_Ref = genre_ref


class Games(Base):
    __tablename__ = 'Games'
    ID_Game = Column(Integer, primary_key=True, autoincrement=True)
    Game_Name = Column(String)
    Game_Code = Column(Integer, unique=True)
    Genre_Name = Column(Integer, ForeignKey("Genre.Genre_Name"))

    genre = relationship("Genre", back_populates="games")
    online_records = relationship("OnlineRecord", back_populates="game")

    def __init__(self, id, game_name, game_code, game_genre):
        self.ID_Game = id
        self.Game_Name = game_name
        self.Game_Code = game_code
        self.Genre_Name = game_genre


class OnlineRecord(Base):
    __tablename__ = 'OnlineRecord'
    ID_Record = Column(Integer)
    Game_Name = Column(Integer, ForeignKey("Games.Game_Name"), primary_key=True)
    Genre_Name = Column(Integer, ForeignKey("Genre.Genre_Name"))
    Online_Num = Column(Integer, nullable=False)
    Date_of_Rec = Column(DateTime, primary_key=True)
    Game_Code = Column(Integer, nullable=False)

    genre = relationship("Genre", back_populates="online_records")
    game = relationship("Games", back_populates="online_records")

    def __init__(self, id, game_name, genre_name, online_num, date_of_rec, game_code):
        self.ID_Record = id
        self.Game_Name = game_name
        self.Genre_Name = genre_name
        self.Online_Num = online_num
        self.Date_of_Rec = date_of_rec
        self.Game_Code = game_code
