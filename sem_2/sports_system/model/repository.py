import sqlite3
from config import DB_PATH
from  model.sportsman import Sportsman

class Repository:
    def __init__(self, db_path: str=DB_PATH) -> None:
        self.db_path = db_path

    def create_table(self)->None:
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sportsmen (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                team_type TEXT NOT NULL,
                position TEXT NOT NULL,
                titles_count INTEGER NOT NULL,
                sport_type TEXT NOT NULL,
                rank TEXT NOT NULL           
            )
        """)

        connection.commit()
        connection.close()

    def add_sportsman(self, sportsman: Sportsman) -> None:
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO sportsmen (
                full_name,
                team_type,
                position,
                titles_count,
                sport_type,
                rank
            )
            VALUE (?, ?, ?, ?, ?, ?)
        """, (
            sportsman.full_name,
            sportsman.team_type,
            sportsman.position,
            sportsman.titles_count,
            sportsman.sport_type,
            sportsman.rank

        ))

        connection.commit()
        connection.close()