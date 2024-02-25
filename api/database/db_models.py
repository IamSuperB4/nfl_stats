"""NFLProjections database ORM Classes"""
    
    
    



# class Base(DeclarativeBase):
#     pass


# class Bets(Base):
#     """Table to store bets placed"""
#     __tablename__ = 'Bets'
#     Id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     UserId:Mapped[int] = mapped_column(ForeignKey('Users.Id'), nullable=False)
#     GameLineId:Mapped[int] = mapped_column(ForeignKey('GameLine.Id'), nullable=True)
#     Type:Mapped[str] = mapped_column(nullable=False)
#     Selection:Mapped[bool] = mapped_column(nullable=False)
#     Amount:Mapped[int] = mapped_column(nullable=False)


# class Divisions(Base):
#     """Table to store division information"""
#     __tablename__ = 'Divisions'
#     Id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     Name:Mapped[int] = mapped_column(nullable=False)
#     ConferenceId:Mapped[int] = mapped_column(ForeignKey('Conference.Id'), nullable=False)
#     SeasonId:Mapped[int] = mapped_column(ForeignKey('Season.Id'), nullable=False)


# class GameLines(Base):
#     """Table to store game lines, odds, and results"""
#     __tablename__ = 'GameLines'
#     Id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     GameId:Mapped[int] = mapped_column(ForeignKey('Games.Id'), nullable=False)
#     LineType:Mapped[str] = mapped_column(nullable=False)
#     Line:Mapped[float] = mapped_column(nullable=True)
#     Odds:Mapped[int] = mapped_column(nullable=True)
#     Winner:Mapped[int] = mapped_column(nullable=True)


# class GameResults(Base):
#     """Table to store final game results"""
#     __tablename__ = 'GameResults'
#     Id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     GameId:Mapped[int] = mapped_column(ForeignKey('Games.Id'), nullable=False)
#     AwayScore:Mapped[int] = mapped_column(nullable=False)
#     HomeScore:Mapped[int] = mapped_column(nullable=False)
#     Overtime:Mapped[bool] = mapped_column(nullable=False)


# class Games(Base):
#     """Table to store game information before the game starts"""
#     __tablename__ = 'Games'
#     Id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     SeasonId:Mapped[int] = mapped_column(ForeignKey('Season.Id'), nullable=False)
#     Week:Mapped[int] = mapped_column(nullable=False)
#     WeekName:Mapped[str] = mapped_column(nullable=False)
#     StartTime:Mapped[DateTime] = mapped_column(nullable=True)
#     AwayTeamId:Mapped[int] = mapped_column(ForeignKey('Team.Id'), nullable=False)
#     HomeTeamId:Mapped[int] = mapped_column(ForeignKey('Team.Id'), nullable=False)


# class Seasons(Base):
#     """Table to store season information"""
#     __tablename__ = 'Seasons'
#     Id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     Name:Mapped[str] = mapped_column(nullable=False)
#     Year:Mapped[int] = mapped_column(nullable=False)
#     RegularSeasonWeekCount:Mapped[int] = mapped_column(nullable=False)
#     PlayoffTeams:Mapped[int] = mapped_column(nullable=False)


# class Teams(Base):
#     """Table to store NFL team information"""
#     __tablename__ = 'Teams'
#     Id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     Location:Mapped[str] = mapped_column(nullable=False)
#     Name:Mapped[str] = mapped_column(nullable=False)
#     FullName:Mapped[str] = mapped_column(nullable=False)
#     DivisionId:Mapped[int] = mapped_column(ForeignKey('Division.Id'), nullable=False)


# class Users(Base):
#     """Table to store information about users"""
#     __tablename__ = 'Users'
#     Id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     Username:Mapped[str] = mapped_column(nullable=False)
#     FirstName:Mapped[str] = mapped_column(nullable=False)
#     LastName:Mapped[str] = mapped_column(nullable=False)
#     Money:Mapped[int] = mapped_column(nullable=False)