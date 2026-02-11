from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey, UniqueConstraint, Index
  
class Base(DeclarativeBase):
    pass

class Match(Base):
    __tablename__ = "matches"

    match_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)

    season_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    match_number: Mapped[int | None] = mapped_column(Integer, nullable=True) 
    match_date: Mapped[str | None] = mapped_column(String(20), nullable=True )  
    match_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    
    venue: Mapped[str | None] = mapped_column(Text, nullable=True) 
    city: Mapped[str | None] = mapped_column(String(80), nullable=True)
    
    team1_name: Mapped[str | None] = mapped_column(String(100), nullable=True) 
    team2_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    toss_winner: Mapped[str |None] = mapped_column(String(100), nullable=True)
    toss_decision: Mapped[str | None] = mapped_column(String(10), nullable=True)
    
    winner: Mapped[str | None] = mapped_column(String(100), nullable=True)
    win_by_runs: Mapped[int | None] = mapped_column(Integer, nullable=True)
    win_by_wickets: Mapped[int |None] = mapped_column(Integer, nullable=True)
    
    player_of_match: Mapped[str | None] = mapped_column(String(120), nullable=True)

    umpire1: Mapped[str | None] = mapped_column(String(120), nullable=True)
    umpire2: Mapped[str | None] = mapped_column(String(120), nullable=True)

# Link match to its players and deliveries for Python ORM access

    players = relationship("MatchPlayer", back_populates="match", cascade="all, delete-orphan")
    deliveries = relationship("Delivery", back_populates="match", cascade="all, delete-orphan")

class MatchPlayer(Base):
    __tablename__ = "match_players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.match_id"), nullable=False)

    team_name: Mapped[str] = mapped_column(String(100), nullable=False)
    player_name: Mapped[str] = mapped_column(String(120), nullable=False)

    match = relationship("Match", back_populates="players")

    __table_args__ = (
        UniqueConstraint("match_id", "team_name", "player_name", name="uq_match_team_player"),
        Index("indexx_match_players_match_id", "match_id"),
    )

class Delivery(Base):
    __tablename__ = "deliveries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    match_id: Mapped[int] = mapped_column(ForeignKey("matches.match_id"), nullable=False)
 
    innings_no: Mapped[int] = mapped_column(Integer, nullable=False)
    batting_team: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    over_no: Mapped[int] = mapped_column(Integer, nullable=False)
    ball_no: Mapped[int] = mapped_column(Integer, nullable=False)
    
    batter: Mapped[str | None] = mapped_column(String(120), nullable=True)
    bowler: Mapped[str | None] = mapped_column(String(120), nullable=True)
    non_striker: Mapped[str | None] = mapped_column(String(120), nullable=True)     #baller side player
    
    runs_batter: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    runs_extras: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    runs_total: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    wide: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    noball: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    bye: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    legbye: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    wicket: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    player_out: Mapped[str | None] = mapped_column(String(120), nullable=True)
    
    wicket_type: Mapped[str | None] = mapped_column(String(120), nullable=True)    #type of out
   

#Link deliveries to its match for python ORM access 
 
    match = relationship("Match", back_populates="deliveries")

    __table_args__ = (Index("index_deliveries_match_id", "match_id"),)
        
       
    

